import grpc
import logging
from concurrent import futures
import socket
import sys
import os
import threading
import time

FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")

# Dynamically insert paths to the protocol buffer utilities for various services.
# This allows the application to access the generated protobuf classes for interacting with gRPC services.
utils_path_order_executor = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_executor'))
sys.path.insert(0, utils_path_order_executor)

utils_path_order_queue = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_queue'))
sys.path.insert(0, utils_path_order_queue)

utils_path_books = os.path.abspath(os.path.join(FILE, '../../../utils/pb/books'))
sys.path.insert(0, utils_path_books)

utils_path_payment = os.path.abspath(os.path.join(FILE, '../../../utils/pb/payment'))
sys.path.insert(0, utils_path_payment)

from utils.pb.order_executor import order_executor_pb2, order_executor_pb2_grpc
from utils.pb.order_queue import order_queue_pb2, order_queue_pb2_grpc
from utils.pb.books import books_pb2, books_pb2_grpc
from utils.pb.payment import payment_pb2, payment_pb2_grpc

class OrderExecutor(order_executor_pb2_grpc.OrderExecutorServicer):
    def __init__(self, executor_id):
        # Initialize the OrderExecutor with unique executor ID and set up gRPC channels and stubs for communication.
        logging.info(f"Initializing OrderExecutor with ID {executor_id}")
        self.executor_id = executor_id
        self.books_db_channel = grpc.insecure_channel('localhost:50051')  
        self.books_db_stub = books_pb2_grpc.BooksDatabaseStub(self.books_db_channel)
        self.payment_channel = grpc.insecure_channel('localhost:50056')  
        self.payment_stub = payment_pb2_grpc.PaymentServiceStub(self.payment_channel)

    def request_leadership(self):
        # Request leadership status from the Order Queue service to determine if this instance can execute orders.
        logging.info("Requesting leadership status.")
        with grpc.insecure_channel('localhost:50054') as channel:
            order_queue_stub = order_queue_pb2_grpc.OrderQueueStub(channel)
            response = order_queue_stub.ElectLeader(order_queue_pb2.ElectionRequest(executorId=self.executor_id))
            logging.info(f"Leadership status received: {response.isLeader}")
            return response.isLeader
        
    def ExecuteOrder(self, request, context):
        logging.info("Attempting to execute order.")
        if self.request_leadership():
            # Main method to execute an order if this instance is the leader.
            # It involves checking leadership, dequeuing an order, checking stock, and performing a two-phase commit.
            order_queue_stub = order_queue_pb2_grpc.OrderQueueStub(self.books_db_channel)
            dequeued_order = order_queue_stub.Dequeue(order_queue_pb2.DequeueRequest())
            if dequeued_order.orderId:
                # Read current stock from Books Database
                read_response = self.books_db_stub.Read(books_pb2.ReadRequest(key=dequeued_order.bookId))
                current_stock = int(read_response.value)
                new_stock = current_stock - dequeued_order.quantity

                # Initiate 2PC
                if self.perform_two_phase_commit(dequeued_order.bookId, dequeued_order.quantity, dequeued_order.quantity * 10):  # Example price calculation
                    print(f"Order {dequeued_order.orderId} executed, stock updated.")
                    response = order_executor_pb2.ExecuteOrderResponse(success=True, message="Order executed and stock updated")
                    logging.info(f"Order {dequeued_order.orderId} execution status: {response.message}")
                    return response
                else:
                    print("Transaction aborted due to preparation failure.")
                    response = order_executor_pb2.ExecuteOrderResponse(success=False, message="Failed to prepare transaction")
                    logging.info(f"Order {dequeued_order.orderId} execution status: {response.message}")
                    return response
            else:
                response = order_executor_pb2.ExecuteOrderResponse(success=False, message="No order to execute")
                logging.info(f"Order {dequeued_order.orderId} execution status: {response.message}")
                return response
        else:
            logging.warning("Not the leader, skipping execution.")
            return order_executor_pb2.ExecuteOrderResponse(success=False, message="Not the leader")

    def perform_two_phase_commit(self, book_key, quantity, price):
        # Perform a two-phase commit across the Books Database and Payment services to ensure data consistency.
        logging.info("Starting two-phase commit.")
        try:
            db_response = self.books_db_stub.Prepare(
                books_pb2.PrepareRequest(key=book_key, amount=quantity),
                timeout=10  # Timeout after 10 seconds
            )
            payment_response = self.payment_stub.Prepare(
                payment_pb2.PrepareRequest(amount=price),
                timeout=10  # Timeout after 10 seconds
            )

            if db_response.success and payment_response.success:
                self.books_db_stub.Commit(books_pb2.CommitRequest(key=book_key))
                self.payment_stub.Commit(payment_pb2.CommitRequest())
                logging.info("Two-phase commit successful.")
                return True
            else:
                raise Exception("Preparation failed in one of the services.")
        except grpc.RpcError as e:
            logging.error(f"RPC failed: {e}")
            self.books_db_stub.Abort(books_pb2.AbortRequest(key=book_key))
            self.payment_stub.Abort(payment_pb2.AbortRequest())
            return False
        except Exception as e:
            logging.error(f"Error during 2PC: {e}")
            self.books_db_stub.Abort(books_pb2.AbortRequest(key=book_key))
            self.payment_stub.Abort(payment_pb2.AbortRequest())
            return False


