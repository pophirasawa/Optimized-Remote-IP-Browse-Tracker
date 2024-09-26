from flask import Flask, request
import json
from Crypto.Hash.SHA256 import SHA256Hash


app = Flask(__name__)
auth = "yourauthorizationkey"


def get_sign(data, timestamp: str) -> str:
    sign = data + timestamp
    sign = SHA256Hash(sign.encode("utf-8")).hexdigest()
    return sign


@app.route("/")
def hello_world():
    auth_sign = request.headers.get("Authorization")
    data_sign = request.headers.get("Sign")
    timestamp = request.headers.get("Timestamp")
    data = request.form
    data_json = json.dumps(data)
    cal_auth_sign = get_sign(auth, timestamp)
    cal_data_sign = get_sign(data_json, timestamp)
    print(cal_auth_sign)
    print(auth_sign)
    return request.form


if __name__ == "__main__":
    app.run(host="localhost", port=1234)
