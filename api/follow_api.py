# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi


class AddFollowingApi(LoginBaseApi):
    """
    添加关注
    """
    url = '/user/addfollowing'

    def build_custom_param(self, data):
        return {'anchor_id': data['anchor_id']}


class RelieveFollowingApi(LoginBaseApi):
    """
    取消关注
    """
    url = '/user/relievefollowing'

    def build_custom_param(self, data):
        return {'anchor_id': data['anchor_id']}


class MyFollowListApi(LoginBaseApi):
    """
    我得关注列表
    """
    url = '/channel/focus'

    def build_custom_param(self, data):
        return {'type':1}