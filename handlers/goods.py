# coding:utf-8
from base import BaseHandler
import logging
from lib.model import Goods, FdGridInfo
from utils.utils import obj2dict

class GoodsListHandler(BaseHandler)
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
        result = {'total_page' : total_num, 'datas' : final]}
        return self.write(200, 'success', result)
