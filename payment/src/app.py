import logging
import sys
import os
import grpc
import threading
from concurrent import futures

FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/payment'))
sys.path.insert(0, utils_path)

from utils.pb.payment import payment_pb2_grpc, payment_pb2

class PaymentServiceImpl(payment_pb2_grpc.PaymentServiceServicer):
    def __init__(self):
       self.reserved_funds = {}
       self.lock = threading.Lock()
       self.recover_state()

    def log_state(self, order_id, state, amount):
        """Log the state transitions to a file for recovery."""
        with open('payment_service.log', 'a') as log_file:
            log_file.write(json.dumps({'order_id': order_id, 'state': state, 'amount': amount}) + '\n')

    def recover_state(self):
        """Recover the last known state from the log file."""
        try:
            with open('payment_service.log', 'r') as log_file:
                for line in log_file:
                    log_entry = json.loads(line)
                    if log_entry['state'] == 'prepared':
                        self.reserved_funds[log_entry['order_id']] = log_entry['amount']
        except FileNotFoundError:
            print("No recovery file found. Starting fresh.")

    def Prepare(self, request, context):
        # Simulate reserving funds
        with self.lock:  # Ensure thread-safe access to reserved_funds
            if request.amount > 0:
                self.reserved_funds[request.orderId] = request.amount
                print(f"Reserved ${request.amount} for order {request.orderId}")
                return payment_pb2.PrepareResponse(success=True)
            else:
                return payment_pb2.PrepareResponse(success=False)

    def Commit(self, request, context):
        # Simulate processing payment
        with self.lock:  # Ensure thread-safe access to reserved_funds
            if request.orderId in self.reserved_funds:
                amount = self.reserved_funds.pop(request.orderId)
                print(f"Processed payment of ${amount} for order {request.orderId}")
                return payment_pb2.CommitResponse(success=True)
            else:
                return payment_pb2.CommitResponse(success=False)

    def Abort(self, request, context):
        # Simulate rolling back the payment
        with self.lock:  # Ensure thread-safe access to reserved_funds
            if request.orderId in self.reserved_funds:
                amount = self.reserved_funds.pop(request.orderId)
                print(f"Payment aborted for order {request.orderId}, ${amount} released")
                return payment_pb2.AbortResponse(success=True)
            else:
                return payment_pb2.AbortResponse(success=False)
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    payment_pb2_grpc.add_PaymentServiceServicer_to_server(PaymentServiceImpl(), server)
    server.add_insecure_port('[::]:50056')
    server.start()
    print("Payment Service is running...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()