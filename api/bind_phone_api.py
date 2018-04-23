# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi
import settings


class BindPhoneApi(LoginBaseApi):
    """
    绑定手机号
    """
    url = '/user/phonebind'

    def build_custom_param(self, data):
        return {'phone': data['phone'], 'code': data['code'],'check_code':data['check_code']}