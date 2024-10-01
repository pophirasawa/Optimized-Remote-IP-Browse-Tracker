from flask import Flask
from flask import request
from flask import abort
from flask import make_response
from utils import ConfigLoader
from utils import MessageUtil
from utils import GetAddressUtil
from utils import CryptoUtil
from authorization import check_authorization, check_sign
from database.db_ins import db
import database


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app


def init_app(app):
    my_config = ConfigLoader().config
    my_message_util = MessageUtil(my_config)
    my_address_uitl = GetAddressUtil(my_config)
    my_crypto_util = CryptoUtil(my_config)
    my_address_uitl.start()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()


app = Flask(__name__)
init_app(app)


@app.route("/synchronize", methods=["GET", "POST"])
@check_authorization
@check_sign
def update_data():
    data = request.form
    timestamp = str(request.headers.get("Timestamp"))
    success = database.update_data(data, timestamp)
    if success is False:
        abort(504)
    return "good"


@app.route("/whoimi")
@check_authorization
def return_server_data():
    config = ConfigLoader().config
    server_name = config["name"]
    ipv4 = GetAddressUtil().get_v4_address()
    ipv6 = GetAddressUtil().get_v6_address()
    data = {
        "name": server_name,
        "ipv4": CryptoUtil().encode(ipv4),
        "ipv6": CryptoUtil().encode(ipv6),
    }
    headers = MessageUtil().get_send_headers(data=data)
    r = make_response(data, 200, headers)
    return r


@app.route("/getdata", methods=["GET"])
@check_authorization
def get_data():
    datas = database.get_all_data()
    headers = MessageUtil().get_send_headers(data=datas)
    r = make_response(datas, 200, headers)
    return r


@app.route("/test")
def test():
    return "1"


if __name__ == "__main__":
    my_config = ConfigLoader().config
    port = my_config["port"]
    my_message_util = MessageUtil(my_config)

    app.run(port=port)
