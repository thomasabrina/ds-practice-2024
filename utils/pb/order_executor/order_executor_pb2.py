# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: order_executor.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14order_executor.proto\x12\rorderexecutor\"&\n\x13\x45xecuteOrderRequest\x12\x0f\n\x07orderId\x18\x01 \x01(\t\"8\n\x14\x45xecuteOrderResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t2j\n\rOrderExecutor\x12Y\n\x0c\x45xecuteOrder\x12\".orderexecutor.ExecuteOrderRequest\x1a#.orderexecutor.ExecuteOrderResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'order_executor_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_EXECUTEORDERREQUEST']._serialized_start=39
  _globals['_EXECUTEORDERREQUEST']._serialized_end=77
  _globals['_EXECUTEORDERRESPONSE']._serialized_start=79
  _globals['_EXECUTEORDERRESPONSE']._serialized_end=135
  _globals['_ORDEREXECUTOR']._serialized_start=137
  _globals['_ORDEREXECUTOR']._serialized_end=243
# @@protoc_insertion_point(module_scope)
