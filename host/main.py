from utils import ConfigLoader
from utils import GetAddressUtil
from utils import GetExtraInfoUtil
from utils import CryptoUtil
from utils import resource_path
from info_synchronizer import InfoSynchronizer
import time
from pystray import Icon, Menu, MenuItem
from PIL import Image
import threading
import ctypes
import os


def is_running() -> bool:
    mutex_name = "MyAppMutex"
    mutex = ctypes.windll.kernel32.CreateMutexW(None, True, mutex_name)
    if ctypes.windll.kernel32.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
        ctypes.windll.kernel32.CloseHandle(mutex)
        return True
    return False


def run():
    config = ConfigLoader().config
    my_crypto_util = CryptoUtil(config)
    my_get_address_util = GetAddressUtil(config)
    net_speed_measure = GetExtraInfoUtil.UpdateNetSpeed()

    my_send_message_util = InfoSynchronizer(
        config, my_get_address_util, my_crypto_util, net_speed_measure
    )
    my_get_address_util.start()
    my_send_message_util.start()
    net_speed_measure.start()

    def main_loop():
        while True:
            time.sleep(1)
            connect_condition = my_send_message_util.get_condition()

            # 生成连接信息
            connect_info = str("Update State: ")
            if connect_condition[0] is True:
                connect_info += "Good\n"
            else:
                connect_info += "Bad\n"
            connect_info += "Ipv4: " + str(connect_condition[1]) + "\n"
            connect_info += "Ipv6: " + str(connect_condition[2])

            icon.title = connect_info

    loop = threading.Thread(target=main_loop)
    loop.daemon = True
    loop.start()


def on_quit():
    icon.stop()


icon = Icon(
    name="My App",
    title="Initalizing...",
    icon=Image.open(resource_path("assets/1.jpg")),
    menu=Menu(MenuItem("Quit", on_quit)),
)


if __name__ == "__main__":

    if is_running():
        raise Exception("software is running.")
    else:
        run()
        icon.run_detached()
