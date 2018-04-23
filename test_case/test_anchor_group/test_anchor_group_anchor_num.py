# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.anchor_group_api import OpenAnchorGroupApi
from utilities.redis_helper import RedisHold,Redis
from utilities.mysql_helper import MysqlOperation
from settings import YULE_TEST_ANCHOR_ID as anchor_id,YULE_TEST_ROOM as room_id
import json, time
from utilities.teardown import TearDown
from settings import YULE_TEST_USER_LOGIN_NAME,YULE_TEST_USER_ID

class TestAnchorGroupAnchorNumApi(BaseCase):
    """
    主播团可纳入主播数量
    """
    user_login_name = YULE_TEST_USER_LOGIN_NAME
    user_id = YULE_TEST_USER_ID
    time_sleep = 0.2



    def setUp(self,*args):
        super(TestAnchorGroupAnchorNumApi,self).setUp(user_id=self.user_id,anchor_id=anchor_id)
        TearDown().guard_teardown(login_name=self.user_login_name,user_id=self.user_id,anchor_id=anchor_id)
        mysql_operation = MysqlOperation(user_id=self.user_id)
        mysql_operation.clean_user_anchor_group()
        Redis().clean_anchor_group(self.user_id, anchor_id=anchor_id)
        RedisHold().clean_redis_room_detail(room_id, anchor_id)

    def test_anchor_colonel_group_anchor_num(self):
        """
        测试用户等级为18时可纳入数量
        :return:
        """
        user_id = self.user_id
        mysql_operation = MysqlOperation(user_id=user_id)
        mysql_operation.fix_user_rank_and_experience(user_rank=18, experience_all=2000000)
        mysql_operation.fix_user_account(gold_num=100000)
        RedisHold().clean_redis_user_detail(self.user_id)
        time.sleep(self.time_sleep)
        open_anchor_group_api = OpenAnchorGroupApi(self.user_login_name)
        response = open_anchor_group_api.get()
        self.assertEqual(open_anchor_group_api.get_code(), 0)

        anchor_group_obj = json.loads(response.content)['result']['anchor_group_obj']
        self.assertEqual(anchor_group_obj['max_num'],2)
        self.assertEqual(anchor_group_obj['next_level_name'],u'1级上校')
        self.assertEqual(anchor_group_obj['next_level'],18)

    def test_anchor_lieutenant_general_group_anchor_num(self):
        """
        测试用户等级为26级时可纳入数量
        :return:
        """
        user_id = self.user_id
        mysql_operation = MysqlOperation(user_id=user_id)
        mysql_operation.fix_user_rank_and_experience(user_rank=26, experience_all=200000000)
        mysql_operation.fix_user_account(gold_num=100000)
        RedisHold().clean_redis_user_detail(self.user_id)
        time.sleep(self.time_sleep)

        open_anchor_group_api = OpenAnchorGroupApi(self.user_login_name)
        response = open_anchor_group_api.get()
        self.assertEqual(open_anchor_group_api.get_code(), 0)

        anchor_group_obj = json.loads(response.content)['result']['anchor_group_obj']
        self.assertEqual(anchor_group_obj['max_num'],4)
        self.assertEqual(anchor_group_obj['next_level_name'],u'1级元帅')
        self.assertEqual(anchor_group_obj['next_level'],35)

    def test_anchor_marshal_group_anchor_num(self):
        """
        测试用户等级为35级时可纳入数量
        :return:
        """
        user_id = self.user_id
        mysql_operation = MysqlOperation(user_id=user_id)
        mysql_operation.fix_user_rank_and_experience(user_rank=35, experience_all=800000000)
        mysql_operation.fix_user_account(gold_num=100000)
        RedisHold().clean_redis_user_detail(self.user_id)
        time.sleep(self.time_sleep)

        open_anchor_group_api = OpenAnchorGroupApi(self.user_login_name)
        response = open_anchor_group_api.get()
        self.assertEqual(open_anchor_group_api.get_code(), 0)

        anchor_group_obj = json.loads(response.content)['result']['anchor_group_obj']
        self.assertEqual(anchor_group_obj['max_num'],5)
        self.assertEqual(anchor_group_obj['next_level_name'],u'1级大元帅')
        self.assertEqual(anchor_group_obj['next_level'],45)

    def test_anchor_generalissimo_group_anchor_num(self):
        """
        测试用户等级为45级时可纳入数量
        :return:
        """
        user_id = self.user_id
        mysql_operation = MysqlOperation(user_id=user_id)
        mysql_operation.fix_user_rank_and_experience(user_rank=45, experience_all=2000000000)
        mysql_operation.fix_user_account(gold_num=100000)
        RedisHold().clean_redis_user_detail(self.user_id)
        time.sleep(self.time_sleep)

        open_anchor_group_api = OpenAnchorGroupApi(self.user_login_name)
        response = open_anchor_group_api.get()
        self.assertEqual(open_anchor_group_api.get_code(), 0)

        anchor_group_obj = json.loads(response.content)['result']['anchor_group_obj']
        self.assertEqual(anchor_group_obj['max_num'],6)
        self.assertEqual(anchor_group_obj['next_level_name'],u'16级大元帅')
        self.assertEqual(anchor_group_obj['next_level'],60)

    def tearDown(self,*args):
        super(TestAnchorGroupAnchorNumApi,self).tearDown(user_id=self.user_id,anchor_id=anchor_id)
        TearDown().guard_teardown(login_name=self.user_login_name,user_id=self.user_id,anchor_id=anchor_id)
        user_id = self.user_id
        mysql_operation = MysqlOperation(user_id=user_id)
        mysql_operation.clean_user_anchor_group()
        Redis().clean_anchor_group(user_id, anchor_id=anchor_id)
        RedisHold().clean_redis_room_detail(room_id,anchor_id)
