'''
获取当前ip地址
'''
import socket
import threading
import time

class GetAddressUtil(threading.Thread):
    '''
    获取地址
    '''
    _instance = None
    _init = False
    v4_address:str = None
    v6_address:str = None
    def __init__(self, config=None):
        threading.Thread.__init__(self)
        if self._init is True and config is None:
            return

        DEFAULT_UPDATE_FREQ = 30
        self._init = True
        self.config = config
        self.daemon = True
        self.write_lock = threading.Lock()
        if self.config is None:
            self.update_freq = DEFAULT_UPDATE_FREQ
        else:
            self.update_freq = self.config['updatefreq']
    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = super(GetAddressUtil, cls).__new__(cls)
        return cls._instance

    def run(self):
        while(True):
            new_v4_address = self.__get_v4_address()
            new_v6_address = self.__get_v6_address()
            with self.write_lock:
                if new_v4_address is not None:
                    self.v4_address = new_v4_address
                if new_v6_address is not None:
                    self.v6_address = new_v6_address

            time.sleep(self.update_freq)

    def get_v4_address(self)->str:
        while(True):
            if self.write_lock.locked():
                continue
            return  self.v4_address

    def get_v6_address(self)->str:
        while(True):
            if self.write_lock.locked():
                continue
            return  self.v6_address

    @classmethod
    def __get_v4_address(cls)->str:
        try:
            # 创建一个UDP socket对象
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # 连接到公网地址
            s.connect(('8.8.8.8', 80))
            # 获取本地IP地址
            ip = s.getsockname()[0]
            # 关闭socket连接
            s.close()
            return ip
        except socket.error as e:
            print(e)
            return None

    @classmethod
    def __get_v6_address(cls)->str:
        try:
            s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
            s.connect(('240c::6666', 80))
            #获取出口ipv6地址
            temporary_v6_address = s.getsockname()[0]
            s.close()
            #ipv6地址列表
            addr_list = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)
            ip = None
            for i in addr_list:
                addr = i[4][0]
                if addr[0:4] != 'fe80' and addr!=temporary_v6_address:
                    #筛选本地地址以及临时地址
                    ip = addr
            if ip is None:
                ip = temporary_v6_address
            return ip

        except socket.error as e:
            print(e)
            return None


if __name__ == '__main__':
    my_address_util = GetAddressUtil(30)
    my_address_util.start()
    while(True):
        time.sleep(5)
        a = my_address_util.get_v4_address()
        b = my_address_util.get_v6_address()
        print(a)
        print(b)
