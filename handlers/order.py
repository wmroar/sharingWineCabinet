# coding:utf-8
from base import BaseHandler
import logging
from lib.model import Goods, FdGridInfo, Order, FdManagerInfo
from utils.utils import obj2dict
from auth.auth import login_required

class UserOrderListHandler(BaseHandler):
    @login_required
    def post(self):
        user = self.get_current_user()
        num = self.args.get('num', 15)
        page = self.args.get('page', 1)
        try:
            num  = int(num)
            page = int(page)
        except Exception, e:
            logging.info(e)
            return self.write_json(600, '参数错误')
        start_num = (page - 1) * num
        orders = self.db.query(Order,Goods).join(Goods, Order.pid == Goods.id).filter(Order.uid == user.id, Order.status >= 1).limit(num).offset(start_num)
        if not orders:
            return self.write_json(603, 'no data found')
        total_num = self.db.query(Order).filter(Order.uid == user.id, Order.status >= 1).count()
        final = []
        for one in orders:
            tmp = obj2dict(one[0])
            tmp['name'] = one[1].name
            tmp['price'] = one[1].price
            tmp['status'] = '支付取消' if one[0].status == 1 else '支付成功'
            final.append(tmp)
        return self.write_json(200, 'success', {'total_page' : total_num, 'page' : page, 'data':final})
    def get(self):
        return self.post()

class GoodsDetailHandler(BaseHandler):
    @login_required
    def post(self):
        user = self.get_current_user()
        order_id = self.args.get('order_id', -1)
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return self.write_json(602, 'args error')
        goods = self.db.query(Goods).filter(Goods.id == order.id).first()
        if not goods:
            return self.write_json(602, 'args error')
        tmp = obj2dict(goods)
        tmp['status'] = '支付取消' if order.status == 1 else '支付成功'
        tmp['address'] = order.address

        tmp['order_id'] = order.id
        tmp['create_time'] = order.create_time
        return self.write_json(200, 'success', tmp)

    def get(self):
        return self.post()

class NewOrderHandler(BaseHandler):
    @login_required
    def post(self):
        fid = self.args.get('fid', 0)
        grid_no = self.args.get('grid_no', 0)
        finfo = self.db.query(FdGridInfo).filter(FdGridInfo.fid == fid, FdGridInfo.grid_no == grid_no).first()
        if not finfo:
            return self.write_json(602, 'args error')
        if finfo.status != 1:
            return self.write_json(604, '该商品已售罄， 请选择其他商品！')
        goods = self.db.query(Goods).filter(Goods.id == finfo.pid).first()
        fd = self.db.query(FdManagerInfo).filter_by(fid = finfo.id).first()
        if not goods:
            return self.write_json(605, '商品被限制购买！')
        order = Order(uid = self.user.id, pid = goods.id, fid = finfo.fid, grid_no = grid_no, status = 0, address = fd.address, num = 1, amount = goods.price)
        self.db.add(order)
        self.db.commit()
        #todo 其他参数确认， 根据微信和支付宝需要的参数格式生成
        return self.write_json(200, 'success', {'order_id' : order.id, 'amount' : goods.price})
