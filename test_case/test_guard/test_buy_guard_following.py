# -*- coding:utf-8 -*-
from utilities.teardown import TearDown
from test_case.test_guard.action import GuardAction



class TestBuyGuardApi(GuardAction):
    """
    购买守护(关注)
    """



    def setUp(self,*args):
        super(TestBuyGuardApi,self).setUp(user_id=self.user_id,anchor_id=self.anchor_id)
        TearDown().guard_teardown(login_name=self.login_name, user_id=self.user_id, anchor_id=self.anchor_id,following=True)

    def test_a_buy_guard_bronze_following(self):
        """
        测试关注主播情况下购买一个月青铜守护
        :return:
        """
        test_data = {'guard_id':1,'user_rank':9,'sun_max_num':60,'anchor_rank':4,'following':True}
        self.action(**test_data)

    def test_b_buy_guard_silver_following(self):
        """
        测试关注主播情况下购买两个月白银守护
        :return:
        """
        test_data = {'guard_id':2,'user_rank':11,'sun_max_num':60,'anchor_rank':5,'following':True}
        self.action(**test_data)

    def test_c_buy_guard_gold_three_following(self):
        """
        测试关注主播情况下购买三个月黄金守护
        :return:
        """
        test_data = {'guard_id': 3, 'user_rank': 11,  'sun_max_num': 60,'anchor_rank':5,'following':True}
        self.action(**test_data)

    def test_d_buy_guard_gold_six_following(self):
        """
        测试关注主播情况下购买六个月黄金守护
        :return:
        """
        test_data = {'guard_id': 6, 'user_rank': 13,'sun_max_num': 65,'anchor_rank':6,'following':True}
        self.action(**test_data)

    def test_e_buy_guard_diamond_one_following(self):
        """
        测试关注主播情况下购买一年钻石守护
        :return:
        """
        test_data = {'guard_id': 12, 'user_rank': 14,'sun_max_num': 70,'anchor_rank':7,'following':True}
        self.action(**test_data)

    def test_f_buy_guard_diamond_two_following(self):
        """
        测试关注主播情况下购买两年钻石守护
        :return:
        """
        test_data = {'guard_id': 13, 'user_rank': 16, 'sun_max_num': 75,'anchor_rank':9,'following':True}
        self.action(**test_data)

    def tearDown(self,*args):
        super(TestBuyGuardApi,self).tearDown(user_id=self.user_id,anchor_id=self.anchor_id)
        TearDown().guard_teardown(login_name=self.login_name,user_id=self.user_id,anchor_id=self.anchor_id,following=True)
