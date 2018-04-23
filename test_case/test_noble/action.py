# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.noble_api import BuyNobleApi
from utilities.mysql_helper import MysqlOperation
from utilities.redis_helper import RedisHold
from api.consumption_api import ConsumptionApi
from api.live_api import EnterRoomApi
import time,json,settings



class NobleAction(BaseCase):
    login_name = settings.YULE_TEST_USER_LOGIN_NAME
    user_id = settings.YULE_TEST_USER_ID
    room_id = settings.YULE_TEST_ROOM
    time_sleep = 1


    def buy_noble_action(self,**kwargs):
        noble_price = kwargs['noble_price']
        noble_time = kwargs['noble_time']
        noble_id = kwargs['noble_id']
        user_rank = kwargs['user_rank']
        noble_rest_time_int = kwargs['noble_rest_time_int']
        user_exp = kwargs['user_exp']

        mysql_operation = MysqlOperation(user_id=self.user_id)
        mysql_operation.fix_user_account(gold_num=noble_price)
        RedisHold().clean_redis_user_detail(self.user_id)
        time.sleep(self.time_sleep)
        buy_noble_api = BuyNobleApi(self.login_name)
        response = buy_noble_api.get({'noble_id': noble_id, 'num': noble_time, 'room_id': self.room_id, 'currency': 'gold'})
        self.assertEqual(buy_noble_api.get_code(), 0)
        self.assertEqual(buy_noble_api.get_response_message(), u'操作成功')

        response_identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(response_identity_obj['diamond'], u'0')
        self.assertEqual(response_identity_obj['gold'], 0)
        self.assertEqual(response_identity_obj['user_rank'], user_rank)
        self.assertEqual(response_identity_obj['user_experience'],user_exp)
        self.assertEqual(response_identity_obj['noble_rank'],noble_id)
        self.assertIn(response_identity_obj['noble_rest_time_int'],noble_rest_time_int)
        noble_rest_time_int_format = []
        for x in noble_rest_time_int:
            noble_rest_time_int_format.append(u'{0}天'.format(x))
        self.assertIn(response_identity_obj['noble_rest_time_str'],noble_rest_time_int_format)

        consumption_api = ConsumptionApi(self.login_name)
        response = consumption_api.get()
        self.assertEqual(consumption_api.get_code(),0)
        self.assertEqual(len(json.loads(response.content)['result']['consume_list']),1)
        consume_list = json.loads(response.content)['result']['consume_list'][0]
        self.assertEqual(consume_list['user_id'],self.user_id)
        self.assertEqual(consume_list['type'],u'2')
        self.assertEqual(consume_list['gold'],noble_price)
        self.assertEqual(consume_list['corresponding_id'],noble_id)
        self.assertEqual(consume_list['corresponding_name'],u'贵族')
        self.assertEqual(consume_list['corresponding_num'],1)
        self.assertEqual(consume_list['room_id'],u'')
        self.assertEqual(consume_list['status'],1)
        self.assertEqual(consume_list['behavior_desc'],u'购买贵族')
        self.assertEqual(consume_list['room_title'],u'-- --')
        self.assertEqual(consume_list['consumption_type'],u'%s金币' % noble_price)
        if noble_time == 1:
            enter_room_api = EnterRoomApi(self.login_name)
            response = enter_room_api.get({'room_id':self.room_id})
            self.assertEqual(enter_room_api.get_code(),0)

            ani_obj = json.loads(response.content)['result']['enter_room_message']['msg']['obj']['ani_obj']
            self.assertEqual(ani_obj['ani_type'],u'entry_noble')
            self.assertEqual(ani_obj['ani_id'], noble_id)
            self.assertEqual(ani_obj['ani_num'],0)
            self.assertIsNone(ani_obj['category_type'])

    def renew_noble_action(self,**kwargs):
        noble_price = kwargs['noble_price']
        first_noble_id = kwargs['first_noble_id']
        second_noble_id = kwargs['second_noble_id']
        user_rank = kwargs['user_rank']

        mysql_operation = MysqlOperation(user_id=self.user_id)
        mysql_operation.fix_user_account(gold_num=noble_price)
        RedisHold().clean_redis_user_detail(self.user_id)
        time.sleep(self.time_sleep)
        buy_noble_api = BuyNobleApi(self.login_name)
        response = buy_noble_api.get({'noble_id': first_noble_id, 'num': 1, 'room_id': self.room_id, 'currency': 'gold'})
        self.assertEqual(buy_noble_api.get_code(), 0)
        self.assertEqual(buy_noble_api.get_response_message(), u'操作成功')
        identity_obj = json.loads(response.content)['result']['identity_obj']

        buy_noble_renew = BuyNobleApi(self.login_name)
        renew_response = buy_noble_renew.get({'noble_id': second_noble_id, 'num': 1,'room_id':self.room_id,'currency':'gold'})
        if second_noble_id < first_noble_id:
            self.assertEqual(buy_noble_renew.get_code(),402026)
            self.assertEqual(buy_noble_renew.get_response_message(),u'您选择的贵族低于您当前已拥有的贵族等级，无法开通')
            self.assertEqual(identity_obj['user_rank'],user_rank)
        else:
            self.assertEqual(buy_noble_renew.get_code(),0)
            self.assertEqual(buy_noble_renew.get_response_message(),u'操作成功')

            renew_response_identity_obj = json.loads(renew_response.content)['result']['identity_obj']
            self.assertEqual(renew_response_identity_obj['diamond'],u'0')
            self.assertEqual(renew_response_identity_obj['gold'],0)
            self.assertEqual(renew_response_identity_obj['user_rank'],user_rank)
            if second_noble_id == first_noble_id:
                noble_rest_time = range(28,32)
                self.assertEqual(renew_response_identity_obj['noble_rank'], first_noble_id)
            else:
                noble_rest_time = [-1,0,1]
                self.assertEqual(renew_response_identity_obj['noble_rank'], second_noble_id)
            self.assertIn(renew_response_identity_obj['noble_rest_time_int']-identity_obj['noble_rest_time_int'],noble_rest_time)


