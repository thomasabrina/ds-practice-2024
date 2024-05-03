from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CheckUserDataRequest(_message.Message):
    __slots__ = ("orderID", "user")
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    orderID: str
    user: User
    def __init__(self, orderID: _Optional[str] = ..., user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class CheckUserDataResponse(_message.Message):
    __slots__ = ("is_fraud", "reason")
    IS_FRAUD_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    is_fraud: bool
    reason: str
    def __init__(self, is_fraud: bool = ..., reason: _Optional[str] = ...) -> None: ...

class FraudDetectionRequest(_message.Message):
    __slots__ = ("orderID", "number", "expirationDate")
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    EXPIRATIONDATE_FIELD_NUMBER: _ClassVar[int]
    orderID: str
    number: str
    expirationDate: str
    def __init__(self, orderID: _Optional[str] = ..., number: _Optional[str] = ..., expirationDate: _Optional[str] = ...) -> None: ...

class FraudDetectionResponse(_message.Message):
    __slots__ = ("is_fraud", "reason")
    IS_FRAUD_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    is_fraud: bool
    reason: str
    def __init__(self, is_fraud: bool = ..., reason: _Optional[str] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ("name", "contact", "address")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONTACT_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    name: str
    contact: str
    address: str
    def __init__(self, name: _Optional[str] = ..., contact: _Optional[str] = ..., address: _Optional[str] = ...) -> None: ...
