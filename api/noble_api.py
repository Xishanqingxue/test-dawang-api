# -*- coding:utf-8 -*-
from base.base_api import  BaseApi
from base.login_base_api import LoginBaseApi



class BuyNobleApi(LoginBaseApi):
    """
    购买贵族
    """
    url = '/live/purchaseNoble'

    def build_custom_param(self, data):
        return {'noble_id': data['noble_id'], 'num': data['num'],'room_id':data['room_id'],'currency':data['currency']}


class NobleListApi(BaseApi):
    """
    贵族商品列表
    """
    url = '/live/noblelist'