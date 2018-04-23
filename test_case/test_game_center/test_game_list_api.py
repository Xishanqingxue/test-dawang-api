# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.login_api import LoginApi
from utilities.mysql_helper import MysqlOperation
from utilities.redis_helper import RedisHold
from selenium import webdriver
from api.exchange_api import ExchangeApi
import json, re, requests, time


class TestGameListApi(BaseCase):
    """
    游戏大厅
    """
    user_mobile = '13511110001'
    user_id = '21991305'

    def test_game_center(self):
        """
        测试游戏大厅接口用户信息
        :return:
        """
        login_api = LoginApi()
        login_resp = login_api.login(self.user_mobile, only_get_identity=False)
        self.assertEqual(login_api.get_code(), 0)
        session_id = json.loads(login_resp.content)['result']['session_id']

        driver = webdriver.PhantomJS()
        driver.get(url='https://hall.game.dwtv.tv/enter/gamecenter?session_id={0}'.format(session_id), )
        page_source = driver.page_source
        p1 = r"(?<=identity:\").+?(?=\",)"
        pattern1 = re.compile(p1)
        matcher1 = re.search(pattern1, page_source)
        identity = matcher1.group(0)

        mysql_opeartion = MysqlOperation(user_id=self.user_id)
        mysql_opeartion.fix_user_account(gold_num=2000, diamond_num=1000)
        mysql_opeartion.fix_user_rank_and_experience(user_rank=12, experience_all=2000000)
        RedisHold().clean_redis_user_detail(self.user_id)
        time.sleep(1)

        game_list_api = requests.get(url='https://hall.game.dwtv.tv/lobby/game?identity={0}'.format(identity))
        response = json.loads(game_list_api.content)
        self.assertEqual(response['code'], 0)
        self.assertEqual(response['result']['api_url'], u'http://api.dawang.tv')
        self.assertEqual(response['result']['img_url'], u'http://api.dawang.tv')
        user_obj = response['result']['user_obj']
        self.assertEqual(user_obj['nickname'], MysqlOperation(user_id=self.user_id).get_user_details()['nickname'])
        self.assertEqual(user_obj['username'], ('dw_' + self.user_id))
        self.assertEqual(user_obj['gender'], 1)
        self.assertEqual(user_obj['icon'], u"/files/images/heads/00/49/20170802110412935.jpeg")
        self.assertIsNotNone(user_obj['identity'])
        self.assertEqual(user_obj['month_end_time'], 0)
        self.assertIsNotNone(user_obj['token'])
        self.assertEqual(user_obj['gold'], u'1000')
        self.assertEqual(user_obj['diamond'], 2000)
        self.assertEqual(user_obj['user_level'], 12)
        self.assertEqual(user_obj['user_exp'], 0)
        self.assertEqual(user_obj['vip_level'], 0)

        exchange_api = ExchangeApi(self.user_mobile)
        response = exchange_api.get({'gold': 1000, 'diamond': 10000, 'product_id': 112})

        self.assertEqual(exchange_api.get_code(), 0)
        self.assertEqual(json.loads(response.content)['result']['gold'], 1000)
        self.assertEqual(json.loads(response.content)['result']['diamond'], 10000)
        self.assertEqual(json.loads(response.content)['result']['identity_obj']['user_rank'], 12)
        self.assertEqual(json.loads(response.content)['result']['identity_obj']['user_experience'], 1000)

        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity_obj['gold'], 1000)
        self.assertEqual(identity_obj['diamond'], u'11000')

        login_api = LoginApi()
        login_resp = login_api.login(self.user_mobile, only_get_identity=False)
        self.assertEqual(login_api.get_code(), 0)
        session_id = json.loads(login_resp.content)['result']['session_id']

        driver = webdriver.PhantomJS()
        driver.get(url='https://hall.game.dwtv.tv/enter/gamecenter?session_id={0}'.format(session_id), )
        page_source = driver.page_source
        p1 = r"(?<=identity:\").+?(?=\",)"
        pattern1 = re.compile(p1)
        matcher1 = re.search(pattern1, page_source)
        identity = matcher1.group(0)

        game_list_api = requests.get(url='https://hall.game.dwtv.tv/lobby/game?identity={0}'.format(identity))
        response = json.loads(game_list_api.content)
        self.assertEqual(response['code'], 0)
        user_obj = response['result']['user_obj']
        self.assertIsNotNone(user_obj['identity'])
        self.assertEqual(user_obj['gold'], u'11000')
        self.assertEqual(user_obj['diamond'], 1000)
        self.assertEqual(user_obj['user_level'], 12)
        self.assertEqual(user_obj['user_exp'], 1000)
        self.assertEqual(user_obj['vip_level'], 0)

    def tearDown(self,*args):
        super(TestGameListApi,self).tearDown(user_id=self.user_id)