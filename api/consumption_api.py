# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi

class ConsumptionApi(LoginBaseApi):
    """
    消费记录
    """
    url = '/user/consumption'



class DiamondAccountApi(LoginBaseApi):
    """
    银币获取记录
    """
    url = '/user/diamondaccount'



class GoldAccountApi(LoginBaseApi):
    """
    金币获取记录
    """
    url = '/user/goldaccount'
