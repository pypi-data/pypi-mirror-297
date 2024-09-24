from typing import Callable, List, Union
import json
import urllib.request
import edgesync360edgehubedgesdk.Common.Constants as constant
import edgesync360edgehubedgesdk.Common.Topic as mqttTopic
from edgesync360edgehubedgesdk.Model.Edge import (
    EdgeAgentOptions,
    EdgeConfig,
    EdgeDeviceStatus,
    MQTTOptions,
    ConfigAck,
    WriteValueCommand,
    Device,
    Tag,
    EdgeData,
)
from edgesync360edgehubedgesdk.Model.Interface import IMessageClient
from edgesync360edgehubedgesdk.Model.MQTTMessage import *
import edgesync360edgehubedgesdk.Common.Converter as Converter
from edgesync360edgehubedgesdk.Model.Event import *
from edgesync360edgehubedgesdk.Common.Utils import RepeatedTimer
from edgesync360edgehubedgesdk.Common.DataRecoverHelper import DataRecoverHelper
import edgesync360edgehubedgesdk.Common.Logger as logger
from edgesync360edgehubedgesdk.Model.MessageClient.AzureIotHub import (
    AzureIotHubMessageClient,
)
from edgesync360edgehubedgesdk.Model.MessageClient.Mqtt import MqttMessageClient


