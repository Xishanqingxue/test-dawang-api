# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi


class MyMilitaryApi(LoginBaseApi):
    """
    获取我的军衔接口
    """
    url = '/my/military'