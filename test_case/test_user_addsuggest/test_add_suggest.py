# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.user_addsuggest_api import UserAddSuggestApi
import json,settings

class TestAddSuggestApi(BaseCase):
    """
    意见反馈
    """
    login_name = settings.YULE_TEST_USER_LOGIN_NAME
    content = '世界那么大,come'

    def test_add_suggest_success(self):
        """
        测试意见反馈成功
        :return:
        """
        add_suggest_api = UserAddSuggestApi(login_name = self.login_name)
        response = add_suggest_api.get({"content":self.content})
        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity_obj['login_name'],(self.login_name))
        self.assertEqual(add_suggest_api.get_code(),0)
        self.assertEqual(add_suggest_api.get_response_message(),u"操作成功")

    def test_add_suggest_null(self):
        """
        测试请求接口反馈内容为空
        :return:
        """
        add_suggest_api = UserAddSuggestApi(login_name = self.login_name)
        add_suggest_api.get({"content":None})
        self.assertEqual(add_suggest_api.get_code(),400109)
        self.assertEqual(add_suggest_api.get_response_message(),u"请填写反馈内容")
