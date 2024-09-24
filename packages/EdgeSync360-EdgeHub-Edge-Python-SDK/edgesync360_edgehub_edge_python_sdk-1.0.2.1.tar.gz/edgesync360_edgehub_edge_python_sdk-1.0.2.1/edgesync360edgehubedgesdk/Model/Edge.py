from __future__ import annotations
import datetime
from typing import List, Optional

import edgesync360edgehubedgesdk.Common.Constants as constant


class EdgeAgentOptions:
    def __init__(
        self,
        reconnectInterval: int = 1,  # seconds
        nodeId: str = "nodeId",  # None
        deviceId: str = "deviceId",  # None
        type: int = constant.EdgeType["Gateway"],
        heartbeat: int = constant.HeartbeatInterval,
        dataRecover: bool = True,
        connectType: str = constant.ConnectType["DCCS"],
        useSecure: bool = False,
        MQTT: Optional[MQTTOptions] = None,
        DCCS: Optional[DCCSOptions] = None,
        AzureIotHub: Optional[AzureIotHubOptions] = None,
    ):
        self.reconnectInterval = reconnectInterval
        self.nodeId = nodeId
        self.deviceId = deviceId
        self.type = type
        self.heartbeat = heartbeat
        self.connectType = connectType
        self.useSecure = useSecure
        self.dataRecover = dataRecover
        self.MQTT = MQTT
        self.DCCS = DCCS
        self.AzureIotHub = AzureIotHub

        if self.heartbeat < 1:
            self.hearbeat = 1


class MQTTOptions:
    def __init__(
        self,
        hostName: str = "",
        port: int = 1883,
        userName: str = "",
        password: str = "",
        protocalType: str = constant.Protocol["TCP"],
    ):
        self.hostName = hostName
        self.port = int(port)
        self.userName = userName
        self.password = password
        self.protocalType = protocalType

        if hostName == "":
            raise ValueError("hostName can not be empty")
        if userName == "":
            raise ValueError("userName can not be empty")
        if password == "":
            raise ValueError("password can not be empty")
        if not protocalType in constant.Protocol.values():
            raise ValueError("protocalType is not exist.")


class DCCSOptions:
    def __init__(self, apiUrl: str = "", credentialKey: str = ""):
        if apiUrl[-1] == "/":
            apiUrl = apiUrl[:-1]
        self.apiUrl = apiUrl
        self.credentialKey = credentialKey
        if apiUrl == "":
            raise ValueError("apiUrl can not be empty")
        if credentialKey == "":
            raise ValueError("credentialKey can not be empty")


class AzureIotHubOptions:
    def __init__(self, connectionString: str = "") -> None:
        self.connectionString = connectionString
        pass


class EdgeData:
    def __init__(self):
        self.tagList: List[EdgeTag] = []
        self.timestamp = datetime.datetime.now()


class EdgeTag:
    def __init__(self, deviceId: str = "", tagName: str = "", value: object = object()):
        self.deviceId = deviceId
        self.tagName = tagName
        self.value = value


class EdgeStatus:
    def __init__(self, id: str = "", status: int = constant.Status["Offline"]):
        self.id = id
        self.status = status


class EdgeDeviceStatus:
    def __init__(self):
        self.deviceList: List[EdgeStatus] = []


class EdgeConfig:
    def __init__(self):
        self.node = NodeConfig()


class NodeConfig:
    def __init__(self, nodeType: int = constant.EdgeType["Gateway"]):
        self.type = nodeType
        self.deviceList: list[DeviceConfig] = []
        self.heartbeat: int = 300

    def isValid(self):
        if self.type:
            return (False, ValueError("nodeType is necessary"))
        if not (self.type in constant.EdgeType.values()):
            return (False, ValueError("nodeType is invalid"))
        return (True, None)


class DeviceConfig:
    def __init__(
        self,
        id: str = "",
        name: str = "",
        comPortNumber: Optional[int] = None,
        deviceType: Optional[str] = None,
        description: Optional[str] = None,
        ip: Optional[str] = None,
        port: Optional[int] = None,
        retentionPolicyName: Optional[str] = None,
    ):
        self.id = id
        self.name = name
        self.comPortNumber = comPortNumber
        self.type = deviceType
        self.description = description
        self.ip = ip
        self.port = port
        self.retentionPolicyName = retentionPolicyName
        self.analogTagList: list[AnalogTagConfig] = []
        self.discreteTagList: list[DiscreteTagConfig] = []
        self.textTagList: list[TextTagConfig] = []
        if self.id == "":
            raise ValueError("id is necessary")

    def addBlock(self, blockName: str, blockConfig: BlockConfig):
        for tag in blockConfig.analogTagList:
            updateTag = tag.copy()
            updateTag.blockType = blockConfig.blockType
            updateTag.name = "{}:{}".format(blockName, tag.name)
            self.analogTagList.append(updateTag)

        for tag in blockConfig.discreteTagList:
            updateTag = tag.copy()
            updateTag.blockType = blockConfig.blockType
            updateTag.name = "{}:{}".format(blockName, tag.name)
            self.discreteTagList.append(updateTag)

        for tag in blockConfig.textTagList:
            updateTag = tag.copy()
            updateTag.blockType = blockConfig.blockType
            updateTag.name = "{}:{}".format(blockName, tag.name)
            self.textTagList.append(updateTag)

    def isValid(self):
        if self.name == "":
            return (False, ValueError("name is necessary"))
        if self.type is None:
            return (False, ValueError("deviceType is necessary"))
        return (True, None)


