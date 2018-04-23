# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi


class SendGiftApi(LoginBaseApi):
    """
    送礼物
    """
    url = '/live/newSendGift'

    def build_custom_param(self, data):
        return {'room_id': data['room_id'], 'gift_id': data['gift_id'], 'gift_count': data['gift_count'],
                'currency': data['currency']}
