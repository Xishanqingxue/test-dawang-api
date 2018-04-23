# -*- coding:utf-8 -*-
from api.bind_phone_api import BindPhoneApi
from api.send_sms_code_api import SendSmsCodeApi
from api.image_code_api import ImageCodeApi
from base.base_case import BaseCase
from utilities.mysql_helper import MysqlOperation
from api.task_api import TaskListApi,TaskNoticeApi,GetTaskRewardApi
from utilities.redis_helper import RedisHold,Redis
import settings,time,json,random

class TestBindMobileTaskApi(BaseCase):
    """
    绑定手机号任务/领取奖励
    """
    user_name = '13877776666'
    bind_mobile = '1512012' + str(random.randint(1234,4321))
    user_id = '22013852'
    count = 1
    max_count = 20
    time_sleep = 0.3


    def test_bind_phone_success(self):
        """
        测试完成绑定手机号任务
        :return:
        """
        task_list_api  = TaskListApi(self.user_name)
        response = task_list_api.get()
        self.assertEqual(task_list_api.get_code(),0)
        task_list = json.loads(response.content)['result']['task_list']
        for x in task_list:
            if x['task_name'] == u'绑定手机':
                self.assertIsNone(x['user_task_obj'])

        task_notice_api = TaskNoticeApi(self.user_name)
        response = task_notice_api.get()
        self.assertEqual(task_notice_api.get_code(),0)

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
        while self.count < self.max_count:
            task_list_api = TaskListApi(self.bind_mobile)
            response = task_list_api.get()
            self.assertEqual(task_list_api.get_code(), 0)
            task_list = json.loads(response.content)['result']['task_list']
            if task_list[0]['user_task_obj'] is not None:
                self.assertEqual(task_list[0]['user_task_obj']['user_id'],(self.user_id))
                self.assertEqual(task_list[0]['user_task_obj']['task_behavior'],u'bind_mobile')
                self.assertEqual(task_list[0]['user_task_obj']['num'],1)
                self.assertEqual(task_list[0]['user_task_obj']['status'],2)
                break
            else:
                self.count+=1
                time.sleep(self.time_sleep)
        self.assertLess(self.count,self.max_count)

        task_notice_api = TaskNoticeApi(self.bind_mobile)
        task_notice_api.get()
        self.assertEqual(task_notice_api.get_code(),0)

        get_task_reward_api = GetTaskRewardApi(self.bind_mobile)
        response = get_task_reward_api.get({'behavior':'bind_mobile'})
        self.assertEqual(get_task_reward_api.get_code(),0)
        self.assertEqual(json.loads(response.content)['result']['task_rewards']['diamond'],5000)

        task_list = json.loads(response.content)['result']['task_list']
        self.assertEqual(task_list[0]['user_task_obj']['status'],3)

        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity_obj['diamond'],u'5000')

    def tearDown(self,*args):
        super(TestBindMobileTaskApi,self).tearDown(user_id=self.user_id)
        Redis().clean_check_mobile_code(self.user_id)
        MysqlOperation(user_id=self.user_id).fix_user_bind_mobile(login_name=self.user_name,mobile_phone=self.user_name,phone_confirm=1).clean_user_task()
        Redis().clean_user_task(self.user_id)