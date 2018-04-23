# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.guard_api import BuyGuardApi
from api.anchor_group_api import AddAnchorToGroupApi,OpenAnchorGroupApi
from api.consumption_api import ConsumptionApi
from utilities.redis_helper import RedisHold,Redis
from utilities.mysql_helper import MysqlOperation
from settings import YULE_TEST_ANCHOR_ID as anchor_id,YULE_TEST_ROOM as room_id
import json, time
from utilities.teardown import TearDown
from settings import YULE_TEST_USER_LOGIN_NAME,YULE_TEST_USER_ID

class TestAddAnchorToGroupApi(BaseCase):
    """
    主播团日志
    """
    user_login_name = YULE_TEST_USER_LOGIN_NAME
    user_id = YULE_TEST_USER_ID
    user_rank = 12
    user_experience_all = 3000000
    count = 1
    max_count = 20
    time_sleep = 0.2

    def setUp(self,*args):
        super(TestAddAnchorToGroupApi,self).setUp(user_id=self.user_id,anchor_id=anchor_id)
        TearDown().guard_teardown(login_name=self.user_login_name,user_id=self.user_id,anchor_id=anchor_id)
        user_id = self.user_id
        mysql_operation = MysqlOperation(user_id=user_id)
        mysql_operation.clean_user_anchor_group()
        Redis().clean_anchor_group(user_id,anchor_id)
        Redis().clean_user_buy_guard(user_id, anchor_id)

    def test_add_anchor_to_group_consumption(self):
        """
        测试主播团日志
        :return:
        """
        user_id = self.user_id
        while self.count < self.max_count:
            mysql_operation = MysqlOperation(user_id=user_id)
            mysql_operation.fix_user_rank_and_experience(user_rank=self.user_rank, experience_all=self.user_experience_all)
            mysql_operation.fix_user_account(gold_num=100000)
            RedisHold().clean_redis_user_detail(self.user_id)
            time.sleep(self.time_sleep)

            open_anchor_group_api = OpenAnchorGroupApi(self.user_login_name)
            open_anchor_group_api.get()
            if open_anchor_group_api.get_code() == 200502:
                time.sleep(self.time_sleep)
                self.count+=1
            else:
                self.assertEqual(open_anchor_group_api.get_code(), 0)
                break
        self.assertLess(self.count,self.max_count)

        consumption_api = ConsumptionApi(self.user_login_name)
        response = consumption_api.get()
        consume_list = json.loads(response.content)['result']['consume_list']
        self.assertEqual(consumption_api.get_code(), 0)
        self.assertEqual(len(consume_list), 1)
        self.assertEqual(consume_list[0]['type'],u'7')
        self.assertEqual(consume_list[0]['gold'], 100000)
        self.assertEqual(consume_list[0]['corresponding_name'], u'主播团')
        self.assertEqual(consume_list[0]['consumption_type'], u'100000金币')
        self.assertEqual(consume_list[0]['behavior_desc'], u'开通主播团')
        while self.count < self.max_count:
            mysql_operation = MysqlOperation(user_id=user_id)
            mysql_operation.fix_user_rank_and_experience(user_rank=self.user_rank, experience_all=self.user_experience_all)
            mysql_operation.fix_user_account(gold_num=638000)
            RedisHold().clean_redis_user_detail(self.user_id)
            time.sleep(self.time_sleep)
            buy_guard_api = BuyGuardApi(self.user_login_name)
            guard_response = buy_guard_api.get({'room_id': room_id, 'guard_id': '1','currency':'gold'})
            if buy_guard_api.get_code() == 100032:
                time.sleep(self.time_sleep)

                self.count+=1
            else:
                self.assertEqual(buy_guard_api.get_code(), 0)
                self.assertEqual(json.loads(guard_response.content)['result']['identity_obj']['user_guard_obj']['guard_rank'], 1)
                break
        self.assertLess(self.count,self.max_count)

        add_anchor_to_group_api = AddAnchorToGroupApi(self.user_login_name)
        response = add_anchor_to_group_api.get({'anchor_id': anchor_id, 'position': 1,'grab_flag': 0,'change_flag': 0})
        self.assertEqual(add_anchor_to_group_api.get_code(), 0)
        self.assertEqual(add_anchor_to_group_api.get_response_message(), u'操作成功')

        anchor_group_anchor_obj = json.loads(response.content)['result']['anchor_group_list'][0]['anchor_group_anchor_obj']
        self.assertEqual(anchor_group_anchor_obj['anchor_id'],int(anchor_id))
        self.assertEqual(anchor_group_anchor_obj['position'],1)
        self.assertEqual(anchor_group_anchor_obj['income_gold'],0)
        self.assertLessEqual(anchor_group_anchor_obj['left_time'],604800)
        # 消费记录
        consumption_api = ConsumptionApi(self.user_login_name)
        response = consumption_api.get()
        consume_list = json.loads(response.content)['result']['consume_list']
        self.assertEqual(consumption_api.get_code(), 0)
        self.assertEqual(consume_list[0]['gold'], 50000)
        self.assertEqual(consume_list[0]['corresponding_name'], u'纳入主播团')
        self.assertEqual(consume_list[0]['consumption_type'], u'50000金币')
        self.assertEqual(consume_list[0]['behavior_desc'], u'纳入主播团')
        self.assertEqual(consume_list[0]['user_id'],self.user_id)
        self.assertEqual(consume_list[0]['room_title'],MysqlOperation(room_id=room_id).get_room_details()['title'])

    def tearDown(self,*args):
        super(TestAddAnchorToGroupApi,self).tearDown(user_id=self.user_id,anchor_id=anchor_id)
        TearDown().guard_teardown(login_name=self.user_login_name,user_id=self.user_id,anchor_id=anchor_id)
        user_id = self.user_id
        mysql_operation = MysqlOperation(user_id=user_id)
        mysql_operation.clean_user_anchor_group()
        Redis().clean_anchor_group(user_id,anchor_id)
        Redis().clean_user_buy_guard(user_id, anchor_id)