# -*- coding:utf-8 -*-
from api.bind_phone_api import BindPhoneApi
from api.send_sms_code_api import SendSmsCodeApi
from api.image_code_api import ImageCodeApi
from base.base_case import BaseCase
from utilities.mysql_helper import MysqlOperation
from utilities.redis_helper import Redis
import settings,json,random
from utilities.teardown import TearDown

class TestBindPhoneApi(BaseCase):
    """
    绑定手机号
    """
    user_name = '13877776666'
    bind_mobile = '1512017' + str(random.randint(1234,4321))
    bind_mobile_upper = '1512019' + str(random.randint(1234,4321))
    user_id = '22013852'

    def setUp(self,*args):
        super(TestBindPhoneApi,self).setUp(user_id=self.user_id)
        TearDown().bind_phone_teardown(user_id=self.user_id,login_name=self.user_name)

    def test_bind_phone_success(self):
        """
        测试绑定手机号成功
        :return:
        """
        send_image_code_api = ImageCodeApi()
        send_image_code_api.get({'device_id': settings.DEVICE_ID})
        image_code = Redis().get_image_captcha(settings.DEVICE_ID)

        send_sms_code_api = SendSmsCodeApi()
        send_sms_code_api.get({'device_id': settings.DEVICE_ID, 'type': 'bind', 'phone': self.bind_mobile,
                'check_code': image_code})
        self.assertEqual(send_sms_code_api.get_code(),0)
        sms_code = MysqlOperation(mobile=self.bind_mobile).get_sms_code()

        bind_phone_api = BindPhoneApi(self.user_name)
        response = bind_phone_api.get({'phone': self.bind_mobile, 'code': sms_code,'check_code':image_code})

        self.assertEqual(bind_phone_api.get_code(),0)
        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(self.bind_mobile,identity_obj['mobilephone'])
        self.assertEqual(self.bind_mobile,identity_obj['login_name'])

    def test_bind_phone_success_code_upper(self):
        """
        测试绑定手机号成功验证码大写
        :return:
        """
        send_image_code_api = ImageCodeApi()
        send_image_code_api.get({'device_id': settings.DEVICE_ID})
        image_code = Redis().get_image_captcha(settings.DEVICE_ID)

        send_sms_code_api = SendSmsCodeApi()
        send_sms_code_api.get({'device_id': settings.DEVICE_ID, 'type': 'bind', 'phone': self.bind_mobile_upper,
                'check_code': image_code})
        self.assertEqual(send_sms_code_api.get_code(),0)
        sms_code = MysqlOperation(mobile=self.bind_mobile_upper).get_sms_code()
        sms_code_upper = str(sms_code).upper()

        bind_phone_api = BindPhoneApi(self.user_name)
        response = bind_phone_api.get({'phone': self.bind_mobile_upper, 'code': sms_code_upper,'check_code':image_code})

        self.assertEqual(bind_phone_api.get_code(),0)
        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(self.bind_mobile_upper,identity_obj['mobilephone'])
        self.assertEqual(self.bind_mobile_upper,identity_obj['login_name'])


    def tearDown(self,*args):
        super(TestBindPhoneApi,self).tearDown(user_id=self.user_id)
        TearDown().bind_phone_teardown(user_id=self.user_id, login_name=self.user_name,mobile_phone=self.user_name,phone_confirm=1)
