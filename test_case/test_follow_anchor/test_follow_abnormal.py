# -*- coding:utf-8 -*-
from api.follow_api import AddFollowingApi,RelieveFollowingApi
from base.base_case import BaseCase
import settings


class TestFollowApi(BaseCase):
    """
    关注
    """
    login_name = settings.YULE_TEST_USER_LOGIN_NAME
    anchor_id = settings.YULE_TEST_ANCHOR_ID

    def test_add_following_anchor_id_error(self):
        """
        测试请求加关注接口主播ID不存在
        :return:
        """
        add_following_api = AddFollowingApi(self.login_name)
        add_following_api.get({'anchor_id': str(self.anchor_id) + '1'})
        self.assertEqual(add_following_api.get_code(), 402008)
        self.assertEqual(add_following_api.get_response_message(), u'主播信息不存在')

    def test_add_following_anchor_id_null(self):
        """
        测试请求加关注接口主播ID为空
        :return:
        """
        add_following_api = AddFollowingApi(self.login_name)
        add_following_api.get({'anchor_id':''})
        self.assertEqual(add_following_api.get_code(), 402005)
        self.assertEqual(add_following_api.get_response_message(), u'主播ID不能为空')

    def test_relieve_following_api_anchor_id_null(self):
        """
        测试请求取消关注接口主播ID为空
        :return:
        """
        relieve_following_api = RelieveFollowingApi(self.login_name)
        relieve_following_api.get({'anchor_id': ''})
        self.assertEqual(relieve_following_api.get_code(),402005)
        self.assertEqual(relieve_following_api.get_response_message(),u'主播ID不能为空')

    def test_relieve_following_anchor_error(self):
        """
        测试请求取消关注接口主播ID不存在
        :return:
        """
        relieve_following_api = RelieveFollowingApi(self.login_name)
        relieve_following_api.get({'anchor_id': str(self.anchor_id) + '1'})
        self.assertEqual(relieve_following_api.get_code(), 402008)
        self.assertEqual(relieve_following_api.get_response_message(), u'主播信息不存在')

    def test_relieve_following_anchoe_not_following(self):
        """
        测试未关注主播情况下请求取消关注接口
        :return:
        """
        relieve_following_api = RelieveFollowingApi(self.login_name)
        relieve_following_api.get({'anchor_id': self.anchor_id})
        self.assertEqual(relieve_following_api.get_code(), 402027)
        self.assertEqual(relieve_following_api.get_response_message(), u'该主播未被关注')