import json
import datetime
import time
from typing import Any
import edgesync360edgehubedgesdk.Common.Constants as constant

format = "%Y-%m-%dT%H:%M:%S.%fZ"


class Message(dict):
    def __init__(self):
        self.message: dict[str, Any] = {}
        self.message["d"] = {}
        self.message["ts"] = datetime.datetime.now().strftime(format)

    def __repr__(self):
        return repr(self.__dict__)

    def getJson(self):
        return json.dumps(self.message)


class LastWillMessage(Message):
    def __init__(self):
        super().__init__()
        self.message["d"] = {"UeD": 1}


class DisconnectMessage(Message):
    def __init__(self):
        super().__init__()
        self.message["d"] = {"DsC": 1}


class HeartbeatMessage(Message):
    def __init__(self):
        super().__init__()
        self.message["d"] = {"Hbt": 1}


class ConnectMessage(Message):
    def __init__(self):
        super().__init__()
        self.message["d"] = {"Con": 1}


class DataMessage(Message):
    def __init__(self):
        super().__init__()

    def setTagValue(self, deviceId: str, tagName: str, value: object):
        if not (deviceId in self.message["d"]):
            self.message["d"][deviceId] = {}
        self.message["d"][deviceId][tagName] = value

    def setTimestamp(self, timestamp: datetime.datetime):
        ts = time.mktime(timestamp.timetuple())
        self.message["ts"] = (
            datetime.datetime.utcfromtimestamp(ts)
            .replace(microsecond=timestamp.microsecond)
            .strftime(format)
        )


class DeviceStatusMessage(Message):
    def __init__(self):
        super().__init__()
        self.message["d"] = {"Dev": {}}

    def setDeviceStatus(self, deviceId: str, status: int):
        self.message["d"]["Dev"][deviceId] = status


class ConfigMessage(Message):
    def __init__(self, action: int = 0, nodeId: str = ""):
        super().__init__()
        if not action in constant.ActionType.values():
            raise ValueError("action is invalid")
        if nodeId == "":
            raise ValueError("action is necessary")

        self.message["d"] = {"Action": action, "Scada": {nodeId: {}}}

    def addNodeConfig(self, nodeId: str, config: object):
        _config = {}
        mapper = constant.NodeConfigMapper
        for key in mapper:
            value = getattr(config, key, None)
            if not value is None:
                _config[mapper[key]] = value
        self.message["d"]["Scada"][nodeId] = _config

    def deleteNodeConfig(self, nodeId: str):
        self.message["d"]["Scada"][nodeId] = {}

    def addDeviceConfig(self, nodeId: str, deviceId: str, config: object):
        _config = {}
        mapper = constant.DeviceConfigMapper
        for key in mapper:
            value = getattr(config, key, None)
            if not value is None:
                _config[mapper[key]] = value

        if not nodeId in self.message["d"]["Scada"]:
            self.message["d"]["Scada"][nodeId] = {}
        if not "Device" in self.message["d"]["Scada"][nodeId]:
            self.message["d"]["Scada"][nodeId]["Device"] = {}
        self.message["d"]["Scada"][nodeId]["Device"][deviceId] = _config

    def deleteDeviceConfig(self, nodeId: str, deviceId: str):
        if not nodeId in self.message["d"]["Scada"]:
            self.message["d"]["Scada"][nodeId] = {}
        if not "Device" in self.message["d"]["Scada"][nodeId]:
            self.message["d"]["Scada"][nodeId]["Device"] = {}
        self.message["d"]["Scada"][nodeId]["Device"][deviceId] = {}

    def addTagConfig(self, nodeId: str, deviceId: str, tagName: str, config: object):
        _config = {}
        mapper = constant.TagConfigMapper
        boolMapper = ["readOnly"]
        for key in mapper:
            value = getattr(config, key, None)
            if not value is None:
                if key in boolMapper:
                    value = 1 if value == True else 0
                _config[mapper[key]] = value

        if not nodeId in self.message["d"]["Scada"]:
            self.message["d"]["Scada"][nodeId] = {}
        if not "Device" in self.message["d"]["Scada"][nodeId]:
            self.message["d"]["Scada"][nodeId]["Device"] = {}
        if not deviceId in self.message["d"]["Scada"][nodeId]["Device"]:
            self.message["d"]["Scada"][nodeId]["Device"][deviceId] = {}
        if not "Tag" in self.message["d"]["Scada"][nodeId]["Device"][deviceId]:
            self.message["d"]["Scada"][nodeId]["Device"][deviceId]["Tag"] = {}
        self.message["d"]["Scada"][nodeId]["Device"][deviceId]["Tag"][tagName] = _config

    def deleteTagConfig(self, nodeId: str, deviceId: str, tagName: str):
        if not nodeId in self.message["d"]["Scada"]:
            self.message["d"]["Scada"][nodeId] = {}
        if not "Device" in self.message["d"]["Scada"][nodeId]:
            self.message["d"]["Scada"][nodeId]["Device"] = {}
        if not deviceId in self.message["d"]["Scada"][nodeId]["Device"]:
            self.message["d"]["Scada"][nodeId]["Device"][deviceId] = {}
        if not "Tag" in self.message["d"]["Scada"][nodeId]["Device"][deviceId]:
            self.message["d"]["Scada"][nodeId]["Device"][deviceId]["Tag"] = {}
        self.message["d"]["Scada"][nodeId]["Device"][deviceId]["Tag"][tagName] = {}
