# -*- coding:utf-8 -*-
from base.base_api import BaseApi

class ChannelBanner(BaseApi):
    """
    获取banner列表数据
    """
    url = "/channel/banner"

    def build_custom_param(self, data):
        return {'type':data['type']}