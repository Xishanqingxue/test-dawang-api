# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi


class ExchangeApi(LoginBaseApi):
    """
    金币兑换银币
    """
    url = '/my/exchange'

    def build_custom_param(self, data):
        return {'gold':data['gold'],'diamond':data['diamond'],'product_id':data['product_id']}