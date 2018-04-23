# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi
from base.base_api import BaseApi


class BuyGuardApi(LoginBaseApi):
    """
    购买守护
    """
    url = '/live/purchaseGuard'


    def build_custom_param(self, data):
        return {'room_id':data['room_id'],'guard_id':data['guard_id'],'currency':data['currency']}


class GuardProductListApi(BaseApi):
    """
    守护商品列表
    """
    url = '/live/guardproductlist'


class MyGuardApi(LoginBaseApi):
    """
    我的守护列表
    """
    url = '/my/guard'