# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi


class AddBlackUserApi(LoginBaseApi):
    """
    添加黑名单
    """
    url = '/live/addblackuser'

    def build_custom_param(self, data):
        return {'user_id': data['user_id'], 'anchor_id': data['anchor_id'], 'blacker_type': data['blacker_type']}
