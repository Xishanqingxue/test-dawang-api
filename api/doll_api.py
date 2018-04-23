# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi


class SetReceivingAddress(LoginBaseApi):
    """
    设置奖品邮寄地址
    """
    url = '/txwawaji/setReceivingAddress'

    def build_custom_param(self, data):
        return {'name': data['name'], 'mobilephone': data['mobilephone'], 'area': data['area'],
                'address': data['address'], 'remarks': data['remarks'], 'doll_log_ids': data['doll_log_ids']}


class ResetMachineStatusApi(LoginBaseApi):
    # 重置娃娃机状态
    url = '/doll/resetMachineStatus'

    def build_custom_param(self, data):
        return {'room_id':data['room_id']}


class OperatingMachineApi(LoginBaseApi):
    # 操作娃娃机
    url = '/doll/operatingMachine'

    def build_custom_param(self, data):
        return {'room_id':data['room_id'],'command':data['command']}


class MyDollLogApi(LoginBaseApi):
    # 我的娃娃列表
    url = '/doll/myDollLog'


class GrabApi(LoginBaseApi):
    # 抢机器
    url = '/doll/grab'

    def build_custom_param(self, data):
        return {'room_id':data['room_id']}


class GetRuleApi(LoginBaseApi):
    # 获取兑换规则
    url = '/doll/getRule'


class GetReceivingAddress(LoginBaseApi):
    """
    获取收货地址
    """

    url = '/txwawaji/getReceivingAddress'

    def build_custom_param(self, data):
        return {'doll_log_id':data['doll_log_id']}


class GetOrderDataApi(LoginBaseApi):
    """
    获取收货地址
    """

    url = '/txwawaji/getOderData'


class GetMachineInfoApi(LoginBaseApi):
    # 获取娃娃机信息
    url = '/doll/getMachineInfo'

    def build_custom_param(self, data):
        return {'room_id':data['room_id']}


class EnterDollRoomApi(LoginBaseApi):
    # 进入娃娃机直播间
    url = '/doll/enterDollRoom'

    def build_custom_param(self, data):
        return {'room_id': data['room_id'], 'channel_id': '10000001',}


class DollOnlineListApi(LoginBaseApi):
    # 娃娃机在线人数列表
    url = '/live/dollOnlinelist'

    def build_custom_param(self, data):
        return {'room_id':data['room_id']}


class DollGameListApi(LoginBaseApi):
    """
    游戏记录
    """

    url = '/doll/dollGameList'

class DollExchangeApi(LoginBaseApi):
    # 娃娃机兑换银币
    url = '/doll/dollExchange'

    def build_custom_param(self, data):
        return {'doll_log_id':data['doll_log_id']}


class ContinueGameApi(LoginBaseApi):
    # 继续游戏
    url = '/doll/continueGame'

    def build_custom_param(self, data):
        return {'room_id':data['room_id']}

