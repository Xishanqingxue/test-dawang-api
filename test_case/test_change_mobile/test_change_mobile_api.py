# -*- coding:utf-8 -*-
from api.bind_phone_api import BindPhoneApi
from api.image_code_api import ImageCodeApi
from api.send_sms_code_api import LoginSendSmsCodeApi
from base.base_case import BaseCase
from utilities.mysql_helper import MysqlOperation
from utilities.redis_helper import Redis
import settings,time,random,json
from utilities.teardown import TearDown


class TestChangeMobileApi(BaseCase):
    """
    修改手机号
    """
    login_name = '18700008888'
    new_mobile = '1310123' + str(random.randint(1111,9999))
    device_id = settings.DEVICE_ID


    def test_change_mobile_success(self):
        """
        测试修改绑定手机号成功
        :return:
        """
        ImageCodeApi().get({'device_id':self.device_id})
        image_code = Redis().get_image_captcha(self.device_id)

        send_sms_code_api = LoginSendSmsCodeApi(self.login_name)
        send_sms_code_api.get( {'type': 'bind', 'phone': self.new_mobile,'check_code': image_code})

        self.assertEqual(send_sms_code_api.get_code(),0)
        time.sleep(1)
        sms_code = MysqlOperation(mobile=self.new_mobile).get_sms_code()
        change_mobile_api = BindPhoneApi(self.login_name)
        response = change_mobile_api.get({'phone':self.new_mobile,'code':sms_code,'check_code':image_code})

        self.assertEqual(change_mobile_api.get_code(),0)
        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity_obj['login_name'],self.new_mobile)
        self.assertEqual(identity_obj['mobilephone'],self.new_mobile)

    def tearDown(self,*args):
        super(TestChangeMobileApi,self).tearDown()
        TearDown().change_mobile_teardown(new_mobile=self.new_mobile,login_name=self.login_name,mobile_phone=self.login_name)