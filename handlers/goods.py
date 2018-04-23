# coding:utf-8
from base import BaseHandler
import logging
from libs.model import Goods, FdGridInfo
from utils.utils import obj2dict
from auth.auth import admin_required, login_required

class GoodsListHandler(BaseHandler):
    def get(self):
        return self.post()
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
        datas = self.db.query(Goods).limit(num).offset(start_num)
        if not datas:
            return self.write_json(601, '未查询到数据')
        total_num = self.db.query(Goods.id).count()
        result = {'total_page' : total_num, 'datas' : [obj2dict(x) for x in datas]}
        return self.write(200, 'success', result)

class FdGoodsListHandler(BaseHandler):
    def get(self):
        return self.post()
    def post(self):
        num = self.args.get('num', 15)
        page = self.args.get('page', 1)
        fd = self.args.get('fid', 0)
        final = []
        try:
            num  = int(num)
            page = int(page)
        except Exception, e:
            logging.info(e)
            return self.write_json(600, '参数错误')
        start_num = (page - 1) * num
        datas = self.db.query(FdGridInfo, Goods).join(Goods, FdGridInfo.gid == Goods.id, FdGridInfo.fid == fid).limit(num).offset(start_num)
        if not datas:
            return self.write_json(601, '未查询到数据')
        total_num = self.db.query(FdGridInfo.id).filter(FdGridInfo.id == fid).count()
        for one in datas:
            tmp = obj2dict(one[1])
            tmp['grid_no'] = one[0].grid_no
            tmp['fid'] = one[0].fid
            final.append(tmp)
        result = {'total_page' : total_num, 'datas' : final}
        return self.write(200, 'success', result)

class FGoodsAddHandler(BaseHandler):
    @admin_required
    def post(self):
        attrs = ['name', 'title', 'discount_info', 'des', 'price', 'ori_price', 'is_best', 'is_hot', 'is_new', 'weight', 'volume', 'quantity', 'quantity_notify', 'pic', 'sellers', 'pay_times']
        good = Goods()
        for attr in attrs:
            if self.args.get(attr, ''):
                setattr(good, attr, self.args.get(attr, ''))
        self.db.add(good)
        self.db.commit()
        return self.write_json(200, 'success')

class FGoodsUpdateHandler(BaseHandler):
    @admin_required
    def post(self):
        pid = self.args.get('pid', 0)
        attrs = ['name', 'title', 'discount_info', 'des', 'price', 'ori_price', 'is_best', 'is_hot', 'is_new', 'weight', 'volume', 'quantity', 'quantity_notify', 'pic', 'sellers', 'pay_times']
        good = self.db.query(Goods).filter(Goods.id == pid).first()
        if not good:
            return self.write_json('602', 'args error')
        for attr in attrs:
            if self.args.get(attr, ''):
                setattr(good, attr, self.args.get(attr, ''))
        self.db.add(good)
        self.db.commit()
        return self.write_json(200, 'success')
