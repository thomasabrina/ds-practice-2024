# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: books.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0b\x62ooks.proto\x12\x07\x62ooksdb\"\x1a\n\x0bReadRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\"\x1d\n\x0cReadResponse\x12\r\n\x05value\x18\x01 \x01(\t\"*\n\x0cWriteRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\" \n\rWriteResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"1\n\x12StockUpdateRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x0e\n\x06\x61mount\x18\x02 \x01(\x05\"&\n\x13StockUpdateResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x32\x96\x02\n\rBooksDatabase\x12\x33\n\x04Read\x12\x14.booksdb.ReadRequest\x1a\x15.booksdb.ReadResponse\x12\x36\n\x05Write\x12\x15.booksdb.WriteRequest\x1a\x16.booksdb.WriteResponse\x12K\n\x0eIncrementStock\x12\x1b.booksdb.StockUpdateRequest\x1a\x1c.booksdb.StockUpdateResponse\x12K\n\x0e\x44\x65\x63rementStock\x12\x1b.booksdb.StockUpdateRequest\x1a\x1c.booksdb.StockUpdateResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'books_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_READREQUEST']._serialized_start=24
  _globals['_READREQUEST']._serialized_end=50
  _globals['_READRESPONSE']._serialized_start=52
  _globals['_READRESPONSE']._serialized_end=81
  _globals['_WRITEREQUEST']._serialized_start=83
  _globals['_WRITEREQUEST']._serialized_end=125
  _globals['_WRITERESPONSE']._serialized_start=127
  _globals['_WRITERESPONSE']._serialized_end=159
  _globals['_STOCKUPDATEREQUEST']._serialized_start=161
  _globals['_STOCKUPDATEREQUEST']._serialized_end=210
  _globals['_STOCKUPDATERESPONSE']._serialized_start=212
  _globals['_STOCKUPDATERESPONSE']._serialized_end=250
  _globals['_BOOKSDATABASE']._serialized_start=253
  _globals['_BOOKSDATABASE']._serialized_end=531
# @@protoc_insertion_point(module_scope)