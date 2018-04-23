# -*- coding:utf-8 -*-
from test_case.test_noble.action import NobleAction
from utilities.teardown import TearDown
import time



class TestBuyNoble(NobleAction):
    """
    购买贵族
    """
    one_month = range(28,32)
    two_month = range(58,63)
    three_month = range(88,93)
    six_month = range(178,186)

    def setUp(self,*args):
        super(TestBuyNoble,self).setUp(user_id=self.user_id)
        TearDown().noble_teardown(user_id=self.user_id)

    def test_buy_knight_one(self):
        """
        测试购买一个月骑士
        :return:
        """
        test_data = {'noble_price':24000,'noble_time':1,'noble_id':1,'user_rank':1,'noble_rest_time_int':self.one_month,'user_exp':24000}
        self.buy_noble_action(**test_data)

    def test_buy_knight_two(self):
        """
        测试购买两个月骑士
        :return:
        """
        test_data = {'noble_price':48000,'noble_time':2,'noble_id':1,'user_rank':1,'noble_rest_time_int':self.two_month,'user_exp':48000}
        self.buy_noble_action(**test_data)

    def test_buy_knight_three(self):
        """
        测试购买三个月骑士
        :return:
        """
        test_data = {'noble_price':72000,'noble_time':3,'noble_id':1,'user_rank':2,'noble_rest_time_int':self.three_month,'user_exp':22000}
        self.buy_noble_action(**test_data)

    def test_buy_knight_six(self):
        """
        测试购买六个月骑士
        :return:
        """
        test_data = {'noble_price':144000,'noble_time':6,'noble_id':1,'user_rank':3,'noble_rest_time_int':self.six_month,'user_exp':44000}
        self.buy_noble_action(**test_data)

    def test_buy_baron_one(self):
        """
        测试购买一个月男爵
        :return:
        """
        test_data = {'noble_price':40000,'noble_time':1,'noble_id':2,'user_rank':1,'noble_rest_time_int':self.one_month,'user_exp':40000}
        self.buy_noble_action(**test_data)

    def test_buy_baron_two(self):
        """
        测试购买两个月男爵
        :return:
        """
        test_data = {'noble_price':80000,'noble_time':2,'noble_id':2,'user_rank':2,'noble_rest_time_int':self.two_month,'user_exp':30000}
        self.buy_noble_action(**test_data)

    def test_buy_baron_three(self):
        """
        测试购买三个月男爵
        :return:
        """
        test_data = {'noble_price':120000,'noble_time':3,'noble_id':2,'user_rank':3,'noble_rest_time_int':self.three_month,'user_exp':20000}
        self.buy_noble_action(**test_data)

    def test_buy_baron_six(self):
        """
        测试购买六个月男爵
        :return:
        """
        test_data = {'noble_price':240000,'noble_time':6,'noble_id':2,'user_rank':5,'noble_rest_time_int':self.six_month,'user_exp':40000}
        self.buy_noble_action(**test_data)

    def test_buy_viscount_one(self):
        """
        测试购买一个月子爵
        :return:
        """
        test_data = {'noble_price':80000,'noble_time':1,'noble_id':3,'user_rank':2,'noble_rest_time_int':self.one_month,'user_exp':30000}
        self.buy_noble_action(**test_data)

    def test_buy_viscount_two(self):
        """
        测试购买两个月子爵
        :return:
        """
        test_data = {'noble_price':160000,'noble_time':2,'noble_id':3,'user_rank':4,'noble_rest_time_int':self.two_month,'user_exp':10000}
        self.buy_noble_action(**test_data)

    def test_buy_viscount_three(self):
        """
        测试购买三个月子爵
        :return:
        """
        test_data = {'noble_price':240000,'noble_time':3,'noble_id':3,'user_rank':5,'noble_rest_time_int':self.three_month,'user_exp':40000}
        self.buy_noble_action(**test_data)

    def test_buy_viscount_six(self):
        """
        测试购买六个月子爵
        :return:
        """
        test_data = {'noble_price':480000,'noble_time':6,'noble_id':3,'user_rank':8,'noble_rest_time_int':self.six_month,'user_exp':80000}
        self.buy_noble_action(**test_data)

    def test_buy_earl_one(self):
        """
        测试购买一个月伯爵
        :return:
        """
        test_data = {'noble_price':400000,'noble_time':1,'noble_id':4,'user_rank':8,'noble_rest_time_int':self.one_month,'user_exp':0}
        self.buy_noble_action(**test_data)

    def test_buy_earl_two(self):
        """
        测试购买两个月伯爵
        :return:
        """
        test_data = {'noble_price':800000,'noble_time':2,'noble_id':4,'user_rank':10,'noble_rest_time_int':self.two_month,'user_exp':50000}
        self.buy_noble_action(**test_data)

    def test_buy_earl_three(self):
        """
        测试购买三个月伯爵
        :return:
        """
        test_data = {'noble_price':1200000,'noble_time':3,'noble_id':4,'user_rank':11,'noble_rest_time_int':self.three_month,'user_exp':200000}
        self.buy_noble_action(**test_data)

    def test_buy_earl_six(self):
        """
        测试购买六个月伯爵
        :return:
        """
        test_data = {'noble_price':2400000,'noble_time':6,'noble_id':4,'user_rank':12,'noble_rest_time_int':self.six_month,'user_exp':400000}
        self.buy_noble_action(**test_data)

    def test_buy_marquis_one(self):
        """
        测试购买一个月侯爵
        :return:
        """
        test_data = {'noble_price':800000,'noble_time':1,'noble_id':5,'user_rank':10,'noble_rest_time_int':self.one_month,'user_exp':50000}
        self.buy_noble_action(**test_data)

    def test_buy_marquis_two(self):
        """
        测试购买两个月侯爵
        :return:
        """
        test_data = {'noble_price':1600000,'noble_time':2,'noble_id':5,'user_rank':11,'noble_rest_time_int':self.two_month,'user_exp':600000}
        self.buy_noble_action(**test_data)

    def test_buy_marquis_three(self):
        """
        测试购买三个月侯爵
        :return:
        """
        test_data = {'noble_price':2400000,'noble_time':3,'noble_id':5,'user_rank':12,'noble_rest_time_int':self.three_month,'user_exp':400000}
        self.buy_noble_action(**test_data)

    def test_buy_marquis_six(self):
        """
        测试购买六个月侯爵
        :return:
        """
        test_data = {'noble_price':4800000,'noble_time':6,'noble_id':5,'user_rank':13,'noble_rest_time_int':self.six_month,'user_exp':1300000}
        self.buy_noble_action(**test_data)

    def test_buy_duck_one(self):
        """
        测试购买一个月公爵
        :return:
        """
        test_data = {'noble_price':2400000,'noble_time':1,'noble_id':6,'user_rank':12,'noble_rest_time_int':self.one_month,'user_exp':400000}
        self.buy_noble_action(**test_data)

    def test_buy_duck_two(self):
        """
        测试购买两个月公爵
        :return:
        """
        test_data = {'noble_price':4800000,'noble_time':2,'noble_id':6,'user_rank':13,'noble_rest_time_int':self.two_month,'user_exp':1300000}
        self.buy_noble_action(**test_data)

    def test_buy_duck_three(self):
        """
        测试购买三个月公爵
        :return:
        """
        test_data = {'noble_price':7200000,'noble_time':3,'noble_id':6,'user_rank':14,'noble_rest_time_int':self.three_month,'user_exp':2200000}
        self.buy_noble_action(**test_data)

    def test_buy_duck_six(self):
        """
        测试购买六个月公爵
        :return:
        """
        test_data = {'noble_price':14400000,'noble_time':6,'noble_id':6,'user_rank':16,'noble_rest_time_int':self.six_month,'user_exp':4400000}
        self.buy_noble_action(**test_data)

    def test_buy_monarch_one(self):
        """
        测试购买一个月帝王
        :return:
        """
        test_data = {'noble_price':24000000,'noble_time':1,'noble_id':7,'user_rank':18,'noble_rest_time_int':self.one_month,'user_exp':4000000}
        self.buy_noble_action(**test_data)

    def test_buy_monarch_two(self):
        """
        测试购买两个月帝王
        :return:
        """
        test_data = {'noble_price':48000000,'noble_time':2,'noble_id':7,'user_rank':19,'noble_rest_time_int':self.two_month,'user_exp':13000000}
        self.buy_noble_action(**test_data)

    def test_buy_monarch_three(self):
        """
        测试购买三个月帝王
        :return:
        """
        test_data = {'noble_price':72000000,'noble_time':3,'noble_id':7,'user_rank':21,'noble_rest_time_int':self.three_month,'user_exp':7000000}
        self.buy_noble_action(**test_data)

    def test_buy_monarch_six(self):
        """
        测试购买六个月帝王
        :return:
        """
        test_data = {'noble_price':144000000,'noble_time':6,'noble_id':7,'user_rank':24,'noble_rest_time_int':self.six_month,'user_exp':24000000}
        self.buy_noble_action(**test_data)

    def tearDown(self,*args):
        super(TestBuyNoble,self).tearDown(user_id=self.user_id)
        TearDown().noble_teardown(user_id=self.user_id)