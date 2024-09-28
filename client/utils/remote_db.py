from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, VARCHAR, TEXT

Base = declarative_base()


class Servers(Base):
    __tablename__ = "Servers"  # 表名
    Id = Column(VARCHAR, primary_key=True, nullable=False)  # 定义列
    Json = Column(VARCHAR, nullable=False)


class Config(Base):
    __tablename__ = "configs"  # 表名
    Key = Column(VARCHAR(64), primary_key=True, nullable=False)  # 定义列
    Value = Column(TEXT, nullable=False)
