# -*- coding:utf-8 -*-
from api.send_gift_api import SendGiftApi
from base.base_case import BaseCase
from api.consumption_api import ConsumptionApi
from utilities.mysql_helper import MysqlOperation
from api.guard_api import BuyGuardApi
from utilities.redis_helper import RedisHold
import json,time,settings
from utilities.teardown import TearDown


class TestSendGuardGift(BaseCase):
    """
    送守护专属礼物
    """
    login_name = settings.YULE_TEST_USER_LOGIN_NAME
    user_id = settings.YULE_TEST_USER_ID
    room_id = settings.YULE_TEST_ROOM
    anchor_id = settings.YULE_TEST_ANCHOR_ID
    count = 1
    max_count = 20
    time_sleep = 0.5
    guard_gift_id = '1006'
    gift_gold = 100000


    def action(self,**kwargs):
        guard_id = kwargs['guard_id']
        guard_price = None
        if guard_id == 1:
            guard_price = 588000
        elif guard_id == 2:
            guard_price = 1176000
        elif guard_id == 3:
            guard_price = 1764000
        elif guard_id == 12:
            guard_price = 7056000
        while self.count < self.max_count:
            mysql_operation = MysqlOperation(user_id=self.user_id)
            mysql_operation.fix_user_account(gold_num=guard_price)
            RedisHold().clean_redis_user_detail(self.user_id)
            time.sleep(self.time_sleep)
            buy_guard_api = BuyGuardApi(self.login_name)
            response = buy_guard_api.get({'room_id':self.room_id,'guard_id':guard_id,'currency':'gold'})
            if buy_guard_api.get_code() == 100032:
                time.sleep(self.time_sleep)
                self.count+=1
            else:
                self.assertEqual(buy_guard_api.get_code(),0)
                identity_obj = json.loads(response.content)['result']['identity_obj']
                if guard_id == 12:
                    self.assertEqual(identity_obj['user_guard_obj']['guard_rank'], 4)
                else:
                    self.assertEqual(identity_obj['user_guard_obj']['guard_rank'],guard_id)
                break
        self.assertLess(self.count,self.max_count)

        while self.count < self.max_count:
            mysql_operation = MysqlOperation(user_id=self.user_id)
            mysql_operation.fix_user_account(gold_num=self.gift_gold)
            RedisHold().clean_redis_user_detail(self.user_id)
            time.sleep(self.time_sleep)
            send_gift_api = SendGiftApi(self.login_name)
            response = send_gift_api.get({'room_id': self.room_id, 'gift_id': self.guard_gift_id, 'gift_count': 1,'currency': 'gold'})
            if send_gift_api.get_code() in [100032,100503]:
                time.sleep(self.time_sleep)
                self.count+=1
            else:
                self.assertEqual(send_gift_api.get_code(),0)
                identity_obj = json.loads(response.content)['result']['identity_obj']
                self.assertEqual(identity_obj['gold'],0)
                self.assertEqual(identity_obj['diamond'],u'0')
                break
        self.assertLess(self.count,self.max_count)

        consumption_api = ConsumptionApi(self.login_name)
        response = consumption_api.get()
        self.assertEqual(consumption_api.get_code(),0)
        consume_list = json.loads(response.content)['result']['consume_list']
        self.assertEqual(len(consume_list),2)
        self.assertEqual(consume_list[0]['user_id'],self.user_id)
        self.assertEqual(consume_list[0]['type'],u'1')
        self.assertEqual(consume_list[0]['gold'],self.gift_gold)
        self.assertEqual(consume_list[0]['corresponding_id'],int(self.guard_gift_id))
        self.assertEqual(consume_list[0]['corresponding_name'],MysqlOperation().get_gift_details(gift_id=self.guard_gift_id)['name'])
        self.assertEqual(consume_list[0]['corresponding_num'],1)
        self.assertEqual(consume_list[0]['room_id'],self.room_id)
        self.assertEqual(consume_list[0]['status'],1)
        self.assertEqual(consume_list[0]['behavior_desc'],u'送礼')
        self.assertEqual(consume_list[0]['room_title'],MysqlOperation(room_id=self.room_id).get_room_details()['title'])
        self.assertEqual(consume_list[0]['consumption_type'],u'%s金币' % self.gift_gold)

    def test_bronze_send_guard_gift(self):
        """
        测试青铜守护送守护礼物
        :return:
        """
        test_data = {'guard_id':1}
        self.action(**test_data)

    def test_silver_send_guard_gift(self):
        """
        测试白银守护送守护礼物
        :return:
        """
        test_data = {'guard_id':2}
        self.action(**test_data)

    def test_gold_send_guard_gift(self):
        """
        测试黄金守护送守护礼物
        :return:
        """
        test_data = {'guard_id': 3}
        self.action(**test_data)

    def test_diamond_send_guard_gift(self):
        """
        测试钻石守护送守护礼物
        :return:
        """
        test_data = {'guard_id':12}
        self.action(**test_data)

    def test_normal_user_send_guard_gift(self):
        """
        测试普通用户送守护礼物
        :return:
        """
        while self.count < self.max_count:
            mysql_operation = MysqlOperation(user_id=self.user_id)
            mysql_operation.fix_user_account(gold_num=self.gift_gold)
            RedisHold().clean_redis_user_detail(self.user_id)
            time.sleep(self.time_sleep)
            send_gift_api = SendGiftApi(self.login_name)
            send_gift_api.get({'room_id': self.room_id, 'gift_id': self.guard_gift_id, 'gift_count': 1,'currency': 'gold'})
            if send_gift_api.get_code() == 100032:
                time.sleep(self.time_sleep)
                self.count+=1
            else:
                self.assertEqual(send_gift_api.get_code(),900019)
                self.assertEqual(send_gift_api.get_response_message(),u'赠送礼物失败:守护等级不足')
                break
        self.assertLess(self.count,self.max_count)

    def tearDown(self,*args):
        super(TestSendGuardGift,self).tearDown(user_id=self.user_id,anchor_id=self.anchor_id)
        TearDown().guard_teardown(login_name=self.login_name, user_id=self.user_id, anchor_id=self.anchor_id)
        TearDown().send_gift_teardown(anchor_id=self.anchor_id, user_id=self.user_id,room_id=self.room_id,following=False)
        # time.sleep(self.time_sleep)