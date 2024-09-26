
import requests
import threading
from utils import GetAddressUtil
from utils import CryptoUtil
import time



class SendMessageUtil(threading.Thread):

    def __init__(self, config, get_address_util:GetAddressUtil, crypto_util:CryptoUtil):
        threading.Thread.__init__(self)
        self.get_address_util = get_address_util
        self.crypto_util = crypto_util
        self.config = config
        self.name = config['name']
        self.uid = config['server']['uid']
        self.authorization = config['server']['authorization']
        self.server_address = config['server']['address']
        self.v4_address = self.get_address_util.get_v4_address()
        self.v6_address = self.get_address_util.get_v6_address()
        self.daemon = True
        self.connect_condition = False
        
    def run(self):
        while True:
                data = self.__get_local_info()
                if self.v4_address is None:
                    continue
                self.__send_local_info(data)
                time.sleep(5)

    def get_condition(self):
        return [self.connect_condition, self.v4_address, self.v6_address]

    def __get_local_info(self):
        '''
        获取ip地址
        '''

        self.v4_address = self.get_address_util.get_v4_address()
        self.v6_address = self.get_address_util.get_v6_address()
        encode_ipv4 =  self.crypto_util.encode(self.v4_address)
        encode_ipv6 =  self.crypto_util.encode(self.v6_address)
        data = {'name':self.name, 'uid':self.uid, 'ipv4':encode_ipv4, 'ipv6':encode_ipv6}
        return data

    def __send_local_info(self, data):
        success = False
        while success is False:
            try:
                r = requests.request('GET',self.server_address,data=data,timeout=5)
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
