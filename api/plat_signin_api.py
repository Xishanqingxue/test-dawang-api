# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi


class PlatSigninApi(LoginBaseApi):
    """
    平台签到
    """
    url = '/platsignin/platsignin'

    def build_custom_param(self, data):
        return {'platform': data['platform'],'channel_id': data['channel_id']}