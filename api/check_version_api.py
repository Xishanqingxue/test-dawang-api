# -*- coding:utf-8 -*-
from base.base_api import BaseApi

class CheckVersionApi(BaseApi):
    """
    检查版本更新
    """
    url = '/version/checkversion'

    def build_custom_param(self, data):
        return {'platform':data['platform'],'pname':data['pname'],'channel_id':data['channel_id']}