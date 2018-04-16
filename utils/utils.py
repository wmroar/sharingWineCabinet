# -*- coding:utf-8 -*-
from datetime import date, datetime
from Crypto import Random
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from hashlib import md5
import os
import json
import time
import logging
import base64
import string
import random

try:
    from lxml import etree
except ImportError:
    from xml.etree import cElementTree as etree
except ImportError:
    from xml.etree import ElementTree as etree



def wechat_sign(raw, mch_key):
    raw = [(k, str(raw[k]) if isinstance(raw[k], int) else raw[k])
           for k in sorted(raw.keys())]
    s = "&".join("=".join(kv) for kv in raw if kv[1])
    s += "&key={0}".format(mch_key)
    return md5(s.encode("utf-8")).hexdigest().upper()

def wechat_check(data, mch_key):
    sign = data.pop("sign")
    return sign == wechat_sign(data, mch_key)

def dict2xml(raw):
    s = ""
    for k, v in raw.items():
        s += "<{0}>{1}</{0}>".format(k, v)
    s = "<xml>{0}</xml>".format(s)
    return s.encode("utf-8")


def xml2dict(content):
    raw = {}
    root = etree.fromstring(content)
    for child in root:
        raw[child.tag] = child.text
    return raw

def now(day = 0):
    theday = datetime.today()
    return  theday.strftime("%Y-%m-%d %H:%M:%S")

def today(day = 0):
    theday = datetime.today()
    return  theday.strftime("%Y-%m-%d")

def day_start_time(day = 0):
    import datetime
    theday = datetime.datetime.today() - datetime.timedelta(days=day)
    start_time= datetime.datetime.combine(theday, datetime.time.min)
    return int(time.mktime(start_time.timetuple()))

def obj2dict(obj) :
    result = []
    for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata' and x != 'passwd' and x != 'create_time' and x != 'update_time']:
        data = obj.__getattribute__(field)
        if isinstance(data, datetime):
            data = data.strftime('%Y-%m-%d %H:%M:%S')
            continue
        if isinstance(data, date) :
            data = data.strftime('%Y.%m.%d')
        result.append((field, data))
    return dict(result)

def datetime2seconds(datetimes) :
    pass

def ordered_data(data):
    complex_keys = []
    for key, value in data.items():
        if isinstance(value, dict):
            complex_keys.append(key)

    # 将字典类型的数据单独排序
    for key in complex_keys:
        data[key] = json.dumps(data[key], sort_keys=True).replace(" ", "")

    return sorted([(k, v) for k, v in data.items()])

def sign_string(key, unsigned_string):
    # 开始计算签名
    key = RSA.importKey(key)
    signer = PKCS1_v1_5.new(key)
    signature = signer.sign(SHA.new(unsigned_string.encode("utf8")))
    # base64 编码，转换为unicode表示并移除回车
    print signature
    sign = base64.b64encode(signature).decode("utf8").replace("\n", "")
    return sign

def validate_sign(key, message, signature):
    # 开始计算签名
    key = RSA.importKey(key)
    signer = PKCS1_v1_5.new(key)
    digest = SHA.new()
    digest.update(message.encode("utf8"))
    if signer.verify(digest, base64.decodestring(signature.encode("utf8"))):
        return True
    return False

def generate():
    """
    生成随机 RSA 秘钥
    :return:
    """
    random_generator = Random.new().read
    rsa = RSA.generate(1024, random_generator)
    private_pem = rsa.exportKey()
    public_pem = rsa.publickey().exportKey()
    return {
        'private_key': private_pem,
        'public_key': public_pem,
    }
def generate_secret_key():
    return md5(os.urandom(24)).hexdigest()


def log_user_info(user, uri) :
    logging.info('%s:%s %s' %(user.id, user.user_name, uri))


def gen_invite_code():
    return ''.join(random.sample(string.ascii_letters + string.digits, 8))

def gen_invide_code_sql(sss, index = 0):

    sql = """insert into invite_code(title,code,gid,can_repeat,expire_time, channel, section) values('%(title)s', '%(code)s', %(gid)s, %(can_repeat)s, '%(expire_time)s', '%(channel)s', %(section)s);"""
    params = {
        'title' : 'new',
        'code' : gen_invite_code(),
        'gid' : 45,
        'can_repeat' : 0,
        'expire_time' :sss,
        'channel' : 'aiqing',
        'section' : 107 + index,
    }
    print sql % params
if __name__ == '__main__':
    import datetime
#     message = """app_id=2017111509948545&auth_app_id=2017111509948545&charset=utf-8&code=10000&msg=Success&out_trade_no=878&seller_id=2088821768922988&timestamp=2017-11-23 15:14:08&total_amount=0.01&trade_no=2017112321001104010514892464"""
#     key = """-----BEGIN PUBLIC KEY-----
# MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDDI6d306Q8fIfCOaTXyiUeJHkrIvYISRcc73s3vF1ZT7XN8RNPwJxo8pWaJMmvyTn9N4HQ632qJBVHf8sxHi/fEsraprwCtzvzQETrNRwVxLO5jVmRGi60j8Ue1efIlzPXV9je9mkjzOmdssymZkh2QhUrCmZYI/FCEa3/cNMW0QIDAQAB
# -----END PUBLIC KEY-----"""
#     signature = """tGz3NdhdhBx86w+F54OORo/6d9e3PIgHe9o9H9cs4WsbKLXHOh2KSlLoCb/F2bJK/5taHVz00cGL3oMCVBe36+aYr49CI2RmHdZ7xnRQ13KcF2i4tyiMwjqcuEYOZsQXmKkiJiikU9SF9dqtsSIf7TOEZHMZ1KJ3mhLfxvwdqDE="""
#     print validate_sign(key, message,signature)
    sss = '2019-03-28 23:59:59.593000'
    for i in range(1005):
        gen_invide_code_sql(sss)