def serve():
    logging.info("Starting Order Executor service.")
    executor_id = socket.gethostname()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    executor_instance = OrderExecutor(executor_id)
    order_executor_pb2_grpc.add_OrderExecutorServicer_to_server(executor_instance, server)
    server.add_insecure_port('[::]:50055')
    server.start()
    logging.info(f"Order Executor {executor_id} running on port 50055")
    # Start the polling in a background thread
    threading.Thread(target=executor_instance.poll_and_execute_orders, daemon=True).start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()

'''
Centralized Leader Election
In a centralized leader election algorithm, one node acts as the coordinator. This node is responsible for managing the election process and declaring the winner. The algorithm typically works as follows:
1. When a node determines that a new leader needs to be elected (e.g., due to the current leader failing or during system startup), it sends an election message to the coordinator.
2. The coordinator receives election messages from various nodes, decides which node should be the leader (usually based on a predetermined criterion such as the lowest node ID, highest available resources, etc.), and then informs all nodes in the system of the election result.
Why Choose Centralized Leader Election?
1. Simplicity: The centralized approach is straightforward to understand and implement. It does not require complex logic or state management across multiple nodes, making it easier to debug and maintain.
2. Efficiency for Small to Medium Systems: For systems with a small to medium number of nodes, a centralized leader election can be very efficient. The overhead of coordinating the election is minimal, and decisions can be made quickly.
3. Clear Coordination Point: Having a single point of coordination simplifies the process of managing elections and can also simplify other aspects of system management, such as configuration changes or updates.
4. Suitability for Your Use Case: Given that your system already involves a centralized Order Queue service, integrating a centralized leader election mechanism for the Order Executor service can align well with your existing architecture. The Order Queue service or a dedicated coordinator service can act as the central authority for leader election among Order Executor instances.
Considerations
Single Point of Failure: The main drawback of a centralized approach is that the coordinator becomes a single point of failure. If the coordinator node fails, the system may not be able to elect a new leader until the coordinator is restored. This issue can be mitigated by implementing failover mechanisms for the coordinator.
Scalability: As the system grows, the coordinator may become a bottleneck. However, for many applications, especially those with a moderate number of nodes, this is not an immediate concern.
Conclusion
A centralized leader election algorithm offers a good balance of simplicity, efficiency, and ease of implementation for your Order Executor service, especially considering the system's current architecture and scale. It provides a clear and straightforward way to manage leader election, making it a practical choice for ensuring mutual exclusion in order processing.
'''