# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.buy_sun_api import BuySunApi
from api.live_api import LiveApi
from api.follow_api import AddFollowingApi,RelieveFollowingApi
from api.consumption_api import ConsumptionApi
from utilities.mysql_helper import MysqlOperation
from utilities.redis_helper import RedisHold
import settings
import time
import json

class TestBuySunApi(BaseCase):
    """
    购买太阳
    """
    user_mobile = settings.YULE_TEST_USER_LOGIN_NAME
    user_id = settings.YULE_TEST_USER_ID
    room_id = settings.YULE_TEST_ROOM
    anchor_id = settings.YULE_TEST_ANCHOR_ID

    def setUp(self,*args):
        super(TestBuySunApi,self).setUp(user_id=self.user_id)
        MysqlOperation(user_id=self.user_id).fix_user_sun_num()

    def test_buy_sun_following_success(self):
        """
        测试关注主播情况下购买太阳成功
        :return:
        """
        follow_api = AddFollowingApi(self.user_mobile)
        follow_api.get({'anchor_id': self.anchor_id})
        self.assertEqual(follow_api.get_code(),0)

        live_api = LiveApi(self.user_mobile)
        response = live_api.get({'room_id': self.room_id})
        self.assertEqual(live_api.get_code(),0)

        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity_obj['user_experience'],0)
        intimacy_obj = identity_obj['intimacy_obj']
        self.assertEqual(intimacy_obj['intimacy_experience'],0)

        sun_num = json.loads(response.content)['result']['room_obj']['sun_num']

        MysqlOperation(user_id=self.user_id).fix_user_account(gold_num=2000)
        RedisHold().clean_redis_user_detail(self.user_id)
        time.sleep(0.5)

        buy_sun_api = BuySunApi(self.user_mobile)
        response = buy_sun_api.get({'room_id':self.room_id})
        self.assertEqual(buy_sun_api.get_code(),0)

        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity_obj['gold'],0) # 校验用户剩余金币
        self.assertEqual(identity_obj['sun_num'],0) # 校验用户剩余太阳数量不变
        self.assertEqual(identity_obj['user_experience'],2000) # 校验用户经验值增加

        intimacy_obj = identity_obj['intimacy_obj']
        self.assertEqual(intimacy_obj['intimacy_experience'], 200) # 校验用户亲密度增加

        after_sun_num = json.loads(response.content)['result']['room_obj']['sun_num']
        self.assertEqual(after_sun_num - sun_num , 20) # 校验主播获得的太阳数量增加

        consum_api = ConsumptionApi(self.user_mobile)
        response = consum_api.get()
        self.assertEqual(consum_api.get_code(),0)
        consume_list = json.loads(response.content)['result']['consume_list']
        # 校验消费记录
        self.assertEqual(len(consume_list),1)
        self.assertEqual(consume_list[0]['user_id'],self.user_id)
        self.assertEqual(consume_list[0]['type'], u'5')
        self.assertEqual(consume_list[0]['gold'], 2000)
        self.assertEqual(consume_list[0]['corresponding_id'], 0)
        self.assertEqual(consume_list[0]['corresponding_name'], u'太阳')
        self.assertEqual(consume_list[0]['corresponding_num'], 1)
        self.assertEqual(consume_list[0]['room_id'], self.room_id)
        self.assertEqual(consume_list[0]['status'], 1)
        self.assertEqual(consume_list[0]['behavior_desc'], u'购买太阳')
        self.assertEqual(consume_list[0]['consumption_type'], u'2000金币')

    def test_buy_sun_not_following_success(self):
        """
        测试未关注主播情况下购买太阳成功
        :return:
        """
        live_api = LiveApi(self.user_mobile)
        response = live_api.get({'room_id': self.room_id})
        self.assertEqual(live_api.get_code(),0)

        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity_obj['user_experience'],0)
        intimacy_obj = identity_obj['intimacy_obj']
        self.assertEqual(intimacy_obj['intimacy_experience'],0)
        self.assertIsNone(intimacy_obj['intimacy_level_obj'])

        sun_num = json.loads(response.content)['result']['room_obj']['sun_num']

        MysqlOperation(user_id=self.user_id).fix_user_account(gold_num=2000)
        RedisHold().clean_redis_user_detail(self.user_id)
        time.sleep(0.5)

        buy_sun_api = BuySunApi(self.user_mobile)
        response = buy_sun_api.get({'room_id':self.room_id})
        self.assertEqual(buy_sun_api.get_code(),0)

        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity_obj['gold'],0) # 校验用户剩余金币
        self.assertEqual(identity_obj['sun_num'],0) # 校验用户剩余太阳数量不变
        self.assertEqual(identity_obj['user_experience'],2000) # 校验用户经验值增加

        intimacy_obj = identity_obj['intimacy_obj']
        self.assertEqual(intimacy_obj['intimacy_experience'], 0) # 校验用户亲密度不变
        self.assertIsNone(intimacy_obj['intimacy_level_obj'])

        after_sun_num = json.loads(response.content)['result']['room_obj']['sun_num']
        self.assertEqual(after_sun_num - sun_num , 20) # 校验主播获得的太阳数量增加

        consum_api = ConsumptionApi(self.user_mobile)
        response = consum_api.get()
        self.assertEqual(consum_api.get_code(),0)
        consume_list = json.loads(response.content)['result']['consume_list']
        # 校验消费记录
        self.assertEqual(len(consume_list),1)
        self.assertEqual(consume_list[0]['user_id'],self.user_id)
        self.assertEqual(consume_list[0]['type'], u'5')
        self.assertEqual(consume_list[0]['gold'], 2000)
        self.assertEqual(consume_list[0]['corresponding_id'], 0)
        self.assertEqual(consume_list[0]['corresponding_name'], u'太阳')
        self.assertEqual(consume_list[0]['corresponding_num'], 1)
        self.assertEqual(consume_list[0]['room_id'], self.room_id)
        self.assertEqual(consume_list[0]['status'], 1)
        self.assertEqual(consume_list[0]['behavior_desc'], u'购买太阳')
        self.assertEqual(consume_list[0]['consumption_type'], u'2000金币')

    def test_buy_sun_room_id_null(self):
        """
        测试请求接口房间ID为空
        :return:
        """
        buy_sun_api = BuySunApi(self.user_mobile)
        buy_sun_api.get({'room_id':None})

        self.assertEqual(buy_sun_api.get_code(),402000)
        self.assertEqual(buy_sun_api.get_response_message(),u'房间ID不能为空')

    def test_buy_sun_gold_low(self):
        """
        测试请求接口账户金币不足
        :return:
        """
        MysqlOperation(user_id=self.user_id).fix_user_account(gold_num=1999)
        RedisHold().clean_redis_user_detail(self.user_id)
        time.sleep(0.5)

        buy_sun_api = BuySunApi(self.user_mobile)
        buy_sun_api.get({'room_id': self.room_id})

        self.assertEqual(buy_sun_api.get_code(), 100032)
        self.assertEqual(buy_sun_api.get_response_message(),u'账户金币不足')

    def tearDown(self,*args):
        super(TestBuySunApi,self).tearDown(user_id=self.user_id)
        MysqlOperation(user_id=self.user_id).fix_user_sun_num()
        relieve_follow_api = RelieveFollowingApi(self.user_mobile)
        relieve_follow_api.get({'anchor_id': self.anchor_id})

