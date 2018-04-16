import os
settings = {
    "cookie_secret": "hahahyouguessthisaaaa123987/Vo=",
    "xsrf_cookies": False,
    'template_path'  :  os.path.join(os.path.dirname(__file__), "../static/uploads/"),
    'static_path'  :  os.path.join(os.path.dirname(__file__), "../static/uploads/"),
    'static_url_prefix' : "/static/",
    'debug' : True,
    'port' : 8888,
    # 'debug' : False,
    'ali_private_key': """MIICXAIBAAKBgQCT/R/f1yH/hutoRUpMzFuJEqtkkY7ab0lH6Vve40LusUGCKf1I
uTy16JxkHdUuO1k1WRppO1lW04EPYAgDSmBNKNRSQ0uUX8bmHkOYCRFkY/JgscMw
0vCNWcij/ti4eJVQjMAzLV/d0/WTioTNAa+MhAE3/lyc+usz/CiUtiDDuQIDAQAB
AoGBAI4XMxyMBkO/epXSOcXFTXouJ8xXCe9nfNgEEsbONDzUis58nInP+Z+7qTVj
g4VxTHUxiW9SobQBPeDSVr86EX1uYU51d1CWg7xqvVf1FBhdA6TWjbeueriEw4Zl
uXhiSWVj5UWqXS6u6gDbhjo54JsxkzDSG/pmp3jeW6zZTuoRAkEAvBNvNhxsxTq2
vYyLxPXQazfb0S+Ku3M8x7m8epysm0glEt1LGyc/xJou3+jI02qQpvYUcYAPQi3I
sNplurM57QJBAMlvbm31Z4rXrnNHojs20VqsectXg4bAtfWpwK/1HlkPpEJ+Ry2a
B4oRQcMVjgcYnUH0/kmByoEKdYTBl90oB30CQAMZbuO9ZC174jcNceA1DNI3gW/Z
ELg2FfJUpT6ABngooDPHYc14wBxFTjBybZzOTMPzmjKkoZu9lWkUsEh7W6ECQGG9
qB/CzBMaxJM7VwTUfJE6z35TYIaqS6CAVfcLQUaFyHZbP75o1u+vn/FBLEFVODkg
36JbUB99K7jXFxFAsyECQF8GTFWmp5SYGMkofGKVj2enPFi6yKWvQ/rvXbHKb4fV
k4nlrH0ydLi5nC5If0s+XSB7OUFNhAgZ3wCVmk1yrUM=""",
    'ali_pub_key' : """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDDI6d306Q8fIfCOaTXyiUeJHkrIvYISRcc73s3vF1ZT7XN8RNPwJxo8pWaJMmvyTn9N4HQ632qJBVHf8sxHi/fEsraprwCtzvzQETrNRwVxLO5jVmRGi60j8Ue1efIlzPXV9je9mkjzOmdssymZkh2QhUrCmZYI/FCEa3/cNMW0QIDAQAB
-----END PUBLIC KEY-----""",
    'wechat_private_key' : '7c2126f7d20700fe8ab2628291d7f9de',
    'wechat_public_key' : 'PtoPAsVRq64YhYQJ3y1ltMTwgE3B4kNl',
}

dbconf = {
    'host' : 'localhost:3306',
    'db_user' : 'godman',
    'db_pass' : 'wang_2016__',
    'db_name' : 'lovelygirl'
}

alipayconf = {
    'app_id' : '2017111509948545',
    'method' : 'alipay.trade.app.pay',
    'charset' : 'utf-8',
}

wechatconf = {
    'appid' : 'wx10e509222db6e05b',
    'mch_id': '1493143322',
}
