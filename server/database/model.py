from .db_ins import db


class Data(db.Model):
    __tablename__ = "data"  # 设置表名, 表名默认为类名小写
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    uid = db.Column(db.String(64), unique=True)
    ipv4 = db.Column(db.String(64), unique=False)
    ipv6 = db.Column(db.String(64), unique=False)
    timestamp = db.Column(db.String(64), unique=False)
