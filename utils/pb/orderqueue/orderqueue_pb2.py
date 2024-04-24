# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: orderqueue.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10orderqueue.proto\x12\norderqueue\"%\n\x04User\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontact\x18\x02 \x01(\t\"A\n\nCreditCard\x12\x0e\n\x06number\x18\x01 \x01(\t\x12\x16\n\x0e\x65xpirationDate\x18\x02 \x01(\t\x12\x0b\n\x03\x63vv\x18\x03 \x01(\t\"&\n\x04\x42ook\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08quantity\x18\x02 \x01(\x05\"[\n\x0e\x42illingAddress\x12\x0e\n\x06street\x18\x01 \x01(\t\x12\x0c\n\x04\x63ity\x18\x02 \x01(\t\x12\r\n\x05state\x18\x03 \x01(\t\x12\x0b\n\x03zip\x18\x04 \x01(\t\x12\x0f\n\x07\x63ountry\x18\x05 \x01(\t\"1\n\x06\x44\x65vice\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\r\n\x05model\x18\x02 \x01(\t\x12\n\n\x02os\x18\x03 \x01(\t\"\xa4\x02\n\x05Order\x12\x1e\n\x04user\x18\x01 \x01(\x0b\x32\x10.orderqueue.User\x12*\n\ncreditCard\x18\x02 \x01(\x0b\x32\x16.orderqueue.CreditCard\x12\x32\n\x0e\x62illingAddress\x18\x03 \x01(\x0b\x32\x1a.orderqueue.BillingAddress\x12\x1f\n\x05\x62ooks\x18\x04 \x03(\x0b\x32\x10.orderqueue.Book\x12\x13\n\x0buserComment\x18\x05 \x01(\t\x12\x16\n\x0eshippingMethod\x18\x06 \x01(\t\x12\x13\n\x0bgiftMessage\x18\x07 \x01(\t\x12\x14\n\x0cgiftWrapping\x18\x08 \x01(\x08\x12\"\n\x06\x64\x65vice\x18\t \x01(\x0b\x32\x12.orderqueue.Device\"7\n\x13\x45nqueueOrderRequest\x12 \n\x05order\x18\x01 \x01(\x0b\x32\x11.orderqueue.Order\"\'\n\x14\x45nqueueOrderResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"&\n\x13\x44\x65queueOrderRequest\x12\x0f\n\x07message\x18\x01 \x01(\t\"\'\n\x14\x44\x65queueOrderResponse\x12\x0f\n\x07message\x18\x01 \x01(\t2\xbd\x01\n\x11OrderQueueService\x12S\n\x0c\x45nqueueOrder\x12\x1f.orderqueue.EnqueueOrderRequest\x1a .orderqueue.EnqueueOrderResponse\"\x00\x12S\n\x0c\x44\x65queueOrder\x12\x1f.orderqueue.DequeueOrderRequest\x1a .orderqueue.DequeueOrderResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'orderqueue_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_USER']._serialized_start=32
  _globals['_USER']._serialized_end=69
  _globals['_CREDITCARD']._serialized_start=71
  _globals['_CREDITCARD']._serialized_end=136
  _globals['_BOOK']._serialized_start=138
  _globals['_BOOK']._serialized_end=176
  _globals['_BILLINGADDRESS']._serialized_start=178
  _globals['_BILLINGADDRESS']._serialized_end=269
  _globals['_DEVICE']._serialized_start=271
  _globals['_DEVICE']._serialized_end=320
  _globals['_ORDER']._serialized_start=323
  _globals['_ORDER']._serialized_end=615
  _globals['_ENQUEUEORDERREQUEST']._serialized_start=617
  _globals['_ENQUEUEORDERREQUEST']._serialized_end=672
  _globals['_ENQUEUEORDERRESPONSE']._serialized_start=674
  _globals['_ENQUEUEORDERRESPONSE']._serialized_end=713
  _globals['_DEQUEUEORDERREQUEST']._serialized_start=715
  _globals['_DEQUEUEORDERREQUEST']._serialized_end=753
  _globals['_DEQUEUEORDERRESPONSE']._serialized_start=755
  _globals['_DEQUEUEORDERRESPONSE']._serialized_end=794
  _globals['_ORDERQUEUESERVICE']._serialized_start=797
  _globals['_ORDERQUEUESERVICE']._serialized_end=986
# @@protoc_insertion_point(module_scope)
