import yaml
from utils import ConfigLoader
from utils import Servers, Config
import threading
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from data_synchronizer import DataSynchronizer
from utils import ConfigLoader
from utils import CryptoUtil
import sqlite3

example_config = yaml.load(
    """
    authorization: 'yourauthorizationkey'
    encodingkey: 'yourencodingkey'
    serveraddress: 'https://127.0.0.1'
    database:
        updatefreq: 10
        address: 'sqlite:///C:\\Users\\PopHirasawa\\Desktop\\1Remote-1.0.0-net6-x64\\1Remote.db'
        maps:
            uid: databaseid

    """,
    Loader=yaml.Loader,
)


def use_1remote():
    ConfigLoader.default_config = example_config


class RemoteSynchronizer(threading.Thread):
    _instance = None
    _init = False

    def __init__(self, config, data_synchronizer):
        if self._init is False and config == None:
            raise Exception("config should not be None")
        if self._init:
            return
        threading.Thread.__init__(self)
        self.config = config
        self.db_address = config["database"]["address"]
        self.update_freq = config["database"]["updatefreq"]
        self.maps = config["database"]["maps"]
        self.daemon = True
        self.session = None
        self.data_synchronizer = data_synchronizer

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(RemoteSynchronizer, cls).__new__(cls)
        return cls._instance

    def run(self):
        self.__connect_database()
        while True:
            self.__update_data()
            time.sleep(10)

    def __update_data(self):
        datas = self.data_synchronizer.get_data()
        for i in datas:
            uid = i["uid"]
            ipv4 = i["ipv4"]
            ipv6 = i["ipv6"]
            name = i["name"]
            remote_id = self.maps.get(uid)
            print(remote_id)
            if remote_id is None:
                continue
            server = (
                self.session.query(Servers)
                .filter(Servers.Id == remote_id)
                .one_or_none()
            )
            if server is None:
                continue
            a = json.loads(server.Json)
            print(a["DisplayName"])
            if str(ipv6) != "None":
                a["Address"] = ipv6
            else:
                if str(ipv4) != "None":
                    a["Address"] = ipv4
            a["DisplayName"] = name
            server.Json = json.dumps(a)
        nowtime = str(int(1000 * time.time()))
        update_time_config = (
            self.session.query(Config).filter(Config.Key == "UpdateTimestamp").one()
        )
        update_time_config.Value = nowtime
        try:
            self.session.commit()
        except Exception as e:
            print(e)

    def __connect_database(self):
        engine = create_engine(self.db_address)
        Session = sessionmaker(bind=engine)
        self.session = Session()


if __name__ == "__main__":
    use_1remote()
    config = ConfigLoader().config
    my_crypto_util = CryptoUtil(config)
    print(config)
    my_data_synchronizer = DataSynchronizer(config)
    my_data_synchronizer.start()
    my_remote_synchronizer = RemoteSynchronizer(config, my_data_synchronizer)
    my_remote_synchronizer.start()
    while True:
        time.sleep(1)
    print(config)
