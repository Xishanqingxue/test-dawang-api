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
    mobile = '1302222' + str(random.randint(1111, 9999))
    password = settings.PUBLIC_PASSWORD
    nickname = 'wulala6'

    def test_b_register_nickname_null(self):
        """
        测试请求注册接口昵称为空
        :return:
        """
        ImageCodeApi().get({'device_id': self.device_id})
        image_code = Redis().get_image_captcha(self.device_id)

        SendSmsCodeApi().get({'device_id': self.device_id, 'type': 'register', 'phone': self.mobile,
                              'check_code': image_code})
        sms_code = MysqlGet(mobile=self.mobile).get_sms_code()

        register_api = RegisterApi()
        register_api.get({'login_name': self.mobile, 'code': sms_code, 'password': self.password,'nickname': None})

        self.assertEqual(register_api.get_code(), 422103)
        self.assertEqual(register_api.get_response_message(),u'昵称不能为空')

    def test_c_register_password_null(self):
        """
        测试请求注册接口密码为空
        :return:
        """
        ImageCodeApi().get({'device_id': self.device_id})
        image_code = Redis().get_image_captcha(self.device_id)

        SendSmsCodeApi().get({'device_id': self.device_id, 'type': 'register', 'phone': self.mobile,
                              'check_code': image_code})
        sms_code = MysqlGet(mobile=self.mobile).get_sms_code()

        register_api = RegisterApi()
        register_api.get({'login_name': self.mobile, 'code': sms_code, 'password': None,'nickname': self.nickname})

        self.assertEqual(register_api.get_code(), 422102)
        self.assertEqual(register_api.get_response_message(),u'密码不能为空')

    def test_d_register_code_null(self):
        """
        测试请求注册接口手机验证码为空
        :return:
        """
        register_api = RegisterApi()
        register_api.get({'login_name': self.mobile, 'code': None, 'password': self.password,'nickname': self.nickname})

        self.assertEqual(register_api.get_code(), 422104)
        self.assertEqual(register_api.get_response_message(),u'手机验证码不能为空')

    def test_e_register_sms_code_error(self):
        """
        测试请求注册接口手机验证码填写错误
        :return:
        """
        ImageCodeApi().get({'device_id': self.device_id})
        image_code = Redis().get_image_captcha(self.device_id)

        SendSmsCodeApi().get({'device_id': self.device_id, 'type': 'register', 'phone': self.mobile,
                              'check_code': image_code})

        register_api = RegisterApi()
        register_api.get({'login_name': self.mobile, 'code': '6666', 'password': self.password,
                                     'device_id': self.device_id, 'nickname': self.nickname})

        self.assertEqual(register_api.get_code(), 400104)
        self.assertEqual(register_api.get_response_message(),u'验证码错误，请重新获取短信验证码')

    def test_f_register_login_name_null(self):
        """
        测试请求注册接口登录名为空
        :return:
        """
        ImageCodeApi().get({'device_id': self.device_id})
        image_code = Redis().get_image_captcha(self.device_id)

        SendSmsCodeApi().get({'device_id': self.device_id, 'type': 'register', 'phone': self.mobile,
                              'check_code': image_code})
        sms_code = MysqlGet(mobile=self.mobile).get_sms_code()

        register_api = RegisterApi()
        register_api.get({'login_name': None, 'code': sms_code, 'password': self.password,
                          'device_id': self.device_id, 'nickname': self.nickname})

        self.assertEqual(register_api.get_code(), 422101)
        self.assertEqual(register_api.get_response_message(), u'登录账号名不能为空')

    def test_g_register_nickname_exits(self):
        """
        测试请求注册接口填写已存在昵称
        :return:
        """
        ImageCodeApi().get({'device_id': self.device_id})
        image_code = Redis().get_image_captcha(self.device_id)

        SendSmsCodeApi().get({'device_id': self.device_id, 'type': 'register', 'phone': self.mobile,
                              'check_code': image_code})
        sms_code = MysqlGet(mobile=self.mobile).get_sms_code()

        register_api = RegisterApi()
        register_api.get({'login_name': self.mobile, 'code': sms_code, 'password': self.password, 'nickname': '123456'})

        self.assertEqual(register_api.get_code(), 422106)
        self.assertEqual(register_api.get_response_message(), u'昵称已存在请替换')

    def test_h_register_nickname_wrongful(self):
        """
        测试请求注册接口填写不合法昵称
        :return:
        """
        ImageCodeApi().get({'device_id': self.device_id})
        image_code = Redis().get_image_captcha(self.device_id)

        SendSmsCodeApi().get({'device_id': self.device_id, 'type': 'register', 'phone': self.mobile,
                              'check_code': image_code})
        sms_code = MysqlGet(mobile=self.mobile).get_sms_code()

        register_api = RegisterApi()
        register_api.get({'login_name': self.mobile, 'code': sms_code, 'password': self.password,
                          'device_id': self.device_id, 'nickname': 'wx_abcd'})

        self.assertEqual(register_api.get_code(), 801061)
        self.assertEqual(register_api.get_response_message(), u'用户昵称不合法，快去换一个吧')

    def test_i_register_nickname_sensitivity(self):
        """
        测试请求注册接口昵称中包含敏感词
        :return:
        """
        ImageCodeApi().get({'device_id': self.device_id})
        image_code = Redis().get_image_captcha(self.device_id)

        SendSmsCodeApi().get({'device_id': self.device_id, 'type': 'register', 'phone': self.mobile,
                              'check_code': image_code})
        sms_code = MysqlGet(mobile=self.mobile).get_sms_code()

        register_api = RegisterApi()
        register_api.get({'login_name': self.mobile, 'code': sms_code, 'password': self.password,
                          'device_id': self.device_id, 'nickname': '习近平胡锦涛'})

        self.assertEqual(register_api.get_code(), 422105)
        self.assertEqual(register_api.get_response_message(), u'昵称包含敏感词，请替换')

    def test_j_register_nickname_too_long(self):
        """
        测试请求注册接口昵称长度超过八位
        :return:
        """
        ImageCodeApi().get({'device_id': self.device_id})
        image_code = Redis().get_image_captcha(self.device_id)

        SendSmsCodeApi().get({'device_id': self.device_id, 'type': 'register', 'phone': self.mobile,
                              'check_code': image_code})
        sms_code = MysqlGet(mobile=self.mobile).get_sms_code()

        register_api = RegisterApi()
        register_api.get({'login_name': self.mobile, 'code': sms_code, 'password': self.password,
                          'device_id': self.device_id, 'nickname': u'我有八个字符串呀呀'})

        self.assertEqual(register_api.get_code(), 400131)
        self.assertEqual(register_api.get_response_message(), u'昵称长度必须为4-8位')

    def test_k_register_nickname_too_short(self):
        """
        测试请求注册接口昵称长度不足4位
        :return:
        """
        ImageCodeApi().get({'device_id': self.device_id})
        image_code = Redis().get_image_captcha(self.device_id)

        SendSmsCodeApi().get({'device_id': self.device_id, 'type': 'register', 'phone': self.mobile,
                              'check_code': image_code})
        sms_code = MysqlGet(mobile=self.mobile).get_sms_code()

        register_api = RegisterApi()
        register_api.get({'login_name': self.mobile, 'code': sms_code, 'password': self.password,
                          'device_id': self.device_id, 'nickname': u'三个字'})

        self.assertEqual(register_api.get_code(), 400131)
        self.assertEqual(register_api.get_response_message(), u'昵称长度必须为4-8位')

    def tearDown(self,*args):
        super(TestRegisterApi, self).tearDown()
        try:
            TearDown().register_teardown(self.mobile)
        except:
            pass