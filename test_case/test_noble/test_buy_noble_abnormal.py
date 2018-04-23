# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.noble_api import BuyNobleApi
from utilities.mysql_helper import MysqlOperation
from utilities.redis_helper import RedisHold
import time,settings



class TestBuyNobleApi(BaseCase):
    """
    购买贵族
    """
    login_name = settings.YULE_TEST_USER_LOGIN_NAME
    user_id = settings.YULE_TEST_USER_ID
    room_id = settings.YULE_TEST_ROOM
    time_sleep = 0.3



    def test_buy_noble_id_null(self):
        """
        测试请求接口贵族ID为空
        :return:
        """
        buy_noble_api = BuyNobleApi(self.login_name)
        buy_noble_api.get({'noble_id': None, 'num': 1, 'room_id': self.room_id, 'currency': 'gold'})
        self.assertEqual(buy_noble_api.get_code(), 402028)
        self.assertEqual(buy_noble_api.get_response_message(), u'贵族ID不符合规则')

    def test_buy_noble_id_error(self):
        """
        测试请求接口贵族ID不存在
        :return:
        """
        buy_noble_api = BuyNobleApi(self.login_name)
        buy_noble_api.get({'noble_id': 999, 'num': 1, 'room_id': self.room_id, 'currency': 'gold'})
        self.assertEqual(buy_noble_api.get_code(), 402025)
        self.assertEqual(buy_noble_api.get_response_message(), u'贵族信息不存在')

    def test_buy_noble_num_null(self):
        """
        测试请求接口购买数量为空
        :return:
        """
        buy_noble_api = BuyNobleApi(self.login_name)
        buy_noble_api.get({'noble_id': 1, 'num': None, 'room_id': self.room_id, 'currency': 'gold'})
        self.assertEqual(buy_noble_api.get_code(), 402029)
        self.assertEqual(buy_noble_api.get_response_message(), u'贵族购买数量有误')

    def test_buy_noble_room_null(self):
        """
        测试请求接口房间ID为空
        :return:
        """
        buy_noble_api = BuyNobleApi(self.login_name)
        buy_noble_api.get({'noble_id': 1, 'num': 1, 'room_id':None, 'currency': 'gold'})
        self.assertEqual(buy_noble_api.get_code(), 402000)
        self.assertEqual(buy_noble_api.get_response_message(), u'房间ID不能为空')

    def test_buy_noble_room_error(self):
        """
        测试请求接口房间ID不存在
        :return:
        """
        buy_noble_api = BuyNobleApi(self.login_name)
        buy_noble_api.get({'noble_id': 1, 'num': 1, 'room_id':'19090909', 'currency': 'gold'})
        self.assertEqual(buy_noble_api.get_code(), 801017)
        self.assertEqual(buy_noble_api.get_response_message(), u'房间信息不存在')

    def test_buy_noble_currency_null(self):
        """
        测试请求接口货币类型为空
        :return:
        """
        buy_noble_api = BuyNobleApi(self.login_name)
        buy_noble_api.get({'noble_id': 1, 'num': 1, 'room_id':self.room_id, 'currency': None})
        self.assertEqual(buy_noble_api.get_code(), 460004)
        self.assertEqual(buy_noble_api.get_response_message(), u'请选择货币类型')

    def test_buy_noble_currency_error(self):
        """
        测试请求接口货币类型不存在
        :return:
        """
        buy_noble_api = BuyNobleApi(self.login_name)
        buy_noble_api.get({'noble_id': 1, 'num': 1, 'room_id':self.room_id, 'currency': 'abcd'})
        self.assertEqual(buy_noble_api.get_code(), 460004)
        self.assertEqual(buy_noble_api.get_response_message(), u'请选择货币类型')

    def test_buy_noble_gold_low(self):
        """
        测试请求接口账户金币不足
        :return:
        """
        mysql_operation = MysqlOperation(user_id=self.user_id)
        mysql_operation.fix_user_account(gold_num=23999)
        RedisHold().clean_redis_user_detail(self.user_id)
        time.sleep(self.time_sleep)
        buy_noble_api = BuyNobleApi(self.login_name)
        buy_noble_api.get({'noble_id': 1, 'num': 1, 'room_id': self.room_id, 'currency': 'gold'})
        self.assertEqual(buy_noble_api.get_code(), 100032)
        self.assertEqual(buy_noble_api.get_response_message(), u'账户金币不足')

