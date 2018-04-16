# coding=utf-8
from handlers import base,user
from conf import settings

urls = [
    # 用户登陆注册接口
    (r'/user/register/', user.Register),
    (r'/user/login/', user.Login),
    (r'/user/logout/', user.Logout),

    # 短信接口, 发送验证码, 校验等
    (r'/user/tel/login', user.TelLoginHandler),
    (r'/user/tel/verify', user.TelCodeValideHandler),
    (r'/user/tel/bind', user.TelBindHandler),
    (r'/user/tel/send/code', user.TelCodeSendHandler),

    (r"/(.*\..*)", base.MyStaticFileHandle, dict(path=settings['static_path']))
]
