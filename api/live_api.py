# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi


class EnterRoomApi(LoginBaseApi):
    """
    进入直播间
    """
    url = '/live/enterRoom'

    def build_custom_param(self, data):
        return {'room_id':data['room_id']}


class LeaveAnchorRoomApi(LoginBaseApi):
    """
    离开直播间
    """
    url = '/live/leaveanchorroom'

    def build_custom_param(self, data):
        return {'room_id': data['room_id']}


class LiveApi(LoginBaseApi):
    """
    获取直播间信息
    """
    url = '/live'

    def build_custom_param(self, data):
        return {'room_id': data['room_id']}