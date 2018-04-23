# -*- coding:utf-8 -*-
from base.base_api import BaseApi
import settings

class LoginServerApi(BaseApi):
    """
    login_server
    """
    url = '/home/loginserver'

    def build_custom_param(self, data):
        return {'package_name': 'com.dawang.tv', 'channel_id': '1'}
