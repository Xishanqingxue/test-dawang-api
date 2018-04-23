# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi


class UpdateNickApi(LoginBaseApi):
    """
    修改昵称
    """
    url = '/user/updatenick'

    def build_custom_param(self, data):
        return {'nickname': data['nickname']}