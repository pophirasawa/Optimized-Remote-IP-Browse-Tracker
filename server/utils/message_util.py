import requests
import threading
from Crypto.Hash.SHA256 import SHA256Hash
import json
import time


class MessageUtil:
    """
    get_send_headers(self, data) 计算需要发送信息的headers内容
    check_headers_authorization(self, headers) 查看headers内签名是否合法
    check_data_sign(self, headers, data) 查看data签名是否合法
    """

    _instance = None
    _init = False

    def __init__(self, config=None):
        if self._init is True and config is None:
            return

        self._init = True
        self.config = config
        self.authorization = config["authorization"]

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(MessageUtil, cls).__new__(cls)
        return cls._instance

    def get_send_headers(self, data) -> dict:
        timestamp = str(time.time())
        authorization_sign = self.__get_authorization_sign(timestamp)
        data_sign = self.__get_data_sign(data, timestamp)
        header = {
            "authorization": authorization_sign,
            "sign": data_sign,
            "timestamp": timestamp,
        }
        return header

    def check_headers_authorization(self, headers) -> bool:
        dict_headers = dict(headers)
        if (
            "Authorization" in dict_headers
            and "Timestamp" in dict_headers
            # and "Sign" in dict_headers
        ) is False:
            return False

        return (
            self.__get_authorization_sign(dict_headers["Timestamp"])
            == dict_headers["Authorization"]
        )

    def check_data_sign(self, headers, data: dict) -> bool:
        dict_headers = dict(headers)
        return self.__get_data_sign(
            data, dict_headers["Timestamp"]
        ) == dict_headers.get("Sign")

    def __get_authorization_sign(self, timestamp: str) -> str:
        authorization_sign = self.authorization + timestamp
        authorization_sign = SHA256Hash(authorization_sign.encode("utf-8")).hexdigest()
        return authorization_sign

    def __get_data_sign(self, data, timestamp: str) -> str:
        data_json = json.dumps(data)
        data_sign = data_json + self.authorization + timestamp
        data_sign = SHA256Hash(data_sign.encode("utf-8")).hexdigest()
        return data_sign
