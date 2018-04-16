# -*- coding:utf-8 -*-
from sqlalchemy import Column, String, Integer, VARCHAR,ForeignKey, Float,Time,Text,DateTime,Date,JSON,BOOLEAN
from sqlalchemy.orm import relationship,backref
from database import engine,Base
import sqlalchemy
from datetime import datetime
import time
# from libs.const.GuideConfig import INIT_GUIDE_ID, INIT_GUIDE_STEP_ID
from libs.const import GuideConfig


def init_db():
    Base.metadata.create_all(engine)

def drop_db():
    Base.metadata.drop_all(engine)

class Recode(object) :
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    id = Column(Integer, primary_key = True, autoincrement = True)

class User(Base, Recode) :
    __tablename__ = 'user'
    user_name = Column(VARCHAR(128))
    passwd = Column(VARCHAR(128))
    tel = Column(VARCHAR(12))
    code = Column(VARCHAR(50))
    nick_name = Column(VARCHAR(50))
    grade = Column(Integer, default = 0)
    sex = Column(Integer, default = 0)
    reg_time = Column(DateTime, default=datetime.now)
    role = Column(Integer, default = 1)
    first_pay = Column(Integer, default = 0)
    idfa = Column(VARCHAR(128))

class SysUser(Base, Recode) :
    __tablename__ = 'sys_user'
    user_name = Column(VARCHAR(128))
    passwd = Column(VARCHAR(128))
    nick_name = Column(VARCHAR(50))
    reg_time = Column(DateTime, default=datetime.now)
    role = Column(Integer, default = 1, doc= '0 超级管理员 1普通管理员 2巡检人员')

class Privilege(Base):
    role = Column(Integer)
    priv = Column(VARCHAR(128), doc='权限详情, 没有也别标注的都是通用的')
    des =  Column(VARCHAR(128),doc='权限详情说明')

class Token(Base, Recode) :
    __tablename__ = 'token'
    tid = Column(Integer, primary_key = True, autoincrement= True)
    user_name =  Column(VARCHAR(40))
    token  = Column(VARCHAR(128))
    times = Column(Integer, default = 0)

class UserLogin(Base, Recode):
    __tablename__ = 'userlogin'
    uid = Column(Integer)
    user_name = Column(VARCHAR(128))
    login_time = Column(Integer)

class UserRegister(Base, Recode):
    __tablename__ = 'userregister'
    uid = Column(Integer)
    user_name = Column(VARCHAR(128))
    register_time = Column(Integer)

class TelLoginCode(Base, Recode):
    __tablename__ = 'user_code'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tel = Column(VARCHAR(16), default = '')
    code = Column(VARCHAR(12), default = '')
    ftime = Column(Integer, default = 0)

class TelLoginLog(Base, Recode):
    __tablename__ = 'user_tel_login'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tel = Column(VARCHAR(16), default = '')
    faild_times = Column(Integer, default = 0)
