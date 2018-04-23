# -*- coding:utf-8 -*-
from api.exchange_api import ExchangeApi
from api.consumption_api import ConsumptionApi
from utilities.mysql_helper import MysqlOperation
from utilities.redis_helper import RedisHold
from base.base_case import BaseCase
from api.diamond_product_list_api import DiamondProductListApi
from api.login_server_api import LoginServerApi
import time,json,requests,settings
from utilities.teardown import TearDown

class TestExchangeApi(BaseCase):
    """
    金币兑换大王豆
    """
    user_mobile = settings.YULE_TEST_USER_LOGIN_NAME
    user_id = settings.YULE_TEST_USER_ID
    time_sleep = 0.5
    ratio = 10

    def setUp(self,*args):
        super(TestExchangeApi,self).setUp(user_id=self.user_id)
        TearDown().gold_exchange_diamond_teardowm(self.user_id)

    def test_exchange_success(self):
        """
        测试兑换成功+消费记录
        :return:
        """
        gold_num = 1000
        MysqlOperation(user_id=self.user_id).fix_user_account(gold_num=gold_num)
        RedisHold().clean_redis_user_detail(self.user_id)
        time.sleep(self.time_sleep)

        exchange_api = ExchangeApi(self.user_mobile)
        response = exchange_api.get({'gold':gold_num,'diamond':gold_num * self.ratio,'product_id':112})

        self.assertEqual(exchange_api.get_code(),0)
        self.assertEqual(json.loads(response.content)['result']['gold'],gold_num)
        self.assertEqual(json.loads(response.content)['result']['diamond'],gold_num * self.ratio)
        self.assertEqual(json.loads(response.content)['result']['identity_obj']['user_rank'],1)
        self.assertEqual(json.loads(response.content)['result']['identity_obj']['user_experience'],gold_num)

        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity_obj['gold'],0)
        self.assertEqual(int(identity_obj['diamond']),int(gold_num * self.ratio))
        time.sleep(1)
        # 消费记录
        consumption_api = ConsumptionApi(self.user_mobile)
        response = consumption_api.get()

        self.assertEqual(consumption_api.get_code(), 0)
        consume_list = json.loads(response.content)['result']['consume_list']
        self.assertEqual(len(consume_list), 1)
        self.assertEqual(consume_list[0]['gold'], gold_num)
        self.assertEqual(consume_list[0]['user_id'],self.user_id)
        self.assertEqual(consume_list[0]['type'],u'6')
        self.assertEqual(consume_list[0]['corresponding_id'],0)
        self.assertEqual(consume_list[0]['corresponding_num'],1)
        self.assertEqual(consume_list[0]['corresponding_name'], u'大王豆')
        self.assertEqual(consume_list[0]['room_id'],u'')
        self.assertEqual(consume_list[0]['room_title'],u'-- --')
        self.assertEqual(consume_list[0]['status'],1)
        self.assertEqual(consume_list[0]['consumption_type'], u'%s金币' % gold_num)
        self.assertEqual(consume_list[0]['behavior_desc'], u'大王豆转换')

    def test_get_diamond_product_list(self):
        """
        测试获取大王豆产品列表
        :return:
        """
        diamond_product_api = DiamondProductListApi(self.user_mobile)
        response = diamond_product_api.get({'platform': 'android'})

        self.assertEqual(diamond_product_api.get_code(), 0)
        product_list = json.loads(response.content)['result']['product_list']

        db_product_list = MysqlOperation().get_diamond_product_info(platform='android')
        self.assertEqual(len(product_list), 7)
        self.assertEqual(len(product_list), len(db_product_list))

        db_product_ids = []
        for x in db_product_list:
            db_product_ids.append(int(x['id']))

        product_ids = []
        for i in product_list:
            product_ids.append(int(i['id']))
        self.assertEqual(product_ids.sort(), db_product_ids.sort())

        db_product_price = []
        for x in db_product_list:
            db_product_price.append(int(x['price']))

        product_price = []
        for i in product_list:
            product_price.append(int(i['price']))
        self.assertEqual(product_price.sort(), db_product_price.sort())

        for i in product_list:
            self.assertEqual(int(i['pay_package'][0]['num']) / int(i['price']), 10)

        db_product_pay_name = []
        for x in db_product_list:
            db_product_pay_name.append(x['pay_name'])

        pay_name = []
        for i in product_list:
            pay_name.append(i['pay_name'])
        self.assertEqual(pay_name.sort(), db_product_pay_name.sort())

        pay_icon = []
        for i in product_list:
            pay_icon.append(i['pay_icon'])

        for x in pay_icon:
            self.assertEqual(x, u'/images/icon/00/00/diamond_box.png')

        login_server_api = LoginServerApi()
        login_server_response = login_server_api.get({'platform': 'android'})
        self.assertEqual(login_server_api.get_code(), 0)
        img_server = json.loads(login_server_response.content)['result']['server_config']['img_server']

        pay_icon_url = '{0}{1}'.format(img_server, pay_icon[0])
        resp = requests.get(pay_icon_url)
        self.assertEqual(resp.status_code, 200)

    def test_exchange_product_id_null(self):
        """
        测试请求兑换接口商品ID为空
        :return:
        """
        exchange_api = ExchangeApi(self.user_mobile)
        exchange_api.get({'gold': None, 'diamond': None, 'product_id': None})

        self.assertEqual(exchange_api.get_code(), 460006)
        self.assertEqual(exchange_api.get_response_message(),u'商品id不能为空')

    def test_exchange_product_id_error(self):
        """
        测试请求兑换接口商品ID错误
        :return:
        """
        exchange_api = ExchangeApi(self.user_mobile)
        exchange_api.get({'gold': None, 'diamond': None, 'product_id': '666'})

        self.assertEqual(exchange_api.get_code(), 460007)
        self.assertEqual(exchange_api.get_response_message(),u'商品不存在')

    def test_exchange_gold_low(self):
        """
        测试请求兑换接口账户金币不足
        :return:
        """
        exchange_api = ExchangeApi(self.user_mobile)
        exchange_api.get({'gold': 1000, 'diamond': 10000, 'product_id': '112'})

        self.assertEqual(exchange_api.get_code(), 100032)
        self.assertEqual(exchange_api.get_response_message(),u'账户金币不足')


    def tearDown(self,*args):
        super(TestExchangeApi,self).tearDown(user_id=self.user_id)
        TearDown().gold_exchange_diamond_teardowm(self.user_id)
