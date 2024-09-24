from azure.iot.device import IoTHubDeviceClient, Message
from edgesync360edgehubedgesdk.Model.Interface import IMessageClient
from typing import Callable, List


class AzureIotHubMessageClient(IMessageClient):

    def __init__(self, connection_string: str):
        self.client: IoTHubDeviceClient = (
            IoTHubDeviceClient.create_from_connection_string(connection_string)
        )
        self.connect_callback: Callable[[], None] | None = None
        self.disconnect_callback: Callable[[], None] | None = None
        self.message_callback: Callable[[str, str], None] | None = None
        self.subscribe_topics: List[str] = []
        self.client.on_message_received = self.message_handler
        self.client.on_connection_state_change = self.on_connection_state_change

    def is_connected(self) -> bool:
        # There is no direct method for checking connection status in azure-iot-device,
        # but we can assume that if the client has connected successfully, it's connected.
        # Azure IoT SDK handles reconnections automatically.
        return self.client.connected

    def publish_message(self, topic: str, message: str) -> None:
        # Azure IoT Hub does not use topics in the same way as MQTT.
        # You can use 'send_message' to send telemetry data.
        function = topic.split("/").pop()
        m = Message(message)
        m.custom_properties[function] = ""
        self.client.send_message(m)

    def subscribe_message(self, topic: str) -> None:
        # You don't need to subscribe to a topic manually in Azure IoT SDK.
        # Instead, you need to define the callback for receiving messages.
        # The IoTHub SDK handles message routing automatically.
        self.subscribe_topics.append(topic)
        pass

    def connect(self) -> None:
        # The connect method for azure-iot-device is handled during the first use of the client.
        # You can call connect explicitly if needed.
        self.client.connect()
        if self.client.connected and self.connect_callback:
            self.connect_callback()

    def disconnect(self) -> None:
        # Disconnect the client from the IoT Hub.
        self.client.disconnect()

    def on_connect(self, fn: Callable[[], None]) -> None:
        self.connect_callback = fn
        # Optionally, you could trigger this callback when a connection is detected

    def on_disconnect(self, fn: Callable[[], None]) -> None:
        self.disconnect_callback = fn
        # Optionally, trigger this callback when a disconnection is detected

    def on_message(self, fn: Callable[[str, str], None]) -> None:
        self.message_callback = fn

    # Azure IoT SDK handles incoming messages via a handler function.
    def message_handler(self, message: Message):
        if self.message_callback:
            self.message_callback("", message.data)

    def on_connection_state_change(self):
        if self.client.connected and self.connect_callback:
            self.connect_callback()
        elif not self.client.connected and self.disconnect_callback:
            self.disconnect_callback()
