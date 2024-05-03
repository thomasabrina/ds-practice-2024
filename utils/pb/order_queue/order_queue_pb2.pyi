from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class OrderRequest(_message.Message):
    __slots__ = ("orderId", "userId", "bookTitles")
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    BOOKTITLES_FIELD_NUMBER: _ClassVar[int]
    orderId: str
    userId: str
    bookTitles: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, orderId: _Optional[str] = ..., userId: _Optional[str] = ..., bookTitles: _Optional[_Iterable[str]] = ...) -> None: ...

class OrderResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class DequeueRequest(_message.Message):
    __slots__ = ("executorId",)
    EXECUTORID_FIELD_NUMBER: _ClassVar[int]
    executorId: str
    def __init__(self, executorId: _Optional[str] = ...) -> None: ...

class ElectionRequest(_message.Message):
    __slots__ = ("executorId",)
    EXECUTORID_FIELD_NUMBER: _ClassVar[int]
    executorId: str
    def __init__(self, executorId: _Optional[str] = ...) -> None: ...

class ElectionResponse(_message.Message):
    __slots__ = ("isLeader",)
    ISLEADER_FIELD_NUMBER: _ClassVar[int]
    isLeader: bool
    def __init__(self, isLeader: bool = ...) -> None: ...

class ClearLeaderRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ClearLeaderResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
