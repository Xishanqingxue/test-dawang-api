# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.guard_api import BuyGuardApi
import settings


class TestBuyGuardApi(BaseCase):
    """
    购买守护
    """
    login_name = settings.YULE_TEST_USER_LOGIN_NAME
    room_id = settings.YULE_TEST_ROOM



    def test_buy_guard_id_null(self):
        """
        测试请求接口守护ID为空
        :return:
        """
        buy_guard_api = BuyGuardApi(self.login_name)
        buy_guard_api.get({'room_id': self.room_id, 'guard_id': None,'currency':'gold'})

        self.assertEqual(buy_guard_api.get_code(), 402012)
        self.assertEqual(buy_guard_api.get_response_message(),u'守护ID不能为空')

    def test_buy_guard_id_error(self):
        """
        测试请求接口守护类型不存在
        :return:
        """
        buy_guard_api = BuyGuardApi(self.login_name)
        buy_guard_api.get({'room_id': self.room_id, 'guard_id': '55','currency':'gold'})

        self.assertEqual(buy_guard_api.get_code(), 411148)
        self.assertEqual(buy_guard_api.get_response_message(),u'无此守护类型')

    def test_buy_room_id_null(self):
        """
        测试请求接口房间ID为空
        :return:
        """
        buy_guard_api = BuyGuardApi(self.login_name)
        buy_guard_api.get({'room_id': None, 'guard_id': '1', 'currency': 'gold'})

        self.assertEqual(buy_guard_api.get_code(), 402000)
        self.assertEqual(buy_guard_api.get_response_message(), u'房间ID不能为空')

    def test_buy_room_id_error(self):
        """
        测试请求接口房间ID不存在
        :return:
        """
        buy_guard_api = BuyGuardApi(self.login_name)
        buy_guard_api.get({'room_id': '666666', 'guard_id': '1', 'currency': 'gold'})

        self.assertEqual(buy_guard_api.get_code(), 200412)
        self.assertEqual(buy_guard_api.get_response_message(), u'参数异常')

    def test_buy_currency_null(self):
        """
        测试请求接口货币类型为空
        :return:
        """
        buy_guard_api = BuyGuardApi(self.login_name)
        buy_guard_api.get({'room_id': self.room_id, 'guard_id': '1', 'currency': None})

        self.assertEqual(buy_guard_api.get_code(), 460004)
        self.assertEqual(buy_guard_api.get_response_message(), u'请选择货币类型')

    def test_buy_currency_error(self):
        """
        测试请求接口货币类型不存在
        :return:
        """
        buy_guard_api = BuyGuardApi(self.login_name)
        buy_guard_api.get({'room_id': self.room_id, 'guard_id': '1', 'currency': 'abc'})

        self.assertEqual(buy_guard_api.get_code(), 460004)
        self.assertEqual(buy_guard_api.get_response_message(), u'请选择货币类型')