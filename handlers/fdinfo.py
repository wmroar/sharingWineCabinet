# coding:utf-8
from base import BaseHandler
import logging
from libs.model import Goods, FdGridInfo
from utils.utils import obj2dict
from auth.auth import admin_required, login_required

class FdinfoListHandler(BaseHandler):
    def get(self):
        return self.post()

    @admin_required
    def post(self):
        num = self.args.get('num', 15)
        page = self.args.get('page', 1)
        try:
            num  = int(num)
            page = int(page)
        except Exception, e:
            logging.info(e)
            return self.write_json(600, '参数错误')
        start_num = (page - 1) * num
        sql = """select fd.id fid,
                        fd.name name,
                        fd.alias alias,
                        fd.status status,
                        fmi.address address,
                        fd.business business,
                        su.name suname,
                        su.id suid,
                        pu.name puname,
                        pu.id puid
                      from fd_manage_info fmi
                      join fdinfo fd
                      on fd.id = fmi.fid
                      join user su
                      on fmi.manage_uid = su.id
                      join user pu
                      on fmi.patrol_uid = pu.id
                      where 2 > 1
              """
        total_sql = """select count(*) from fd_manage_info where 2 > 1"""
        if self.user.role != 100:
            sql += """ and fmi.uid = %""" % self.user.id
            total_sql += """ and fmi.uid = %""" % self.user.id
        total_num = self.db.execute(total_sql)
        sql += """ limit %s, %s""" % (start_num, num)
        datas =  self.db.execute(sql)
        result = []
        for one in datas:
            tmp = {}
            tmp['fid'] = one['fid']
            tmp['name'] = one['name']
            tmp['alias'] = one['alias']
            tmp['status'] ='在线' if one['status'] else '未运营'
            tmp['address'] = one['address']
            tmp['business'] = one['business']
            tmp['suname'] = one['suname']
            tmp['suid'] = one['suid']
            tmp['puname'] = one['puname']
            tmp['puid'] = one['puid']
            result.append(tmp)
        return self.write(200, 'success', {'total' : total_num[0][0], 'data' : result, 'page' : page})

class FdinfoDetailHandler(BaseHandler):
    def get(self):
        return self.post()

    @admin_required
    def post(self):
        fid = self.args.get('fid', 0)
        sql = """select fd.id fid,
                        fd.name name,
                        fd.alias alias,
                        fd.status status,
                        fmi.address address,
                        fd.business business,
                        su.name suname,
                        su.id suid,
                        pu.name puname,
                        pu.id puid
                      from fd_manage_info fmi
                      join fdinfo fd
                      on fd.id = fmi.fid
                      join user su
                      on fmi.manage_uid = su.id
                      join user pu
                      on fmi.patrol_uid = pu.id
                      where fid = %s
              """ % fid
        total_sql = """select count(*) from fd_manage_info where 2 > 1"""
        if self.user.role != 100:
            sql += """ and fmi.uid = %""" % self.user.id
            total_sql += """ and fmi.uid = %""" % self.user.id
        total_num = self.db.execute(total_sql)
        sql += """ limit %s, %s""" % (start_num, num)
        datas =  self.db.execute(sql)
        result = []
        for one in datas:
            tmp = {}
            tmp['fid'] = one['fid']
            tmp['name'] = one['name']
            tmp['alias'] = one['alias']
            tmp['status'] ='在线' if one['status'] else '未运营'
            tmp['address'] = one['address']
            tmp['business'] = one['business']
            tmp['suname'] = one['suname']
            tmp['suid'] = one['suid']
            tmp['puname'] = one['puname']
            tmp['puid'] = one['puid']
            result.append(tmp)
        return self.write(200, 'success', {'total' : total_num[0][0], 'data' : result, 'page' : page})
