import logging
import sys
import os
import grpc
from concurrent import futures

FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/books'))
sys.path.insert(0, utils_path)

from utils.pb.books import books_pb2_grpc, books_pb2

class BooksDatabaseServicer(books_pb2_grpc.BooksDatabaseServicer):
    def __init__(self):
        self.data_store = {}  # Simple key-value store
        self.version = 0  # Simple versioning for concurrency control

    def Read(self, request, context):
        value = self.data_store.get(request.key, "")
        return books_pb2.ReadResponse(value=value)

    def Write(self, request, context):
        if request.version == self.version:
            self.data_store[request.key] = request.value
            self.version += 1
            return books_pb2.WriteResponse(success=True)
        return books_pb2.WriteResponse(success=False)

    def IncrementStock(self, request, context):
        if request.key in self.data_store:
            self.data_store[request.key] += request.amount
            return books_pb2.StockUpdateResponse(success=True)
        return books_pb2.StockUpdateResponse(success=False)

    def DecrementStock(self, request, context):
        if request.key in self.data_store and self.data_store[request.key] >= request.amount:
            self.data_store[request.key] -= request.amount
            return books_pb2.StockUpdateResponse(success=True)
        return books_pb2.StockUpdateResponse(success=False)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    books_pb2_grpc.add_BooksDatabaseServicer_to_server(BooksDatabaseServicer(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()