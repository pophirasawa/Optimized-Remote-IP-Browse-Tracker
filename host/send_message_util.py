import requests
import threading
from utils import GetAddressUtil
from utils import CryptoUtil
from Crypto.Hash.SHA256 import SHA256Hash
import time
import json


class SendMessageUtil(threading.Thread):
    """发送加密后的IP地址
    headers:
        - authorization = SHA256(authorization_key + timestamp)
        - sign = SHA256(data_json + authorization_key + timestamp)
        - timestamp
    data:
        - name
        - uid
        - ipv4
        - ipv6
    """

    def __init__(
        self, config, get_address_util: GetAddressUtil, crypto_util: CryptoUtil
    ):
        threading.Thread.__init__(self)
        self.get_address_util = get_address_util
        self.crypto_util = crypto_util
        self.config = config
        self.name = config["name"]
        self.uid = config["server"]["uid"]
        self.authorization = config["server"]["authorization"]
        self.server_address = config["server"]["address"]
        self.v4_address = self.get_address_util.get_v4_address()
        self.v6_address = self.get_address_util.get_v6_address()
        self.daemon = True
        self.connect_condition = False

    def run(self):
        while True:
            data, header = self.__get_local_info()
            if self.v4_address is None:
                continue

            self.__send_local_info(data, header)
            time.sleep(5)

    def get_condition(self):
        return [self.connect_condition, self.v4_address, self.v6_address]

    def __get_local_info(self):
        """
        获取ip地址
        """

        self.v4_address = self.get_address_util.get_v4_address()
        self.v6_address = self.get_address_util.get_v6_address()
        encode_ipv4 = self.crypto_util.encode(self.v4_address)
        encode_ipv6 = self.crypto_util.encode(self.v6_address)
        data = {
            "name": self.name,
            "uid": self.uid,
            "ipv4": encode_ipv4,
            "ipv6": encode_ipv6,
        }

        timestamp = str(time.time())
        authorization_sign = self.__get_authorization_sign(timestamp)
        data_sign = self.__get_data_sign(data, timestamp)
        header = {
            "authorization": authorization_sign,
            "sign": data_sign,
            "timestamp": timestamp,
        }

        return data, header

    def __send_local_info(self, data, header):
        success = False
        while not success:
            try:
                r = requests.request(
                    "GET", self.server_address, data=data, headers=header, timeout=5
                )

                if r.status_code == 200:
                    success = True
                else:
                    time.sleep(1)
                    print(r)
                self.connect_condition = success

            except Exception as e:
                self.connect_condition = success
                time.sleep(1)
                print(e)

    def __get_authorization_sign(self, timestamp: str) -> str:
        authorization_sign = self.authorization + timestamp
        authorization_sign = SHA256Hash(authorization_sign.encode("utf-8")).hexdigest()
        return authorization_sign

    def __get_data_sign(self, data, timestamp: str) -> str:
        data_json = json.dumps(data)
        data_sign = data_json + self.authorization + timestamp
        data_sign = SHA256Hash(data_sign.encode("utf-8")).hexdigest()
        return data_sign
