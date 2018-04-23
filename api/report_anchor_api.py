# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi


class ReportUserApi(LoginBaseApi):
    """
    举报用户
    """
    url = '/user/reportuser'

    def build_custom_param(self, data):
        return {'to_user_id': data['to_user_id'],'reason': data['reason']}