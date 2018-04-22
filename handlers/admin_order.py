# coding:utf-8
from base import BaseHandler
import logging
from lib.model import Goods, FdGridInfo, Order, FdManagerInfo
from utils.utils import obj2dict
from auth.auth import admin_required

class OrderListHandler(BaseHandler):
    @admin_required
    def post(self):
        num = self.args.get('num', 15)
        page = self.args.get('page', 1)
        stime = self.args.get('stime', None)
        etime = self.args.get('etime', None)
        status = self.args.get('status', 1)
        order_id = self.args.get('order_id', 0)
        try:
            num  = int(num)
            page = int(page)
        except Exception, e:
            logging.info(e)
            return self.write_json(600, '参数错误')
        start_num = (page - 1) * num
        sql = """select o.id order_id,
                        g.name,
                        g.price,
                        o.create_time,
                        o.fid,
                        o.address,
                        o.status
                 from `order` o
                    join fd_manage_info fmi
                    on o.fid = fmi.fid
                    join goods g
                    on o.pid = g.id where o.status > 0 """
        total_sql =  """select count(*)
                        from `order` o
                        join fd_manage_info fmi
                        on o.fid = fmi.fid
                        join goods g
                        on o.pid = g.id where o.status > 0 """
        if self.user.role != 100:
            sql += """ and fmi.uid = %""" % self.user.id
            total_sql += """ and fmi.uid = %""" % self.user.id

        if stime:
            sql += ' and o.create_time >= %s' % stime
            total_sql += ' and o.create_time >= %s' % stime
        if etime :
            sql += ' and o.create_time <= %s' % etime
            total_sql += ' and o.create_time <= %s' % etime

        if status:
            ostatus = 1 if status in ['1', '已支付'，1] else 2
            sql += ' and o.status < %s' % ostatus
            total_sql += ' and o.status < %s' % ostatus
        if order_id:
            sql += ' and o.id = %s' % order_id
            total_sql += ' and o.id = %s' % order_id

        total_num = self.db.execute(total_sql)
        sql += """ limit %s, %s""" % (start_num, num)
        datas =  self.db.execute(sql)
        result = []
        for one in datas:
            tmp = {}
            tmp['order_id'] = one['order_id']
            tmp['name'] = one['name']
            tmp['price'] = one['price']
            tmp['create_time'] = one['create_time']
            tmp['fid'] = one['fid']
            tmp['address'] = one['address']
            tmp['status'] = '已支付' if one['status'] == 1 else '已退款'
            result.append(tmp)
        return self.write(200, 'success', {'total' : total_num[0][0], 'data' : result, 'page' : page})
