# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.update_nickname_api import UpdateNickApi
import settings

class TestUpdateNickApi(BaseCase):
    """
    修改昵称
    """
    user_mobile = settings.YULE_TEST_USER_LOGIN_NAME

    def test_update_nick_is_null(self):
        """
        测试请求接口昵称为空
        :return:
        """
        update_nick_api = UpdateNickApi(self.user_mobile)
        update_nick_api.get({'nickname':None})

        self.assertEqual(update_nick_api.get_code(),400108)
        self.assertEqual(update_nick_api.get_response_message(),u'昵称不能为空')


    def test_update_nick_name_is_too_long(self):
        """
        测试请求接口昵称长度超过8位
        :return:
        """
        update_nick_api = UpdateNickApi(self.user_mobile)
        update_nick_api.get({'nickname':'yiersans9'})

        self.assertEqual(update_nick_api.get_code(),400131)
        self.assertEqual(update_nick_api.get_response_message(),u'昵称长度必须为4-8位')


    def test_update_nick_name_is_too_short(self):
        """
        测试请求接口昵称长度小于4位
        :return:
        """
        update_nick_api = UpdateNickApi(self.user_mobile)
        update_nick_api.get({'nickname':'yqw'})

        self.assertEqual(update_nick_api.get_code(),400131)
        self.assertEqual(update_nick_api.get_response_message(),u'昵称长度必须为4-8位')


    def test_update_nick_have_sensitive_word(self):
        """
        测试请求接口昵称中包含敏感词
        :return:
        """
        update_nick_api = UpdateNickApi(self.user_mobile)
        update_nick_api.get({'nickname':'习近平12'})

        self.assertEqual(update_nick_api.get_code(),100014)
        self.assertEqual(update_nick_api.get_response_message(),u'很抱歉，根据相关法规和政策，此内容无法发布。')


    def test_update_nick_is_exist(self):
        """
        测试请求接口修改已经存在的昵称
        :return:
        """
        update_nick_api = UpdateNickApi(self.user_mobile)
        update_nick_api.get({'nickname':'123456'})

        self.assertEqual(update_nick_api.get_code(),801012)
        self.assertEqual(update_nick_api.get_response_message(),u'昵称已存在，请更换昵称')

    def test_update_nick_gold_low(self):
        """
        测试请求接口金币不足
        :return:
        """
        update_nick_api = UpdateNickApi(self.user_mobile)
        update_nick_api.get({'nickname':'ihsgrm'})

        self.assertEqual(update_nick_api.get_code(),100032)
        self.assertEqual(update_nick_api.get_response_message(),u'金币不足请充值')

