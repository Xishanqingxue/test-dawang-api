# -*- coding:utf-8 -*-
from base.base_api import BaseApi
import settings


class RegisterApi(BaseApi):
    """
    注册接口
    """
    url = '/home/register'

    def build_custom_param(self, data):
        return {'login_name': data['login_name'], 'code': data['code'], 'password': settings.PUBLIC_PASSWORD,
                'nickname': data['nickname'], 'channel_id': 1}
