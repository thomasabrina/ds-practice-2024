# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: transaction_verification.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1etransaction_verification.proto\x12\x18transaction_verification\"6\n\x04User\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontact\x18\x02 \x01(\t\x12\x0f\n\x07\x61\x64\x64ress\x18\x03 \x01(\t\"A\n\nCreditCard\x12\x0e\n\x06number\x18\x01 \x01(\t\x12\x16\n\x0e\x65xpirationDate\x18\x02 \x01(\t\x12\x0b\n\x03\x63vv\x18\x03 \x01(\t\"\xa8\x01\n\x1eTransactionVerificationRequest\x12\x0f\n\x07orderID\x18\x01 \x01(\t\x12\r\n\x05title\x18\x02 \x01(\t\x12,\n\x04user\x18\x03 \x01(\x0b\x32\x1e.transaction_verification.User\x12\x38\n\ncreditCard\x18\x04 \x01(\x0b\x32$.transaction_verification.CreditCard\"D\n\x1fTransactionVerificationResponse\x12\x10\n\x08is_valid\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"j\n\x1dVerifyCreditCardFormatRequest\x12\x0f\n\x07orderID\x18\x01 \x01(\t\x12\x38\n\ncreditCard\x18\x02 \x01(\x0b\x32$.transaction_verification.CreditCard\"C\n\x1eVerifyCreditCardFormatResponse\x12\x10\n\x08is_valid\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"_\n\x1eVerifyMandatoryUserDataRequest\x12\x0f\n\x07orderID\x18\x01 \x01(\t\x12,\n\x04user\x18\x02 \x01(\x0b\x32\x1e.transaction_verification.User\"D\n\x1fVerifyMandatoryUserDataResponse\x12\x10\n\x08is_valid\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t2\xbc\x02\n\x17TransactionVerification\x12\x8d\x01\n\x16VerifyCreditCardFormat\x12\x37.transaction_verification.VerifyCreditCardFormatRequest\x1a\x38.transaction_verification.VerifyCreditCardFormatResponse\"\x00\x12\x90\x01\n\x17VerifyMandatoryUserData\x12\x38.transaction_verification.VerifyMandatoryUserDataRequest\x1a\x39.transaction_verification.VerifyMandatoryUserDataResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'transaction_verification_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_USER']._serialized_start=60
  _globals['_USER']._serialized_end=114
  _globals['_CREDITCARD']._serialized_start=116
  _globals['_CREDITCARD']._serialized_end=181
  _globals['_TRANSACTIONVERIFICATIONREQUEST']._serialized_start=184
  _globals['_TRANSACTIONVERIFICATIONREQUEST']._serialized_end=352
  _globals['_TRANSACTIONVERIFICATIONRESPONSE']._serialized_start=354
  _globals['_TRANSACTIONVERIFICATIONRESPONSE']._serialized_end=422
  _globals['_VERIFYCREDITCARDFORMATREQUEST']._serialized_start=424
  _globals['_VERIFYCREDITCARDFORMATREQUEST']._serialized_end=530
  _globals['_VERIFYCREDITCARDFORMATRESPONSE']._serialized_start=532
  _globals['_VERIFYCREDITCARDFORMATRESPONSE']._serialized_end=599
  _globals['_VERIFYMANDATORYUSERDATAREQUEST']._serialized_start=601
  _globals['_VERIFYMANDATORYUSERDATAREQUEST']._serialized_end=696
  _globals['_VERIFYMANDATORYUSERDATARESPONSE']._serialized_start=698
  _globals['_VERIFYMANDATORYUSERDATARESPONSE']._serialized_end=766
  _globals['_TRANSACTIONVERIFICATION']._serialized_start=769
  _globals['_TRANSACTIONVERIFICATION']._serialized_end=1085
# @@protoc_insertion_point(module_scope)
