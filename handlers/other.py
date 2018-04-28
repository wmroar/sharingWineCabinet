# coding:utf-8
from base import BaseHandler
import logging
from libs.model import Goods, FdGridInfo, Order, FdManagerInfo, FAQ
from utils.utils import obj2dict
from auth.auth import login_required
from config.conf import wechatconf, alipayconf, settings
import copy
import uuid
import requests
import time
from utils import utils
import urllib
from utils.return_info import res_content


class FAQHandler(BaseHandler):
    def post(self):
        datas = self.db.query(FAQ).all()
        result = []
        for one in datas:
            tmp = {'question' : one.question, 'answer' : one.answer}
            result.append(tmp)
        return self.write_json(200, 'success', result)
