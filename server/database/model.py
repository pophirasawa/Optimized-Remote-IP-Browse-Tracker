from .db_ins import db
from sqlalchemy import Column, VARCHAR, TEXT


class Data(db.Model):
    __tablename__ = "data"  # 设置表名, 表名默认为类名小写
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=False)
    uid = db.Column(db.String(64), unique=True)
    ipv4 = db.Column(db.String(64), unique=False)
    ipv6 = db.Column(db.String(64), unique=False)
    extra = db.Column(TEXT, default="null")
    timestamp = db.Column(db.String(64), unique=False)
