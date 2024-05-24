import logging
import sys
import os
import grpc
import socket
from concurrent import futures
from pyraft.raft import RaftNode

# Set up the path for importing protobuf definitions
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/books'))
sys.path.insert(0, utils_path)

from utils.pb.books import books_pb2_grpc, books_pb2

# Configure logging for the application
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BooksDatabaseServicer(books_pb2_grpc.BooksDatabaseServicer, RaftNode):
    """
    A service class that implements the BooksDatabase gRPC service and includes Raft consensus.
    It handles book database operations with distributed consensus and direct socket communication.
    """
    def __init__(self, node_id, peers, host, port):
        """
        Initialize the server with specific node details and start listening on a socket.
        """
        RaftNode.__init__(self, node_id=node_id, peers=peers, host=host, port=port)
        self.data_store = {}  # In-memory data store
        self.version = 0  # Version for maintaining consistency
        self.recover_state()  # Recover state from log if available
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen()
        logging.info(f"Server initialized on {host}:{port} with node ID {node_id}")

    def start_server(self):
        """
        Start the TCP server to handle direct client connections.
        """
        print(f"Server starting on {self.host}:{self.port}")
        while True:
            conn, addr = self.socket.accept()
            with conn:
                print(f"Connected by {addr}")
                logging.info(f"Connected by {addr}, starting to receive data")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)

    def recover_state(self):
        """
        Recover the server state from a log file to ensure consistency after restarts.
        """
        try:
            with open('books_db.log', 'r') as log_file:
                for line in log_file:
                    key, state, version = line.strip().split(',')
                    if state == 'prepare':
                        self.data_store[key] = {'lock': True}
        except FileNotFoundError:
            print("No recovery file found.")
        logging.info("State recovery completed. Current data store state: {self.data_store}")

    def log_state(self, key, state, version):
        """
        Log the state of a key to a file for recovery purposes.
        """
        with open('books_db.log', 'a') as log_file:
            log_file.write(f"{key},{state},{version}\n")

    def Read(self, request, context):
        """
        Handle a read request for a specific key.
        """
        if not self.is_leader():
            return self.redirect_to_leader(request)
        value = self.data_store.get(request.key, "")
        logging.info(f"Read request for key {request.key}: {value}")
        return books_pb2.ReadResponse(value=value)

    def Write(self, request, context):
        """
        Handle a write request for a specific key.
        """
        if not self.is_leader():
            return self.redirect_to_leader(request)
        entry = {'key': request.key, 'value': request.value, 'version': request.version}
        self.append_entries([entry])
        logging.info(f"Write request for key {request.key} with value {request.value}")
        return books_pb2.WriteResponse(success=True)

    def IncrementStock(self, request, context):
        """
        Handle an increment stock request for a specific key.
        """
        if not self.is_leader():
            return self.redirect_to_leader(request)
        self.data_store[request.key] = max(0, int(self.data_store.get(request.key, 0)) + request.amount)
        logging.info(f"Incremented stock for key {request.key} by {request.amount}")
        return books_pb2.StockUpdateResponse(success=True)

    def DecrementStock(self, request, context):
        """
        Handle a decrement stock request for a specific key.
        """
        if not self.is_leader():
            return self.redirect_to_leader(request)
        current_stock = int(self.data_store.get(request.key, 0))
        if current_stock >= request.amount:
            self.data_store[request.key] = current_stock - request.amount
            logging.info(f"Decremented stock for key {request.key} by {request.amount}")
            return books_pb2.StockUpdateResponse(success=True)
        else:
            return books_pb2.StockUpdateResponse(success=False, message="Insufficient stock")

    def apply_entry(self, entry):
        """
        Apply a log entry to the state machine if the entry version matches the current version.
        """
        if entry['version'] == self.version:
            self.data_store[entry['key']] = entry['value']
            self.version += 1

    def redirect_to_leader(self, request):
        """
        Redirect a request to the leader node if the current node is not the leader.
        """
        # Assuming leader's address is stored in self.leader_address
        leader_address = self.leader_address
        return books_pb2.ReadResponse(redirect_address=leader_address)

    def start_raft_server(self):
        """
        Start the Raft server.
        """
        server = RaftServer(self)
        server.start()

    def Prepare(self, request, context):
        """
        Handle the prepare phase of a transaction.
        """
        # Lock the resource for transaction
        if request.key in self.data_store and 'lock' not in self.data_store[request.key]:
            self.data_store[request.key]['lock'] = True
            print(f"Locked {request.key} for writing")
            self.log_state(request.key, 'prepare')
            logging.info(f"Prepare phase for key {request.key}")
            return books_pb2.PrepareResponse(success=True)
        else:
            return books_pb2.PrepareResponse(success=False)

    def Commit(self, request, context):
        """
        Handle the commit phase of a transaction.
        """
        # Commit the transaction
        if request.key in self.data_store and 'lock' in self.data_store[request.key]:
            print(f"Committing write to {request.key}")
            self.data_store[request.key].pop('lock', None)  # Remove lock
            self.log_state(request.key, 'commit')
            logging.info(f"Commit phase for key {request.key}")
            return books_pb2.CommitResponse(success=True)
        else:
            return books_pb2.CommitResponse(success=False)

    def Abort(self, request, context):
        """
        Handle the abort phase of a transaction.
        """
        # Abort the transaction and unlock the resource
        if request.key in self.data_store and 'lock' in self.data_store[request.key]:
            print(f"Aborting write to {request.key}")
            self.data_store[request.key].pop('lock', None)  # Remove lock
            self.log_state(request.key, 'abort')
            logging.info(f"Abort phase for key {request.key}")
            return books_pb2.AbortResponse(success=True)
        else:
            return books_pb2.AbortResponse(success=False)

def serve():
    """
    Configure the environment, initialize the service, and start the gRPC server.
    """
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
    logging.info("gRPC server starting")
    grpc_server.start()
    logging.info("gRPC server started, waiting for termination")

if __name__ == '__main__':
    serve()