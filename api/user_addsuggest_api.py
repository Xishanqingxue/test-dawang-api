# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi

class UserAddSuggestApi(LoginBaseApi):
    """
    意见反馈
    """
    url = '/user/addsuggest'

    def build_custom_param(self, data):
        return {'content': data['content']}