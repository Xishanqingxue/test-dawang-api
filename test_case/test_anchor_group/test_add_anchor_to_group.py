# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.guard_api import BuyGuardApi
from api.anchor_group_api import AddAnchorToGroupApi,OpenAnchorGroupApi
from utilities.redis_helper import RedisHold,Redis
from utilities.mysql_helper import MysqlOperation
from settings import YULE_TEST_ANCHOR_ID as anchor_id,YULE_TEST_ROOM as room_id
import json, time
from utilities.teardown import TearDown
from settings import YULE_TEST_USER_LOGIN_NAME,YULE_TEST_USER_ID

class TestAddAnchorToGroupApi(BaseCase):
    """
    纳入主播团
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
        Redis().clean_anchor_group(self.user_id,anchor_id)
        for i in [self.user_id, anchor_id]:
            MysqlOperation(user_id=i).clean_user_anchor_group()
        Redis().clean_user_buy_guard(self.user_id, anchor_id)
        RedisHold().clean_redis_room_detail(room_id,anchor_id)

    def test_bronze_add_anchor_to_group(self):
        """
        测试将青铜守护纳入主播团
        :return:
        """
        while self.count < self.max_count:
            mysql_operation = MysqlOperation(self.user_id)
            mysql_operation.fix_user_rank_and_experience(user_rank=self.user_rank, experience_all=self.user_experience_all)
            mysql_operation.fix_user_account(gold_num=100000)
            RedisHold().clean_redis_user_detail(self.user_id)
            time.sleep(self.time_sleep)

            open_anchor_group_api = OpenAnchorGroupApi(self.user_login_name)
            response = open_anchor_group_api.get()
            if open_anchor_group_api.get_code() == 100032:
                time.sleep(self.time_sleep)
                self.count+=1
            else:
                self.assertEqual(open_anchor_group_api.get_code(), 0)

                anchor_group_obj = json.loads(response.content)['result']['anchor_group_obj']
                self.assertEqual(anchor_group_obj['user_id'],int(self.user_id))
                self.assertEqual(anchor_group_obj['gold'],0)
                self.assertEqual(anchor_group_obj['max_num'],2)
                self.assertEqual(anchor_group_obj['next_level'],18)
                self.assertEqual(anchor_group_obj['next_level_name'],u'1级上校')
                self.assertEqual(anchor_group_obj['owend_anchor_count'],0)

                while self.count < self.max_count:
                    mysql_operation = MysqlOperation(self.user_id)
                    mysql_operation.fix_user_rank_and_experience(user_rank=self.user_rank,
                                                                 experience_all=self.user_experience_all)
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

                        add_anchor_to_group_api = AddAnchorToGroupApi(self.user_login_name)
                        response = add_anchor_to_group_api.get({'anchor_id': anchor_id, 'position': 1,'grab_flag': 0,'change_flag': 0})
                        self.assertEqual(add_anchor_to_group_api.get_code(), 0)
                        self.assertEqual(add_anchor_to_group_api.get_response_message(), u'操作成功')

                        anchor_group_anchor_obj = json.loads(response.content)['result']['anchor_group_list'][0]['anchor_group_anchor_obj']
                        self.assertEqual(anchor_group_anchor_obj['anchor_id'],int(anchor_id))
                        self.assertEqual(anchor_group_anchor_obj['position'],1)
                        self.assertEqual(anchor_group_anchor_obj['income_gold'],0)
                        self.assertLessEqual(anchor_group_anchor_obj['left_time'],604800)

                        anchor_obj = json.loads(response.content)['result']['anchor_group_list'][0]['anchor_obj']
                        self.assertEqual(anchor_obj['id'],anchor_id)
                        self.assertEqual(anchor_obj['anchor_rank'],4)
                        self.assertEqual(anchor_obj['anchor_experience_all'],588000)
                        break
                self.assertLess(self.count,self.max_count)
                break
        self.assertLess(self.count,self.max_count)

    def test_silver_add_anchor_to_group(self):
        """
        测试将白银守护纳入主播团
        :return:
        """
        while self.count < self.max_count:
            mysql_operation = MysqlOperation(self.user_id)
            mysql_operation.fix_user_rank_and_experience(user_rank=self.user_rank, experience_all=self.user_experience_all)
            mysql_operation.fix_user_account(gold_num=100000)
            RedisHold().clean_redis_user_detail(self.user_id)
            time.sleep(self.time_sleep)
            open_anchor_group_api = OpenAnchorGroupApi(self.user_login_name)
            response = open_anchor_group_api.get()
            if open_anchor_group_api.get_code() == 100032:
                time.sleep(self.time_sleep)
                self.count+=1
            else:
                self.assertEqual(open_anchor_group_api.get_code(), 0)
                anchor_group_obj = json.loads(response.content)['result']['anchor_group_obj']
                self.assertEqual(anchor_group_obj['user_id'], int(self.user_id))
                self.assertEqual(anchor_group_obj['gold'], 0)
                self.assertEqual(anchor_group_obj['max_num'], 2)
                self.assertEqual(anchor_group_obj['next_level'], 18)
                self.assertEqual(anchor_group_obj['next_level_name'], u'1级上校')
                self.assertEqual(anchor_group_obj['owend_anchor_count'], 0)
                while self.count < self.max_count:
                    mysql_operation = MysqlOperation(self.user_id)
                    mysql_operation.fix_user_rank_and_experience(user_rank=self.user_rank,
                                                                 experience_all=self.user_experience_all)
                    mysql_operation.fix_user_account(gold_num=1226000)
                    RedisHold().clean_redis_user_detail(self.user_id)
                    time.sleep(self.time_sleep)
                    buy_guard_api = BuyGuardApi(self.user_login_name)
                    guard_response = buy_guard_api.get({'room_id': room_id, 'guard_id': '2','currency':'gold'})
                    if buy_guard_api.get_code() == 100032:
                        time.sleep(self.time_sleep)
                        self.count+=1
                    else:
                        self.assertEqual(buy_guard_api.get_code(), 0)

                        self.assertEqual(json.loads(guard_response.content)['result']['identity_obj']['user_guard_obj']['guard_rank'], 2)

                        add_anchor_to_group_api = AddAnchorToGroupApi(self.user_login_name)
                        response = add_anchor_to_group_api.get({'anchor_id': anchor_id, 'position': 1, 'grab_flag': 0,'change_flag': 0})
                        self.assertEqual(add_anchor_to_group_api.get_code(), 0)

                        self.assertEqual(add_anchor_to_group_api.get_response_message(), u'操作成功')
                        anchor_group_anchor_obj = json.loads(response.content)['result']['anchor_group_list'][0]['anchor_group_anchor_obj']
                        self.assertEqual(anchor_group_anchor_obj['anchor_id'],int(anchor_id))
                        self.assertEqual(anchor_group_anchor_obj['position'],1)
                        self.assertEqual(anchor_group_anchor_obj['income_gold'],0)
                        self.assertLessEqual(anchor_group_anchor_obj['left_time'],604800)

                        anchor_obj = json.loads(response.content)['result']['anchor_group_list'][0]['anchor_obj']
                        self.assertEqual(anchor_obj['id'],anchor_id)
                        self.assertEqual(anchor_obj['anchor_rank'],5)
                        self.assertEqual(anchor_obj['anchor_experience_all'],1176000)
                        break
                self.assertLess(self.count,self.max_count)
                break
        self.assertLess(self.count,self.max_count)

    def test_gold_add_anchor_to_group(self):
        """
        测试将黄金守护纳入主播团
        :return:
        """
        while self.count < self.max_count:
            mysql_operation = MysqlOperation(self.user_id)
            mysql_operation.fix_user_rank_and_experience(user_rank=self.user_rank, experience_all=self.user_experience_all)
            mysql_operation.fix_user_account(gold_num=100000)
            RedisHold().clean_redis_user_detail(self.user_id)
            time.sleep(self.time_sleep)

            open_anchor_group_api = OpenAnchorGroupApi(self.user_login_name)
            response = open_anchor_group_api.get()
            if open_anchor_group_api.get_code() == 100032:
                time.sleep(self.time_sleep)
                self.count+=1
            else:
                self.assertEqual(open_anchor_group_api.get_code(), 0)
                anchor_group_obj = json.loads(response.content)['result']['anchor_group_obj']
                self.assertEqual(anchor_group_obj['user_id'], int(self.user_id))
                self.assertEqual(anchor_group_obj['gold'], 0)
                self.assertEqual(anchor_group_obj['max_num'], 2)
                self.assertEqual(anchor_group_obj['next_level'], 18)
                self.assertEqual(anchor_group_obj['next_level_name'], u'1级上校')
                self.assertEqual(anchor_group_obj['owend_anchor_count'], 0)
                while self.count < self.max_count:
                    mysql_operation = MysqlOperation(self.user_id)
                    mysql_operation.fix_user_rank_and_experience(user_rank=self.user_rank,
                                                                 experience_all=self.user_experience_all)
                    mysql_operation.fix_user_account(gold_num=1814000)
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

                        add_anchor_to_group_api = AddAnchorToGroupApi(self.user_login_name)
                        response = add_anchor_to_group_api.get({'anchor_id': anchor_id, 'position': 1,'grab_flag': 0,'change_flag': 0})
                        self.assertEqual(add_anchor_to_group_api.get_code(), 0)
                        self.assertEqual(add_anchor_to_group_api.get_response_message(), u'操作成功')

                        anchor_group_anchor_obj = json.loads(response.content)['result']['anchor_group_list'][0]['anchor_group_anchor_obj']
                        self.assertEqual(anchor_group_anchor_obj['anchor_id'],int(anchor_id))
                        self.assertEqual(anchor_group_anchor_obj['position'],1)
                        self.assertEqual(anchor_group_anchor_obj['income_gold'],0)
                        self.assertLessEqual(anchor_group_anchor_obj['left_time'],604800)

                        anchor_obj = json.loads(response.content)['result']['anchor_group_list'][0]['anchor_obj']
                        self.assertEqual(anchor_obj['id'],anchor_id)
                        self.assertEqual(anchor_obj['anchor_rank'],5)
                        self.assertEqual(anchor_obj['anchor_experience_all'],1764000)
                        break
                self.assertLess(self.count,self.max_count)
                break
        self.assertLess(self.count,self.max_count)

    def test_diamond_add_anchor_to_group(self):
        """
        测试将钻石守护纳入主播团
        :return:
        """
        while self.count < self.max_count:
            mysql_operation = MysqlOperation(self.user_id)
            mysql_operation.fix_user_rank_and_experience(user_rank=self.user_rank, experience_all=self.user_experience_all)
            mysql_operation.fix_user_account(gold_num=100000)
            RedisHold().clean_redis_user_detail(self.user_id)
            time.sleep(self.time_sleep)

            open_anchor_group_api = OpenAnchorGroupApi(self.user_login_name)
            response = open_anchor_group_api.get()
            if open_anchor_group_api.get_code() == 100032:
                time.sleep(self.time_sleep)
                self.count+=1
            else:

                self.assertEqual(open_anchor_group_api.get_code(), 0)
                anchor_group_obj = json.loads(response.content)['result']['anchor_group_obj']
                self.assertEqual(anchor_group_obj['user_id'], int(self.user_id))
                self.assertEqual(anchor_group_obj['gold'], 0)
                self.assertEqual(anchor_group_obj['max_num'], 2)
                self.assertEqual(anchor_group_obj['next_level'], 18)
                self.assertEqual(anchor_group_obj['next_level_name'], u'1级上校')
                self.assertEqual(anchor_group_obj['owend_anchor_count'], 0)
                while self.count < self.max_count:
                    mysql_operation = MysqlOperation(self.user_id)
                    mysql_operation.fix_user_rank_and_experience(user_rank=self.user_rank,
                                                                 experience_all=self.user_experience_all)
                    mysql_operation.fix_user_account(gold_num=7106000)
                    RedisHold().clean_redis_user_detail(self.user_id)
                    time.sleep(self.time_sleep)
                    buy_guard_api = BuyGuardApi(self.user_login_name)
                    guard_response = buy_guard_api.get({'room_id': room_id, 'guard_id': '12','currency':'gold'})
                    if buy_guard_api.get_code() == 100032:
                        time.sleep(self.time_sleep)
                        self.count+=1
                    else:
                        self.assertEqual(buy_guard_api.get_code(), 0)
                        self.assertEqual(json.loads(guard_response.content)['result']['identity_obj']['user_guard_obj']['guard_rank'], 4)

                        add_anchor_to_group_api = AddAnchorToGroupApi(self.user_login_name)
                        response = add_anchor_to_group_api.get({'anchor_id': anchor_id, 'position': 1,'grab_flag': 0,'change_flag': 0})
                        self.assertEqual(add_anchor_to_group_api.get_code(), 0)
                        self.assertEqual(add_anchor_to_group_api.get_response_message(), u'操作成功')

                        anchor_group_anchor_obj = json.loads(response.content)['result']['anchor_group_list'][0]['anchor_group_anchor_obj']
                        self.assertEqual(anchor_group_anchor_obj['anchor_id'],int(anchor_id))
                        self.assertEqual(anchor_group_anchor_obj['position'],1)
                        self.assertEqual(anchor_group_anchor_obj['income_gold'],0)
                        self.assertLessEqual(anchor_group_anchor_obj['left_time'],604800)

                        anchor_obj = json.loads(response.content)['result']['anchor_group_list'][0]['anchor_obj']
                        self.assertEqual(anchor_obj['id'], anchor_id)
                        self.assertEqual(anchor_obj['anchor_rank'], 7)
                        self.assertEqual(anchor_obj['anchor_experience_all'], 7056000)
                        break
                self.assertLess(self.count,self.max_count)
                break
        self.assertLess(self.count,self.max_count)

    def tearDown(self,*args):
        super(TestAddAnchorToGroupApi,self).tearDown(user_id=self.user_id,anchor_id=anchor_id)
        TearDown().guard_teardown(login_name=self.user_login_name,user_id=self.user_id,anchor_id=anchor_id)
        Redis().clean_anchor_group(self.user_id,anchor_id)
        for i in [self.user_id, anchor_id]:
            MysqlOperation(user_id=i).clean_user_anchor_group()
        Redis().clean_user_buy_guard(self.user_id, anchor_id)
        RedisHold().clean_redis_room_detail(room_id,anchor_id)
