from utils import ConfigLoader
from utils import GetAddressUtil
from utils import CryptoUtil
from utils import resource_path
from send_message_util import SendMessageUtil
import time
import sys
from pystray import Icon, Menu, MenuItem
from PIL import Image
import threading


def run():
    config = ConfigLoader().config
    my_crypto_util = CryptoUtil(config)
    my_get_address_util = GetAddressUtil(config)
    my_send_message_util = SendMessageUtil(config, my_get_address_util, my_crypto_util)
    my_get_address_util.start()
    my_send_message_util.start()

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
    run()
    icon.run_detached()
