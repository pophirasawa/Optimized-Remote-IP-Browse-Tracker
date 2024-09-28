from app import app
from data_synchronizer import DataSynchronizer
from utils import ConfigLoader
from utils import CryptoUtil
import time

if __name__ == "__main__":
    config = ConfigLoader().config
    my_crypto_util = CryptoUtil(config)
    my_data_synchronizer = DataSynchronizer(config)
    my_data_synchronizer.start()
    while True:
        time.sleep(1)
        print(my_data_synchronizer.get_data())
