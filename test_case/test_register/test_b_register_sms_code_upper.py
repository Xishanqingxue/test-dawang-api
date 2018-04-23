# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.image_code_api import ImageCodeApi
from api.send_sms_code_api import SendSmsCodeApi
from api.register_api import RegisterApi
from utilities.redis_helper import Redis
from utilities.mysql_helper import MysqlGet
from utilities.teardown import TearDown
import settings, random


class TestRegisterApi(BaseCase):
    """
    注册
    """
    device_id = settings.DEVICE_ID
    mobile = '1303333' + str(random.randint(1111, 9999))
    password = settings.PUBLIC_PASSWORD
    nickname = 'wul'+ str(random.randint(1111, 9999))


    def test_register_sms_code_upper(self):
        """
        注册时验证码填写大写
        :return:
        """
        ImageCodeApi().get({'device_id': self.device_id})
        image_code = Redis().get_image_captcha(self.device_id)
        send_sms_code_api = SendSmsCodeApi()
        send_sms_code_api.get({'device_id': self.device_id, 'type': 'register', 'phone': self.mobile,
                              'check_code': image_code})
        self.assertEqual(send_sms_code_api.get_code(),0)
        sms_code = MysqlGet(mobile=self.mobile).get_sms_code()
        upper_sms_code = (str(sms_code)).upper()

        register_api = RegisterApi()
        register_api.get({'login_name': self.mobile, 'code': upper_sms_code, 'password': self.password,
                                     'device_id': self.device_id, 'nickname': self.nickname})

        self.assertEqual(register_api.get_code(), 0)

    def tearDown(self,*args):
        super(TestRegisterApi, self).tearDown()
        TearDown().register_teardown(self.mobile)
