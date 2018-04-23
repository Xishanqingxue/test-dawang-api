# -*- coding:utf-8 -*-
from api.reset_password_api import ResetPasswordApi
from api.image_code_api import ImageCodeApi
from api.send_sms_code_api import LoginSendSmsCodeApi
from api.login_api import LoginApi
from base.base_case import BaseCase
from utilities.mysql_helper import MysqlGet
from utilities.mysql_helper import MysqlFix
from utilities.redis_helper import Redis
import settings,time,json



class TestResetPasswordApi(BaseCase):
    """
    忘记密码
    """
    login_name='15844444444'
    device_id = settings.DEVICE_ID
    new_password = '1234abcd'



    def test_reset_password_sucess(self):
        """
        测试修改密码成功
        :return:
        """
        ImageCodeApi().get({'device_id':self.device_id})
        image_code = Redis().get_image_captcha(self.device_id)

        send_sms_code_api = LoginSendSmsCodeApi(self.login_name)
        send_sms_code_api.get( {'device_id': self.device_id, 'type': 'forget', 'phone': self.login_name,'check_code': image_code})

        self.assertEqual(send_sms_code_api.get_code(),0)
        time.sleep(1)
        sms_code = MysqlGet(mobile=self.login_name).get_sms_code()

        reset_password_api = ResetPasswordApi(self.login_name)
        response = reset_password_api.get({'phone': self.login_name,'code': sms_code,'new_password':self.new_password,
                 'confirm_password':self.new_password})

        self.assertEqual(reset_password_api.get_code(),0)
        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity_obj['login_name'],self.login_name)
        self.assertIsNotNone(identity_obj['user_sign'])
        self.assertEqual(identity_obj['identity'],identity_obj['user_sign'])

        login_api = LoginApi()
        response = login_api.login(login_name=self.login_name,password=self.new_password)
        self.assertEqual(login_api.get_code(),0)
        self.assertIsNotNone(response)

        login_api = LoginApi()
        login_api.login(login_name=self.login_name,only_get_identity=False)
        self.assertEqual(login_api.get_code(), 422110)
        self.assertEqual(login_api.get_response_message(),u'密码错误')


    def tearDown(self,*args):
        super(TestResetPasswordApi,self).tearDown()
        MysqlFix(user_id=MysqlGet(mobile=self.login_name).get_user_id()).fix_user_password()



