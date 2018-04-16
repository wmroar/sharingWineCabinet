# -*- coding:utf-8 -*-
from handlers import base
from libs.model import ReuqestLog
from utils.return_info import res_content
import functools
import greenlet
import tornado

def login_required(f):
    @tornado.web.asynchronous
    @functools.wraps(f)
    def wrapper(self,*args,**kwargs):
        def greenlet_base_func():
            user = self.get_current_user()
            if not user :
                result = self.write(res_content(401, u'用户尚未登录,请登录'))
                self.finish()
            else:
                self.user = user
                # self.set_user_game_info(self.user.id)
                result = f(self, *args,**kwargs)
                # 记录访问请求
                rl = ReuqestLog(uid = self.user.id, host = self.request.remote_ip, uri = self.request.uri)
                self.db.add(rl)
                self.db.commit()
                self.finish()
            return result
        # greenlet_base_func()
        gr = greenlet.greenlet(greenlet_base_func)
        gr.switch()
    return wrapper

def admin_required(f):
    @functools.wraps(f)
    def wrapper(self,*args,**kwargs):
        user = self.get_current_user()
        if not user :
            return self.write(res_content(401, u'用户尚未登录,请登录'))
        # 普通管理员权限
        if user.role != 10:
            return self.write(res_content(405, u'需要管理员权限'))
        else:
            return f(self,*args,**kwargs)
    return wrapper

def super_required(f):
    @functools.wraps(f)
    def wrapper(self,*args,**kwargs):
        user = self.get_current_user()
        if not user :
            return self.write(res_content(401, u'用户尚未登录,请登录'))
        #超级管理员权限
        if user.role != 100:
            return self.write(res_content(405, u'需要超级管理员权限'))
        else:
            return f(self,*args,**kwargs)
    return wrapper
