# -*- coding:utf-8 -*-
from tornado.web import RequestHandler
import tornado.gen
import json
import os
from libs import model,database
from libs.model import User,Token,UserLogin, UserRegister
from config.conf import settings
import json
import base64
from datetime import datetime,date
import time
import logging
from tornado.web import StaticFileHandler
from utils import utils
from utils.utils import obj2dict
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class DictLikeArgs(object):
    def __init__(self, dic):
        self.d = dic

    def __iter__(self):
        return self.d.__iter__()

    def get(self, key, default):
        '''
        返回 self.d[key] 的首个元素, 若有该 key 的话
        '''
        v = self.d.get(key, default)
        if v and isinstance(v, list):
            # print 'return v[:1][0]=', v[:1][0]    # debug
            return v[:1][0]
        else:
            # print 'return v=', v        # debug
            return v

    def __str__(self):
        return str(self.d)

class BaseHandler(RequestHandler) :

    def initialize(self):
        self.db = database.DB_Session()
        try:
            self.args = json.loads(self.request.body)
        except Exception, e:
            self.args = DictLikeArgs(self.request.arguments)

    def on_finish(self):
        self.db.close()

    def commit(self) :
        try :
            self.db.commit()
            return True
        except Exception, e:
            logging.error(e)
            # self.db.rollback()
            return False

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get_current_user(self):
        try :
            authinfo = base64.b64decode(self.args.get('Authorization', '')).split(',')
        except Exception, e :
            logging.error(e)
            return None
        if len(authinfo) != 4 :
            return None
        user_name = authinfo[1]
        token = self.db.query(Token).filter(Token.token == self.args.get('Authorization', ''), Token.user_name == user_name).order_by(Token.id.desc()).first()
        if not token :
            return None
        if (datetime.now() - token.update_time).seconds > 20 * 24 * 60 * 60 :
            self.del_token(user_name)
            return None
        user = self.db.query(User).filter_by(user_name=user_name).first()
        if not user:
            return None
        # 用户冻结之后不能正常登陆和使用
        if user.role == -1:
            return None
        self.user = user
        return user

    def del_token(self, user_name) :
        self.db.query(Token).filter_by(user_name =  user_name).delete()
        self.db.commit()

    def add_token(self, user_name) :
        if not user_name:
            return None
        self.del_token(user_name)
        token_str = base64.b64encode(','.join(['emm', user_name, 'youcanguessthis', str(int(time.time()))]))
        token = Token(token = token_str, user_name = user_name)
        # self.record_login(user_name)
        self.db.add(token)
        # self.add_token2redis(user_name,token_str)
        self.db.commit()
        return token_str

    def write_json(self, code, info, data = None):
        result = {'code' : code if code else 200, 'info' : info, 'data' : {}}
        if data:
            result['data'] = data
        self.write(result)

class UploadHandler(BaseHandler) :
    def options(self) :
        result = {}
        for key, value in self.request.files.items():
            for one in value:
                filename = os.path.dirname(__file__) + '/../static/uploads/' +one['filename']
                with open(filename, 'wb') as a:
                    a.write(one['body'])
                result['url'] = self.oss.get_sign_url(one['filename'])
                result['name'] = one['filename']
        return self.write(json.dumps(result))

    def post(self) :
        return self.options()
