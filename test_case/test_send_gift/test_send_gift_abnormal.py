# -*- coding:utf-8 -*-
from api.send_gift_api import SendGiftApi
from base.base_case import BaseCase
import settings


class TestSendGift(BaseCase):
    """
    送礼物
    """
    login_name = settings.YULE_TEST_USER_LOGIN_NAME
    user_id = settings.YULE_TEST_USER_ID
    room_id = settings.YULE_TEST_ROOM
    anchor_id = settings.YULE_TEST_ANCHOR_ID
    time_sleep = 0.3

    def test_send_gift_room_id_null(self):
        """
        测试请求接口房间ID为空
        :return:
        """
        send_gift_api = SendGiftApi(self.login_name)
        send_gift_api.get({'room_id': None, 'gift_id': 6, 'gift_count': 1, 'currency': 'gold'})

        self.assertEqual(send_gift_api.get_code(), 402000)
        self.assertEqual(send_gift_api.get_response_message(),u'房间ID不能为空')

    def test_send_gift_room_id_error(self):
        """
        测试请求接口房间ID不存在
        :return:
        """
        send_gift_api = SendGiftApi(self.login_name)
        send_gift_api.get({'room_id': 123000, 'gift_id': 6, 'gift_count': 1, 'currency': 'gold'})

        self.assertEqual(send_gift_api.get_code(), 402004)
        self.assertEqual(send_gift_api.get_response_message(),u'获取直播间数据错误:直播间不存在')

    def test_send_gift_id_null(self):
        """
        测试请求接口礼物ID为空
        :return:
        """
        send_gift_api = SendGiftApi(self.login_name)
        send_gift_api.get({'room_id': self.room_id, 'gift_id': None, 'gift_count': 1, 'currency': 'gold'})

        self.assertEqual(send_gift_api.get_code(), 402009)
        self.assertEqual(send_gift_api.get_response_message(),u'礼物ID不存在')

    def test_send_gift_id_error(self):
        """
        测试请求接口礼物ID不存在
        :return:
        """
        send_gift_api = SendGiftApi(self.login_name)
        send_gift_api.get({'room_id': self.room_id, 'gift_id': 999999, 'gift_count': 1, 'currency': 'gold'})

        self.assertEqual(send_gift_api.get_code(), 402020)
        self.assertEqual(send_gift_api.get_response_message(),u'礼物信息不存在')

    def test_send_gift_count_null(self):
        """
        测试请求接口礼物数量为空
        :return:
        """
        send_gift_api = SendGiftApi(self.login_name)
        send_gift_api.get({'room_id': self.room_id, 'gift_id': 6, 'gift_count': None, 'currency': 'gold'})

        self.assertEqual(send_gift_api.get_code(), 402010)
        self.assertEqual(send_gift_api.get_response_message(),u'礼物数量不能是空')

    def test_send_gift_count_error(self):
        """
        测试请求接口送金币礼物账户金币不足
        :return:
        """
        send_gift_api = SendGiftApi(self.login_name)
        send_gift_api.get({'room_id': self.room_id, 'gift_id': 6, 'gift_count': 9999999999, 'currency': 'gold'})

        self.assertEqual(send_gift_api.get_code(), 100032)
        self.assertEqual(send_gift_api.get_response_message(),u'账户金币不足')

    def test_send_gift_currency_null(self):
        """
        测试请求接口货币类型为空
        :return:
        """
        send_gift_api = SendGiftApi(self.login_name)
        send_gift_api.get({'room_id': self.room_id, 'gift_id': 6, 'gift_count': 1, 'currency': None})

        self.assertEqual(send_gift_api.get_code(), 460004)
        self.assertEqual(send_gift_api.get_response_message(),u'请选择货币类型')

    def test_send_gift_currency_error(self):
        """
        测试请求接口货币类型错误
        :return:
        """
        send_gift_api = SendGiftApi(self.login_name)
        send_gift_api.get({'room_id': self.room_id, 'gift_id': 6, 'gift_count': 1, 'currency': 'abc'})

        self.assertEqual(send_gift_api.get_code(), 460004)
        self.assertEqual(send_gift_api.get_response_message(),u'请选择货币类型')

    def test_send_diamond_gift_account_low(self):
        """
        测试请求接口送大王豆礼物账户金币不足
        :return:
        """
        send_gift_api = SendGiftApi(self.login_name)
        send_gift_api.get({'room_id': self.room_id, 'gift_id': 6, 'gift_count': 9999999999, 'currency': 'diamond'})

        self.assertEqual(send_gift_api.get_code(), 460005)
        self.assertEqual(send_gift_api.get_response_message(),u'您的大王豆余额不足，请转换')

    def test_send_package_gift_low(self):
        """
        测试请求接口送背包礼物数量不足
        :return:
        """
        send_gift_api = SendGiftApi(self.login_name)
        send_gift_api.get({'room_id': self.room_id, 'gift_id': 1009, 'gift_count': 1, 'currency': 'bag'})

        self.assertEqual(send_gift_api.get_code(), 402034)
        self.assertEqual(send_gift_api.get_response_message(),u'背包礼物数量不足,无法送出')

