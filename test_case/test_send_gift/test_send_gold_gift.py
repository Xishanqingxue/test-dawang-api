# -*- coding:utf-8 -*-
from test_case.test_send_gift.action import SendGiftAction
import time
from utilities.teardown import TearDown


class TestSendGift(SendGiftAction):
    """
    送普通金币礼物
    """
    gift_id = 67
    gift_gold = 1000


    def setUp(self,*args):
        super(TestSendGift,self).tearDown(user_id=self.user_id,anchor_id=self.anchor_id)
        TearDown().send_gift_teardown(login_name=None,anchor_id=self.anchor_id, user_id=self.user_id,room_id=self.room_id,following=False)


    def test_send_gold_gift_1(self):
        """
        测试送出1个金币礼物
        :return:
        """
        test_data = {'gift_gold':self.gift_gold,'gift_diamond':0,'gift_id':self.gift_id,'gift_num':1,'is_following':False}
        self.send_gift_action(**test_data)

    def test_send_gold_gift_10(self):
        """
        测试送出10个金币礼物
        :return:
        """
        test_data = {'gift_gold':self.gift_gold,'gift_diamond':0,'gift_id':self.gift_id,'gift_num':10,'is_following':False}
        self.send_gift_action(**test_data)

    def test_send_gold_gift_66(self):
        """
        测试送出66个金币礼物
        :return:
        """
        test_data = {'gift_gold':self.gift_gold,'gift_diamond':0,'gift_id':self.gift_id,'gift_num':66,'is_following':False}
        self.send_gift_action(**test_data)

    def test_send_gold_gift_99(self):
        """
        测试送出99个金币礼物
        :return:
        """
        test_data = {'gift_gold':self.gift_gold,'gift_diamond':0,'gift_id':self.gift_id,'gift_num':99,'is_following':False}
        self.send_gift_action(**test_data)

    def test_send_gold_gift_188(self):
        """
        测试送出188个金币礼物
        :return:
        """
        test_data = {'gift_gold':self.gift_gold,'gift_diamond':0,'gift_id':self.gift_id,'gift_num':188,'is_following':False}
        self.send_gift_action(**test_data)

    def test_send_gold_gift_520(self):
        """
        测试送出520个金币礼物
        :return:
        """
        test_data = {'gift_gold':self.gift_gold,'gift_diamond':0,'gift_id':self.gift_id,'gift_num':520,'is_following':False}
        self.send_gift_action(**test_data)

    def test_send_gold_gift_1314(self):
        """
        测试送出1314个金币礼物
        :return:
        """
        test_data = {'gift_gold':self.gift_gold,'gift_diamond':0,'gift_id':self.gift_id,'gift_num':1314,'is_following':False}
        self.send_gift_action(**test_data)

    def tearDown(self,*args):
        super(TestSendGift,self).tearDown(user_id=self.user_id,anchor_id=self.anchor_id)
        TearDown().send_gift_teardown(login_name=None, anchor_id=self.anchor_id, user_id=self.user_id,room_id=self.room_id, following=False)