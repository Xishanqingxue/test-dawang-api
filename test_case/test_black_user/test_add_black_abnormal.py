# -*- coding:utf-8 -*-
from unittest import TestCase
from api.add_black_user_api import AddBlackUserApi
import settings

class TestAnchorAddBlackUserNormalApi(TestCase):
    """
    黑名单
    """
    anchor_login_name = settings.YULE_TEST_ANCHOR_LOGIN_NAME
    anchor_id = settings.YULE_TEST_ANCHOR_ID
    user_id = '22014102'

    def test_user_id_is_null(self):
        """
        测试请求接口用户ID为空
        :return:
        """
        add_black_user_api = AddBlackUserApi(self.anchor_login_name)
        add_black_user_api.get({'user_id': '', 'anchor_id': self.anchor_id, 'blacker_type': 'forbid_visit'})

        self.assertEqual(add_black_user_api.get_code(),801020)
        self.assertEqual(add_black_user_api.get_response_message(),u'用户id不能为空')

    def test_user_id_is_error(self):
        """
        测试请求接口用户ID错误
        :return:
        """
        add_black_user_api = AddBlackUserApi(self.anchor_login_name)
        add_black_user_api.get({'user_id': self.user_id + '333333', 'anchor_id': self.anchor_id, 'blacker_type': 'forbid_visit'})

        self.assertEqual(add_black_user_api.get_code(),801027)
        self.assertEqual(add_black_user_api.get_response_message(),u'用户信息不存在')

    def test_anchor_id_is_null(self):

        """
        测试请求接口主播ID为空
        :return:
        """
        add_black_user_api = AddBlackUserApi(self.anchor_login_name)
        add_black_user_api.get({'user_id': self.user_id, 'anchor_id': '', 'blacker_type': 'forbid_visit'})

        self.assertEqual(add_black_user_api.get_code(),402005)
        self.assertEqual(add_black_user_api.get_response_message(),u'主播ID不能为空')

    def test_anchor_id_is_error(self):
        """
        测试请求接口主播ID错误
        :return:
        """
        add_black_user_api = AddBlackUserApi(self.anchor_login_name)
        add_black_user_api.get({'user_id': self.user_id, 'anchor_id': str(self.anchor_id) + '222', 'blacker_type': 'forbid_visit'})

        self.assertEqual(add_black_user_api.get_code(),801017)
        self.assertEqual(add_black_user_api.get_response_message(),u'房间信息不存在')

    def test_blacker_type_is_null(self):
        """
        测试请求接口黑名单类型为空
        :return:
        """
        add_black_user_api = AddBlackUserApi(self.anchor_login_name)
        add_black_user_api.get({'user_id': self.user_id, 'anchor_id': self.anchor_id, 'blacker_type': ''})

        self.assertEqual(add_black_user_api.get_code(),801013)
        self.assertEqual(add_black_user_api.get_response_message(),u'请求参数错误')

    def test_blacker_type_is_error(self):
        """
        测试请求接口黑名单类型错误
        :return:
        """
        add_black_user_api = AddBlackUserApi(self.anchor_login_name)
        add_black_user_api.get({'user_id': self.user_id, 'anchor_id': self.anchor_id, 'blacker_type': '123'})

        self.assertEqual(add_black_user_api.get_code(),801026)
        self.assertEqual(add_black_user_api.get_response_message(),u'黑名单类型不合法')
