# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi


class UserGetSunApi(LoginBaseApi):
    """
    获取太阳
    """
    url = '/live/usergetsun'

    def build_custom_param(self, data):
        return {'room_id': data['room_id']}
