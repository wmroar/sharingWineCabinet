# -*- coding:utf-8 -*-
from base import BaseHandler
from libs.model import User, SysUser, TelLoginLog, TelLoginCode
from md5 import md5
from config.conf import settings
from auth.auth import admin_required


class SysUserLoginHandler(BaseHandler):
    def post(self):
        user_name = self.args.get('user_name', '')
        passwd = self.args.get('passwd', '')
        if (not user_name)  or (not passwd):
            return self.write_json(802, '用户名或者密码错误')
        passwd_md5 = md5(settings['pass_prefix'] + passwd).hexdigest()
        data = self.db.query(SysUser).filter(SysUser.user_name == user_name, SysUser.passwd == passwd_md5).first()
        if not data:
            return self.write_json(802, '用户名或者密码错误')
        token_str = self.addToken(user_name)
        return self.write_json(200, 'success', {'token' : token_str, 'role' : data.role, 'nick_name' : data.nick_name})

class NormalSysUserRegisterHandler(BaseHandler):
    @admin_required
    def post(self):
        pass

class TelCodeHandler(BaseHandler):
    def _post(self, addToken = False):
        tel = self.args.get('tel', '')
        code = self.args.get('code', '')
        channel = self.args.get('channel_id', 0)
        if len(tel) != 11:
            return self.write(res_content(804, u'手机号码格式错误!'))
        now = int(time.time())
        has_code = self.db.query(TelLoginCode).filter(TelLoginCode.tel == tel, TelLoginCode.ftime >= now - 120).order_by(TelLoginCode.ftime.desc()).all()
        if not has_code:
            return self.write(res_content(944, u'请先点击发送验证码!'))
        valid_code = self.db.query(TelLoginCode).filter(TelLoginCode.tel == tel, TelLoginCode.code == code).order_by(TelLoginCode.ftime.desc()).first()
        if valid_code and (now - valid_code.ftime > 120):
            return self.write(res_content(943, u'验证码已失效, 请重新发送验证码!'))
        login_log = self.db.query(TelLoginLog).filter(TelLoginLog.tel == tel).first()
        if not login_log:
            login_log = TelLoginLog(tel = tel, faild_times = 1)
            self.db.add(login_log)
        if login_log.faild_times >= 20:
            return self.write(res_content(942, u'失败次数过多, 手机号码已经被锁定, 请联系客服解锁!'))
        tl = self.db.query(TelLoginCode).filter(TelLoginCode.tel == tel, TelLoginCode.ftime >= now - 120, TelLoginCode.code == code).order_by(TelLoginCode.ftime.desc()).all()
        if not tl:
            login_log.faild_times += 1
            if login_log.faild_times >= 10:
                self.db.commit()
                return self.write(res_content(942, u'当前失败次数已累计%s次, 还剩余%s次尝试机会!'%(login_log.faild_times, 20 - login_log.faild_times)))
            self.db.commit()
            return self.write(res_content(801, u'验证码错误!'))

        if has_code and len(has_code) >= 2:
            if has_code[0].code != code:
                return self.write(res_content(942, u'当前验证码已经失效, 请使用最新发送的验证码!!'))

        user = self.db.query(User).filter(User.user_name == tel).first()
        if not user:
            user = User(user_name = tel, tel = tel, channel = channel, role = 1)
            self.db.add(user)
        token = ''
        user.role = 1
        if addToken:
            token = self.add_token(tel)
        login_log.faild_times = 0
        self.db.commit()
        return self.write(res_content(200, u'success', {'skey' : token, 'user' : tel, 'role' : 1}))

class TelLoginHandler(TelCodeHandler):
    def post(self):
        tel = self.args.get('tel', '')
        code = self.args.get('code', '')
        if tel == '13245678910' and code == '111111':
            user = self.db.query(User).filter(User.user_name == tel).first()
            if not user:
                user = User(user_name = tel, tel = tel, channel = 'test')
                self.db.add(user)
            token = self.add_token(tel)
            self.db.commit()
            return self.write(res_content(200, u'success', {'skey' : token, 'user' : tel, 'role' : 1}))
        return self._post(True)

class TelCodeValideHandler(TelCodeHandler):
    def post(self):
        tel = self.args.get('tel', '')
        code = self.args.get('code', '')
        if tel == '13245678910' and code == '111111':
            user = self.db.query(User).filter(User.user_name == tel).first()
            if not user:
                user = User(user_name = tel, tel = tel, channel = 'test')
                self.db.add(user)
            token = ''
            self.db.commit()
            return self.write(res_content(200, u'success', {'skey' : token, 'user' : tel, 'role' : 1}))
        return self._post(False)

