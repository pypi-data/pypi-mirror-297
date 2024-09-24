import paho.mqtt.client as mqtt
import uuid
from typing import Callable, Optional

from edgesync360edgehubedgesdk.EdgeAgent import Any, mqttTopic
from edgesync360edgehubedgesdk.Model.Interface import IMessageClient
import edgesync360edgehubedgesdk.Common.Constants as constant
from edgesync360edgehubedgesdk.Model.MQTTMessage import LastWillMessage


class MqttMessageClient(IMessageClient):
    def __init__(
        self,
        broker: str,
        port: int = 1883,
        username: str = "",
        password: str = "",
        nodeId: str = "",
        protocalType: str = constant.Protocol["TCP"],
        reconnectInterval: int = 1000,
    ):
        self.broker = broker
        self.port = port
        self.connect_callback: Optional[Callable[[], None]] = None
        self.disconnect_callback: Optional[Callable[[], None]] = None
        self.message_callback: Optional[Callable[[str, str], None]] = None
        self.__isConnected: bool = False

        cliendId = "EdgeAgent_" + str(uuid.uuid4())
        self.client = mqtt.Client(
            client_id=cliendId, clean_session=True, transport=protocalType
        )
        self.client.username_pw_set(username, password)
        self.client.on_connect = self.on_connect_internal
        self.client.on_disconnect = self.on_disconnect_internal
        self.client.on_message = self.on_message_internal
        willPayload = LastWillMessage().getJson()
        topic = mqttTopic.NodeConnTopic.format(nodeId)
        self.client.will_set(
            topic,
            payload=willPayload,
            qos=constant.MqttQualityOfServiceLevel["AtLeastOnce"],
            retain=True,
        )
        # TLS
        self.client.reconnect_delay_set(
            min_delay=reconnectInterval,
            max_delay=reconnectInterval,
        )

    def is_connected(self) -> bool:
        return self.__isConnected

    def connect(self) -> None:
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

    def disconnect(self) -> None:
        self.client.loop_stop()
        self.client.disconnect()

    def publish_message(self, topic: str, message: str) -> None:
        self.client.publish(
            topic, message, constant.MqttQualityOfServiceLevel["AtLeastOnce"], False
        )

    def subscribe_message(self, topic: str) -> None:
        self.client.subscribe(topic)

    def on_connect(self, fn: Callable[[], None]) -> None:
        self.connect_callback = fn

    def on_disconnect(self, fn: Callable[[], None]) -> None:
        self.disconnect_callback = fn

    def on_message(self, fn: Callable[[str, str], None]) -> None:
        self.message_callback = fn

    def on_connect_internal(
        self, client: mqtt.Client, userdata: Any, flags: dict[str, int], rc: int
    ):
        if rc == 0:
            self.__isConnected = True
            print("Connected OK Returned code=", rc)
        else:
            print("Bad connection Returned code=", rc)

        if self.connect_callback:
            self.connect_callback()

    def on_disconnect_internal(self, client: mqtt.Client, userdata: Any, rc: int):
        if self.disconnect_callback:
            self.disconnect_callback()
        self.__isConnected = False

    def on_message_internal(
        self, client: mqtt.Client, userdata: Any, message: mqtt.MQTTMessage
    ):
        if self.message_callback:
            self.message_callback(message.topic, message.payload.decode("utf-8"))
