# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.anchor_group_api import AddAnchorToGroupApi,AnchorGroupWithdrawApi,MyAnchorGroupApi,MyAnchorGroupLogsApi,OpenAnchorGroupApi
from api.guard_api import BuyGuardApi
from api.send_gift_api import SendGiftApi
from api.consumption_api import GoldAccountApi
from utilities.teardown import TearDown
from utilities.redis_helper import RedisHold,Redis
from utilities.mysql_helper import MysqlOperation
from settings import YULE_TEST_ANCHOR_ID as anchor_id,YULE_TEST_ROOM as room_id
import json, time
from settings import YULE_TEST_USER_LOGIN_NAME,YULE_TEST_USER_ID


class TestAnchorGroupWithdrawApi(BaseCase):
    """
    主播团金库
    """
    user_login_name = YULE_TEST_USER_LOGIN_NAME
    user_id = YULE_TEST_USER_ID
    user_rank = 12
    user_experience_all = 3000000
    time_sleep = 0.2

    def setUp(self,*args):
        super(TestAnchorGroupWithdrawApi,self).setUp(user_id=self.user_id,anchor_id=anchor_id)
        TearDown().guard_teardown(login_name=self.user_login_name,user_id=self.user_id,anchor_id=anchor_id)
        user_id = self.user_id
        mysql_operation = MysqlOperation(user_id=user_id,anchor_id=anchor_id)
        mysql_operation.clean_user_anchor_group()
        Redis().clean_anchor_group(user_id, anchor_id=anchor_id)
        mysql_operation.clean_user_anchor_group()
        Redis().clean_user_buy_guard(user_id, anchor_id)
        mysql_operation.clean_send_gift()
        RedisHold().clean_redis_room_detail(room_id, anchor_id)

    def test_anchor_group_withdraw(self):
        """
        测试主播团金库金币收入和提出
        :return:
        """
        user_id = self.user_id
        mysql_operation = MysqlOperation(user_id=user_id,anchor_id=anchor_id)
        expect_gold_num = (int(mysql_operation.get_gift_details(gift_id=67)['gold']) * 2000) * 0.05
        mysql_operation.fix_user_rank_and_experience(user_rank=self.user_rank, experience_all=self.user_experience_all)
        mysql_operation.fix_user_account(gold_num=2738000)
        RedisHold().clean_redis_user_detail(self.user_id)
        # 开通主播团
        open_anchor_group_api = OpenAnchorGroupApi(self.user_login_name)
        response = open_anchor_group_api.get()
        self.assertEqual(open_anchor_group_api.get_code(), 0)
        self.assertEqual(json.loads(response.content)['result']['identity_obj']['gold'],2638000)
        # 购买守护
        buy_guard_api = BuyGuardApi(self.user_login_name)
        guard_response = buy_guard_api.get({'room_id': room_id, 'guard_id': '1','currency':'gold'})
        self.assertEqual(buy_guard_api.get_code(), 0)
        self.assertEqual(json.loads(guard_response.content)['result']['identity_obj']['user_guard_obj']['guard_rank'], 1)
        self.assertEqual(json.loads(guard_response.content)['result']['identity_obj']['gold'],2050000)
        time.sleep(1)
        # 将主播纳入主播团
        add_anchor_to_group_api = AddAnchorToGroupApi(self.user_login_name)
        response = add_anchor_to_group_api.get({'anchor_id': anchor_id, 'position': 1,'grab_flag': 0,'change_flag': 0})
        self.assertEqual(add_anchor_to_group_api.get_code(), 0)
        self.assertEqual(add_anchor_to_group_api.get_response_message(), u'操作成功')
        anchor_group_anchor_obj = json.loads(response.content)['result']['anchor_group_list'][0]['anchor_group_anchor_obj']
        self.assertEqual(anchor_group_anchor_obj['anchor_id'], int(anchor_id))
        self.assertEqual(anchor_group_anchor_obj['position'], 1)
        self.assertEqual(anchor_group_anchor_obj['income_gold'], 0)
        self.assertLessEqual(anchor_group_anchor_obj['left_time'], 604800)

        self.assertEqual(json.loads(response.content)['result']['identity_obj']['gold'],2000000)
        time.sleep(1)
        # 给主播团内主播送礼物
        send_gift_api = SendGiftApi(self.user_login_name)
        send_gift_response = send_gift_api.get({'room_id': room_id, 'gift_id': 67, 'gift_count': 2000,'currency':'gold'})
        self.assertEqual(send_gift_api.get_code(), 0)
        self.assertEqual(json.loads(send_gift_response.content)['result']['identity_obj']['gold'],0)
        time.sleep(1)
        # 查询主播团金库金币
        my_anchor_group_api = MyAnchorGroupApi(self.user_login_name)
        my_anchor_group_response = my_anchor_group_api.get()
        self.assertEqual(my_anchor_group_api.get_code(),0)
        anchor_group_gold = json.loads(my_anchor_group_response.content)['result']['anchor_group_obj']['gold']
        self.assertEqual(anchor_group_gold,expect_gold_num)
        # 提取主播团金库金币
        anchor_group_withdraw_api = AnchorGroupWithdrawApi(self.user_login_name)
        withdraw_response = anchor_group_withdraw_api.get()
        self.assertEqual(anchor_group_withdraw_api.get_code(),0)
        anchor_group_obj = json.loads(withdraw_response.content)['result']['anchor_group_obj']
        self.assertEqual(anchor_group_obj['gold'],0)
        time.sleep(3)
        db_user_gold = mysql_operation.get_user_account_details()['gold']
        self.assertEqual(int(db_user_gold),int(expect_gold_num * 0.9))
        time.sleep(3)
        # 查询主播团日志
        my_anchor_group_logs_api = MyAnchorGroupLogsApi(self.user_login_name)
        logs_response = my_anchor_group_logs_api.get()
        anchor_group_log_list = json.loads(logs_response.content)['result']['anchor_group_log_list']
        self.assertEqual(my_anchor_group_logs_api.get_code(),0)
        self.assertEqual(len(anchor_group_log_list),3)
        self.assertIn(u'金库资金被转出',anchor_group_log_list[0]['content'])
        self.assertIn(u'为金库贡献了',anchor_group_log_list[1]['content'])
        self.assertIn(u'被纳入主播团',anchor_group_log_list[2]['content'])

        # 金币获取记录
        gold_account_api = GoldAccountApi(self.user_login_name)
        response = gold_account_api.get()
        self.assertEqual(gold_account_api.get_code(), 0)
        account_list = json.loads(response.content)['result']['account_list']
        self.assertEqual(len(account_list),1)
        self.assertEqual(account_list[0]['gold'], int(expect_gold_num) * 0.9)
        self.assertEqual(account_list[0]['consumption_type'], u'%s金币' % (int(int(expect_gold_num) * 0.9)))
        self.assertEqual(account_list[0]['behavior_desc'], u'主播团提现')


    def test_anchor_group_withdraw_failed(self):
        """
        测试主播团金库数量小于100000不可转出
        :return:
        """
        user_id = self.user_id
        mysql_operation = MysqlOperation(user_id=user_id,anchor_id=anchor_id)
        mysql_operation.fix_user_rank_and_experience(user_rank=self.user_rank, experience_all=self.user_experience_all)
        mysql_operation.fix_user_account(gold_num=51326000)
        RedisHold().clean_redis_user_detail(self.user_id)
        # 开通主播团
        open_anchor_group_api = OpenAnchorGroupApi(self.user_login_name)
        open_anchor_group_api.get()
        self.assertEqual(open_anchor_group_api.get_code(), 0)
        # 购买守护
        buy_guard_api = BuyGuardApi(self.user_login_name)
        guard_response = buy_guard_api.get({'room_id': room_id, 'guard_id': '2','currency':'gold'})
        self.assertEqual(buy_guard_api.get_code(), 0)
        self.assertEqual(json.loads(guard_response.content)['result']['identity_obj']['user_guard_obj']['guard_rank'], 2)
        time.sleep(1)
        # 将主播纳入主播团
        add_anchor_to_group_api = AddAnchorToGroupApi(self.user_login_name)
        response = add_anchor_to_group_api.get({'anchor_id': anchor_id, 'position': 1,'grab_flag': 0,'change_flag': 0})
        self.assertEqual(add_anchor_to_group_api.get_code(), 0)
        self.assertEqual(add_anchor_to_group_api.get_response_message(), u'操作成功')
        anchor_group_anchor_obj = json.loads(response.content)['result']['anchor_group_list'][0]['anchor_group_anchor_obj']
        self.assertEqual(anchor_group_anchor_obj['anchor_id'], int(anchor_id))
        self.assertEqual(anchor_group_anchor_obj['position'], 1)
        self.assertEqual(anchor_group_anchor_obj['income_gold'], 0)
        self.assertLessEqual(anchor_group_anchor_obj['left_time'], 604800)
        time.sleep(1)
        # 给主播团内主播送礼物
        send_gift_api = SendGiftApi(self.user_login_name)
        send_gift_api.get({'room_id': room_id, 'gift_id': 2, 'gift_count': 1,'currency':'gold'})
        self.assertEqual(send_gift_api.get_code(), 0)
        time.sleep(3)
        # 查询主播团金库金币
        my_anchor_group_api = MyAnchorGroupApi(self.user_login_name)
        my_anchor_group_response = my_anchor_group_api.get()
        response_gold = json.loads(my_anchor_group_response.content)['result']['anchor_group_obj']['gold']
        self.assertEqual(my_anchor_group_api.get_code(),0)
        expect_gold_num = (int(mysql_operation.get_gift_details(gift_id=2)['gold']) * 1) * 0.05
        self.assertEqual(response_gold,expect_gold_num)
        # 提取主播团金库金币
        anchor_group_withdraw_api = AnchorGroupWithdrawApi(self.user_login_name)
        anchor_group_withdraw_api.get()
        self.assertEqual(anchor_group_withdraw_api.get_code(),200510)
        self.assertEqual(anchor_group_withdraw_api.get_response_message(),u'金库余额大于等于100000金币才可转出')

    def tearDown(self,*args):
        super(TestAnchorGroupWithdrawApi,self).tearDown(user_id=self.user_id,anchor_id=anchor_id)
        TearDown().guard_teardown(login_name=self.user_login_name,user_id=self.user_id,anchor_id=anchor_id)
        user_id = self.user_id
        mysql_operation = MysqlOperation(user_id=user_id,anchor_id=anchor_id)
        mysql_operation.clean_user_anchor_group()
        Redis().clean_anchor_group(user_id, anchor_id=anchor_id)
        mysql_operation.clean_user_anchor_group()
        Redis().clean_user_buy_guard(user_id, anchor_id)
        mysql_operation.clean_send_gift()
        RedisHold().clean_redis_room_detail(room_id, anchor_id)
