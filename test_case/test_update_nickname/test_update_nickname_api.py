# -*- coding:utf-8 -*-
from api.update_nickname_api import UpdateNickApi
from utilities.redis_helper import RedisHold
from utilities.mysql_helper import MysqlOperation
from api.consumption_api import ConsumptionApi
from base.base_case import BaseCase
import time,json,settings
from utilities.teardown import TearDown

class TestUpdateNickApi(BaseCase):
    """
    修改昵称
    """
    user_mobile = settings.YULE_TEST_USER_LOGIN_NAME
    user_id = settings.YULE_TEST_USER_ID
    anchor_mobile = settings.YULE_TEST_GAME_ANCHOR_LOGIN_NAME
    anchor_id = settings.YULE_TEST_GAME_ANCHOR_ID
    time_sleep = 1
    new_nick_name = u'cilywb'
    anchor_new_nick_name = u'主播称昵啊'

    def setUp(self,*args):
        super(TestUpdateNickApi, self).setUp(user_id=[self.user_id,self.anchor_id])
        TearDown().update_nickname_api_teardown(self.user_id,rename_num=1,nick_name='dongci')
        TearDown().update_nickname_api_teardown(self.anchor_id, rename_num=1, nick_name='YaTo_猫小艺')


    def test_free_update_nick(self):
        """
        测试免费修改修改昵称和收费修改昵称成功
        :return:
        """
        update_nick_api = UpdateNickApi(self.user_mobile)
        response = update_nick_api.get({'nickname':self.new_nick_name})

        self.assertEqual(update_nick_api.get_code(),0)
        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity_obj['nickname'],self.new_nick_name)
        self.assertEqual(identity_obj['gold'],0)
        self.assertEqual(identity_obj['diamond'],u'0')
        self.assertEqual(identity_obj['left_rename_num'],0)
        time.sleep(self.time_sleep)

        MysqlOperation(user_id=self.user_id).fix_user_account(gold_num=20000)
        RedisHold().clean_redis_user_detail(self.user_id)
        time.sleep(self.time_sleep)

        update_nick_api = UpdateNickApi(self.user_mobile)
        response = update_nick_api.get({'nickname': 'ubiwm'})

        self.assertEqual(update_nick_api.get_code(),0)
        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity_obj['nickname'], 'ubiwm')
        self.assertEqual(identity_obj['gold'], 0)
        self.assertEqual(identity_obj['diamond'],u'0')
        self.assertEqual(identity_obj['left_rename_num'],0)

        consumption_api = ConsumptionApi(self.user_mobile)
        response = consumption_api.get()
        self.assertEqual(consumption_api.get_code(),0)
        consume_list = json.loads(response.content)['result']['consume_list']
        self.assertEqual(len(consume_list),1)
        self.assertEqual(consume_list[0]['type'],u'8')
        self.assertEqual(consume_list[0]['gold'],20000)
        self.assertEqual(consume_list[0]['corresponding_id'],0)
        self.assertEqual(consume_list[0]['corresponding_name'],u'修改昵称')
        self.assertEqual(consume_list[0]['corresponding_num'],1)
        self.assertEqual(consume_list[0]['status'],1)
        self.assertEqual(consume_list[0]['room_id'],u'')
        self.assertEqual(consume_list[0]['behavior_desc'],u'修改昵称')
        self.assertEqual(consume_list[0]['room_title'],u'-- --')
        self.assertEqual(consume_list[0]['consumption_type'], u'20000金币')

    def test_anchr_free_update_nick(self):
        """
        测试主播可以随意修改昵称
        :return:
        """
        update_nick_api = UpdateNickApi(self.anchor_mobile)
        response = update_nick_api.get({'nickname': self.anchor_new_nick_name})

        self.assertEqual(update_nick_api.get_code(), 0)
        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity_obj['nickname'], self.anchor_new_nick_name)
        self.assertEqual(identity_obj['gold'], 0)
        self.assertEqual(identity_obj['diamond'], u'0')
        self.assertEqual(identity_obj['left_rename_num'], 1)
        time.sleep(self.time_sleep)

        update_nick_api = UpdateNickApi(self.anchor_mobile)
        response = update_nick_api.get({'nickname': self.anchor_new_nick_name + '1'})

        self.assertEqual(update_nick_api.get_code(), 0)
        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity_obj['nickname'], self.anchor_new_nick_name + '1')
        self.assertEqual(identity_obj['gold'], 0)
        self.assertEqual(identity_obj['diamond'], u'0')
        self.assertEqual(identity_obj['left_rename_num'], 1)
        time.sleep(self.time_sleep)

        update_nick_api = UpdateNickApi(self.anchor_mobile)
        response = update_nick_api.get({'nickname': 'YaTo_猫小艺'})

        self.assertEqual(update_nick_api.get_code(), 0)
        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity_obj['nickname'], u'YaTo_猫小艺')
        self.assertEqual(identity_obj['gold'], 0)
        self.assertEqual(identity_obj['diamond'], u'0')
        self.assertEqual(identity_obj['left_rename_num'], 1)

        consumption_api = ConsumptionApi(self.anchor_mobile)
        response = consumption_api.get()
        self.assertEqual(consumption_api.get_code(), 0)
        consume_list = json.loads(response.content)['result']['consume_list']
        self.assertEqual(len(consume_list), 0)

    def tearDown(self,*args):
        super(TestUpdateNickApi, self).tearDown(user_id=[self.user_id,self.anchor_id])
        TearDown().update_nickname_api_teardown(self.user_id,rename_num=0,nick_name='dongci')
        TearDown().update_nickname_api_teardown(self.anchor_id, rename_num=0, nick_name='YaTo_猫小艺')
