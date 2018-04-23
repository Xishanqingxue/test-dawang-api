# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.get_sun_api import UserGetSunApi
import json,settings
from utilities.teardown import TearDown


class TestUserGetSunApi(BaseCase):
    """
    获取太阳
    """
    user_mobile = settings.YULE_TEST_USER_LOGIN_NAME
    user_id = settings.YULE_TEST_USER_ID
    room_id = settings.YULE_TEST_ROOM


    def setUp(self,*args):
        super(TestUserGetSunApi,self).setUp(user_id=self.user_id)
        TearDown().get_sun_api_teardown(self.user_id)

    def test_user_get_sun(self):
        """
        测试获取太阳成功
        :return:
        """
        user_get_sun_api = UserGetSunApi(self.user_mobile)
        response = user_get_sun_api.get({'room_id': self.room_id})

        self.assertEqual(user_get_sun_api.get_code(), 0)
        self.assertEqual(user_get_sun_api.get_response_message(), u'操作成功')

        response_identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(response_identity_obj['sun_num'], 1)

    def test_user_get_sun_room_id_null(self):
        """
        测试请求接口房间ID为空
        :return:
        """
        user_get_sun_api = UserGetSunApi(self.user_mobile)
        user_get_sun_api.get({'room_id': ''})

        self.assertEqual(user_get_sun_api.get_code(), 402000)
        self.assertEqual(user_get_sun_api.get_response_message(), u'房间ID不能为空')

    def test_sun_number_has_been_capped(self):
        """
        测试太阳达到上限
        :return:
        """
        for i in range(50):
            user_get_sun_api = UserGetSunApi(self.user_mobile)
            user_get_sun_api.get({'room_id': self.room_id})
            self.assertEqual(user_get_sun_api.get_code(), 0)

        user_get_sun_api = UserGetSunApi(self.user_mobile)
        user_get_sun_api.get({'room_id': self.room_id})

        self.assertEqual(user_get_sun_api.get_code(), 402016)
        self.assertEqual(user_get_sun_api.get_response_message(), u'到达上限')

    def tearDown(self,*args):
        super(TestUserGetSunApi, self).tearDown(user_id=self.user_id)
        TearDown().get_sun_api_teardown(self.user_id)