class TagConfig:
    def __init__(
        self,
        name: str = "",
        description: str = "",
        readOnly: bool = False,
        arraySize: int = 0,
        type: int = 0,
    ):
        self.name = name
        self.description = description
        self.readOnly = readOnly
        self.arraySize = arraySize
        self.blockType: None | str = None
        self.type = type
        if self.name == "":
            raise ValueError("name is necessary")


class AnalogTagConfig(TagConfig):
    def __init__(
        self,
        name: str = "",
        description: str = "",
        readOnly: bool = False,
        arraySize: int = 0,
        spanHigh: int = 0,
        spanLow: int = 0,
        engineerUnit: str = "",
        integerDisplayFormat: int = 0,
        fractionDisplayFormat: int = 0,
    ):
        super(AnalogTagConfig, self).__init__(
            name=name,
            description=description,
            readOnly=readOnly,
            arraySize=arraySize,
            type=constant.TagType["Analog"],
        )
        self.spanHigh = spanHigh
        self.spanLow = spanLow
        self.engineerUnit = engineerUnit
        self.integerDisplayFormat = integerDisplayFormat
        self.fractionDisplayFormat = fractionDisplayFormat

    def copy(self) -> AnalogTagConfig:
        return AnalogTagConfig(
            name=self.name,
            description=self.description,
            readOnly=self.readOnly,
            arraySize=self.arraySize,
            spanHigh=self.spanHigh,
            spanLow=self.spanLow,
            engineerUnit=self.engineerUnit,
            integerDisplayFormat=self.integerDisplayFormat,
            fractionDisplayFormat=self.fractionDisplayFormat,
        )


class DiscreteTagConfig(TagConfig):
    def __init__(
        self,
        name: str = "",
        description: str = "",
        readOnly: bool = False,
        arraySize: int = 0,
        state0: Optional[str] = None,
        state1: Optional[str] = None,
        state2: Optional[str] = None,
        state3: Optional[str] = None,
        state4: Optional[str] = None,
        state5: Optional[str] = None,
        state6: Optional[str] = None,
        state7: Optional[str] = None,
    ):
        super(DiscreteTagConfig, self).__init__(
            name=name,
            description=description,
            readOnly=readOnly,
            arraySize=arraySize,
            type=constant.TagType["Discrete"],
        )
        self.state0 = state0
        self.state1 = state1
        self.state2 = state2
        self.state3 = state3
        self.state4 = state4
        self.state5 = state5
        self.state6 = state6
        self.state7 = state7

    def copy(self) -> DiscreteTagConfig:
        return DiscreteTagConfig(
            name=self.name,
            description=self.description,
            readOnly=self.readOnly,
            arraySize=self.arraySize,
            state0=self.state0,
            state1=self.state1,
            state2=self.state2,
            state3=self.state3,
            state4=self.state4,
            state5=self.state5,
            state6=self.state6,
            state7=self.state7,
        )


class TextTagConfig(TagConfig):
    def __init__(
        self,
        name: str = "",
        description: str = "",
        readOnly: bool = False,
        arraySize: int = 0,
    ):
        super(TextTagConfig, self).__init__(
            name=name,
            description=description,
            readOnly=readOnly,
            arraySize=arraySize,
            type=constant.TagType["Text"],
        )

    def copy(self) -> TextTagConfig:
        return TextTagConfig(
            name=self.name,
            description=self.description,
            readOnly=self.readOnly,
            arraySize=self.arraySize,
        )


class BlockConfig:
    def __init__(
        self,
        blockType: str,
        analogTagList: list[AnalogTagConfig],
        discreteTagList: list[DiscreteTagConfig],
        textTagList: list[TextTagConfig],
    ):
        self.blockType = blockType
        self.analogTagList = analogTagList
        self.discreteTagList = discreteTagList
        self.textTagList = textTagList


class TimeSyncCommand:
    def __init__(self, time: datetime.datetime = datetime.datetime.now()):
        self.UTCTime = time


class ConfigAck:
    def __init__(self, result: bool = False):
        self.result = result


class WriteValueCommand:
    def __init__(self):
        self.deviceList: List[Device] = []


class Device:
    def __init__(self, id: str = ""):
        self.id = id
        self.tagList: List[Tag] = []


class Tag:
    def __init__(self, name: str = "", value: object = object()):
        self.name = name
        self.value = value
