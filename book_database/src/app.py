import logging
import sys
import os
import grpc
import socket
from concurrent import futures
from pyraft.raft import RaftNode

FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/books'))
sys.path.insert(0, utils_path)

from utils.pb.books import books_pb2_grpc, books_pb2

class BooksDatabaseServicer(books_pb2_grpc.BooksDatabaseServicer, RaftNode):
    def __init__(self, node_id, peers, host, port):
       RaftNode.__init__(self, node_id=node_id, peers=peers, host=host, port=port)
       self.data_store = {}
       self.version = 0
       self.recover_state()
       self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       self.socket.bind((host, port))
       self.socket.listen()

    def start_server(self):
        print(f"Server starting on {self.host}:{self.port}")
        while True:
            conn, addr = self.socket.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)

    def log_state(key, state, version):
       with open('books_db.log', 'a') as log_file:
           log_file.write(f"{key},{state},{version}\n")
    
    def recover_state(self):
       try:
           with open('books_db.log', 'r') as log_file:
               for line in log_file:
                   key, state, version = line.strip().split(',')
                   if state == 'prepare':
                       self.data_store[key] = {'lock': True}
       except FileNotFoundError:
           print("No recovery file found.")

    def Read(self, request, context):
        if not self.is_leader():
            return self.redirect_to_leader(request)
        value = self.data_store.get(request.key, "")
        return books_pb2.ReadResponse(value=value)

    def Write(self, request, context):
        if not self.is_leader():
            return self.redirect_to_leader(request)
        entry = {'key': request.key, 'value': request.value, 'version': request.version}
        self.append_entries([entry])
        return books_pb2.WriteResponse(success=True)

    def IncrementStock(self, request, context):
        if not self.is_leader():
            return self.redirect_to_leader(request)
        self.data_store[request.key] = max(0, int(self.data_store.get(request.key, 0)) + request.amount)
        return books_pb2.StockUpdateResponse(success=True)

    def DecrementStock(self, request, context):
        if not self.is_leader():
            return self.redirect_to_leader(request)
        current_stock = int(self.data_store.get(request.key, 0))
        if current_stock >= request.amount:
            self.data_store[request.key] = current_stock - request.amount
            return books_pb2.StockUpdateResponse(success=True)
        else:
            return books_pb2.StockUpdateResponse(success=False, message="Insufficient stock")

    def apply_entry(self, entry):
        if entry['version'] == self.version:
            self.data_store[entry['key']] = entry['value']
            self.version += 1

    def redirect_to_leader(self, request):
        # Assuming leader's address is stored in self.leader_address
        leader_address = self.leader_address
        return books_pb2.ReadResponse(redirect_address=leader_address)

    def start_raft_server(self):
        server = RaftServer(self)
        server.start()

    def Prepare(self, request, context):
        # Lock the resource for transaction
        if request.key in self.data_store and 'lock' not in self.data_store[request.key]:
            self.data_store[request.key]['lock'] = True
            print(f"Locked {request.key} for writing")
            self.log_state(request.key, 'prepare')
            return books_pb2.PrepareResponse(success=True)
        else:
            return books_pb2.PrepareResponse(success=False)

    def Commit(self, request, context):
        # Commit the transaction
        if request.key in self.data_store and 'lock' in self.data_store[request.key]:
            print(f"Committing write to {request.key}")
            self.data_store[request.key].pop('lock', None)  # Remove lock
            self.log_state(request.key, 'commit')
            return books_pb2.CommitResponse(success=True)
        else:
            return books_pb2.CommitResponse(success=False)
        
    def Abort(self, request, context):
        # Abort the transaction and unlock the resource
        if request.key in self.data_store and 'lock' in self.data_store[request.key]:
            print(f"Aborting write to {request.key}")
            self.data_store[request.key].pop('lock', None)  # Remove lock
            self.log_state(request.key, 'abort')
            return books_pb2.AbortResponse(success=True)
        else:
            return books_pb2.AbortResponse(success=False)


def serve():
    node_id = os.getenv("NODE_ID", "node1")
    peers = {
        "node2": ("localhost", 50052),
        "node3": ("localhost", 50053)
    }
    host = os.getenv("HOST", "localhost")
    port = int(os.getenv("PORT", 50051))
    servicer = BooksDatabaseServicer(node_id, peers, host, port)
    servicer.start_server()

    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    books_pb2_grpc.add_BooksDatabaseServicer_to_server(servicer, grpc_server)
    grpc_server.add_insecure_port(f'{host}:{port}')
    grpc_server.start()
    grpc_server.wait_for_termination()

if __name__ == '__main__':
    serve()