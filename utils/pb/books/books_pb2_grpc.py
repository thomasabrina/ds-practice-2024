# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import books_pb2 as books__pb2


class BooksDatabaseStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Read = channel.unary_unary(
                '/booksdb.BooksDatabase/Read',
                request_serializer=books__pb2.ReadRequest.SerializeToString,
                response_deserializer=books__pb2.ReadResponse.FromString,
                )
        self.Write = channel.unary_unary(
                '/booksdb.BooksDatabase/Write',
                request_serializer=books__pb2.WriteRequest.SerializeToString,
                response_deserializer=books__pb2.WriteResponse.FromString,
                )
        self.IncrementStock = channel.unary_unary(
                '/booksdb.BooksDatabase/IncrementStock',
                request_serializer=books__pb2.StockUpdateRequest.SerializeToString,
                response_deserializer=books__pb2.StockUpdateResponse.FromString,
                )
        self.DecrementStock = channel.unary_unary(
                '/booksdb.BooksDatabase/DecrementStock',
                request_serializer=books__pb2.StockUpdateRequest.SerializeToString,
                response_deserializer=books__pb2.StockUpdateResponse.FromString,
                )


class BooksDatabaseServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Read(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Write(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def IncrementStock(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DecrementStock(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BooksDatabaseServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Read': grpc.unary_unary_rpc_method_handler(
                    servicer.Read,
                    request_deserializer=books__pb2.ReadRequest.FromString,
                    response_serializer=books__pb2.ReadResponse.SerializeToString,
            ),
            'Write': grpc.unary_unary_rpc_method_handler(
                    servicer.Write,
                    request_deserializer=books__pb2.WriteRequest.FromString,
                    response_serializer=books__pb2.WriteResponse.SerializeToString,
            ),
            'IncrementStock': grpc.unary_unary_rpc_method_handler(
                    servicer.IncrementStock,
                    request_deserializer=books__pb2.StockUpdateRequest.FromString,
                    response_serializer=books__pb2.StockUpdateResponse.SerializeToString,
            ),
            'DecrementStock': grpc.unary_unary_rpc_method_handler(
                    servicer.DecrementStock,
                    request_deserializer=books__pb2.StockUpdateRequest.FromString,
                    response_serializer=books__pb2.StockUpdateResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'booksdb.BooksDatabase', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class BooksDatabase(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Read(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/booksdb.BooksDatabase/Read',
            books__pb2.ReadRequest.SerializeToString,
            books__pb2.ReadResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Write(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/booksdb.BooksDatabase/Write',
            books__pb2.WriteRequest.SerializeToString,
            books__pb2.WriteResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def IncrementStock(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/booksdb.BooksDatabase/IncrementStock',
            books__pb2.StockUpdateRequest.SerializeToString,
            books__pb2.StockUpdateResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DecrementStock(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/booksdb.BooksDatabase/DecrementStock',
            books__pb2.StockUpdateRequest.SerializeToString,
            books__pb2.StockUpdateResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
