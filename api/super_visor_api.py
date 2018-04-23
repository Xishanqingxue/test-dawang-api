# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi


class AddSuperVisorApi(LoginBaseApi):
    """
    添加房管
    """
    url = '/live/addsupervisor'

    def build_custom_param(self, data):
        return {'user_id': data['user_id'], 'anchor_id': data['anchor_id'], 'type': data['type']}


class DelSuperVisorApi(LoginBaseApi):
    """
    删除房管
    """
    url = '/live/delsupervisor'

    def build_custom_param(self, data):
        return {'user_id': data['user_id'], 'anchor_id': data['anchor_id']}

class SuperVisorList(LoginBaseApi):
    """
    房管列表
    """
    url = '/helper/supervisorlist'