import requests
import threading
from utils import CryptoUtil
from utils import decode_datas
from Crypto.Hash.SHA256 import SHA256Hash
import time
import json


class DataSynchronizer(threading.Thread):
    """获得Data并解码"""

    SynchronizerRouting = "/getdata"
    _instance = None
    _init = False
    data = []
    update_time = time.time()

    def __init__(self, config=None):

        if self._init and not config:
            return
        threading.Thread.__init__(self)

        self.config = config
        self.daemon = True
        self.authorization = self.config["authorization"]
        self.server_address = self.config["serveraddress"]
        self.write_lock = threading.Lock()

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(DataSynchronizer, cls).__new__(cls)
        return cls._instance

    def run(self):
        while True:
            self.refresh_data()
            time.sleep(5)

    def refresh_data(self):
        header = self.__get_headers()
        send = threading.Thread(target=self.__send_request, args=[header])
        send.daemon = True
        send.start()

    def get_data(self):
        while True:
            if self.write_lock.locked():
                continue
            return decode_datas(self.data)

    def __get_headers(self):
        """
        获取ip地址
        """

        timestamp = str(time.time())
        authorization_sign = self.__get_authorization_sign(timestamp)
        headers = {
            "authorization": authorization_sign,
            "timestamp": timestamp,
        }

        return headers

    def __send_request(self, header):
        try:
            r = requests.request(
                "GET",
                self.server_address + self.SynchronizerRouting,
                headers=header,
                timeout=3,
                verify=False,
            )

            if r.status_code == 200:
                print(r)
            else:
                print(r)
                return
        except Exception as e:
            print(e)
            return
        # print(r.json())
        self.__update_data(r.json())

    def __update_data(self, data):
        nowtime = time.time()
        if nowtime < self.update_time:
            return
        with self.write_lock:
            self.data = data
            self.update_time = nowtime

    def __get_authorization_sign(self, timestamp: str) -> str:
        authorization_sign = self.authorization + timestamp
        authorization_sign = SHA256Hash(authorization_sign.encode("utf-8")).hexdigest()
        return authorization_sign
