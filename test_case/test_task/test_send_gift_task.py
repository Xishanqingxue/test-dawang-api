# -*- coding:utf-8 -*-
from api.send_gift_api import SendGiftApi
from base.base_case import BaseCase
from utilities.mysql_helper import MysqlOperation
from api.task_api import TaskListApi,TaskNoticeApi,GetTaskRewardApi
from utilities.redis_helper import RedisHold,Redis
import settings,time,json

class TestSendGiftTaskApi(BaseCase):
    """
    送礼物任务/领取奖励
    """
    user_name = '13877776666'
    user_id = '22013852'
    room_id = settings.YULE_TEST_ROOM
    anchor_id = settings.YULE_TEST_ANCHOR_ID
    count = 1
    max_count = 20
    time_sleep = 0.3


    def test_bind_phone_success(self):
        """
        测试完成送礼物任务
        :return:
        """
        task_list_api  = TaskListApi(self.user_name)
        response = task_list_api.get()
        self.assertEqual(task_list_api.get_code(),0)
        task_list = json.loads(response.content)['result']['task_list']
        for x in task_list:
            if x['task_name'] == u'送礼':
                self.assertIsNone(x['user_task_obj'])

        task_notice_api = TaskNoticeApi(self.user_name)
        response = task_notice_api.get()
        self.assertEqual(task_notice_api.get_code(),0)


        while self.count < self.max_count:
            mysql_operation = MysqlOperation(user_id=self.user_id)
            mysql_operation.fix_user_account(gold_num=1000)
            RedisHold().clean_redis_user_detail(self.user_id)
            time.sleep(self.time_sleep)
            send_gift_api = SendGiftApi(self.user_name)
            send_gift_api.get({'room_id': self.room_id, 'gift_id': 67, 'gift_count': 1,'currency': 'gold'})
            if send_gift_api.get_code() == 100032:
                time.sleep(self.time_sleep)
                self.count += 1
            else:
                self.assertEqual(send_gift_api.get_code(), 0)
                break
        self.assertLess(self.count, self.max_count)

        while self.count < self.max_count:
            task_list_api = TaskListApi(self.user_name)
            response = task_list_api.get()
            self.assertEqual(task_list_api.get_code(), 0)
            task_list = json.loads(response.content)['result']['task_list']
            if task_list[3]['user_task_obj'] is not None:
                self.assertEqual(task_list[3]['user_task_obj']['user_id'],(self.user_id))
                self.assertEqual(task_list[3]['user_task_obj']['task_behavior'],u'send_gift')
                self.assertEqual(task_list[3]['user_task_obj']['num'],1)
                self.assertEqual(task_list[3]['user_task_obj']['status'],2)
                break
            else:
                self.count+=1
                time.sleep(self.time_sleep)
        self.assertLess(self.count,self.max_count)

        task_notice_api = TaskNoticeApi(self.user_name)
        response = task_notice_api.get()
        self.assertEqual(task_notice_api.get_code(),0)

        get_task_reward_api = GetTaskRewardApi(self.user_name)
        response = get_task_reward_api.get({'behavior':'send_gift'})
        self.assertEqual(get_task_reward_api.get_code(),0)
        self.assertEqual(json.loads(response.content)['result']['task_rewards']['exp'],500)

        task_list = json.loads(response.content)['result']['task_list']
        self.assertEqual(task_list[3]['user_task_obj']['status'],3)

        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity_obj['user_experience'],1500)

    def tearDown(self,*args):
        super(TestSendGiftTaskApi,self).tearDown(user_id=self.user_id,anchor_id=self.anchor_id)
        MysqlOperation(user_id=self.user_id).clean_user_task()
        Redis().clean_user_task(self.user_id)
        mysql_operation = MysqlOperation(user_id=self.user_id, anchor_id=self.anchor_id)
        mysql_operation.clean_send_gift()
        RedisHold().clean_redis_room_detail(self.room_id, self.anchor_id)
