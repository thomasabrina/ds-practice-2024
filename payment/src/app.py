import logging
import sys
import os
import grpc
import threading
from concurrent import futures

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up the path to import the protobuf files dynamically based on the file location.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/payment'))
sys.path.insert(0, utils_path)

from utils.pb.payment import payment_pb2_grpc, payment_pb2

class PaymentServiceImpl(payment_pb2_grpc.PaymentServiceServicer):
    def __init__(self):
       self.reserved_funds = {}  # Dictionary to keep track of reserved funds per order
       self.lock = threading.Lock()  # Lock to ensure thread-safe operations on reserved_funds
       self.recover_state()  # Recover state from log file on service start
       logging.info("Payment service initialized.")

    def log_state(self, order_id, state, amount):
        """Log the state transitions to a file for recovery."""
        with open('payment_service.log', 'a') as log_file:
            log_file.write(json.dumps({'order_id': order_id, 'state': state, 'amount': amount}) + '\n')
        logging.info(f"Logged state: {state} for order ID: {order_id} with amount: ${amount}")

    def recover_state(self):
        """Recover the last known state from the log file."""
        try:
            with open('payment_service.log', 'r') as log_file:
                for line in log_file:
                    log_entry = json.loads(line)
                    if log_entry['state'] == 'prepare':
                        self.reserved_funds[log_entry['order_id']] = log_entry['amount']
            logging.info("State recovered from log file.")
        except FileNotFoundError:
            print("No recovery file found. Starting fresh.")

    def Prepare(self, request, context):
        """Reserve funds for a transaction."""
        with self.lock:
            if request.amount > 0:
                self.reserved_funds[request.orderId] = request.amount
                self.log_state(request.orderId, 'prepare', request.amount)
                logging.info(f"Prepare request received for order ID: {request.orderId} with amount: ${request.amount}")
                return payment_pb2.PrepareResponse(success=True)
            else:
                return payment_pb2.PrepareResponse(success=False)

    def Commit(self, request, context):
        """Finalize the transaction and process the payment."""
        with self.lock:
            if request.orderId in self.reserved_funds:
                amount = self.reserved_funds.pop(request.orderId)
                self.log_state(request.orderId, 'commit', amount)
                logging.info(f"Commit request processed for order ID: {request.orderId}")
                return payment_pb2.CommitResponse(success=True)
            else:
                return payment_pb2.CommitResponse(success=False)

    def Abort(self, request, context):
        """Roll back the transaction and release the reserved funds."""
        with self.lock:
            if request.orderId in self.reserved_funds:
                amount = self.reserved_funds.pop(request.orderId)
                self.log_state(request.orderId, 'abort', amount)
                logging.info(f"Abort request processed for order ID: {request.orderId}")
                return payment_pb2.AbortResponse(success=True)
            else:
                return payment_pb2.AbortResponse(success=False)
    
def serve():
    """Start the gRPC server and listen for requests."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    payment_pb2_grpc.add_PaymentServiceServicer_to_server(PaymentServiceImpl(), server)
    server.add_insecure_port('[::]:50056')
    server.start()
    logging.info("Payment Service is running on port 50056.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()