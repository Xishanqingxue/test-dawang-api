# -*- coding:utf-8 -*-
from api.send_gift_api import SendGiftApi
from base.base_case import BaseCase
from api.consumption_api import ConsumptionApi
from utilities.mysql_helper import MysqlOperation
from api.noble_api import BuyNobleApi
from utilities.redis_helper import RedisHold
import json,time,settings
from utilities.teardown import TearDown


class TestSendNobleGift(BaseCase):
    """
    送贵族专属礼物
    """
    login_name = settings.YULE_TEST_USER_LOGIN_NAME
    user_id = settings.YULE_TEST_USER_ID
    room_id = settings.YULE_TEST_ROOM
    anchor_id = settings.YULE_TEST_ANCHOR_ID
    count = 1
    max_count = 20
    time_sleep = 0.5
    noble_gift_id = '2004'
    gift_gold = 60000


    def action(self,**kwargs):
        noble_id = kwargs['noble_id']
        noble_price = None
        if noble_id == 1:
            noble_price = 24000
        elif noble_id == 2:
            noble_price = 40000
        elif noble_id == 3:
            noble_price = 80000
        elif noble_id == 4:
            noble_price = 400000
        elif noble_id == 5:
            noble_price = 800000
        elif noble_id == 6:
            noble_price = 2400000
        elif noble_id == 7:
            noble_price = 24000000
        while self.count < self.max_count:
            mysql_operation = MysqlOperation(user_id=self.user_id)
            mysql_operation.fix_user_account(gold_num=noble_price)
            RedisHold().clean_redis_user_detail(self.user_id)
            time.sleep(self.time_sleep)

            buy_noble_api = BuyNobleApi(self.login_name)
            response = buy_noble_api.get({'noble_id': noble_id, 'num': 1,'room_id':self.room_id,'currency':'gold'})
            if buy_noble_api.get_code() == 100032:
                time.sleep(self.time_sleep)
                self.count+=1
            else:
                self.assertEqual(buy_noble_api.get_code(),0)
                self.assertEqual(json.loads(response.content)['result']['identity_obj']['noble_rank'],noble_id)
                break
        self.assertLess(self.count,self.max_count)

        while self.count < self.max_count:
            mysql_operation = MysqlOperation(user_id=self.user_id)
            mysql_operation.fix_user_account(gold_num=self.gift_gold)
            RedisHold().clean_redis_user_detail(self.user_id)
            time.sleep(self.time_sleep)
            send_gift_api = SendGiftApi(self.login_name)
            response = send_gift_api.get({'room_id': self.room_id, 'gift_id': self.noble_gift_id, 'gift_count': 1,'currency': 'gold'})
            if send_gift_api.get_code() == 100032:
                time.sleep(self.time_sleep)
                self.count+=1
            else:
                self.assertEqual(send_gift_api.get_code(),0)
                self.assertEqual(json.loads(response.content)['result']['identity_obj']['gold'],0)
                break
        self.assertLess(self.count,self.max_count)

        consumption_api = ConsumptionApi(self.login_name)
        response = consumption_api.get()
        self.assertEqual(consumption_api.get_code(),0)
        self.assertEqual(len(json.loads(response.content)['result']['consume_list']),2)
        consume_list = json.loads(response.content)['result']['consume_list'][0]
        self.assertEqual(consume_list['user_id'],self.user_id)
        self.assertEqual(consume_list['type'],u'1')
        self.assertEqual(consume_list['gold'],self.gift_gold)
        self.assertEqual(consume_list['corresponding_id'],int(self.noble_gift_id))
        self.assertEqual(consume_list['corresponding_name'],MysqlOperation().get_gift_details(self.noble_gift_id)['name'])
        self.assertEqual(consume_list['corresponding_num'],1)
        self.assertEqual(consume_list['room_id'],self.room_id)
        self.assertEqual(consume_list['status'],1)
        self.assertEqual(consume_list['behavior_desc'],u'送礼')
        self.assertEqual(consume_list['room_title'],MysqlOperation(room_id=self.room_id).get_room_details()['title'])
        self.assertEqual(consume_list['consumption_type'],u'%s金币' % self.gift_gold)

    def test_knight_send_noble_gift(self):
        """
        测试骑士贵族送贵族礼物
        :return:
        """
        self.action(**{'noble_id':1})

    def test_baron_send_noble_gift(self):
        """
        测试男爵贵族送贵族礼物
        :return:
        """
        self.action(**{'noble_id':2})

    def test_viscount_send_noble_gift(self):
        """
        测试子爵贵族送贵族礼物
        :return:
        """
        self.action(**{'noble_id':3})

    def test_earl_send_noble_gift(self):
        """
        测试伯爵贵族送贵族礼物
        :return:
        """
        self.action(**{'noble_id':4})

    def test_marquis_send_noble_gift(self):
        """
        测试侯爵贵族送贵族礼物
        :return:
        """
        self.action(**{'noble_id':5})

    def test_duck_send_noble_gift(self):
        """
        测试公爵贵族送贵族礼物
        :return:
        """
        self.action(**{'noble_id':6})

    def test_monarch_send_noble_gift(self):
        """
        测试帝王贵族送贵族礼物
        :return:
        """
        self.action(**{'noble_id':7})

    def test_normal_user_send_noble_gift(self):
        """
        测试普通用户送贵族礼物
        :return:
        """
        while self.count < self.max_count:
            mysql_operation = MysqlOperation(user_id=self.user_id)
            mysql_operation.fix_user_account(gold_num=self.gift_gold)
            RedisHold().clean_redis_user_detail(self.user_id)
            time.sleep(self.time_sleep)
            send_gift_api = SendGiftApi(self.login_name)
            send_gift_api.get({'room_id': self.room_id, 'gift_id': self.noble_gift_id, 'gift_count': 1,'currency': 'gold'})
            if send_gift_api.get_code() == 100032:
                time.sleep(self.time_sleep)
                self.count+=1
            else:
                self.assertEqual(send_gift_api.get_code(),900018)
                self.assertEqual(send_gift_api.get_response_message(),u'赠送礼物失败:贵族等级不足')
                break
        self.assertLess(self.count,self.max_count)

    def tearDown(self,*args):
        super(TestSendNobleGift,self).tearDown(user_id=self.user_id,anchor_id=self.anchor_id)
        MysqlOperation(user_id=self.user_id).clean_user_noble()
        TearDown().send_gift_teardown(anchor_id=self.anchor_id, user_id=self.user_id,room_id=self.room_id, following=False)
        # time.sleep(self.time_sleep)