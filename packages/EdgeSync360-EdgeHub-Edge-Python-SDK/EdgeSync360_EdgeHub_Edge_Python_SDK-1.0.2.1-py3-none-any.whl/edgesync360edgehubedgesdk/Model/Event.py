from typing import Any


class MessageReceivedEventArgs:
    def __init__(self, msgType: int, message: Any):
        self.__type = msgType
        self.__message = message

    @property
    def type(self) -> int:
        return self.__type

    @type.setter
    def type(self, value: int):
        self.__type = value

    @property
    def message(self) -> Any:
        return self.__message

    @message.setter
    def message(self, value: Any):
        self.__message = value
