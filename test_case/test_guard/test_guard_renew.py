# -*- coding:utf-8 -*-
from test_case.test_guard.action import GuardAction
from utilities.teardown import TearDown

class TestBuyGuardRenewApi(GuardAction):
    """
    守护续费
    """


    def setUp(self,*args):
        super(TestBuyGuardRenewApi,self).setUp(user_id=self.user_id,anchor_id=self.anchor_id)
        TearDown().guard_teardown(login_name=self.login_name,user_id=self.user_id,anchor_id=self.anchor_id)

    def test_bronze_renew_bronze(self):
        """
        测试青铜守护续费青铜守护
        :return:
        """
        test_data = {'guard_price':1176000,'first_guard_id':1,'second_guard_id':1,'following':False,'user_rank':11,'sun_max_num':60,
                     'anchor_rank':5,'guard_rank':2,'expire_time_num':range(58,63)}
        self.renew_action(**test_data)

    def test_bronze_renew_silver(self):
        """
        测试青铜守护续费白银守护
        :return:
        """
        test_data = {'guard_price':1764000,'first_guard_id':1,'second_guard_id':2,'following':False,'user_rank':11,'sun_max_num':60,
                     'anchor_rank':5,'guard_rank':3,'expire_time_num':range(89,94)}
        self.renew_action(**test_data)

    def test_bronze_renew_gold_three(self):
        """
        测试青铜守护续费三个月黄金守护
        :return:
        """
        test_data = {'guard_price':2352000,'first_guard_id':1,'second_guard_id':3,'following':False,'user_rank':12,'sun_max_num':65,
                     'anchor_rank':6,'guard_rank':3,'expire_time_num':range(120,125)}
        self.renew_action(**test_data)

    def test_bronze_renew_gold_six(self):
        """
        测试青铜守护续费六个月黄金守护
        :return:
        """
        test_data = {'guard_price':4116000,'first_guard_id':1,'second_guard_id':6,'following':False,'user_rank':13,'sun_max_num':65,
                     'anchor_rank':7,'guard_rank':3,'expire_time_num':range(214,218)}
        self.renew_action(**test_data)

    def test_bronze_renew_diamond_one(self):
        """
        测试青铜守护续费一年钻石守护
        :return:
        """
        test_data = {'guard_price':7644000,'first_guard_id':1,'second_guard_id':12,'following':False,'user_rank':15,'sun_max_num':70,
                     'anchor_rank':7,'guard_rank':4,'expire_time_num':range(398,404)}
        self.renew_action(**test_data)

    def test_bronze_renew_diamond_two(self):
        """
        测试青铜守护续费两年钻石守护
        :return:
        """
        test_data = {'guard_price':14700000,'first_guard_id':1,'second_guard_id':13,'following':False,'user_rank':16,'sun_max_num':75,
                     'anchor_rank':9,'guard_rank':4,'expire_time_num':range(769,776)}
        self.renew_action(**test_data)

    def test_silver_renew_bronze(self):
        """
        测试白银守护续费青铜守护
        :return:
        """
        test_data = {'guard_price':1764000,'first_guard_id':2,'second_guard_id':1,'following':False,'user_rank':11,'sun_max_num':60,
                     'anchor_rank':5,'guard_rank':3,'expire_time_num':range(89,94)}
        self.renew_action(**test_data)

    def test_silver_renew_silver(self):
        """
        测试白银守护续费白银守护
        :return:
        """
        test_data = {'guard_price':2352000,'first_guard_id':2,'second_guard_id':2,'following':False,'user_rank':12,'sun_max_num':65,
                     'anchor_rank':6,'guard_rank':3,'expire_time_num':range(120,125)}
        self.renew_action(**test_data)

    def test_silver_renew_gold_three(self):
        """
        测试白银守护续费三个月黄金守护
        :return:
        """
        test_data = {'guard_price':2940000,'first_guard_id':2,'second_guard_id':3,'following':False,'user_rank':12,'sun_max_num':65,
                     'anchor_rank':6,'guard_rank':3,'expire_time_num':range(152,156)}
        self.renew_action(**test_data)

    def test_silver_renew_gold_six(self):
        """
        测试白银守护续费六个月黄金守护
        :return:
        """
        test_data = {'guard_price':4704000,'first_guard_id':2,'second_guard_id':6,'following':False,'user_rank':13,'sun_max_num':65,
                     'anchor_rank':7,'guard_rank':3,'expire_time_num':range(245,249)}
        self.renew_action(**test_data)

    def test_silver_renew_diamond_one(self):
        """
        测试白银守护续费一年钻石守护
        :return:
        """
        test_data = {'guard_price':8232000,'first_guard_id':2,'second_guard_id':12,'following':False,'user_rank':15,'sun_max_num':70,
                     'anchor_rank':8,'guard_rank':4,'expire_time_num':range(430,435)}
        self.renew_action(**test_data)

    def test_silver_renew_diamond_two(self):
        """
        测试白银守护续费两年钻石守护
        :return:
        """
        test_data = {'guard_price':15288000,'first_guard_id':2,'second_guard_id':13,'following':False,'user_rank':17,'sun_max_num':75,
                     'anchor_rank':9,'guard_rank':4,'expire_time_num':range(801,807)}
        self.renew_action(**test_data)

    def test_gold_three_renew_bronze(self):
        """
        测试三个月黄金守护续费青铜守护
        :return:
        """
        test_data = {'guard_price':2352000,'first_guard_id':3,'second_guard_id':1,'following':False,'user_rank':12,'sun_max_num':65,
                     'anchor_rank':6,'guard_rank':3,'expire_time_num':range(120,125)}
        self.renew_action(**test_data)

    def test_gold_three_renew_silver(self):
        """
        测试三个月黄金守护续费白银守护
        :return:
        """
        test_data = {'guard_price':2940000,'first_guard_id':3,'second_guard_id':2,'following':False,'user_rank':12,'sun_max_num':65,
                     'anchor_rank':6,'guard_rank':3,'expire_time_num':range(151,156)}
        self.renew_action(**test_data)

    def test_gold_three_renew_gold_three(self):
        """
        测试三个月黄金守护续费三个月黄金守护
        :return:
        """
        test_data = {'guard_price':3528000,'first_guard_id':3,'second_guard_id':3,'following':False,'user_rank':13,'sun_max_num':65,
                     'anchor_rank':6,'guard_rank':3,'expire_time_num':range(182,187)}
        self.renew_action(**test_data)

    def test_gold_three_renew_gold_six(self):
        """
        测试三个月黄金守护续费六个月黄金守护
        :return:
        """
        test_data = {'guard_price':5292000,'first_guard_id':3,'second_guard_id':6,'following':False,'user_rank':14,'sun_max_num':70,
                     'anchor_rank':7,'guard_rank':3,'expire_time_num':range(275,280)}
        self.renew_action(**test_data)

    def test_gold_three_renew_diamond_one(self):
        """
        测试三个月黄金守护续费一年钻石守护
        :return:
        """
        test_data = {'guard_price':8820000,'first_guard_id':3,'second_guard_id':12,'following':False,'user_rank':15,'sun_max_num':70,
                     'anchor_rank':8,'guard_rank':4,'expire_time_num':range(460,466)}
        self.renew_action(**test_data)

    def test_gold_three_renew_diamond_two(self):
        """
        测试三个月黄金守护续费两年钻石守护
        :return:
        """
        test_data = {'guard_price':15876000,'first_guard_id':3,'second_guard_id':13,'following':False,'user_rank':17,'sun_max_num':75,
                     'anchor_rank':9,'guard_rank':4,'expire_time_num':range(833,838)}
        self.renew_action(**test_data)

    def test_gold_six_renew_bronze(self):
        """
        测试六个月黄金守护续费青铜守护
        :return:
        """
        test_data = {'guard_price':4116000,'first_guard_id':6,'second_guard_id':1,'following':False,'user_rank':13,'sun_max_num':65,
                     'anchor_rank':7,'guard_rank':3,'expire_time_num':range(213,218)}
        self.renew_action(**test_data)

    def test_gold_six_renew_silver(self):
        """
        测试六个月黄金守护续费白银守护
        :return:
        """
        test_data = {'guard_price':4704000,'first_guard_id':6,'second_guard_id':2,'following':False,'user_rank':13,'sun_max_num':65,
                     'anchor_rank':7,'guard_rank':3,'expire_time_num':range(243,249)}
        self.renew_action(**test_data)

    def test_gold_six_renew_gold_three(self):
        """
        测试六个月黄金守护续费三个月黄金守护
        :return:
        """
        test_data = {'guard_price':5292000,'first_guard_id':6,'second_guard_id':3,'following':False,'user_rank':14,'sun_max_num':70,
                     'anchor_rank':7,'guard_rank':3,'expire_time_num':range(276,282)}
        self.renew_action(**test_data)

    def test_gold_six_renew_gold_six(self):
        """
        测试六个月黄金守护续费六个月黄金守护
        :return:
        """
        test_data = {'guard_price':7056000,'first_guard_id':6,'second_guard_id':6,'following':False,'user_rank':14,'sun_max_num':70,
                     'anchor_rank':7,'guard_rank':3,'expire_time_num':range(368,373)}
        self.renew_action(**test_data)

    def test_gold_six_renew_diamond_one(self):
        """
        测试六个月黄金守护续费一年钻石守护
        :return:
        """
        test_data = {'guard_price':10584000,'first_guard_id':6,'second_guard_id':12,'following':False,'user_rank':16,'sun_max_num':75,
                     'anchor_rank':8,'guard_rank':4,'expire_time_num':range(555,560)}
        self.renew_action(**test_data)

    def test_gold_six_renew_diamond_two(self):
        """
        测试六个月黄金守护续费两年钻石守护
        :return:
        """
        test_data = {'guard_price':17640000,'first_guard_id':6,'second_guard_id':13,'following':False,'user_rank':17,'sun_max_num':75,
                     'anchor_rank':9,'guard_rank':4,'expire_time_num':range(925,935)}
        self.renew_action(**test_data)

    def test_diamond_one_renew_bronze(self):
        """
        测试一年钻石守护续费青铜守护
        :return:
        """
        test_data = {'guard_price': 7644000, 'first_guard_id': 12, 'second_guard_id': 1, 'following': False,
                     'user_rank': 15, 'sun_max_num': 70,
                     'anchor_rank': 7, 'guard_rank': 4, 'expire_time_num': range(400,404)}
        self.renew_action(**test_data)

    def test_diamond_one_renew_silver(self):
        """
        测试一年钻石守护续费白银守护
        :return:
        """
        test_data = {'guard_price': 8232000, 'first_guard_id': 12, 'second_guard_id': 2, 'following': False,
                     'user_rank': 15, 'sun_max_num': 70,
                     'anchor_rank': 8, 'guard_rank': 4, 'expire_time_num': range(430,435)}
        self.renew_action(**test_data)

    def test_diamond_one_renew_gold_three(self):
        """
        测试一年钻石守护续费三个月黄金守护
        :return:
        """
        test_data = {'guard_price': 8820000, 'first_guard_id': 12, 'second_guard_id': 3, 'following': False,
                     'user_rank': 15, 'sun_max_num': 70,
                     'anchor_rank': 8, 'guard_rank': 4, 'expire_time_num': range(461,467)}
        self.renew_action(**test_data)

    def test_diamond_one_renew_gold_six(self):
        """
        测试一年钻石守护续费六个月黄金守护
        :return:
        """
        test_data = {'guard_price': 10584000, 'first_guard_id': 12, 'second_guard_id': 6, 'following': False,
                     'user_rank': 16, 'sun_max_num': 75,
                     'anchor_rank': 8, 'guard_rank': 4, 'expire_time_num': range(555,560)}
        self.renew_action(**test_data)

    def test_diamond_one_renew_diamond_one(self):
        """
        测试一年钻石守护续费一年钻石守护
        :return:
        """
        test_data = {'guard_price': 14112000, 'first_guard_id': 12, 'second_guard_id': 12, 'following': False,
                     'user_rank': 16, 'sun_max_num': 75,
                     'anchor_rank': 9, 'guard_rank': 4, 'expire_time_num': range(740,746)}
        self.renew_action(**test_data)

    def test_diamond_one_renew_diamond_two(self):
        """
        测试一年钻石守护续费两年钻石守护
        :return:
        """
        test_data = {'guard_price': 21168000, 'first_guard_id': 12, 'second_guard_id': 13, 'following': False,
                     'user_rank': 18, 'sun_max_num': 80,
                     'anchor_rank': 10, 'guard_rank': 4, 'expire_time_num': range(1110,1119)}
        self.renew_action(**test_data)

    def test_diamond_two_renew_bronze(self):
        """
        测试两年钻石守护续费青铜守护
        :return:
        """
        test_data = {'guard_price': 14700000, 'first_guard_id': 13, 'second_guard_id': 1, 'following': False,
                     'user_rank': 16, 'sun_max_num': 75,
                     'anchor_rank': 9, 'guard_rank': 4, 'expire_time_num': range(772,776)}
        self.renew_action(**test_data)

    def test_diamond_two_renew_silver(self):
        """
        测试两年钻石守护续费白银守护
        :return:
        """
        test_data = {'guard_price': 15288000, 'first_guard_id': 13, 'second_guard_id': 2, 'following': False,
                     'user_rank': 17, 'sun_max_num': 75,
                     'anchor_rank': 9, 'guard_rank': 4, 'expire_time_num': range(802,808)}
        self.renew_action(**test_data)

    def test_diamond_two_renew_gold_three(self):
        """
        测试两年钻石守护续费三个月黄金守护
        :return:
        """
        test_data = {'guard_price': 15876000, 'first_guard_id': 13, 'second_guard_id': 3, 'following': False,
                     'user_rank': 17, 'sun_max_num': 75,
                     'anchor_rank': 9, 'guard_rank': 4, 'expire_time_num': range(835,839)}
        self.renew_action(**test_data)

    def test_diamond_two_renew_gold_six(self):
        """
        测试两年钻石守护续费六个月黄金守护
        :return:
        """
        test_data = {'guard_price': 17640000, 'first_guard_id': 13, 'second_guard_id': 6, 'following': False,
                     'user_rank': 17, 'sun_max_num': 75,
                     'anchor_rank': 9, 'guard_rank': 4, 'expire_time_num': range(928,932)}
        self.renew_action(**test_data)

    def test_diamond_two_renew_diamond_one(self):
        """
        测试两年钻石守护续费一年钻石守护
        :return:
        """
        test_data = {'guard_price': 21168000, 'first_guard_id': 13, 'second_guard_id': 12, 'following': False,
                     'user_rank': 18, 'sun_max_num': 80,
                     'anchor_rank': 10, 'guard_rank': 4, 'expire_time_num': range(1114,1118)}
        self.renew_action(**test_data)

    def test_diamond_two_renew_diamond_two(self):
        """
        测试两年钻石守护续费两年钻石守护
        :return:
        """
        test_data = {'guard_price': 28224000, 'first_guard_id': 13, 'second_guard_id': 13, 'following': False,
                     'user_rank': 18, 'sun_max_num': 80,
                     'anchor_rank': 10, 'guard_rank': 4, 'expire_time_num': range(1486,1490)}
        self.renew_action(**test_data)

    def tearDown(self,*args):
        super(TestBuyGuardRenewApi,self).tearDown(user_id=self.user_id,anchor_id=self.anchor_id)
        TearDown().guard_teardown(login_name=self.login_name,user_id=self.user_id,anchor_id=self.anchor_id)