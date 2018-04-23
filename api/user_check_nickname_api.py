# -*- coding:utf-8 -*-
from base.base_api import BaseApi

class UserCheckNickname(BaseApi):
    """
    检查昵称
    """
    url = '/user/checknickname'

    def build_custom_param(self, data):
        return {'nickname': data['nickname']}