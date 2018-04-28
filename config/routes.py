# coding=utf-8
from handlers import base,user,admin_index, admin_order, fdinfo, goods, order, other
from conf import settings
from tornado import web

urls = [
    # 用户登陆注册接口
    # (r'/user/register/', user.Register),
    (r'/sys/user/login', user.SysUserLoginHandler),

    # 首页概览
    (r'/sys/data/overview', admin_index.OverviewHandler),

    # 管理订单信息
    (r'/sys/orders', admin_order.OrderListHandler),

    #用户订单信息
    (r'/user/orders', order.UserOrderListHandler),
    (r'/user/products/detail', order.GoodsDetailHandler),
    (r'/user/products/buy', order.NewOrderHandler),

    # 商品信息
    (r'/user/products', goods.FdGoodsListHandler),
    (r'/products/add', goods.FGoodsAddHandler),
    (r'/products/update', goods.FGoodsUpdateHandler),

    # 设备
    (r'/fds', fdinfo.FdinfoListHandler),
    (r'/fds/detail', fdinfo.FdinfoDetailHandler),

    # 其他基础信息
    (r'/faq', other.FAQHandler),
    (r'/img/upload', base.UploadHandler),

    # 短信接口, 发送验证码, 校验等
    (r'/user/tel/login', user.TelLoginHandler),
    (r'/user/tel/verify', user.TelCodeValideHandler),
    (r'/user/tel/bind', user.TelBindHandler),
    (r'/user/tel/send/code', user.TelCodeSendHandler),

    (r"/(.*\..*)", web.StaticFileHandler, dict(path=settings['static_path']))
]
