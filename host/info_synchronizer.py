import requests
import threading
from utils import GetAddressUtil
from utils import CryptoUtil
from utils import GetExtraInfoUtil
from Crypto.Hash.SHA256 import SHA256Hash
import time
import re
import yaml
import json


class InfoSynchronizer(threading.Thread):
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

    SynchronizerRouting = "/synchronize"

    def __init__(
        self, config, get_address_util: GetAddressUtil, crypto_util: CryptoUtil, update_net_speed: GetExtraInfoUtil.UpdateNetSpeed
    ):
        threading.Thread.__init__(self)
        self.get_address_util = get_address_util
        self.crypto_util = crypto_util
        self.update_net_speed = update_net_speed
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

            send = threading.Thread(target=self.__send_local_info, args=[data, header])
            send.daemon = True
            send.start()
            time.sleep(5)

    def get_condition(self):
        return [self.connect_condition, self.v4_address, self.v6_address]

    def __get_extra_info(self):
        # def convert_to_function_name(extra_name):
        #     # 先转换成大驼峰 使用正则表达式切分 再转换为蛇形
        #     extra_name = extra_name[0].upper() + extra_name[1:]
        #     spilt = ["get"] + re.findall(r'[A-Z][a-z]*', extra_name)
        #     function_name = '_'.join(spilt).lower()
        #     return function_name

        extra_dict = {
            "cpuUsage": [GetExtraInfoUtil.get_cpu_usage],
            "netSpeed": [GetExtraInfoUtil.get_net_speed, self.update_net_speed],
        }

        config_path = "A.yaml"
        extra_info = []

        with open(config_path, "r") as f:
            config = yaml.load(f, Loader=yaml.Loader)
            extra_list = config["extra"]

        for extra_name in extra_list:
            if extra_dict.get(extra_name):
                if len(extra_dict[extra_name]) > 1:
                    extra_function = extra_dict[extra_name][0]
                    extra_args = extra_dict[extra_name][1:]
                    extra_info.append(extra_function(*extra_args))

                else:
                    extra_function = extra_dict[extra_name][0]
                    extra_info.append(extra_function())
    
        return extra_info

    def __get_local_info(self):
        """
        获取ip地址
        """

        self.v4_address = self.get_address_util.get_v4_address()
        self.v6_address = self.get_address_util.get_v6_address()
        encode_ipv4 = self.crypto_util.encode(self.v4_address)
        encode_ipv6 = self.crypto_util.encode(self.v6_address)
        extra_info = self.__get_extra_info()
        data = {
            "name": self.name,
            "uid": self.uid,
            "ipv4": encode_ipv4,
            "ipv6": encode_ipv6,
            "extra": json.dumps(extra_info),
        }
        print(data)

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
        try:
            r = requests.request(
                "GET",
                self.server_address + self.SynchronizerRouting,
                data=data,
                headers=header,
                timeout=10,
                verify=False,
            )

            if r.status_code == 200:
                success = True
            else:
                print(r)
            self.connect_condition = success

        except Exception as e:
            self.connect_condition = success
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