class EdgeAgent:
    def __init__(self, options: EdgeAgentOptions):
        self.__options = options
        self.__client: IMessageClient
        self.__heartbeatInterval = constant.HeartbeatInterval
        self.__heartBeatTimer: RepeatedTimer | None = None
        if options and options.heartbeat:
            self.__heartbeatInterval = options.heartbeat
        self.__recoverHelper = DataRecoverHelper()
        self.__dataRecoverTimer: RepeatedTimer | None = None
        self.__on_connected: Callable[[bool], None] | None = None
        self.__on_disconnected: Callable[[bool], None] | None = None
        self.__on_messageReceived: Callable[[MessageReceivedEventArgs], None] | None = (
            None
        )

    def __sendData(self, data: EdgeData) -> bool:
        try:
            (result, payloads) = Converter.convertData(data)
            if result:
                for payload in payloads:
                    if not self.isConnected():
                        self.__recoverHelper.write(payload)
                    else:
                        topic = mqttTopic.DataTopic.format(self.__options.nodeId)
                        self.__client.publish_message(topic, payload)
            return result
        except Exception as error:
            logger.printError(e=error, msg="Send data error !")
            return False

    def __sendDataArray(self, datas: List[EdgeData]) -> bool:
        try:
            (result, payloads) = Converter.convertDataWithArray(datas)
            payloads_msg = json.dumps(payloads)
            if result:
                if not self.isConnected():
                    self.__recoverHelper.write(payloads_msg)
                else:
                    topic = mqttTopic.DataTopic.format(self.__options.nodeId)
                    self.__client.publish_message(topic, payloads_msg)
            return result
        except Exception as error:
            print("sendData fail", str(error))
            return False

    def __getCredentialFromDCCS(self):
        try:
            if not self.__options.DCCS:
                raise ValueError("option DCCS should not be empty")

            uri = "{0}/v1/serviceCredentials/{1}".format(
                self.__options.DCCS.apiUrl, self.__options.DCCS.credentialKey
            )
            response = (
                urllib.request.urlopen(uri).read().decode("utf-8").replace('"', '"')
            )
            response = json.loads(response)
            host = response["serviceHost"]
            if self.__options.useSecure:
                port = response["credential"]["protocols"]["mqtt+ssl"]["port"]
                userName = response["credential"]["protocols"]["mqtt+ssl"]["username"]
                password = response["credential"]["protocols"]["mqtt+ssl"]["password"]
            else:
                port = response["credential"]["protocols"]["mqtt"]["port"]
                userName = response["credential"]["protocols"]["mqtt"]["username"]
                password = response["credential"]["protocols"]["mqtt"]["password"]
            mqttOptions = MQTTOptions(
                hostName=host, port=port, userName=userName, password=password
            )
            self.__options.MQTT = mqttOptions
        except Exception as error:
            logger.printError(e=error, msg="Get MQTT credentials from DCCS failed !")

    def __initClient(self) -> IMessageClient:
        if self.__options.connectType == constant.ConnectType["MQTT"]:
            self.__getCredentialFromDCCS()
            if not self.__options.MQTT:
                raise ValueError(f"mqtt connect option should not be empty")

            return MqttMessageClient(
                self.__options.MQTT.hostName,
                self.__options.MQTT.port,
                self.__options.MQTT.userName,
                self.__options.MQTT.password,
                self.__options.nodeId,
                self.__options.MQTT.protocalType,
            )
        elif self.__options.connectType == constant.ConnectType["DCCS"]:
            if not self.__options.MQTT:
                raise ValueError(f"mqtt connect option should not be empty")

            return MqttMessageClient(
                self.__options.MQTT.hostName,
                self.__options.MQTT.port,
                self.__options.MQTT.userName,
                self.__options.MQTT.password,
                self.__options.nodeId,
                self.__options.MQTT.protocalType,
            )
        elif self.__options.connectType == constant.ConnectType["AzureIotHub"]:
            if not self.__options.AzureIotHub:
                raise ValueError(f"azure iot hub connect option should not be empty")

            return AzureIotHubMessageClient(self.__options.AzureIotHub.connectionString)
        else:
            raise ValueError(f"Unsupported client type: {self.__options.connectType}")

    def __sendHeartbeat(self):
        if not self.__client.is_connected():
            return

        if self.__options.type == constant.EdgeType["Gateway"]:
            topic = mqttTopic.NodeConnTopic.format(self.__options.nodeId)
        else:
            topic = mqttTopic.DeviceConnTopic.format(
                self.__options.nodeId, self.__options.deviceId
            )

        heartbeatPayload = HeartbeatMessage().getJson()
        self.__client.publish_message(
            topic,
            heartbeatPayload,
        )

    def __dataRecover(self):
        if not self.__client.is_connected():
            return

        if not self.__recoverHelper.isDataExist():
            return

        payloads = self.__recoverHelper.read()
        topic = mqttTopic.DataTopic.format(self.__options.nodeId)
        for payload in payloads:
            self.__client.publish_message(
                topic,
                payload,
            )

    def __on_connect(self):
        # subscribe
        if self.__options.type == constant.EdgeType["Gateway"]:
            cmdTopic = mqttTopic.NodeCmdTopic.format(self.__options.nodeId)
            connTopic = mqttTopic.NodeConnTopic.format(self.__options.nodeId)
        else:
            cmdTopic = mqttTopic.DeviceCmdTopic.format(
                self.__options.nodeId, self.__options.deviceId
            )
            connTopic = mqttTopic.DeviceConnTopic.format(
                self.__options.nodeId, self.__options.deviceId
            )
        ackTopic = mqttTopic.AckTopic.format(self.__options.nodeId)
        for topic in [ackTopic, cmdTopic]:
            self.__client.subscribe_message(topic)
            print("subscribe {0} successfully".format(topic))

        # publish
        connectPayload = ConnectMessage().getJson()
        self.__client.publish_message(
            connTopic,
            connectPayload,
        )

        self.__sendHeartbeat()
        second = self.__heartbeatInterval
        self.__heartBeatTimer = RepeatedTimer(second, self.__sendHeartbeat)
        if self.__options.dataRecover:
            self.__dataRecoverTimer = RepeatedTimer(
                constant.DataRecoverInterval, self.__dataRecover
            )

        if self.__on_connected is not None:
            self.__on_connected(self.__client.is_connected())

    def __on_disconnect(self):
        if self.__heartBeatTimer is not None:
            self.__heartBeatTimer.stop()
        if self.__dataRecoverTimer is not None:
            self.__dataRecoverTimer.stop()
        if self.__on_disconnected is not None:
            self.__on_disconnected(not self.__client.is_connected())

    def __on_message(self, topic: str, payload: str):
        try:
            message = json.loads(payload)
            # topic = msg.topic
            if not message or not message["d"]:
                return
            if "Cmd" in message["d"]:
                if not message["d"]["Cmd"]:
                    return
                cmd = message["d"]["Cmd"]
                if cmd == "WV":
                    messageType = constant.MessageType["WriteValue"]
                    writeValueMessage = WriteValueCommand()
                    if message["d"]["Val"]:
                        for deviceId, tags in message["d"]["Val"].items():
                            d = Device(deviceId)
                            for tagName, value in tags.items():
                                d.tagList.append(Tag(tagName, value))
                            writeValueMessage.deviceList.append(d)
                    message = writeValueMessage
                else:
                    return
            elif "Cfg" in message["d"]:
                messageType = constant.MessageType["ConfigAck"]
                result = bool(message["d"]["Cfg"])
                message = ConfigAck(result=result)
            else:
                return

            if self.__on_messageReceived:
                self.__on_messageReceived(
                    MessageReceivedEventArgs(msgType=messageType, message=message)
                )

        except Exception as error:
            logger.printError(
                e=error,
                msg=f"Message received event error! topic: {topic}, payload: {payload}",
            )
            pass

    def connect(self):
        try:
            self.__client = self.__initClient()
            self.__client.on_connect(self.__on_connect)
            self.__client.on_disconnect(self.__on_disconnect)
            self.__client.on_message(self.__on_message)
        except Exception as error:
            logger.printError(e=error, msg="Connection setting error !")
        try:
            self.__client.connect()
        except Exception as error:
            logger.printError(e=error, msg="Connect error !")

    def disconnect(self):
        if self.__options.type == constant.EdgeType["Gateway"]:
            topic = mqttTopic.NodeConnTopic.format(self.__options.nodeId)
        else:
            topic = mqttTopic.DeviceConnTopic.format(
                self.__options.nodeId, self.__options.deviceId
            )
        disconnectPayload = DisconnectMessage().getJson()
        self.__client.publish_message(
            topic,
            disconnectPayload,
        )
        self.__client.disconnect()

    def isConnected(self) -> bool:
        return self.__client.is_connected()

    def uploadConfig(self, action: int, edgeConfig: EdgeConfig):
        try:
            nodeId = self.__options.nodeId
            if action == constant.ActionType["Create"]:
                (result, payload) = Converter.convertCreateorUpdateConfig(
                    action=action,
                    nodeId=nodeId,
                    config=edgeConfig,
                    heartbeat=self.__options.heartbeat,
                )
            elif action == constant.ActionType["Update"]:
                (result, payload) = Converter.convertCreateorUpdateConfig(
                    action=action,
                    nodeId=nodeId,
                    config=edgeConfig,
                    heartbeat=self.__options.heartbeat,
                )
            elif action == constant.ActionType["Delete"]:
                (result, payload) = Converter.convertDeleteConfig(
                    action=action, nodeId=nodeId, config=edgeConfig
                )
            elif action == constant.ActionType["Delsert"]:
                (result, payload) = Converter.convertCreateorUpdateConfig(
                    action=action,
                    nodeId=nodeId,
                    config=edgeConfig,
                    heartbeat=self.__options.heartbeat,
                )
            else:
                raise ValueError("config action is invalid !")

            topic = mqttTopic.ConfigTopic.format(self.__options.nodeId)
            self.__client.publish_message(
                topic,
                payload,
            )
            return result
        except Exception as error:
            logger.printError(e=error, msg="Upload config error !")
            return False

    def sendData(self, data: Union[List[EdgeData], EdgeData]) -> bool:
        if isinstance(data, list):
            if len(data) > 0 and type(data[0]) == type(EdgeData()):
                return self.__sendDataArray(data)
            else:
                raise ValueError("sendData(data): data is invalid")
        else:
            return self.__sendData(data)

    def sendDeviceStatus(self, deviceStatus: EdgeDeviceStatus):
        try:
            (result, payload) = Converter.convertDeviceStatus(deviceStatus)
            if result and payload:
                topic = mqttTopic.NodeConnTopic.format(self.__options.nodeId)
                self.__client.publish_message(topic, payload)
            return result
        except Exception as error:
            logger.printError(e=error, msg="Send device status error !")
            return False

    @property
    def on_connected(self):
        return self.__on_connected

    @on_connected.setter
    def on_connected(self, func: Callable[[bool], None]):
        self.__on_connected = func

    @property
    def on_disconnected(self):
        return self.__on_disconnected

    @on_disconnected.setter
    def on_disconnected(self, func: Callable[[bool], None]):
        self.__on_disconnected = func

    @property
    def on_message(self):
        return self.__on_messageReceived

    @on_message.setter
    def on_message(self, func: Callable[[MessageReceivedEventArgs], None]):
        self.__on_messageReceived = func
