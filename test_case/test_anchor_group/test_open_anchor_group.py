# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.anchor_group_api import OpenAnchorGroupApi
from settings import YULE_TEST_ANCHOR_ID as anchor_id
from utilities.mysql_helper import MysqlOperation
from utilities.redis_helper import RedisHold,Redis
from utilities.teardown import TearDown
from settings import YULE_TEST_USER_LOGIN_NAME,YULE_TEST_USER_ID
import json,time

class TestOpenAnchorGroup(BaseCase):
    """
    开通主播团
    """
    user_login_name = YULE_TEST_USER_LOGIN_NAME
    user_id = YULE_TEST_USER_ID
    user_rank = 12
    user_experience_all = 2000000
    count = 1
    max_count = 20
    time_sleep = 0.3

    def setUp(self,*args):
        super(TestOpenAnchorGroup,self).setUp(user_id=self.user_id,anchor_id=anchor_id)
        TearDown().guard_teardown(login_name=self.user_login_name,user_id=self.user_id,anchor_id=anchor_id)
        user_id = self.user_id
        mysql_operation = MysqlOperation(user_id=user_id)
        mysql_operation.fix_anchor_group_gold()
        mysql_operation.clean_user_anchor_group()
        Redis().clean_anchor_group(user_id, anchor_id)

    def test_open_anchor_group_rank_deficient(self):
        """
        测试开通主播团所需军衔
        :return:
        """
        open_anchor_group_api = OpenAnchorGroupApi(self.user_login_name)
        open_anchor_group_api.get()
        self.assertEqual(open_anchor_group_api.get_code(),200501)
        self.assertEqual(open_anchor_group_api.get_response_message(),u'军衔达到1级上尉才可开通')

    def test_open_anchor_rank_insufficient_balance(self):
        """
        测试开通主播团金币不足
        :return:
        """
        mysql_operation = MysqlOperation(user_id=self.user_id)
        mysql_operation.fix_user_rank_and_experience(user_rank=self.user_rank,experience_all=self.user_experience_all)
        RedisHold().clean_redis_user_detail(self.user_id)
        time.sleep(self.time_sleep)
        open_anchor_group_api = OpenAnchorGroupApi(self.user_login_name)
        open_anchor_group_api.get()
        self.assertEqual(open_anchor_group_api.get_code(),200502)
        self.assertEqual(open_anchor_group_api.get_response_message(),u'金币不足，是否立即充值')

    def test_open_anchor_group_successful(self):
        """
        测试开通主播团成功
        :return:
        """
        while self.count < self.max_count:
            mysql_operation = MysqlOperation(user_id=self.user_id)
            mysql_operation.fix_user_rank_and_experience(user_rank=self.user_rank,experience_all=self.user_experience_all)
            mysql_operation.fix_user_account(gold_num=100000)
            RedisHold().clean_redis_user_detail(self.user_id)
            time.sleep(self.time_sleep)

            open_anchor_group_api = OpenAnchorGroupApi(self.user_login_name)
            response = open_anchor_group_api.get()
            if open_anchor_group_api.get_code() == 100032:
                time.sleep(self.time_sleep)
                self.count+=1
            else:

                self.assertEqual(open_anchor_group_api.get_code(),0)
                anchor_group_obj = json.loads(response.content)['result']['anchor_group_obj']
                self.assertEqual(anchor_group_obj['user_id'], int(self.user_id))
                self.assertEqual(anchor_group_obj['gold'], 0)
                self.assertEqual(anchor_group_obj['max_num'], 2)
                self.assertEqual(anchor_group_obj['next_level'], 18)
                self.assertEqual(anchor_group_obj['next_level_name'], u'1级上校')
                self.assertEqual(anchor_group_obj['owend_anchor_count'], 0)
                break
        self.assertLess(self.count,self.max_count)


    def test_open_anchor_group_again(self):
        """
        测试重复开通主播团
        :return:
        """
        while self.count < self.max_count:
            mysql_operation = MysqlOperation(user_id=self.user_id)
            mysql_operation.fix_user_rank_and_experience(user_rank=self.user_rank,experience_all=self.user_experience_all)
            mysql_operation.fix_user_account(gold_num=100000)
            RedisHold().clean_redis_user_detail(self.user_id)
            time.sleep(self.time_sleep)
            open_anchor_group_api = OpenAnchorGroupApi(self.user_login_name)
            open_anchor_group_api.get()
            if open_anchor_group_api.get_code() == 200502:
                time.sleep(self.time_sleep)
                self.count+=1
            else:
                self.assertEqual(open_anchor_group_api.get_code(),0)
                while self.count < self.max_count:
                    mysql_operation = MysqlOperation(user_id=self.user_id)
                    mysql_operation.fix_user_account(gold_num=100000)
                    RedisHold().clean_redis_user_detail(self.user_id)
                    time.sleep(self.time_sleep)
                    open_anchor_group_api_again = OpenAnchorGroupApi(self.user_login_name)
                    open_anchor_group_api_again.get()
                    if open_anchor_group_api_again.get_code() == 200502:
                        time.sleep(self.time_sleep)
                        self.count+=1
                    else:
                        self.assertEqual(open_anchor_group_api_again.get_code(),200503)
                        self.assertEqual(open_anchor_group_api_again.get_response_message(),u'已经创建过主播团')
                        break
                self.assertLess(self.count,self.max_count)
                break
        self.assertLess(self.count,self.max_count)

    def tearDown(self,*args):
        super(TestOpenAnchorGroup,self).tearDown(user_id=self.user_id,anchor_id=anchor_id)
        TearDown().guard_teardown(login_name=self.user_login_name,user_id=self.user_id,anchor_id=anchor_id)
        user_id = self.user_id
        mysql_operation = MysqlOperation(user_id=user_id)
        mysql_operation.fix_anchor_group_gold()
        mysql_operation.clean_user_anchor_group()
        Redis().clean_anchor_group(user_id, anchor_id)