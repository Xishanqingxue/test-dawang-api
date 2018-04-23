# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.guard_api import BuyGuardApi
from api.anchor_group_api import OpenAnchorGroupApi,AddAnchorToGroupApi,MyAnchorGroupLogsApi,MyAnchorGroupListApi
from utilities.redis_helper import Redis,RedisHold
from utilities.mysql_helper import MysqlOperation
from settings import YULE_TEST_ANCHOR_ID as anchor_id,YULE_TEST_ROOM as room_id,YULE_TEST_USER_ID
import json, time
from settings import YULE_TEST_USER_LOGIN_NAME
from utilities.teardown import TearDown

class TestAnchorGroupRobApi(BaseCase):
    """
    主播团中抢主播
    """
    user_login_name = YULE_TEST_USER_LOGIN_NAME
    user_id = YULE_TEST_USER_ID
    rob_user_login_name = '15899999999'
    rob_user_id = MysqlOperation(mobile=rob_user_login_name).get_user_id()
    user_rank = 12
    user_experience_all = 3000000
    time_sleep = 0.2

    def setUp(self,*args):
        super(TestAnchorGroupRobApi,self).setUp(user_id=[self.user_id,self.rob_user_id],anchor_id=anchor_id)
        for id in [self.user_id,self.rob_user_id]:
            TearDown().guard_teardown(user_id=id, anchor_id=anchor_id)
            mysql_operation = MysqlOperation(user_id=id)
            mysql_operation.clean_user_anchor_group()
            MysqlOperation(user_id=id).clean_user_anchor_group()
            Redis().clean_user_buy_guard(id, anchor_id)
            RedisHold().clean_redis_room_detail(room_id, anchor_id)

    def test_anchor_group_rob(self):
        """
        测试将其他主播团中主播纳入到自己的主播团
        :return:
        """
        for login_name in [self.user_login_name, self.rob_user_login_name]:
            mysql_operation = MysqlOperation(mobile=login_name)
            user_id = str(mysql_operation.get_user_id())
            mysql_operation = MysqlOperation(user_id=user_id)
            mysql_operation.fix_user_rank_and_experience(user_rank=self.user_rank, experience_all=self.user_experience_all)
            mysql_operation.fix_user_account(gold_num=51326000)
            RedisHold().clean_redis_user_detail(user_id)
            # 依次给用户开通主播团
            open_anchor_group_api = OpenAnchorGroupApi(login_name)
            open_anchor_group_api.get()
            self.assertEqual(open_anchor_group_api.get_code(), 0)
            # 用户依次购买守护
            buy_guard_api = BuyGuardApi(login_name)
            buy_guard_api.get({'room_id': room_id, 'guard_id': '2','currency':'gold'})
            self.assertEqual(buy_guard_api.get_code(), 0)
            time.sleep(self.time_sleep * 2)

        # 用户将主播纳入主播团
        add_anchor_to_group_api = AddAnchorToGroupApi(self.user_login_name)
        add_anchor_to_group_api.get({'anchor_id': anchor_id, 'position': 1,'grab_flag': 0,'change_flag': 0})
        self.assertEqual(add_anchor_to_group_api.get_code(), 0)
        time.sleep(0.5)

        # 查询主播团信息
        my_anchor_group_list_api = MyAnchorGroupListApi(self.user_login_name)
        list_response = my_anchor_group_list_api.get()
        self.assertEqual(my_anchor_group_list_api.get_code(), 0)

        anchor_group_opening_info = json.loads(list_response.content)['result']['anchor_group_opening_info']
        self.assertEqual(anchor_group_opening_info['gold_needed'],100000)
        self.assertEqual(anchor_group_opening_info['is_opened'],1)
        anchor_group_obj = json.loads(list_response.content)['result']['anchor_group_obj']
        self.assertEqual(anchor_group_obj['owend_anchor_count'],1)

        # 用户将主播抢到自己的主播团
        add_anchor_to_group_api = AddAnchorToGroupApi(self.rob_user_login_name)
        add_anchor_to_group_api.get({'anchor_id': anchor_id, 'position': 1,'grab_flag': 1,'change_flag': 0})
        self.assertEqual(add_anchor_to_group_api.get_code(), 0)
        time.sleep(0.5)


        # 查询15020170001主播团信息
        my_anchor_group_list_api = MyAnchorGroupListApi(self.rob_user_login_name)
        list_response = my_anchor_group_list_api.get()
        self.assertEqual(my_anchor_group_list_api.get_code(), 0)
        anchor_group_opening_info = json.loads(list_response.content)['result']['anchor_group_opening_info']
        self.assertEqual(anchor_group_opening_info['gold_needed'],100000)
        self.assertEqual(anchor_group_opening_info['is_opened'],1)
        anchor_group_obj = json.loads(list_response.content)['result']['anchor_group_obj']
        self.assertEqual(anchor_group_obj['owend_anchor_count'],1)


        # 查询13501077762主播团信息
        my_anchor_group_list_api = MyAnchorGroupListApi(self.user_login_name)
        list_response = my_anchor_group_list_api.get()
        self.assertEqual(my_anchor_group_list_api.get_code(), 0)
        anchor_group_obj = json.loads(list_response.content)['result']['anchor_group_obj']
        self.assertEqual(anchor_group_obj['owend_anchor_count'],0)
        time.sleep(2)

        # 查询13501077762主播团日志
        my_anchor_group_logs_api = MyAnchorGroupLogsApi(self.user_login_name)
        logs_response = my_anchor_group_logs_api.get()
        anchor_group_log_list = json.loads(logs_response.content)['result']['anchor_group_log_list']
        self.assertEqual(my_anchor_group_logs_api.get_code(), 0)
        self.assertEqual(len(anchor_group_log_list), 2)
        self.assertIn(u'抢走', anchor_group_log_list[0]['content'])
        self.assertIn(u'被纳入主播团', anchor_group_log_list[1]['content'])

        # 查询15020170001主播团日志
        my_anchor_group_logs_api = MyAnchorGroupLogsApi(self.rob_user_login_name)
        logs_response = my_anchor_group_logs_api.get()
        anchor_group_log_list = json.loads(logs_response.content)['result']['anchor_group_log_list']
        self.assertEqual(my_anchor_group_logs_api.get_code(), 0)
        self.assertEqual(len(anchor_group_log_list), 1)
        self.assertIn(u'被纳入主播团', anchor_group_log_list[0]['content'])

    def tearDown(self,*args):
        super(TestAnchorGroupRobApi,self).tearDown(user_id=[self.user_id,self.rob_user_id],anchor_id=anchor_id)
        for id in [self.user_id,self.rob_user_id]:
            TearDown().guard_teardown(user_id=id, anchor_id=anchor_id)
            mysql_operation = MysqlOperation(user_id=id)
            mysql_operation.clean_user_anchor_group()
            Redis().clean_anchor_group(id, anchor_id=anchor_id)
            MysqlOperation(user_id=id).clean_user_anchor_group()
            Redis().clean_user_buy_guard(id, anchor_id)
            RedisHold().clean_redis_room_detail(room_id, anchor_id)
