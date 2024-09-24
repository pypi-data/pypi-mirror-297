from typing import Callable


class IMessageClient:
    def is_connected(self) -> bool:
        raise NotImplementedError("IsConnected method not implemented.")

    def publish_message(self, topic: str, message: str) -> None:
        raise NotImplementedError("PublishMessageAsync method not implemented.")

    def subscribe_message(self, topic: str) -> None:
        raise NotImplementedError("SubscribeMessageAsync method not implemented.")

    def connect(self) -> None:
        raise NotImplementedError("ConnectAsync method not implemented.")

    def disconnect(self) -> None:
        raise NotImplementedError("DisconnectAsync method not implemented.")

    def on_connect(self, fn: Callable[[], None]) -> None:
        raise NotImplementedError("OnConnect method not implemented.")

    def on_disconnect(self, fn: Callable[[], None]) -> None:
        raise NotImplementedError("OnDisconnect method not implemented.")

    def on_message(self, fn: Callable[[str, str], None]) -> None:
        raise NotImplementedError("OnMessage method not implemented.")
