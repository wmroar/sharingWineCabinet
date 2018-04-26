import requests
import json
import time
import md5



host = 'http://120.79.79.20'
# host = 'http://localhost:8081'

skey = 'ZW1tLDEzNTcxODI2Nzk5LHlvdWNhbmd1ZXNzdGhpcywxNTI0NTMyOTk2'
USER_NAME = 'wangshisan55'
PWD = '123'

# host = 'http://127.0.0.1:8081'

def test_register():
    data = {'username': 'wangnmanni', 'passwd' : '123'}
    r = requests.post(host + '/user/register', data = json.dumps(data))
    print r.content

def test_login() :
    data = {'username': USER_NAME, 'passwd' : PWD}
    r = requests.post(host + '/user/login/', data = json.dumps(data))
    print r.content

def test_logout() :
    data = {'username': 'wangshisan', 'passwd' : '123','Authorization' : skey}
    r = requests.post(host + '/user/logout/', data = json.dumps(data), headers = {'Authorization' : skey})
    print r.content

def test_guest() :
    data = {'username' : 'wangshisan1211-111', 'channel' : 'xdns_ios2'}
    # data = {}
    r = requests.post(host + '/user/guest/', data = json.dumps(data))
    print r.content

def test_tel_send_code():
    data = {'tel' : '13571826799'}
    r = requests.post(host + '/user/tel/send/code',  data=json.dumps(data))
    # s = json.loads(r.content)
    print r.content

def test_tel_login():
    data = {'tel' : '13571826799', 'code' : '483939'}
    r = requests.post(host + '/user/tel/login',  data=json.dumps(data))
    # s = json.loads(r.content)
    print r.content

def test_tel_verify():
    data = {'tel' : '13571826799', 'code' : '389457'}
    r = requests.post(host + '/user/tel/verify',  data=json.dumps(data))
    # s = json.loads(r.content)
    print r.content

def test_goods_list():
    data = {'fid' : 1}
    r = requests.post(host + '/user/products',  data=json.dumps(data))
    # s = json.loads(r.content)
    print r.content

def test_order_list():
    data = {'Authorization' : skey, 'num' : 2}
    r = requests.post(host + '/user/orders',  data=json.dumps(data))
    # s = json.loads(r.content)
    print r.content

def test_order_detail():
    data = {'Authorization' : skey, 'order_id' : 1}
    r = requests.post(host + '/user/products/detail',  data=json.dumps(data))
    # s = json.loads(r.content)
    print r.content

def test_order_new():
    data = {'Authorization' : skey, 'fid' : 1, 'grid_no' : 1, 'channel' : 'wechat'}
    r = requests.post(host + '/user/products/buy',  data=json.dumps(data))
    # s = json.loads(r.content)
    print r.content

if __name__=='__main__':
    test_order_detail()
    # test_order_new()
    # test_order_list()
    # test_goods_list()
    # test_u8_login()
    # test_u8_notify()
    # test_login()
    # test_tel_send_code()
    # test_tel_login()
    # test_register()
    # test_guest()
    # test_logout()
