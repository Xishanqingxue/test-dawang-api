# -*- coding:utf-8 -*-
from base.base_api import BaseApi
from base.login_base_api import LoginBaseApi


class SendSmsCodeApi(BaseApi):
    """
    发送短信验证码接口
    """
    url = '/user/sendSms'

    def build_custom_param(self, data):
        return {'type': data['type'], 'phone': data['phone'],
                'check_code': data['check_code']}

class LoginSendSmsCodeApi(LoginBaseApi):
    url = '/user/sendSms'

    def build_custom_param(self, data):
        return {'type': data['type'], 'phone': data['phone'],
                'check_code': data['check_code']}