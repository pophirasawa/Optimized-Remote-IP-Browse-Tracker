from flask_sqlalchemy import SQLAlchemy
from .db_ins import db
from .model import Data
import time


def update_data(data: dict, timestamp: str) -> bool:
    data_uid = data["uid"]
    name = data["name"]
    ipv4 = data["ipv4"]
    ipv6 = data["ipv6"]
    extra = data["extra"]
    data_already_exist = Data.query.filter(Data.uid == data_uid).count()
    if data_already_exist == 0:
        new_data = Data(
            uid=data_uid,
            ipv4=ipv4,
            ipv6=ipv6,
            timestamp=timestamp,
            name=name,
            extra=extra,
        )
        print(new_data.name)
        db.session.add(new_data)
    else:
        now_time = float(time.time())
        if now_time < float(timestamp) + 30:
            Data.query.filter(Data.uid == data_uid).update(
                {
                    "ipv4": ipv4,
                    "ipv6": ipv6,
                    "timestamp": timestamp,
                    "name": name,
                    "extra": extra,
                }
            )
        else:
            return False
    success = True
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        print("asdasdas")
        success = False
    return success


def get_all_data() -> list:
    all_data = Data.query.all()
    res = []
    now_time = str(time.time())
    for data in all_data:
        dict_data = {
            "uid": data.uid,
            "ipv4": data.ipv4,
            "ipv6": data.ipv6,
            "name": data.name,
            "extra": data.extra,
            "online": check_online(data.timestamp, now_time),
        }
        res.append(dict_data)
    return res


def check_online(time1: str, nowtime: str) -> bool:
    return float(nowtime) - float(time1) < 10
