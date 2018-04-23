# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.image_code_api import ImageCodeApi
from api.send_sms_code_api import SendSmsCodeApi
from api.register_api import RegisterApi
from utilities.redis_helper import Redis
from utilities.mysql_helper import MysqlGet
from utilities.teardown import TearDown
import random, json,settings


class TestRegisterApi(BaseCase):
    """
    注册
    """
    device_id = settings.DEVICE_ID
    mobile = '1301111' + str(random.randint(1111, 9999))
    password = settings.PUBLIC_PASSWORD
    nickname = 'lil' + str(random.randint(1111, 9999))

    def test_register_success(self):
        """
        测试正常请求注册接口
        """
        ImageCodeApi().get({'device_id': self.device_id})
        image_code = Redis().get_image_captcha(self.device_id)
        send_sms_code_api = SendSmsCodeApi()
        send_sms_code_api.get({'device_id': self.device_id, 'type': 'register', 'phone': self.mobile,
                              'check_code': image_code})
        self.assertEqual(send_sms_code_api.get_code(),0)
        sms_code = MysqlGet(mobile=self.mobile).get_sms_code()

        register_api = RegisterApi()
        response = register_api.get({'login_name': self.mobile, 'code': sms_code, 'password': self.password,
                                     'device_id': self.device_id, 'nickname': self.nickname})

        self.assertEqual(register_api.get_code(), 0)
        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity_obj['nickname'], self.nickname)
        for x in [identity_obj['login_name'], identity_obj['mobilephone']]:
            self.assertEqual(x, self.mobile)

        for x in [identity_obj['gold'], identity_obj['diamond'], identity_obj['ticket']]:
            self.assertEqual(x, 0)

        self.assertEqual(identity_obj['user_rank'], 1)
        self.assertEqual(identity_obj['user_experience'], 0)
        self.assertEqual(identity_obj['current_rank_user_need_total_experience'], 50000)
        for x in [identity_obj['anchor_rank'], identity_obj['anchor_experience']]:
            self.assertEqual(x, 0)

        self.assertEqual(identity_obj['current_rank_anchor_need_total_experience'], 1)
        self.assertEqual(identity_obj['sun_num'], 5)
        self.assertEqual(identity_obj['follow_num'], 0)

        for x in [identity_obj['introduction'], identity_obj['email'], identity_obj['small_head_url']]:
            self.assertEqual(x, u'')

        user_guard_obj = identity_obj['user_guard_obj']
        self.assertEqual(user_guard_obj['user_id'], u'')
        self.assertEqual(user_guard_obj['expire_time'], u'')
        self.assertEqual(user_guard_obj['guard_rank'], 0)

        intimacy_obj = identity_obj['intimacy_obj']
        for x in [intimacy_obj['intimacy_experience'], intimacy_obj['intimacy_rank'],
                  intimacy_obj['intimacy_next_experience']]:
            self.assertEqual(x, 0)
        self.assertIsNone(intimacy_obj['intimacy_level_obj'])

        self.assertIsNone(identity_obj['user_signin_obj'])
        self.assertEqual(identity_obj['user_type'], 1)
        self.assertIsNotNone(identity_obj['identity'])
        self.assertEqual(identity_obj['identity'], identity_obj['user_sign'])

        self.assertIsNone(identity_obj['blacker_type'])
        for x in [identity_obj['guard_top_num'], identity_obj['has_followed']]:
            self.assertEqual(x, 0)
        self.assertEqual(identity_obj['sun_resumed_time'], 180)
        self.assertEqual(identity_obj['sun_max_num'], 50)

        self.assertEqual(identity_obj['chat_resumed_time'], 1)
        self.assertEqual(identity_obj['shout_resumed_time'], 5)

        for x in [identity_obj['today_is_sign'], identity_obj['signin_max_num'], identity_obj['noble_rank'],
                  identity_obj['noble_rest_time_int']]:
            self.assertEqual(x, 0)

        for x in [identity_obj['signin_date'], identity_obj['noble_expiretime'], identity_obj['noble_rest_time_str']]:
            self.assertEqual(x, u'')
        self.assertEqual(identity_obj['if_receive_push'], 1)

        self.assertEqual(identity_obj['play_area'], -1)
        for x in [identity_obj['is_anchor'], identity_obj['sns_id'], identity_obj['sns_from'],
                  identity_obj['has_plat_signin'], identity_obj['plat_signin_days']]:
            self.assertEqual(x, 0)

        self.assertEqual(identity_obj['left_rename_num'],1)
        self.assertEqual(identity_obj['status'],1)
        self.assertEqual(len(identity_obj['user_package']),0)


    def tearDown(self,*args):
        super(TestRegisterApi, self).tearDown()
        TearDown().register_teardown(self.mobile)
