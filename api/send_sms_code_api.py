# -*- coding:utf-8 -*-
from base.base_api import BaseApi
import settings


class SendSmsCodeApi(BaseApi):
    """
    发送短信验证码接口
    """
    url = '/user/sendSms'

    def build_custom_param(self, data):
        return {'type': data['type'], 'phone': data['phone'],
                'check_code': data['check_code']}