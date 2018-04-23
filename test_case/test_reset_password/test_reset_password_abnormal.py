# -*- coding:utf-8 -*-
from api.reset_password_api import ResetPasswordApi
from base.base_case import BaseCase
from utilities.mysql_helper import MysqlGet
from utilities.mysql_helper import MysqlFix
import settings



class TestResetPasswordApi(BaseCase):
    """
    忘记密码
    """
    login_name='15899999999'
    user_id = MysqlGet(mobile=login_name).get_user_id()
    device_id = settings.DEVICE_ID
    new_password = '1234abcd'



    def test_reset_password_phone_null(self):
        """
        测试请求接口手机号为空
        :return:
        """
        reset_password_api = ResetPasswordApi(self.login_name)
        reset_password_api.get({'phone': None,'code': '6666','new_password':self.new_password,
                 'confirm_password':self.new_password})

        self.assertEqual(reset_password_api.get_code(),400101)
        self.assertEqual(reset_password_api.get_response_message(),u'手机号不能为空')

    def test_reset_password_sms_code_null(self):
        """
        测试请求接口手机验证码为空
        :return:
        """
        reset_password_api = ResetPasswordApi(self.login_name)
        reset_password_api.get({'phone': self.login_name,'code': None,'new_password':self.new_password,
                 'confirm_password':self.new_password})

        self.assertEqual(reset_password_api.get_code(),400102)
        self.assertEqual(reset_password_api.get_response_message(),u'验证码为空')


    def test_reset_password_sms_new_password_null(self):
        """
        测试请求接口新密码为空
        :return:
        """
        reset_password_api = ResetPasswordApi(self.login_name)
        reset_password_api.get({'phone': self.login_name,'code': '6666','new_password':None,
                 'confirm_password':self.new_password})

        self.assertEqual(reset_password_api.get_code(),400120)
        self.assertEqual(reset_password_api.get_response_message(),u'新密码不能为空')

    def test_reset_password_sms_confirm_password_null(self):
        """
        测试请求接口确认密码为空
        :return:
        """
        reset_password_api = ResetPasswordApi(self.login_name)
        reset_password_api.get({'phone': self.login_name,'code': '6666','new_password':self.new_password,
                 'confirm_password':None})

        self.assertEqual(reset_password_api.get_code(),400121)
        self.assertEqual(reset_password_api.get_response_message(),u'对比密码不能为空')

    def test_reset_password_sms_confirm_password_error(self):
        """
        测试请求接口两次输入密码不一致
        :return:
        """
        reset_password_api = ResetPasswordApi(self.login_name)
        reset_password_api.get({'phone': self.login_name,'code': '6666','new_password':self.new_password,
                 'confirm_password':self.new_password + '2'})

        self.assertEqual(reset_password_api.get_code(),400138)
        self.assertEqual(reset_password_api.get_response_message(),u'两次密码不一致')

    def test_reset_password_sms_sms_code_error(self):
        """
        测试请求接口手机验证码错误
        :return:
        """
        reset_password_api = ResetPasswordApi(self.login_name)
        reset_password_api.get({'phone': self.login_name,'code': '6666','new_password':self.new_password,
                 'confirm_password':self.new_password})

        self.assertEqual(reset_password_api.get_code(),400135)
        self.assertEqual(reset_password_api.get_response_message(),u'验证码已失效请重新获取')


    def tearDown(self,*args):
        super(TestResetPasswordApi,self).tearDown()
        MysqlFix(user_id=self.user_id).fix_user_password()



