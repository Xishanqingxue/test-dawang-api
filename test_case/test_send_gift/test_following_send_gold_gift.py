# -*- coding:utf-8 -*-
from test_case.test_send_gift.action import SendGiftAction
from utilities.teardown import TearDown


class TestFollowingSendGift(SendGiftAction):
    """
    送金币礼物(关注)
    """
    gift_id = 67
    gift_gold = 1000


    def setUp(self,*args):
        super(TestFollowingSendGift,self).setUp(user_id=self.user_id,anchor_id=self.anchor_id)
        TearDown().send_gift_teardown(login_name=self.login_name,anchor_id=self.anchor_id,user_id=self.user_id,room_id=self.room_id)


    def test_send_gold_gift_1_following(self):
        """
        测试关注主播情况下送出1个金币礼物
        :return:
        """
        test_data = {'gift_gold':self.gift_gold,'gift_diamond':0,'gift_id':self.gift_id,'gift_num':1,'is_following':True}
        self.send_gift_action(**test_data)

    def test_send_gold_gift_10_following(self):
        """
        测试关注主播情况下送出10个金币礼物
        :return:
        """
        test_data = {'gift_gold':self.gift_gold,'gift_diamond':0,'gift_id':self.gift_id,'gift_num':10,'is_following':True}
        self.send_gift_action(**test_data)

    def test_send_gold_gift_66_following(self):
        """
        测试关注主播情况下送出66个金币礼物
        :return:
        """
        test_data = {'gift_gold':self.gift_gold,'gift_diamond':0,'gift_id':self.gift_id,'gift_num':66,'is_following':True}
        self.send_gift_action(**test_data)

    def test_send_gold_gift_99_following(self):
        """
        测试关注主播情况下送出99个金币礼物
        :return:
        """
        test_data = {'gift_gold':self.gift_gold,'gift_diamond':0,'gift_id':self.gift_id,'gift_num':99,'is_following':True}
        self.send_gift_action(**test_data)

    def test_send_gold_gift_188_following(self):
        """
        测试关注主播情况下送出188个金币礼物
        :return:
        """
        test_data = {'gift_gold':self.gift_gold,'gift_diamond':0,'gift_id':self.gift_id,'gift_num':188,'is_following':True}
        self.send_gift_action(**test_data)

    def test_send_gold_gift_520_following(self):
        """
        测试关注主播情况下送出520个金币礼物
        :return:
        """
        test_data = {'gift_gold':self.gift_gold,'gift_diamond':0,'gift_id':self.gift_id,'gift_num':520,'is_following':True}
        self.send_gift_action(**test_data)

    def test_send_gold_gift_1314_following(self):
        """
        测试关注主播情况下送出1314个金币礼物
        :return:
        """
        test_data = {'gift_gold':self.gift_gold,'gift_diamond':0,'gift_id':self.gift_id,'gift_num':1314,'is_following':True}
        self.send_gift_action(**test_data)

    def tearDown(self,*args):
        super(TestFollowingSendGift,self).tearDown(user_id=self.user_id,anchor_id=self.anchor_id)
        TearDown().send_gift_teardown(login_name=self.login_name, anchor_id=self.anchor_id, user_id=self.user_id,room_id=self.room_id)