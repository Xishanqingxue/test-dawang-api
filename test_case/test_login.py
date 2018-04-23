# -*- coding:utf-8 -*-
from api.login_api import LoginApi
from base.base_case import BaseCase
import json,settings


class TestLoginApi(BaseCase):
    """
    登录
    """
    login_name = settings.YULE_TEST_USER_LOGIN_NAME

    def test_login_success(self):
        """
        测试登录成功
        :return:
        """
        login_api = LoginApi()
        response = login_api.login(login_name=self.login_name,only_get_identity=False)

        self.assertEqual(login_api.get_resp_code(),0)
        identity = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity['login_name'],self.login_name)
        # self.assertEqual(identity['mobilephone'],self.login_name)
        self.assertIsNotNone(identity['identity'])
        self.assertEqual(identity['identity'],identity['user_sign'])

    def test_login_name_null(self):
        """
        测试请求接口登录名为空
        :return:
        """
        login_api = LoginApi()
        login_api.login(login_name=None, only_get_identity=False)
        self.assertEqual(login_api.get_resp_code(), 422101)
        self.assertEqual(login_api.get_resp_message(),u'登录账号名不能为空')

    def test_login_name_error(self):
        """
        测试请求接口登录帐号不存在
        :return:
        """
        login_api = LoginApi()
        login_api.login(login_name='13501077766', only_get_identity=False)
        self.assertEqual(login_api.get_resp_code(), 422109)
        self.assertEqual(login_api.get_resp_message(),u'登录账号不存在')

    def test_login_password_null(self):
        """
        测试请求接口密码为空
        :return:
        """
        login_api = LoginApi()
        login_api.login(login_name=self.login_name,password=None, only_get_identity=False)
        self.assertEqual(login_api.get_resp_code(), 422102)
        self.assertEqual(login_api.get_resp_message(),u'密码不能为空')

    def test_login_password_error(self):
        """
        测试请求接口密码错误
        :return:
        """
        login_api = LoginApi()
        login_api.login(login_name=self.login_name, password='123456', only_get_identity=False)
        self.assertEqual(login_api.get_resp_code(), 422110)
        self.assertEqual(login_api.get_resp_message(), u'密码错误')