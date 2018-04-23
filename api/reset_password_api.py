# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi


class ResetPasswordApi(LoginBaseApi):
    """
    修改密码
    """
    url = '/user/resetpassword'

    def build_custom_param(self, data):
        return {'phone': data['phone'],'code': data['code'],'new_password':data['new_password'],
                 'confirm_password':data['confirm_password']}