from flask import Flask
from flask import request
from utils import ConfigLoader
from utils import MessageUtil
from flask import abort
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


app = create_app()


@app.route("/synchronize")
@check_authorization
@check_sign
def update_data():
    data = request.form
    timestamp = str(request.headers.get("Timestamp"))
    success = database.update_data(data, timestamp)
    if success is False:
        abort(504)
    return "good"


@app.route("/getdata")
@check_authorization
def get_data():
    datas = database.get_all_data()
    return datas


if __name__ == "__main__":
    my_config = ConfigLoader().config
    port = my_config["port"]
    my_message_util = MessageUtil(my_config)

    app.run(port=port)
