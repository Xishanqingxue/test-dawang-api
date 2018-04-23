# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi

class BuySunApi(LoginBaseApi):
    """
    购买太阳
    """
    url = '/live/buysun'

    def build_custom_param(self, data):
        return {'room_id':data['room_id']}