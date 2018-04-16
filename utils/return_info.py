# -*- coding:utf-8 -*-
import json
code_map = {
    200 : u'成功',
    401 : u'登录失败',
    804 : u'参数错误',
    405 : u'用户权限不够',
}

def res_content(code, message = None, data = None) :
    result =  { 'code' : code, 'data' : data,  'info' : code_map.get(code,message) if not message else message}
    return json.dumps(result)
