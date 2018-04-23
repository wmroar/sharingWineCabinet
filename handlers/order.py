# coding:utf-8
from base import BaseHandler
import logging
from libs.model import Goods, FdGridInfo, Order, FdManagerInfo
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
        if channel == 'wechat':
            result = self.weichat_order(order, gift.product_id)
            if ('return_code' in result) and ('result_code' in result):
                data = dict(utils.xml2dict(result))
                if data['return_code'] == 'FAIL':
                    return self.write(res_content(838, u'请求微信支付失败'))
                if data['result_code'] == 'FAIL':
                    return self.write(res_content(839, u'请求微信支付失败'))
                safeCode = data['prepay_id']
                params = {'appid' : wechatconf['appid'],
                        'partnerid' : wechatconf['mch_id'],
                        'prepayid' : safeCode,
                        'package' : 'Sign=WXPay',
                        'noncestr' : uuid.uuid4().hex,
                        'timestamp' : str(int(time.time()))}
                sign= utils.wechat_sign(params, settings['wechat_public_key'])
                params['sign'] = sign
                params['order_id'] = str(order.id)
                return self.write(res_content(200, u'success', params))
        elif channel == 'alipay':
            params = self.alipay_order(order, gift.product_id)
        return self.write_json(200, 'success', {'order_id' : order.id, 'amount' : goods.price})

    def weichat_order(self, order, gname):
        url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
        params = copy.copy(wechatconf)
        params_new = {
            'nonce_str': uuid.uuid4().hex,
            'version' : '1.0',
            'sign_type' : 'MD5',
            'notify_url' : 'http://www.dmgame.com/payment/wechat/notify/',
            'body' : gname,
            'out_trade_no' : str(order.id),
            'total_fee' : str(int(order.amount * 100)),
            'spbill_create_ip' : '47.104.129.1',
            'trade_type' : 'APP',
        }
        params.update(params_new)
        sign= utils.wechat_sign(params, settings['wechat_public_key'])
        params['sign'] = sign
        logging.info(utils.dict2xml(params))
        r = requests.post(url, data = utils.dict2xml(params))
        result = r.content
        logging.info(result)
        return result

    def alipay_order(self, order, gname):
        params = copy.copy(alipayconf)
        params_new = {
            'timestamp': utils.now(),
            'version' : '1.0',
            'sign_type' : 'RSA',
            'notify_url' : 'http://www.dmgame.com/payment/alipay/notify/',
            'biz_content' : {
               'subject' : gname,
               'out_trade_no' : str(order.id),
               'timeout_express' : '90m',
               'total_amount' : str(order.amount),
               'product_code' : 'QUICK_MSECURITY_PAY',
            }
        }
        params.update(params_new)
        unsigned_items = utils.ordered_data(params)
        unsigned_string = "&".join("{}={}".format(k, v) for k, v in unsigned_items)
        signed_string = utils.sign_string(settings['ali_private_key'], unsigned_string)
        params['sign'] = signed_string.encode('unicode_escape').decode('string_escape')
        unsigned_items = utils.ordered_data(params)
        unsigned_string = "&".join("{}={}".format(k, urllib.quote(v) if isinstance(v, str) else urllib.quote(json.dumps(v))) for k, v in unsigned_items)
        return unsigned_string
