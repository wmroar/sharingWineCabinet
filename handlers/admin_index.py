# coding:utf-8
from base import BaseHandler
import logging
from libs.model import Goods, FdGridInfo, Order, FdManagerInfo
from utils.utils import obj2dict
from auth.auth import admin_required

class OverviewHandler(BaseHandler):
    @admin_required
    def post(self):
        result = {
            'sellers' : self._sellers(),
            'user_num' : self._user_num(),
            'order_num' : self._order_num()
        }
        return self.write_json(200, 'success', result)

    def _sellers(self):
        if self.user.role != 100:
            sql = """select sum(amount) from `order` where status = 1 and fid in (select fid from fd_manage_info where manage_uid = %s)""" % self.user.id
        else:
            sql = """select sum(amount) from `order` where status = 1"""
        data = self.db.execute(sql)
        return data[0][0]

    def _user_num(self):
        sql = """select count(1) from `user`"""
        data = self.db.execute(sql)
        return data[0][0]

    def _order_num(self):
        if self.user.role != 100:
            sql = """select count(1) from `order` where status = 1 and fid in (select fid from fd_manage_info where manage_uid = %s)""" % self.user.id
        else:
            sql = """select count(1) from `order` where status = 1"""
        data = self.db.execute(sql)
        return data[0][0]
