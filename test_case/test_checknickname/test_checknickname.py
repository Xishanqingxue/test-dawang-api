# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.user_check_nickname_api import UserCheckNickname

class TestCheckNicknameApi(BaseCase):
    """
    检查昵称
    """
    nickname = "123456"
    new_nickname = "streets"

    def test_check_nickname_exist(self):
        """
        测试请求接口已存在昵称
        :return:
        """
        #用户昵称存在 "昵称已存在请替换"
        check_nickname_api = UserCheckNickname()
        check_nickname_api.get({'nickname': self.nickname})
        self.assertEqual(check_nickname_api.get_code(),422106)
        self.assertEqual(check_nickname_api.get_response_message(),u"昵称已存在请替换")

    def test_check_nickname_success(self):
        """
        测试检查昵称成功
        :return:
        """
        check_nickname_api = UserCheckNickname()
        check_nickname_api.get({'nickname': self.new_nickname})
        self.assertEqual(check_nickname_api.get_code(),0)
        self.assertEqual(check_nickname_api.get_response_message(),u"操作成功")

    def test_check_nickname_null(self):
        """
        测试请求接口昵称为空
        :return:
        """
        #昵称为空 "昵称不能为空"
        check_nickname_api = UserCheckNickname()
        check_nickname_api.get({'nickname':None})
        self.assertEqual(check_nickname_api.get_code(),422103)
        self.assertEqual(check_nickname_api.get_response_message(),u"昵称不能为空")

    def test_check_nickname_sensitivity(self):
        """
        测试请求接口昵称中包含敏感词
        :return:
        """
        check_nickname_api = UserCheckNickname()
        check_nickname_api.get({'nickname': '习近平m1'})
        self.assertEqual(check_nickname_api.get_code(),422105)
        self.assertEqual(check_nickname_api.get_response_message(),u"昵称包含敏感词，请替换")
