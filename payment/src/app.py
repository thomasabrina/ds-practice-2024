import logging
import sys
import os
import grpc
from concurrent import futures

FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/payment'))
sys.path.insert(0, utils_path)

from utils.pb.payment import payment_pb2_grpc, payment_pb2

class PaymentServiceImpl(payment_pb2_grpc.PaymentServiceServicer):
    def ExecutePayment(self, request, context):
        print(f"Processing payment for order {request.orderId} of amount {request.amount}")
        return payment_pb2.PaymentResponse(success=True)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    payment_pb2_grpc.add_PaymentServiceServicer_to_server(PaymentServiceImpl(), server)
    server.add_insecure_port('[::]:50056')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()