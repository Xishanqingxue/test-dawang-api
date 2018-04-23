# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi


class GetGrabHistoryApi(LoginBaseApi):
    """
    抢红包记录
    """
    url = '/redpacket/getRedPacketLog'

    def build_custom_param(self, data):
        return {'red_packet_id':data['red_packet_id']}


class GetHistoryApi(LoginBaseApi):
    """
    发红包历史
    """
    url = '/redpacket/getHistory'


    
class RedPacketConfigApi(LoginBaseApi):
    """
    获取红包配置
    """
    url = '/redpacket/getRedpacketConfig'


class GetRedPacketListApi(LoginBaseApi):
    """
    可抢红包列表
    """
    url = '/redpacket/getRedPacket'

    def build_custom_param(self, data):
        return {'room_id':data['room_id']}


class GrabRedPacket(LoginBaseApi):
    """
    抢红包
    """
    url = '/redpacket/grabRedPacket'

    def build_custom_param(self, data):
        return {'red_packet_id':data['red_packet_id'],'room_id':data['room_id']}


class SendRedPacketApi(LoginBaseApi):
    """
    发红包
    """
    url = '/redpacket/sendRedPacket'

    def build_custom_param(self, data):
        return {'conf_id':data['conf_id'],'room_id':data['room_id'],'num':data['num'],'currency':data['currency']}


