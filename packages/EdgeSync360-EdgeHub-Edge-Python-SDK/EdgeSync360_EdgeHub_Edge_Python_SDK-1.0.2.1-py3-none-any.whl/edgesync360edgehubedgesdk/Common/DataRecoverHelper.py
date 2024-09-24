import sqlite3
import os
import threading
from typing import Any, List
import edgesync360edgehubedgesdk.Common.Constants as constants
import edgesync360edgehubedgesdk.Common.Logger as logger


class DataRecoverHelper:
    def __init__(self):
        self.__filePath = os.path.join(os.getcwd(), constants.DBFileName)
        self.__lock = threading.Lock()

    def isDataExist(self):
        result = False
        try:
            if not os.path.isfile(self.__filePath):
                return False
            self.__lock.acquire()
            conn = sqlite3.connect(self.__filePath)
            c = conn.cursor()
            cursor = c.execute("SELECT * FROM Data LIMIT 1")
            for _ in cursor:
                result = True
            conn.close()
            self.__lock.release()
            return result
        except Exception as error:
            self.__lock.release()
            logger.printError(e=error, msg="Check recovery data process error !")
            return False

    def read(self, count: int = constants.DefaultReadRecordCount) -> List[Any]:
        try:
            messages: List[Any] = []
            ids: List[Any] = []
            if not os.path.isfile(self.__filePath):
                return messages
            self.__lock.acquire()
            conn = sqlite3.connect(self.__filePath)
            c = conn.cursor()
            c.execute(
                """CREATE TABLE IF Not exists Data 
      (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      message TEXT NOT NULL);"""
            )
            cursor = c.execute("SELECT * FROM Data LIMIT (?)", (count,))
            for row in cursor:
                ids.append(row[0])
                messages.append(row[1])
            c.execute("DELETE FROM Data WHERE id IN (%s)" % ("?," * len(ids))[:-1], ids)
            conn.commit()
            conn.close()
            self.__lock.release()
            return messages
        except Exception as error:
            self.__lock.release()
            logger.printError(e=error, msg="Read recovery data process error !")
            return []

    def write(self, message: str = ""):
        try:
            self.__lock.acquire()
            conn = sqlite3.connect(self.__filePath)
            c = conn.cursor()
            c.execute(
                """CREATE TABLE IF Not exists Data 
      (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      message TEXT NOT NULL);"""
            )
            c.execute("INSERT INTO Data (message) VALUES (?)", (message,))
            conn.commit()
            conn.close()
            self.__lock.release()
            return True
        except Exception as error:
            self.__lock.release()
            logger.printError(e=error, msg="Write recovery data process error !")
            return False
