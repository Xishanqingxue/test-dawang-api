# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.my_military_api import MyMilitaryApi
from utilities.redis_helper import Redis,RedisHold
from utilities.mysql_helper import MysqlFix
import json,time,settings

class TestMyMilitaryApi(BaseCase):
    """
    我的军衔
    """
    user_mobile = settings.YULE_TEST_USER_LOGIN_NAME
    user_id = settings.YULE_TEST_USER_ID
    time_sleep = 0.3

    def fix_user_experience(self,rank,experience_all):
        MysqlFix(user_id=self.user_id).fix_user_rank_and_experience(user_rank=rank, experience_all=int(experience_all))
        RedisHold().clean_redis_user_detail(self.user_id)
        time.sleep(self.time_sleep)

    def flow_path(self,**kwargs):
            self.fix_user_experience(rank=kwargs['user_rank'],experience_all=kwargs['user_exp'])
            my_military_api = MyMilitaryApi(self.user_mobile)
            response = my_military_api.get()
            military = json.loads(response.content)['result']['military']

            self.assertEqual(my_military_api.get_code(),0)
            self.assertEqual(military['max_rank'],60)
            self.assertEqual(military['current_exp'],kwargs['current_exp'])
            self.assertEqual(military['next_rank'],kwargs['user_rank'] + 1)
            self.assertEqual(military['next_military_name'],kwargs['next_military_name'])
            self.assertEqual(military['level_up_exp'],kwargs['current_exp'])
            self.assertEqual(military['current_privilege'], kwargs['current_privilege'])
            self.assertEqual(military['next_privilege'], kwargs['next_privilege'])


    def test_a_get_my_military_soldier(self):
        """
        测试新兵-->准尉军衔
        :return:
        """
        test_data = {'user_rank':1,'user_exp':0,'current_level':u'新兵','current_exp':50000,
                     'current_privilege':50,'next_privilege':50,'next_military_name':u'列兵'}
        self.flow_path(**test_data)
        test_data = {'user_rank':2,'user_exp':50000,'current_level':u'列兵','current_exp':50000,
                     'current_privilege':50,'next_privilege':50,'next_military_name':u'下士'}
        self.flow_path(**test_data)
        test_data = {'user_rank':3,'user_exp':100000,'current_level':u'下士','current_exp':50000,
                     'current_privilege':50,'next_privilege':50,'next_military_name':u'中士'}
        self.flow_path(**test_data)
        test_data = {'user_rank':4,'user_exp':150000,'current_level':u'中士','current_exp':50000,
                     'current_privilege':50,'next_privilege':50,'next_military_name':u'上士'}
        self.flow_path(**test_data)
        test_data = {'user_rank':5,'user_exp':200000,'current_level':u'上士','current_exp':50000,
                     'current_privilege':50,'next_privilege':50,'next_military_name':u'准尉'}
        self.flow_path(**test_data)
        test_data = {'user_rank':6,'user_exp':250000,'current_level':u'准尉','current_exp':50000,
                     'current_privilege':50,'next_privilege':55,'next_military_name':u'1级少尉'}
        self.flow_path(**test_data)

    def test_get_my_military_acting_sublieutenant(self):
        """
        测试少尉军衔
        :return:
        """
        test_data = {'user_rank':7,'user_exp':300000,'current_level':u'1级少尉','current_exp':100000,
                     'current_privilege':55,'next_privilege':55,'next_military_name':u'2级少尉'}
        self.flow_path(**test_data)
        test_data = {'user_rank':8,'user_exp':400000,'current_level':u'2级少尉','current_exp':100000,
                     'current_privilege':55,'next_privilege':60,'next_military_name':u'1级中尉'}
        self.flow_path(**test_data)

    def test_get_my_military_lieutenant(self):
        """
        测试中尉军衔
        :return:
        """
        test_data = {'user_rank':9,'user_exp':500000,'current_level':u'1级中尉','current_exp':250000,
                     'current_privilege':60,'next_privilege':60,'next_military_name':u'2级中尉'}
        self.flow_path(**test_data)
        test_data = {'user_rank':10,'user_exp':750000,'current_level':u'2级中尉','current_exp':250000,
                     'current_privilege':60,'next_privilege':60,'next_military_name':u'3级中尉'}
        self.flow_path(**test_data)
        test_data = {'user_rank':11,'user_exp':1000000,'current_level':u'3级中尉','current_exp':1000000,
                     'current_privilege':60,'next_privilege':65,'next_military_name':u'1级上尉'}
        self.flow_path(**test_data)

    def test_get_my_military_captain(self):
        """
        测试上尉军衔
        :return:
        """
        test_data = {'user_rank':12,'user_exp':2000000,'current_level':u'1级上尉','current_exp':1500000,
                     'current_privilege':65,'next_privilege':65,'next_military_name':u'2级上尉'}
        self.flow_path(**test_data)
        test_data = {'user_rank':13,'user_exp':3500000,'current_level':u'2级上尉','current_exp':1500000,
                     'current_privilege':65,'next_privilege':70,'next_military_name':u'1级少校'}
        self.flow_path(**test_data)

    def test_get_my_military_squadron_leader(self):
        """
        测试少校军衔
        :return:
        """
        test_data = {'user_rank':14,'user_exp':5000000,'current_level':u'1级少校','current_exp':2500000,
                     'current_privilege':70,'next_privilege':70,'next_military_name':u'2级少校'}
        self.flow_path(**test_data)
        test_data = {'user_rank':15,'user_exp':7500000,'current_level':u'2级少校','current_exp':2500000,
                     'current_privilege':70,'next_privilege':75,'next_military_name':u'1级中校'}
        self.flow_path(**test_data)

    def test_get_my_military_lieutenant_colonel(self):
        """
        测试中校军衔
        :return:
        """
        test_data = {'user_rank':16,'user_exp':10000000,'current_level':u'1级中校','current_exp':5000000,
                     'current_privilege':75,'next_privilege':75,'next_military_name':u'2级中校'}
        self.flow_path(**test_data)
        test_data = {'user_rank':17,'user_exp':15000000,'current_level':u'2级中校','current_exp':5000000,
                     'current_privilege':75,'next_privilege':80,'next_military_name':u'1级上校'}
        self.flow_path(**test_data)

    def test_get_my_military_colonel(self):
        """
        测试上校军衔
        :return:
        """
        test_data = {'user_rank':18,'user_exp':20000000,'current_level':u'1级上校','current_exp':15000000,
                     'current_privilege':80,'next_privilege':80,'next_military_name':u'2级上校'}
        self.flow_path(**test_data)
        test_data = {'user_rank':19,'user_exp':35000000,'current_level':u'2级上校','current_exp':15000000,
                     'current_privilege':80,'next_privilege':90,'next_military_name':u'1级大校'}
        self.flow_path(**test_data)

    def test_get_my_military_senior_colonel(self):
        """
        测试大校军衔
        :return:
        """
        test_data = {'user_rank': 20, 'user_exp': 50000000, 'current_level': u'1级大校', 'current_exp': 15000000,
                     'current_privilege': 90, 'next_privilege': 90, 'next_military_name': u'2级大校'}
        self.flow_path(**test_data)
        test_data = {'user_rank': 21, 'user_exp': 65000000, 'current_level': u'2级大校', 'current_exp': 15000000,
                     'current_privilege': 90, 'next_privilege': 90, 'next_military_name': u'3级大校'}
        self.flow_path(**test_data)
        test_data = {'user_rank': 22, 'user_exp': 80000000, 'current_level': u'3级大校', 'current_exp': 20000000,
                     'current_privilege': 90, 'next_privilege': 100, 'next_military_name': u'1级少将'}
        self.flow_path(**test_data)

    def test_get_my_military_air_vice_marshal(self):
        """
        测试少将军衔
        :return:
        """
        test_data = {'user_rank': 23, 'user_exp': 100000000, 'current_level': u'1级少将', 'current_exp': 20000000,
                     'current_privilege': 100, 'next_privilege': 100, 'next_military_name': u'2级少将'}
        self.flow_path(**test_data)
        test_data = {'user_rank': 24, 'user_exp': 120000000, 'current_level': u'2级少将', 'current_exp': 40000000,
                     'current_privilege': 100, 'next_privilege': 100, 'next_military_name': u'3级少将'}
        self.flow_path(**test_data)
        test_data = {'user_rank': 25, 'user_exp': 160000000, 'current_level': u'3级少将', 'current_exp': 40000000,
                     'current_privilege': 100, 'next_privilege': 110, 'next_military_name': u'1级中将'}
        self.flow_path(**test_data)

    def test_get_my_military_lieutenant_general(self):
        """
        测试中将军衔
        :return:
        """
        test_data = {'user_rank': 26, 'user_exp': 200000000, 'current_level': u'1级中将', 'current_exp': 50000000,
                     'current_privilege': 110, 'next_privilege': 115, 'next_military_name': u'2级中将'}
        self.flow_path(**test_data)
        test_data = {'user_rank': 27, 'user_exp': 250000000, 'current_level': u'2级中将', 'current_exp': 50000000,
                     'current_privilege': 115, 'next_privilege': 120, 'next_military_name': u'3级中将'}
        self.flow_path(**test_data)
        test_data = {'user_rank': 28, 'user_exp': 300000000, 'current_level': u'3级中将', 'current_exp': 50000000,
                     'current_privilege': 120, 'next_privilege': 130, 'next_military_name': u'1级上将'}
        self.flow_path(**test_data)

    def test_get_my_military_general(self):
        """
        测试上将军衔
        :return:
        """
        test_data = {'user_rank': 29, 'user_exp': 350000000, 'current_level': u'1级上将', 'current_exp': 60000000,
                     'current_privilege': 130, 'next_privilege': 135, 'next_military_name': u'2级上将'}
        self.flow_path(**test_data)
        test_data = {'user_rank': 30, 'user_exp': 410000000, 'current_level': u'2级上将', 'current_exp': 60000000,
                     'current_privilege': 135, 'next_privilege': 140, 'next_military_name': u'3级上将'}
        self.flow_path(**test_data)
        test_data = {'user_rank': 31, 'user_exp': 470000000, 'current_level': u'3级上将', 'current_exp': 80000000,
                     'current_privilege': 140, 'next_privilege': 150, 'next_military_name': u'1级大将'}
        self.flow_path(**test_data)

    def test_get_my_military_senior_general(self):
        """
        测试大将军衔
        :return:
        """
        test_data = {'user_rank': 32, 'user_exp': 550000000, 'current_level': u'1级大将', 'current_exp': 70000000,
                     'current_privilege': 150, 'next_privilege': 155, 'next_military_name': u'2级大将'}
        self.flow_path(**test_data)
        test_data = {'user_rank': 33, 'user_exp': 620000000, 'current_level': u'2级大将', 'current_exp': 80000000,
                     'current_privilege': 155, 'next_privilege': 160, 'next_military_name': u'3级大将'}
        self.flow_path(**test_data)
        test_data = {'user_rank': 34, 'user_exp': 700000000, 'current_level': u'3级大将', 'current_exp': 100000000,
                     'current_privilege': 160, 'next_privilege': 200, 'next_military_name': u'1级元帅'}
        self.flow_path(**test_data)

    def test_get_my_military_marshal(self):
        """
        测试元帅军衔
        :return:
        """
        test_data = {'user_rank': 35, 'user_exp': 800000000, 'current_level': u'1级元帅', 'current_exp': 100000000,
                     'current_privilege': 200, 'next_privilege': 210, 'next_military_name': u'2级元帅'}
        self.flow_path(**test_data)
        test_data = {'user_rank': 36, 'user_exp': 900000000, 'current_level': u'2级元帅', 'current_exp': 100000000,
                     'current_privilege': 210,'next_privilege': 220, 'next_military_name': u'3级元帅'}
        self.flow_path(**test_data)
        test_data = {'user_rank': 37, 'user_exp': 1000000000, 'current_level': u'3级元帅', 'current_exp': 100000000,
                     'current_privilege': 220, 'next_privilege': 230, 'next_military_name': u'4级元帅'}
        self.flow_path(**test_data)
        test_data = {'user_rank': 38, 'user_exp': 1100000000, 'current_level': u'4级元帅', 'current_exp': 100000000,
                     'current_privilege': 230, 'next_privilege': 240, 'next_military_name': u'5级元帅'}
        self.flow_path(**test_data)
        test_data = {'user_rank': 39, 'user_exp': 1200000000, 'current_level': u'5级元帅', 'current_exp': 100000000,
                     'current_privilege': 240, 'next_privilege': 250, 'next_military_name': u'6级元帅'}
        self.flow_path(**test_data)
        test_data = {'user_rank': 40, 'user_exp': 1300000000, 'current_level': u'6级元帅', 'current_exp': 100000000,
                     'current_privilege': 250, 'next_privilege': 260, 'next_military_name': u'7级元帅'}
        self.flow_path(**test_data)
        test_data = {'user_rank': 41, 'user_exp': 1400000000, 'current_level': u'7级元帅', 'current_exp': 100000000,
                     'current_privilege': 260, 'next_privilege': 270, 'next_military_name': u'8级元帅'}
        self.flow_path(**test_data)
        test_data = {'user_rank': 42, 'user_exp': 1500000000, 'current_level': u'8级元帅', 'current_exp': 100000000,
                     'current_privilege': 270, 'next_privilege': 280, 'next_military_name': u'9级元帅'}
        self.flow_path(**test_data)
        test_data = {'user_rank': 43, 'user_exp': 1600000000, 'current_level': u'9级元帅', 'current_exp': 200000000,
                     'current_privilege': 280, 'next_privilege': 290, 'next_military_name': u'10级元帅'}
        self.flow_path(**test_data)
        test_data = {'user_rank': 44, 'user_exp': 1800000000, 'current_level': u'10级元帅', 'current_exp': 200000000,
                     'current_privilege': 290, 'next_privilege': 300, 'next_military_name': u'1级大元帅'}
        self.flow_path(**test_data)

    def test_get_my_military_generalissimo(self):
        """
        测试大元帅军衔
        :return:
        """
        test_data = {'user_rank': 45, 'user_exp': 2000000000, 'current_level': u'1级大元帅', 'current_exp': 200000000,
                     'current_privilege': 300, 'next_privilege': 320, 'next_military_name': u'2级大元帅'}
        self.flow_path(**test_data)

    def tearDown(self,*args):
        super(TestMyMilitaryApi,self).tearDown()
        self.fix_user_experience(rank=1,experience_all=0)