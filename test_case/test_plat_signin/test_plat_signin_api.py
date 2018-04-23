# -*- coding:utf-8 -*-
import datetime,json,time
from base.base_case import BaseCase
from api.plat_signin_api import PlatSigninApi
from utilities.redis_helper import Redis
from utilities.teardown import TearDown
import settings

class TestPlatSigninApi(BaseCase):
    """
    平台签到
    """
    user_login_name = '15188888888'
    anchor_id = settings.YULE_TEST_ANCHOR_ID
    user_id = '22013903'
    room_id = settings.YULE_TEST_ROOM
    kiss_gift_id = 56
    briefs_gift_id = 47
    time_sleep = 0.3


    def test_continuous_sign_in_one(self):
        """
        测试平台签到第一天
        :return:
        """
        plat_signin_api = PlatSigninApi(self.user_login_name)
        response = plat_signin_api.get({'platform': 'android','channel_id': settings.CHANNEL_ID})
        self.assertEqual(plat_signin_api.get_code(),0)

        plat_sign_obj = json.loads(response.content)['result']['plat_sign_obj']
        self.assertEqual(plat_sign_obj['signin_series_num'],1)
        expect_next_date = (datetime.datetime.now() + datetime.timedelta(days=+1)).strftime("%Y-%m-%d")
        self.assertEqual(expect_next_date,plat_sign_obj['signin_next_date'])

        signin_last_date = (datetime.datetime.now() + datetime.timedelta()).strftime("%Y-%m-%d")
        self.assertEqual(plat_sign_obj['signin_last_date'],signin_last_date)

        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity_obj['diamond'],u'1000')


    def test_continuous_sign_in_two(self):
        """
        测试平台签到第二天
        :return:
        """
        plat_signin_api = PlatSigninApi(self.user_login_name)
        plat_signin_api.get({'platform': 'android', 'channel_id': settings.CHANNEL_ID})

        self.assertEqual(plat_signin_api.get_code(), 0)

        Redis().set_user_plat_signin_day(self.user_id,1)
        time.sleep(self.time_sleep)
        # 签到第二天

        plat_signin_api = PlatSigninApi(self.user_login_name)
        response = plat_signin_api.get({'platform': 'android','channel_id': settings.CHANNEL_ID})

        self.assertEqual(plat_signin_api.get_code(),0)
        plat_sign_obj = json.loads(response.content)['result']['plat_sign_obj']
        self.assertEqual(plat_sign_obj['signin_series_num'], 2)
        expect_next_date = (datetime.datetime.now() + datetime.timedelta(days=+1)).strftime("%Y-%m-%d")
        self.assertEqual(expect_next_date, plat_sign_obj['signin_next_date'])

        signin_last_date = (datetime.datetime.now() + datetime.timedelta()).strftime("%Y-%m-%d")
        self.assertEqual(plat_sign_obj['signin_last_date'], signin_last_date)

        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity_obj['diamond'], u'2000')

    def test_continuous_sign_in_three(self):
        """
        测试平台签到第三天
        :return:
        """
        plat_signin_api = PlatSigninApi(self.user_login_name)
        plat_signin_api.get({'platform': 'android', 'channel_id': settings.CHANNEL_ID})

        self.assertEqual(plat_signin_api.get_code(), 0)

        Redis().set_user_plat_signin_day(self.user_id, 2)
        time.sleep(self.time_sleep)
        # 签到第三天

        plat_signin_api = PlatSigninApi(self.user_login_name)
        response = plat_signin_api.get({'platform': 'android','channel_id': settings.CHANNEL_ID})

        self.assertEqual(plat_signin_api.get_code(), 0)

        plat_sign_obj = json.loads(response.content)['result']['plat_sign_obj']
        self.assertEqual(plat_sign_obj['signin_series_num'], 3)
        expect_next_date = (datetime.datetime.now() + datetime.timedelta(days=+1)).strftime("%Y-%m-%d")
        self.assertEqual(expect_next_date, plat_sign_obj['signin_next_date'])

        signin_last_date = (datetime.datetime.now() + datetime.timedelta()).strftime("%Y-%m-%d")
        self.assertEqual(plat_sign_obj['signin_last_date'], signin_last_date)

        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity_obj['diamond'], u'3000')


    def test_continuous_sign_in_four(self):
        """
        测试平台签到第四天
        :return:
        """
        plat_signin_api = PlatSigninApi(self.user_login_name)
        plat_signin_api.get({'platform': 'android', 'channel_id': 1})
        self.assertEqual(plat_signin_api.get_code(), 0)
        Redis().set_user_plat_signin_day(self.user_id, 3)
        time.sleep(self.time_sleep)
        # 签到第四天
        plat_signin_api = PlatSigninApi(self.user_login_name)
        response = plat_signin_api.get({'platform': 'android','channel_id': settings.CHANNEL_ID})
        self.assertEqual(plat_signin_api.get_code(), 0)
        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity_obj['diamond'], u'3000')

    def test_continuous_sign_in_five(self):
        """
        测试平台签到第五天
        :return:
        """
        plat_signin_api = PlatSigninApi(self.user_login_name)
        plat_signin_api.get({'platform': 'android', 'channel_id': settings.CHANNEL_ID})

        self.assertEqual(plat_signin_api.get_code(), 0)

        Redis().set_user_plat_signin_day(self.user_id, 4)
        time.sleep(self.time_sleep)
        # 签到第五天
        plat_signin_api = PlatSigninApi(self.user_login_name)
        response = plat_signin_api.get({'platform': 'android','channel_id': settings.CHANNEL_ID})

        self.assertEqual(plat_signin_api.get_code(), 0)

        plat_sign_obj = json.loads(response.content)['result']['plat_sign_obj']
        self.assertEqual(plat_sign_obj['signin_series_num'], 5)
        expect_next_date = (datetime.datetime.now() + datetime.timedelta(days=+1)).strftime("%Y-%m-%d")
        self.assertEqual(expect_next_date, plat_sign_obj['signin_next_date'])

        signin_last_date = (datetime.datetime.now() + datetime.timedelta()).strftime("%Y-%m-%d")
        self.assertEqual(plat_sign_obj['signin_last_date'], signin_last_date)

        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity_obj['diamond'], u'4000')


    def test_continuous_sign_in_six(self):
        """
        测试平台签到第六天
        :return:
        """
        plat_signin_api = PlatSigninApi(self.user_login_name)
        plat_signin_api.get({'platform': 'android', 'channel_id': settings.CHANNEL_ID})

        self.assertEqual(plat_signin_api.get_code(), 0)

        Redis().set_user_plat_signin_day(self.user_id, 5)
        time.sleep(self.time_sleep)
        # 签到第六天

        plat_signin_api = PlatSigninApi(self.user_login_name)
        response = plat_signin_api.get({'platform': 'android','channel_id': settings.CHANNEL_ID})

        self.assertEqual(plat_signin_api.get_code(), 0)
        plat_sign_obj = json.loads(response.content)['result']['plat_sign_obj']
        self.assertEqual(plat_sign_obj['signin_series_num'], 6)
        expect_next_date = (datetime.datetime.now() + datetime.timedelta(days=+1)).strftime("%Y-%m-%d")
        self.assertEqual(expect_next_date, plat_sign_obj['signin_next_date'])

        signin_last_date = (datetime.datetime.now() + datetime.timedelta()).strftime("%Y-%m-%d")
        self.assertEqual(plat_sign_obj['signin_last_date'], signin_last_date)

        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity_obj['diamond'], u'4000')


    def test_continuous_sign_in_seven(self):
        """
        测试平台签到第七天
        :return:
        """
        plat_signin_api = PlatSigninApi(self.user_login_name)
        plat_signin_api.get({'platform': 'android', 'channel_id': settings.CHANNEL_ID})
        self.assertEqual(plat_signin_api.get_code(), 0)
        Redis().set_user_plat_signin_day(self.user_id, 6)
        time.sleep(self.time_sleep)


        plat_signin_api = PlatSigninApi(self.user_login_name)
        response = plat_signin_api.get({'platform': 'android','channel_id': settings.CHANNEL_ID})

        self.assertEqual(plat_signin_api.get_code(), 0)
        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity_obj['diamond'], u'6000')

    def test_sign_in_plat_is_null(self):
        """
        测试请求接口平台信息为空
        :return:
        """
        plat_sign_in_api = PlatSigninApi(self.user_login_name)
        plat_sign_in_api.get({'platform': '','channel_id': settings.CHANNEL_ID})

        self.assertEqual(plat_sign_in_api.get_code(),422123)
        self.assertEqual(plat_sign_in_api.get_response_message(),u'平台不能为空')


    def test_sign_in_channel_id_is_null(self):
        """
        测试请求接口渠道为空
        :return:
        """
        plat_sign_in_api = PlatSigninApi(self.user_login_name)
        plat_sign_in_api.get({'platform': 'android','channel_id': None})

        self.assertEqual(plat_sign_in_api.get_code(),401002)
        self.assertEqual(plat_sign_in_api.get_response_message(),u'缺少渠道参数')


    def test_continuous_sign_in_one_again(self):
        """
        测试当天重复签到
        :return:
        """
        plat_signin_api = PlatSigninApi(self.user_login_name)
        plat_signin_api.get({'platform': 'android','channel_id': settings.CHANNEL_ID})

        self.assertEqual(plat_signin_api.get_code(),0)

        plat_signin_api = PlatSigninApi(self.user_login_name)
        plat_signin_api.get({'platform': 'android','channel_id': settings.CHANNEL_ID})

        self.assertEqual(plat_signin_api.get_code(),507001)
        self.assertEqual(plat_signin_api.get_response_message(),u'今天已签过了，明天再来吧')


    def tearDown(self,*args):
        super(TestPlatSigninApi,self).tearDown(user_id=self.user_id)
        TearDown().platform_signin_teardown(self.user_id)
