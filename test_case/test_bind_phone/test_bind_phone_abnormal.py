# -*- coding:utf-8 -*-
from api.bind_phone_api import BindPhoneApi
from api.send_sms_code_api import SendSmsCodeApi
from api.image_code_api import ImageCodeApi
from base.base_case import BaseCase
from utilities.mysql_helper import MysqlOperation
from utilities.redis_helper import Redis
import settings,random
from utilities.teardown import TearDown
import unittest


class TestBindPhoneApi(BaseCase):
    """
    绑定手机号
    """
    user_name = settings.YULE_TEST_USER_LOGIN_NAME
    bind_mobile = '15120172027'
    user_id = settings.YULE_TEST_USER_ID

    def setUp(self,*args):
        super(TestBindPhoneApi,self).setUp(user_id=self.user_id)
        TearDown().bind_phone_teardown(user_id=self.user_id, login_name=self.user_name)

    def test_bind_phone_image_code_is_null(self):
        """
        测试请求接口图形验证码为空
        :return:
        """
        bind_phone_api = BindPhoneApi(self.user_name)
        bind_phone_api.get({'phone': self.bind_mobile, 'code': 1234,'check_code':None})
        self.assertEqual(bind_phone_api.get_code(),422126)
        self.assertEqual(bind_phone_api.get_response_message(),u'图形验证码不能为空')

    def test_bind_phone_sms_code_is_null(self):
        """
        测试请求接口短信验证码为空
        :return:
        """
        bind_phone_api = BindPhoneApi(self.user_name)
        bind_phone_api.get({'phone': self.bind_mobile, 'code': None,'check_code':1234})
        self.assertEqual(bind_phone_api.get_code(),400102)
        self.assertEqual(bind_phone_api.get_response_message(),u'验证码为空')

    def test_bind_phone_image_code_is_error(self):
        """
        测试请求接口图形验证码错误
        :return:
        """
        send_image_code_api = ImageCodeApi()
        send_image_code_api.get({'device_id': settings.DEVICE_ID})
        image_code = Redis().get_image_captcha(settings.DEVICE_ID)
        num = random.randint(1111,9999)
        phone = '1580101' + str(num)
        send_sms_code_api = SendSmsCodeApi()
        send_sms_code_api.get({'device_id': settings.DEVICE_ID, 'type': 'bind', 'phone': phone,
                'check_code': image_code})

        self.assertEqual(send_sms_code_api.get_code(), 0)

        sms_code = MysqlOperation(mobile=phone).get_sms_code()

        bind_phone_api = BindPhoneApi(self.user_name)
        bind_phone_api.get({'phone': phone, 'code': sms_code,'check_code':1234})
        self.assertEqual(bind_phone_api.get_code(),422107)
        self.assertEqual(bind_phone_api.get_response_message(),u'验证码错误,请重新输入')

    def test_bind_phone_sms_code_error(self):
        """
        测试请求接口短信验证码错误
        :return:
        """
        send_image_code_api = ImageCodeApi()
        send_image_code_api.get({'device_id': settings.DEVICE_ID})
        image_code = Redis().get_image_captcha(settings.DEVICE_ID)
        num = random.randint(1111, 9999)
        phone = '1580202' + str(num)
        send_sms_code_api = SendSmsCodeApi()
        send_sms_code_api.get({'device_id': settings.DEVICE_ID, 'type': 'bind', 'phone': phone,'check_code': image_code})

        self.assertEqual(send_sms_code_api.get_code(), 0)

        bind_phone_api = BindPhoneApi(self.user_name)
        bind_phone_api.get({'phone': phone, 'code': '123u', 'check_code': image_code})
        self.assertEqual(bind_phone_api.get_code(), 400104)
        self.assertEqual(bind_phone_api.get_response_message(), u'验证码错误，请重新获取短信验证码')

    def test_bind_phone_sms_code_error_do_not_send_sms_code(self):
        """
        测试请求接口没有获取短信验证码
        :return:
        """
        send_image_code_api = ImageCodeApi()
        send_image_code_api.post({'device_id': settings.DEVICE_ID})

        image_code = Redis().get_image_captcha(settings.DEVICE_ID)
        bind_phone_api = BindPhoneApi(self.user_name)
        bind_phone_api.get({'phone': self.bind_mobile, 'code': 1234,'check_code':image_code})
        self.assertEqual(bind_phone_api.get_code(),400103)
        self.assertEqual(bind_phone_api.get_response_message(),u'请获取手机短信验证码')

    def test_bind_phone_failed_five_times(self):
        """
        测试绑定手机号当天只允许失败5次
        :return:
        """
        phone =None
        num = 1
        flag = True
        image_code = None
        while flag:
            send_image_code_api = ImageCodeApi()
            send_image_code_api.get({'device_id': settings.DEVICE_ID})
            image_code = Redis().get_image_captcha(settings.DEVICE_ID)
            phone = '133' + str(random.randint(11111111, 99999999))
            send_sms_code_api = SendSmsCodeApi()
            send_sms_code_api.get({'device_id': settings.DEVICE_ID, 'type': 'bind', 'phone': phone,'check_code': image_code})
            if send_sms_code_api.get_code() in [400126,400136]:
                continue
            else:
                bind_phone_api = BindPhoneApi(self.user_name)
                bind_phone_api.get({'phone': phone, 'code': 1234, 'check_code': image_code})
                self.assertEqual(bind_phone_api.get_code(), 400104)
                self.assertEqual(bind_phone_api.get_response_message(), u'验证码错误，请重新获取短信验证码')
                num+=1
                if num == 6:
                    flag = False

        flag = True
        while flag:
            send_image_code_api = ImageCodeApi()
            send_image_code_api.get({'device_id': settings.DEVICE_ID})
            phone = '130' + str(random.randint(11111111, 99999999))
            image_code = Redis().get_image_captcha(settings.DEVICE_ID)
            send_sms_code_api = SendSmsCodeApi()
            send_sms_code_api.get({'device_id': settings.DEVICE_ID, 'type': 'bind', 'phone': phone,'check_code': image_code})
            if send_sms_code_api.get_code() in [400126,400136]:
                continue
            else:
                self.assertEqual(send_sms_code_api.get_code(), 0)
                flag=False

        bind_phone_api = BindPhoneApi(self.user_name)
        bind_phone_api.get({'phone': phone, 'code': 1234,'check_code':image_code})
        self.assertEqual(bind_phone_api.get_code(),400133)
        self.assertEqual(bind_phone_api.get_response_message(),u'您今日操作过多，请明天再试')

    def tearDown(self,*args):
        super(TestBindPhoneApi,self).tearDown(user_id=self.user_id)
        TearDown().bind_phone_teardown(user_id=self.user_id,login_name=self.user_name)