# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.guard_api import BuyGuardApi
from api.anchor_group_api import ListCanBeAddApi,OpenAnchorGroupApi
from utilities.redis_helper import Redis,RedisHold
from utilities.mysql_helper import MysqlOperation
from settings import YULE_TEST_ANCHOR_ID as anchor_id,YULE_TEST_ROOM as room_id
import json, time
from utilities.teardown import TearDown
from settings import YULE_TEST_USER_LOGIN_NAME,YULE_TEST_USER_ID

class TestListCanBeAddApi(BaseCase):
    """
    可纳入主播团的主播列表
    """
    user_login_name = YULE_TEST_USER_LOGIN_NAME
    user_id = YULE_TEST_USER_ID
    user_rank = 12
    user_experience_all = 3000000
    count = 1
    max_count = 20
    time_sleep = 0.3


    def setUp(self,*args):
        super(TestListCanBeAddApi,self).setUp(user_id=self.user_id,anchor_id=anchor_id)
        TearDown().guard_teardown(login_name=self.user_login_name,user_id=self.user_id,anchor_id=anchor_id)
        user_id = self.user_id
        for i in [user_id, anchor_id]:
            MysqlOperation(user_id=i).clean_user_anchor_group()
        Redis().clean_user_buy_guard(user_id, anchor_id)
        Redis().clean_anchor_group(user_id,anchor_id)

    def test_bronze_get_list_can_be_add(self):
        """
        测试青铜守护可纳入主播团
        :return:
        """
        user_id = self.user_id
        while self.count < self.max_count:
            mysql_operation = MysqlOperation(user_id=user_id)
            mysql_operation.fix_user_rank_and_experience(user_rank=self.user_rank,experience_all=self.user_experience_all)
            mysql_operation.fix_user_account(gold_num=100000)
            RedisHold().clean_redis_user_detail(self.user_id)
            time.sleep(self.time_sleep)

            open_anchor_group_api = OpenAnchorGroupApi(self.user_login_name)
            open_anchor_group_api.get()
            if open_anchor_group_api.get_code() == 100032:
                time.sleep(self.time_sleep)
                self.count+=1
            else:
                self.assertEqual(open_anchor_group_api.get_code(),0)
                break
        self.assertLess(self.count,self.max_count)
        while self.count < self.max_count:
            mysql_operation = MysqlOperation(user_id=user_id)
            mysql_operation.fix_user_rank_and_experience(user_rank=self.user_rank,
                                                         experience_all=self.user_experience_all)
            mysql_operation.fix_user_account(gold_num=588000)
            RedisHold().clean_redis_user_detail(self.user_id)
            time.sleep(self.time_sleep)
            buy_guard_api = BuyGuardApi(self.user_login_name)
            guard_response = buy_guard_api.get({'room_id': room_id, 'guard_id': '1','currency':'gold'})
            if buy_guard_api.get_code() == 100032:
                time.sleep(self.time_sleep)
                self.count+=1
            else:
                self.assertEqual(buy_guard_api.get_code(),0)
                self.assertEqual(json.loads(guard_response.content)['result']['identity_obj']['user_guard_obj']['guard_rank'], 1)

                list_can_be_add_api = ListCanBeAddApi(self.user_login_name)
                response = list_can_be_add_api.get()
                self.assertEqual(list_can_be_add_api.get_code(),0)
                self.assertEqual(list_can_be_add_api.get_response_message(),u'操作成功')
                anchor_list = json.loads(response.content)['result']['anchor_list']
                self.assertEqual(len(anchor_list),1)
                self.assertEqual(anchor_list[0]['room_obj']['id'],room_id)
                break
        self.assertLess(self.count,self.max_count)

    def test_silver_get_list_can_be_add(self):
        """
        测试白银守护可纳入主播团
        :return:
        """
        user_id = self.user_id
        while self.count < self.max_count:
            mysql_operation = MysqlOperation(user_id=user_id)
            mysql_operation.fix_user_rank_and_experience(user_rank=self.user_rank,experience_all=self.user_experience_all)
            mysql_operation.fix_user_account(gold_num=100000)
            RedisHold().clean_redis_user_detail(self.user_id)
            time.sleep(self.time_sleep)

            open_anchor_group_api = OpenAnchorGroupApi(self.user_login_name)
            open_anchor_group_api.get()
            if open_anchor_group_api.get_code() == 100032:
                time.sleep(self.time_sleep)
                self.count+=1
            else:
                self.assertEqual(open_anchor_group_api.get_code(),0)
                break
        self.assertLess(self.count,self.max_count)
        while self.count < self.max_count:
            mysql_operation = MysqlOperation(user_id=user_id)
            mysql_operation.fix_user_rank_and_experience(user_rank=self.user_rank,experience_all=self.user_experience_all)
            mysql_operation.fix_user_account(gold_num=1176000)
            RedisHold().clean_redis_user_detail(self.user_id)
            time.sleep(self.time_sleep)
            buy_guard_api = BuyGuardApi(self.user_login_name)
            guard_response = buy_guard_api.get({'room_id': room_id, 'guard_id': '2','currency':'gold'})
            if buy_guard_api.get_code() == 100032:
                time.sleep(self.time_sleep)
                self.count +=1
            else:
                self.assertEqual(buy_guard_api.get_code(), 0)
                self.assertEqual(json.loads(guard_response.content)['result']['identity_obj']['user_guard_obj']['guard_rank'], 2)

                list_can_be_add_api = ListCanBeAddApi(self.user_login_name)
                response = list_can_be_add_api.get()
                self.assertEqual(list_can_be_add_api.get_code(), 0)
                self.assertEqual(list_can_be_add_api.get_response_message(), u'操作成功')
                anchor_list = json.loads(response.content)['result']['anchor_list']
                self.assertEqual(len(anchor_list), 1)
                self.assertEqual(anchor_list[0]['room_obj']['id'], room_id)
                break
        self.assertLess(self.count,self.max_count)

    def test_gold_get_list_can_be_add(self):
        """
        测试黄金守护可纳入主播团
        :return:
        """
        user_id = self.user_id
        while self.count < self.max_count:
            mysql_operation = MysqlOperation(user_id=user_id)
            mysql_operation.fix_user_rank_and_experience(user_rank=self.user_rank,experience_all=self.user_experience_all)
            mysql_operation.fix_user_account(gold_num=100000)
            RedisHold().clean_redis_user_detail(self.user_id)
            time.sleep(self.time_sleep)

            open_anchor_group_api = OpenAnchorGroupApi(self.user_login_name)
            open_anchor_group_api.get()
            if open_anchor_group_api.get_code() == 100032:
                time.sleep(self.time_sleep)
                self.count+=1
            else:
                self.assertEqual(open_anchor_group_api.get_code(),0)
                break
        self.assertLess(self.count,self.max_count)
        while self.count < self.max_count:
            mysql_operation = MysqlOperation(user_id=user_id)
            mysql_operation.fix_user_rank_and_experience(user_rank=self.user_rank,
                                                         experience_all=self.user_experience_all)
            mysql_operation.fix_user_account(gold_num=1764000)
            RedisHold().clean_redis_user_detail(self.user_id)
            time.sleep(self.time_sleep)
            buy_guard_api = BuyGuardApi(self.user_login_name)
            guard_response = buy_guard_api.get({'room_id': room_id, 'guard_id': '3','currency':'gold'})
            if buy_guard_api.get_code() == 100032:
                time.sleep(self.time_sleep)
                self.count+=1
            else:
                self.assertEqual(buy_guard_api.get_code(), 0)
                self.assertEqual(json.loads(guard_response.content)['result']['identity_obj']['user_guard_obj']['guard_rank'], 3)

                list_can_be_add_api = ListCanBeAddApi(self.user_login_name)
                response = list_can_be_add_api.get()
                self.assertEqual(list_can_be_add_api.get_code(), 0)
                self.assertEqual(list_can_be_add_api.get_response_message(), u'操作成功')
                anchor_list = json.loads(response.content)['result']['anchor_list']
                self.assertEqual(len(anchor_list), 1)
                self.assertEqual(anchor_list[0]['room_obj']['id'], (room_id))
                break
        self.assertLess(self.count,self.max_count)

    def test_diamond_get_list_can_be_add(self):
        """
        测试钻石守护可纳入主播团
        :return:
        """
        user_id = self.user_id
        while self.count < self.max_count:
            mysql_operation = MysqlOperation(user_id=user_id)
            mysql_operation.fix_user_rank_and_experience(user_rank=self.user_rank,experience_all=self.user_experience_all)
            mysql_operation.fix_user_account(gold_num=7156000)
            RedisHold().clean_redis_user_detail(self.user_id)
            time.sleep(self.time_sleep)

            open_anchor_group_api = OpenAnchorGroupApi(self.user_login_name)
            open_anchor_group_api.get()
            if open_anchor_group_api.get_code() == 100032:
                time.sleep(self.time_sleep)
                self.count+=1
            else:
                self.assertEqual(open_anchor_group_api.get_code(),0)
                break
        self.assertLess(self.count,self.max_count)
        while self.count < self.max_count:
            mysql_operation = MysqlOperation(user_id=user_id)
            mysql_operation.fix_user_rank_and_experience(user_rank=self.user_rank,experience_all=self.user_experience_all)
            mysql_operation.fix_user_account(gold_num=7056000)
            RedisHold().clean_redis_user_detail(self.user_id)
            time.sleep(self.time_sleep)
            buy_guard_api = BuyGuardApi(self.user_login_name)
            guard_response = buy_guard_api.get({'room_id': room_id, 'guard_id': '12','currency':'gold'})
            if buy_guard_api.get_code() == 100032:
                time.sleep(self.time_sleep)
                self.count+=1
            else:
                self.assertEqual(buy_guard_api.get_code(), 0)

                self.assertEqual(json.loads(guard_response.content)['result']['guard_list'][0]['user_guard_obj']['guard_rank'],4)
                list_can_be_add_api = ListCanBeAddApi(self.user_login_name)
                response = list_can_be_add_api.get()

                self.assertEqual(list_can_be_add_api.get_code(), 0)
                self.assertEqual(list_can_be_add_api.get_response_message(), u'操作成功')
                anchor_list = json.loads(response.content)['result']['anchor_list']
                self.assertEqual(len(anchor_list), 1)
                self.assertEqual(anchor_list[0]['room_obj']['id'], (room_id))
                break
        self.assertLess(self.count,self.max_count)

    def tearDown(self,*args):
        super(TestListCanBeAddApi,self).tearDown(user_id=self.user_id,anchor_id=anchor_id)
        TearDown().guard_teardown(login_name=self.user_login_name,user_id=self.user_id,anchor_id=anchor_id)
        user_id = self.user_id
        for i in [user_id, anchor_id]:
            MysqlOperation(user_id=i).clean_user_anchor_group()
        Redis().clean_user_buy_guard(user_id, anchor_id)
        Redis().clean_anchor_group(user_id,anchor_id)
