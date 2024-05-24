import grpc
import threading
from concurrent import futures
import sys
import os
import logging
import heapq

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Setting up paths to include custom protobuf definitions for order executor and order queue
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path_order_executor = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_executor'))
sys.path.insert(0, utils_path_order_executor)

utils_path_order_queue = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_queue'))
sys.path.insert(0, utils_path_order_queue)

from utils.pb.order_queue import order_queue_pb2, order_queue_pb2_grpc
# from utils.vector_clock import VectorClock  

class OrderQueueService(order_queue_pb2_grpc.OrderQueueServicer):
    def __init__(self):
        self.order_queue = [] # Priority queue to manage orders
        self.current_leader = None # ID of the current leader
        self.leader_lock = threading.Lock() # Lock to manage concurrent access to leader

    def ElectLeader(self, request, context):
        # Elects a new leader if there is none, otherwise confirms if the requester is the leader
        with self.leader_lock:
            if not self.current_leader:
                self.current_leader = request.executorId
                logging.info(f"New leader elected: {self.current_leader}")
                return order_queue_pb2.ElectionResponse(isLeader=True)
            else:
                isLeader = request.executorId == self.current_leader
                logging.info(f"Leader election requested by {request.executorId}, is leader: {isLeader}")
                return order_queue_pb2.ElectionResponse(isLeader=isLeader)

    def ClearCurrentLeader(self, request, context):
        # Clears the current leader, allowing for a new leader election
        with self.leader_lock:
            logging.info("Clearing current leader")
            self.current_leader = None
            return order_queue_pb2.ClearLeaderResponse() 

    def Enqueue(self, request, context):
        # Adds an order to the queue with priority based on the number 

        # vc = VectorClock.from_proto(request.vector_clock)
        # vc.increment("order_queue_service")

        # Determine the priority of the order
        # The priority is related to the number of books (more books = higher priority)
        # Heapq is a min heap, so we use negative to simulate a max heap behavior
        priority = -len(request.bookTitles) # Negative to simulate max heap behavior

        # Use a tuple (priority, request, vc) to maintain the queue
        with self.leader_lock:
            heapq.heappush(self.order_queue, (priority, request))

        logging.info(f"Order {request.orderId} enqueued with priority {priority}")
        return order_queue_pb2.OrderResponse(
            success=True, 
            message="Order enqueued successfully."
            # vector_clock=vc.to_proto(order_queue_pb2.VectorClock)
        )

    def Dequeue(self, request, context):
        # Removes and returns the highest priority order if the requester is the current leader
        with self.leader_lock:
            if request.executorId != self.current_leader:
                logging.warning(f"Unauthorized dequeue attempt by {request.executorId}")
                return order_queue_pb2.OrderRequest()
            if self.order_queue:
                order = self.order_queue.pop(0)
                # vc.increment("order_queue_service")
                logging.info(f"Order {order[1].orderId} dequeued by leader {request.executorId}")
                return order_queue_pb2.OrderRequest(
                    orderId=order.orderId,
                    userId=order.userId,
                    bookTitles=order.bookTitles
                    # vector_clock=vc.to_proto(order_queue_pb2.VectorClock)
                )
            else:
                logging.info("Dequeue attempted but queue is empty")
                return order_queue_pb2.OrderRequest()

def serve():
    # Sets up and starts the gRPC server
    logging.info("Starting Order Queue Server on port 50054")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_queue_pb2_grpc.add_OrderQueueServicer_to_server(OrderQueueService(), server)
    server.add_insecure_port('[::]:50054')  
    server.start()
    server.wait_for_termination()
    logging.info("Order Queue Server terminated")

if __name__ == '__main__':
    serve()
