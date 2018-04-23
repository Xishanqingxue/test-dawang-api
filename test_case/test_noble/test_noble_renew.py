# -*- coding:utf-8 -*-
from test_case.test_noble.action import NobleAction
from utilities.teardown import TearDown



class TestBuyNobleRenew(NobleAction):
    """
    贵族续费
    """


    def setUp(self,*args):
        super(TestBuyNobleRenew,self).setUp(user_id=self.user_id)
        TearDown().noble_teardown(user_id=self.user_id)


    def test_renew_noble_knight_to_knight(self):
        """
        测试骑士续费骑士
        :return:
        """
        test_data = {'noble_price':42000,'first_noble_id':1,'second_noble_id':1,'user_rank':1}
        self.renew_noble_action(**test_data)

    def test_renew_noble_knight_to_baron(self):
        """
        测试骑士续费男爵
        :return:
        """
        test_data = {'noble_price':64000,'first_noble_id':1,'second_noble_id':2,'user_rank':2}
        self.renew_noble_action(**test_data)

    def test_renew_noble_knight_to_viscount(self):
        """
        测试骑士续费子爵
        :return:
        """
        test_data = {'noble_price':104000,'first_noble_id':1,'second_noble_id':3,'user_rank':3}
        self.renew_noble_action(**test_data)

    def test_renew_noble_knight_to_earl(self):
        """
        测试骑士续费伯爵
        :return:
        """
        test_data = {'noble_price':424000,'first_noble_id':1,'second_noble_id':4,'user_rank':8}
        self.renew_noble_action(**test_data)

    def test_renew_noble_knight_to_marquis(self):
        """
        测试骑士续费侯爵
        :return:
        """
        test_data = {'noble_price':824000,'first_noble_id':1,'second_noble_id':5,'user_rank':10}
        self.renew_noble_action(**test_data)

    def test_renew_noble_knight_to_duck(self):
        """
        测试骑士续费公爵
        :return:
        """
        test_data = {'noble_price':2424000,'first_noble_id':1,'second_noble_id':6,'user_rank':12}
        self.renew_noble_action(**test_data)

    def test_renew_noble_knight_to_monarch(self):
        """
        测试骑士续费帝王
        :return:
        """
        test_data = {'noble_price':24024000,'first_noble_id':1,'second_noble_id':7,'user_rank':18}
        self.renew_noble_action(**test_data)

    def test_renew_noble_baron_to_knight(self):
        """
        测试男爵续费骑士
        :return:
        """
        test_data = {'noble_price':40000,'first_noble_id':2,'second_noble_id':1,'user_rank':1}
        self.renew_noble_action(**test_data)

    def test_renew_noble_baron_to_baron(self):
        """
        测试男爵续费男爵
        :return:
        """
        test_data = {'noble_price':70000,'first_noble_id':2,'second_noble_id':2,'user_rank':2}
        self.renew_noble_action(**test_data)

    def test_renew_noble_baron_to_viscount(self):
        """
        测试男爵续费子爵
        :return:
        """
        test_data = {'noble_price':120000,'first_noble_id':2,'second_noble_id':3,'user_rank':3}
        self.renew_noble_action(**test_data)

    def test_renew_noble_baron_to_earl(self):
        """
        测试男爵续费伯爵
        :return:
        """
        test_data = {'noble_price':440000,'first_noble_id':2,'second_noble_id':4,'user_rank':8}
        self.renew_noble_action(**test_data)

    def test_renew_noble_baron_to_marquis(self):
        """
        测试男爵续费侯爵
        :return:
        """
        test_data = {'noble_price':840000,'first_noble_id':2,'second_noble_id':5,'user_rank':10}
        self.renew_noble_action(**test_data)

    def test_renew_noble_baron_to_duck(self):
        """
        测试男爵续费公爵
        :return:
        """
        test_data = {'noble_price':2440000,'first_noble_id':2,'second_noble_id':6,'user_rank':12}
        self.renew_noble_action(**test_data)

    def test_renew_noble_baron_to_monarch(self):
        """
        测试男爵续费帝王
        :return:
        """
        test_data = {'noble_price':24040000,'first_noble_id':2,'second_noble_id':7,'user_rank':18}
        self.renew_noble_action(**test_data)

    def test_renew_noble_viscount_to_knight(self):
        """
        测试子爵续费骑士
        :return:
        """
        test_data = {'noble_price':80000,'first_noble_id':3,'second_noble_id':1,'user_rank':2}
        self.renew_noble_action(**test_data)

    def test_renew_noble_viscount_to_baron(self):
        """
        测试子爵续费男爵
        :return:
        """
        test_data = {'noble_price':80000,'first_noble_id':3,'second_noble_id':2,'user_rank':2}
        self.renew_noble_action(**test_data)

    def test_renew_noble_viscount_to_viscount(self):
        """
        测试子爵续费子爵
        :return:
        """
        test_data = {'noble_price':140000,'first_noble_id':3,'second_noble_id':3,'user_rank':3}
        self.renew_noble_action(**test_data)

    def test_renew_noble_viscount_to_earl(self):
        """
        测试子爵续费伯爵
        :return:
        """
        test_data = {'noble_price':480000,'first_noble_id':3,'second_noble_id':4,'user_rank':8}
        self.renew_noble_action(**test_data)

    def test_renew_noble_viscount_to_marquis(self):
        """
        测试子爵续费侯爵
        :return:
        """
        test_data = {'noble_price':880000,'first_noble_id':3,'second_noble_id':5,'user_rank':10}
        self.renew_noble_action(**test_data)

    def test_renew_noble_viscount_to_duck(self):
        """
        测试子爵续费公爵
        :return:
        """
        test_data = {'noble_price':2480000,'first_noble_id':3,'second_noble_id':6,'user_rank':12}
        self.renew_noble_action(**test_data)

    def test_renew_noble_viscount_to_monarch(self):
        """
        测试子爵续费帝王
        :return:
        """
        test_data = {'noble_price':24080000,'first_noble_id':3,'second_noble_id':7,'user_rank':18}
        self.renew_noble_action(**test_data)

    def test_renew_noble_earl_to_knight(self):
        """
        测试伯爵续费骑士
        :return:
        """
        test_data = {'noble_price':400000,'first_noble_id':4,'second_noble_id':1,'user_rank':8}
        self.renew_noble_action(**test_data)

    def test_renew_noble_earl_to_baron(self):
        """
        测试伯爵续费男爵
        :return:
        """
        test_data = {'noble_price':400000,'first_noble_id':4,'second_noble_id':2,'user_rank':8}
        self.renew_noble_action(**test_data)

    def test_renew_noble_earl_to_viscount(self):
        """
        测试伯爵续费子爵
        :return:
        """
        test_data = {'noble_price':400000,'first_noble_id':4,'second_noble_id':3,'user_rank':8}
        self.renew_noble_action(**test_data)

    def test_renew_noble_earl_to_earl(self):
        """
        测试伯爵续费伯爵
        :return:
        """
        test_data = {'noble_price':700000,'first_noble_id':4,'second_noble_id':4,'user_rank':9}
        self.renew_noble_action(**test_data)

    def test_renew_noble_earl_to_marquis(self):
        """
        测试伯爵续费侯爵
        :return:
        """
        test_data = {'noble_price':1200000,'first_noble_id':4,'second_noble_id':5,'user_rank':11}
        self.renew_noble_action(**test_data)

    def test_renew_noble_earl_to_duck(self):
        """
        测试伯爵续费公爵
        :return:
        """
        test_data = {'noble_price':2800000,'first_noble_id':4,'second_noble_id':6,'user_rank':12}
        self.renew_noble_action(**test_data)

    def test_renew_noble_earl_to_monarch(self):
        """
        测试伯爵续费帝王
        :return:
        """
        test_data = {'noble_price':24400000,'first_noble_id':4,'second_noble_id':7,'user_rank':18}
        self.renew_noble_action(**test_data)

    def test_renew_noble_marquis_to_knight(self):
        """
        测试侯爵续费骑士
        :return:
        """
        test_data = {'noble_price':800000,'first_noble_id':5,'second_noble_id':1,'user_rank':10}
        self.renew_noble_action(**test_data)

    def test_renew_noble_marquis_to_baron(self):
        """
        测试侯爵续费男爵
        :return:
        """
        test_data = {'noble_price':800000,'first_noble_id':5,'second_noble_id':2,'user_rank':10}
        self.renew_noble_action(**test_data)

    def test_renew_noble_marquis_to_viscount(self):
        """
        测试侯爵续费子爵
        :return:
        """
        test_data = {'noble_price':800000,'first_noble_id':5,'second_noble_id':3,'user_rank':10}
        self.renew_noble_action(**test_data)

    def test_renew_noble_marquis_to_earl(self):
        """
        测试侯爵续费伯爵
        :return:
        """
        test_data = {'noble_price':800000,'first_noble_id':5,'second_noble_id':4,'user_rank':10}
        self.renew_noble_action(**test_data)

    def test_renew_noble_marquis_to_marquis(self):
        """
        测试侯爵续费侯爵
        :return:
        """
        test_data = {'noble_price':1400000,'first_noble_id':5,'second_noble_id':5,'user_rank':11}
        self.renew_noble_action(**test_data)

    def test_renew_noble_marquis_to_duck(self):
        """
        测试侯爵续费公爵
        :return:
        """
        test_data = {'noble_price':3200000,'first_noble_id':5,'second_noble_id':6,'user_rank':12}
        self.renew_noble_action(**test_data)

    def test_renew_noble_marquis_to_monarch(self):
        """
        测试侯爵续费帝王
        :return:
        """
        test_data = {'noble_price':24800000,'first_noble_id':5,'second_noble_id':7,'user_rank':18}
        self.renew_noble_action(**test_data)

    def test_renew_noble_duck_to_knight(self):
        """
        测试公爵续费骑士
        :return:
        """
        test_data = {'noble_price':2400000,'first_noble_id':6,'second_noble_id':1,'user_rank':12}
        self.renew_noble_action(**test_data)

    def test_renew_noble_duck_to_baron(self):
        """
        测试公爵续费男爵
        :return:
        """
        test_data = {'noble_price':2400000,'first_noble_id':6,'second_noble_id':2,'user_rank':12}
        self.renew_noble_action(**test_data)

    def test_renew_noble_duck_to_viscount(self):
        """
        测试公爵续费子爵
        :return:
        """
        test_data = {'noble_price':2400000,'first_noble_id':6,'second_noble_id':3,'user_rank':12}
        self.renew_noble_action(**test_data)

    def test_renew_noble_duck_to_earl(self):
        """
        测试公爵续费伯爵
        :return:
        """
        test_data = {'noble_price':2400000,'first_noble_id':6,'second_noble_id':4,'user_rank':12}
        self.renew_noble_action(**test_data)

    def test_renew_noble_duck_to_marquis(self):
        """
        测试公爵续费侯爵
        :return:
        """
        test_data = {'noble_price':2400000,'first_noble_id':6,'second_noble_id':5,'user_rank':12}
        self.renew_noble_action(**test_data)

    def test_renew_noble_duck_to_duck(self):
        """
        测试公爵续费公爵
        :return:
        """
        test_data = {'noble_price':4200000,'first_noble_id':6,'second_noble_id':6,'user_rank':13}
        self.renew_noble_action(**test_data)

    def test_renew_noble_duck_to_monarch(self):
        """
        测试公爵续费帝王
        :return:
        """
        test_data = {'noble_price':26400000,'first_noble_id':6,'second_noble_id':7,'user_rank':18}
        self.renew_noble_action(**test_data)

    def test_renew_noble_monarch_to_knight(self):
        """
        测试帝王续费骑士
        :return:
        """
        test_data = {'noble_price':24000000,'first_noble_id':7,'second_noble_id':1,'user_rank':18}
        self.renew_noble_action(**test_data)

    def test_renew_noble_monarch_to_baron(self):
        """
        测试帝王续费男爵
        :return:
        """
        test_data = {'noble_price':24000000,'first_noble_id':7,'second_noble_id':2,'user_rank':18}
        self.renew_noble_action(**test_data)

    def test_renew_noble_monarch_to_viscount(self):
        """
        测试帝王续费子爵
        :return:
        """
        test_data = {'noble_price':24000000,'first_noble_id':7,'second_noble_id':3,'user_rank':18}
        self.renew_noble_action(**test_data)

    def test_renew_noble_monarch_to_earl(self):
        """
        测试帝王续费伯爵
        :return:
        """
        test_data = {'noble_price':24000000,'first_noble_id':7,'second_noble_id':4,'user_rank':18}
        self.renew_noble_action(**test_data)

    def test_renew_noble_monarch_to_marquis(self):
        """
        测试帝王续费侯爵
        :return:
        """
        test_data = {'noble_price':24000000,'first_noble_id':7,'second_noble_id':5,'user_rank':18}
        self.renew_noble_action(**test_data)

    def test_renew_noble_monarch_to_duck(self):
        """
        测试帝王续费公爵
        :return:
        """
        test_data = {'noble_price':24000000,'first_noble_id':7,'second_noble_id':6,'user_rank':18}
        self.renew_noble_action(**test_data)

    def test_renew_noble_monarch_to_monarch(self):
        """
        测试帝王续费帝王
        :return:
        """
        test_data = {'noble_price':42000000,'first_noble_id':7,'second_noble_id':7,'user_rank':19}
        self.renew_noble_action(**test_data)

    def tearDown(self,*args):
        super(TestBuyNobleRenew,self).tearDown(user_id=self.user_id)
        TearDown().noble_teardown(user_id=self.user_id)