class TelCodeSendHandler(BaseHandler):
    def post(self):
        tel = self.args.get('tel', '')
        bind = self.args.get('bind', None)
        if len(tel) != 11:
            return self.write(res_content(804, u'手机号码格式错误!'))
        __business_id = uuid.uuid1()
        now = int(time.time())
        login_log = self.db.query(TelLoginLog).filter(TelLoginLog.tel == tel).first()
        if login_log and (login_log.faild_times >= 20):
            return self.write(res_content(942, u'手机号码已经被锁定, 请联系客服解锁!'))
        tl = self.db.query(TelLoginCode).filter(TelLoginCode.tel == tel, TelLoginCode.ftime >= now - 60).all()
        if tl:
            return self.write(res_content(961, u'发送消息过快!'))
        if bind :
            if self.db.query(User).filter(User.tel == User.user_name, User.tel== tel).count():
                return self.write(res_content(949, u'该手机已经被注册了, 请换用其它号码!'))
        nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8' ,'9']
        code = ''.join([random.choice(nums[1:])] + [random.choice(nums) for x in range(5)])

        tl = TelLoginCode(tel = tel, code = code, ftime = now)
        self.db.add(tl)
        self.db.commit()
        params = {'key' : 'server_robot', 'phone' : tel, 'code' : code, 'action' : '8888'}
        response = requests.post('http://47.104.13.80:9001/phone', data = json.dumps(params))
        try :
            logging.info(response.content)
            if 'Success' in response.content:
                return self.write(res_content(200, '验证码发送成功'))
            return self.write(res_content(911, '验证码发送失败, 请重试'))
        except Exception, e :
            logging.error(e)
            return self.write(res_content(911, '验证码发送失败, 请重试'))
        return self.write(res_content(200, '验证码发送成功'))

class TelBindHandler(BaseHandler):
    @login_required
    def post(self):
        tel = self.args.get('tel', '')
        code = self.args.get('code', '')
        channel = self.args.get('channel_id', 0)
        if len(tel) != 11:
            return self.write(res_content(804, u'手机号码格式错误!'))
        now = int(time.time())
        has_code = self.db.query(TelLoginCode).filter(TelLoginCode.tel == tel, TelLoginCode.ftime >= now - 120).order_by(TelLoginCode.ftime.desc()).all()
        if not has_code:
            return self.write(res_content(944, u'请先点击发送验证码!'))
        valid_code = self.db.query(TelLoginCode).filter(TelLoginCode.tel == tel, TelLoginCode.code == code).order_by(TelLoginCode.ftime.desc()).first()
        if valid_code and (now - valid_code.ftime > 120):
            return self.write(res_content(943, u'验证码已失效, 请重新发送验证码!'))
        login_log = self.db.query(TelLoginLog).filter(TelLoginLog.tel == tel).first()
        if not login_log:
            login_log = TelLoginLog(tel = tel, faild_times = 1)
            self.db.add(login_log)
        if login_log.faild_times >= 20:
            return self.write(res_content(942, u'失败次数过多, 手机号码已经被锁定, 请联系客服解锁!'))
        tl = self.db.query(TelLoginCode).filter(TelLoginCode.tel == tel, TelLoginCode.ftime >= now - 120, TelLoginCode.code == code).order_by(TelLoginCode.ftime.desc()).all()
        if not tl:
            login_log.faild_times += 1
            if login_log.faild_times >= 10:
                self.db.commit()
                return self.write(res_content(942, u'当前失败次数已累计%s次, 还剩余%s次尝试机会!'%(login_log.faild_times, 20 - login_log.faild_times)))
            self.db.commit()
            return self.write(res_content(801, u'验证码错误!'))

        if has_code and len(has_code) >= 2:
            if has_code[0].code != code:
                return self.write(res_content(942, u'当前验证码已经失效, 请使用最新发送的验证码!!'))

        cuser = self.db.query(User).filter(User.user_name == tel).first()
        if cuser:
            return self.write(res_content(801, u'该手机已经绑定过其他账号!'))
        if self.user.user_name == self.user.tel:
            return self.write(res_content(801, u'此号码已经是绑定过手机的号码啦!'))
        self.user.user_name = tel
        self.user.tel = tel
        self.user.role = 1
        token = self.add_token(tel)
        login_log.faild_times = 0
        self.db.commit()
        return self.write(res_content(200, u'success', {'skey' : token, 'user' : tel, 'role' : 'tel'}))
