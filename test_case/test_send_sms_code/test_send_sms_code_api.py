# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.image_code_api import ImageCodeApi
from api.send_sms_code_api import SendSmsCodeApi,LoginSendSmsCodeApi
from utilities.redis_helper import Redis
from utilities.mysql_helper import MysqlGet
import settings,random


class TestSendSmsCodeApi(BaseCase):
    """
    短信验证码
    """
    device_id = settings.DEVICE_ID
    mobile = '1300000' + str(random.randint(1111,9999))
    mobile2 = '1370000' + str(random.randint(1111, 9999))

    def test_a_send_register_sms_code_success(self):
        """
        测试发送注册短信验证码
        """
        ImageCodeApi().get({'device_id': self.device_id})
        image_code = Redis().get_image_captcha(self.device_id)

        send_sms_code_api = SendSmsCodeApi()
        send_sms_code_api.get({'device_id': self.device_id, 'type': 'register', 'phone': self.mobile,
                               'check_code': image_code})
        self.assertEqual(send_sms_code_api.get_code(), 0)
        sms_code = MysqlGet(mobile=self.mobile).get_sms_code()

        self.assertIsNotNone(sms_code)
        self.assertEqual(len(sms_code), 4)

    def test_a_send_forget_sms_code_success(self):
        """
        测试发送忘记密码短信验证码
        """
        mobile = '15877777777'
        ImageCodeApi().get({'device_id': self.device_id})
        image_code = Redis().get_image_captcha(self.device_id)

        send_sms_code_api = LoginSendSmsCodeApi(mobile)
        send_sms_code_api.get({'device_id': self.device_id, 'type': 'forget', 'phone': mobile,
                               'check_code': image_code})
        self.assertEqual(send_sms_code_api.get_code(), 0)
        sms_code = MysqlGet(mobile=mobile).get_sms_code()

        self.assertIsNotNone(sms_code)
        self.assertEqual(len(sms_code), 4)

    def test_a_send_bind_sms_code_success(self):
        """
        测试发送绑定手机号短信验证码
        """
        send_image_code_api = ImageCodeApi()
        send_image_code_api.get({'device_id': settings.DEVICE_ID})
        image_code = Redis().get_image_captcha(settings.DEVICE_ID)

        send_sms_code_api = SendSmsCodeApi()
        send_sms_code_api.get({'device_id': settings.DEVICE_ID, 'type': 'bind', 'phone': self.mobile2,
                               'check_code': image_code})
        self.assertEqual(send_sms_code_api.get_code(), 0)
        sms_code = MysqlGet(mobile=self.mobile2).get_sms_code()
        self.assertIsNotNone(sms_code)
        self.assertEqual(len(sms_code), 4)

    def test_c_send_register_sms_code_type_null(self):
        """
        测试发送短信验证码未定义类型
        :return:
        """
        send_sms_code_api = SendSmsCodeApi()
        send_sms_code_api.get({'device_id': self.device_id, 'type': None, 'phone': self.mobile,
                               'check_code': '6666'})
        self.assertEqual(send_sms_code_api.get_code(), 400111)
        self.assertEqual(send_sms_code_api.get_response_message(), u'短信类型不能为空')

    def test_d_send_register_sms_code_phone_null(self):
        """
        测试发送短信验证码手机号码为空
        """
        send_sms_code_api = SendSmsCodeApi()
        send_sms_code_api.get({'device_id': self.device_id, 'type': 'register', 'phone': None,
                               'check_code': '6666'})
        self.assertEqual(send_sms_code_api.get_code(), 400101)
        self.assertEqual(send_sms_code_api.get_response_message(), u'手机号不能为空')

    def test_e_send_register_sms_code_check_code_null(self):
        """
        测试发送短信验证码图形验证码为空
        """
        send_sms_code_api = SendSmsCodeApi()
        send_sms_code_api.get({'device_id': self.device_id, 'type': 'register', 'phone': self.mobile,
                               'check_code': None})
        self.assertEqual(send_sms_code_api.get_code(), 422126)
        self.assertEqual(send_sms_code_api.get_response_message(), u'图形验证码不能为空')

    def test_f_send_register_sms_code_check_code_error(self):
        """
        测试发送给短信验证码图形验证码输入错误
        """
        send_sms_code_api = SendSmsCodeApi()
        send_sms_code_api.get({'device_id': self.device_id, 'type': 'register', 'phone': self.mobile,
                               'check_code': '6666'})
        self.assertEqual(send_sms_code_api.get_code(), 422107)
        self.assertEqual(send_sms_code_api.get_response_message(), u'验证码错误,请重新输入')

    def test_g_send_register_sms_code_check_code_not_send(self):
        """
        测试发送短信验证码未发送图形验证码
        """
        Redis().delete_image_captcha(self.device_id)
        send_sms_code_api = SendSmsCodeApi()
        send_sms_code_api.get({'device_id': self.device_id, 'type': 'register', 'phone': self.mobile,
                               'check_code': '6666'})
        self.assertEqual(send_sms_code_api.get_code(), 422107)
        self.assertEqual(send_sms_code_api.get_response_message(), u'验证码错误,请重新输入')

    def test_h_send_register_sms_code_mobile_too_long(self):
        """
        测试发送短信验证码手机号超过11位
        """
        ImageCodeApi().get({'device_id': self.device_id})
        image_code = Redis().get_image_captcha(self.device_id)

        send_sms_code_api = SendSmsCodeApi()
        send_sms_code_api.get({'device_id': self.device_id, 'type': 'register', 'phone': self.mobile + '123123',
                               'check_code': image_code})
        self.assertEqual(send_sms_code_api.get_code(), 400126)
        self.assertEqual(send_sms_code_api.get_response_message(),u'手机号格式不合法')

    def test_i_send_register_sms_code_mobile_too_short(self):
        """
        测试发送短信验证码手机号不足11位
        """
        ImageCodeApi().get({'device_id': self.device_id})
        image_code = Redis().get_image_captcha(self.device_id)

        send_sms_code_api = SendSmsCodeApi()
        send_sms_code_api.get({'device_id': self.device_id, 'type': 'register', 'phone': '1309876',
                               'check_code': image_code})
        self.assertEqual(send_sms_code_api.get_code(), 400126)
        self.assertEqual(send_sms_code_api.get_response_message(),u'手机号格式不合法')

    def test_j_send_register_sms_code_mobile_english(self):
        """
        测试发送短信验证码手机号码中带英文
        :return:
        """
        ImageCodeApi().get({'device_id': self.device_id})
        image_code = Redis().get_image_captcha(self.device_id)

        send_sms_code_api = SendSmsCodeApi()
        send_sms_code_api.get({'device_id': self.device_id, 'type': 'register', 'phone': 'abcdefg',
                               'check_code': image_code})
        self.assertEqual(send_sms_code_api.get_code(), 400126)
        self.assertEqual(send_sms_code_api.get_response_message(),u'手机号格式不合法')

    def test_k_send_register_sms_code_mobile_exits(self):
        """
        测试用已经注册的手机号码获取注册类型短信验证码
        :return:
        """
        ImageCodeApi().get({'device_id': self.device_id})
        image_code = Redis().get_image_captcha(self.device_id)

        send_sms_code_api = SendSmsCodeApi()
        send_sms_code_api.get({'device_id': self.device_id, 'type': 'register', 'phone': '15899999999',
                               'check_code': image_code})
        self.assertEqual(send_sms_code_api.get_code(), 400113)
        self.assertEqual(send_sms_code_api.get_response_message(),u'该手机号已经被注册')
