# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.red_package_api import SendRedPacketApi,GetRedPacketListApi,GetHistoryApi,GrabRedPacket,GetGrabHistoryApi
from api.consumption_api import ConsumptionApi,GoldAccountApi
from utilities.mysql_helper import MysqlOperation
from utilities.redis_helper import RedisHold
import time,json,settings,datetime



class Action(BaseCase):
    login_name = settings.YULE_TEST_USER_LOGIN_NAME
    user_id = settings.YULE_TEST_USER_ID
    room_id = settings.YULE_TEST_ROOM
    anchor_id=settings.YULE_TEST_ANCHOR_ID
    time_sleep = 1

    def send_action(self,**kwargs):
        price = kwargs['price']
        conf_id = kwargs['conf_id']
        num = kwargs['num']
        red_gift_id = None
        red_type=None

        red_name = None
        if conf_id == 1:
            red_name = u'福利包'
            red_gift_id = 44
            red_type = 1
        elif conf_id == 2:
            red_name = u'土豪包'
            red_gift_id = 45
            red_type = 2
        elif conf_id == 3:
            red_name = u'至尊包'
            red_gift_id = 46
            red_type = 3

        mysql_operation = MysqlOperation(user_id=self.user_id)
        mysql_operation.fix_user_account(gold_num=price)
        RedisHold().clean_redis_user_detail(self.user_id)
        time.sleep(self.time_sleep)
        # 发红包
        send_red_packet_api = SendRedPacketApi(self.login_name)
        response = send_red_packet_api.get({'conf_id': conf_id,'room_id': self.room_id,'num': num,'currency':'gold'})

        self.assertEqual(send_red_packet_api.get_code(),0)
        red_packet_obj = json.loads(response.content)['result']['red_packet_obj']
        red_package_id = red_packet_obj['id']
        self.assertEqual(red_packet_obj['user_id'],int(self.user_id))
        self.assertEqual(red_packet_obj['room_id'],int(self.room_id))
        self.assertEqual(red_packet_obj['num'],num)
        self.assertEqual(red_packet_obj['gold'],price)
        self.assertEqual(red_packet_obj['real_gold'],price)
        self.assertEqual(red_packet_obj['left_num'],num)
        self.assertEqual(red_packet_obj['left_gold'],price * 0.8)
        self.assertEqual(red_packet_obj['fact_gold'],price * 0.8)
        self.assertEqual(red_packet_obj['red_gift_id'],red_gift_id)
        for x in [red_packet_obj['diamond'],red_packet_obj['real_diamond'],red_packet_obj['left_diamond'],red_packet_obj['fact_diamond']]:
            self.assertEqual(x,0)

        start_time = red_packet_obj['start_time']
        end_time = red_packet_obj['end_time']
        self.assertEqual(int(end_time) - int(start_time),86400)
        self.assertEqual(red_packet_obj['red_status'],1)
        self.assertEqual(red_packet_obj['type'],red_type)
        self.assertEqual(red_packet_obj['name'],red_name)
        self.assertLessEqual(red_packet_obj['count_down_time'],60)
        self.assertLessEqual(55,red_packet_obj['count_down_time'])
        self.assertEqual(red_packet_obj['currency_type'],1)

        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity_obj['gold'],0)
        if red_type == 3:
            self.assertEqual(identity_obj['user_experience'],int(price * 0.2) - 100000)
        else:
            self.assertEqual(identity_obj['user_experience'], int(price * 0.2))

        # 获取房间内可抢红包列表
        get_red_packet_list_api = GetRedPacketListApi(self.login_name)
        list_response = get_red_packet_list_api.get({'room_id': self.room_id})

        self.assertEqual(get_red_packet_list_api.get_code(), 0)

        user_red_packet_list = json.loads(list_response.content)['result']['user_red_packet_list']
        self.assertEqual(len(user_red_packet_list), 1)

        list_red_packet_obj = user_red_packet_list[0]['red_packet_obj']
        self.assertEqual(list_red_packet_obj['id'],red_packet_obj['id'])
        self.assertEqual(list_red_packet_obj['user_id'],int(self.user_id))
        self.assertEqual(list_red_packet_obj['room_id'],int(self.room_id))
        self.assertEqual(list_red_packet_obj['num'],num)
        self.assertEqual(list_red_packet_obj['gold'],price)
        self.assertEqual(list_red_packet_obj['real_gold'],price)
        self.assertEqual(list_red_packet_obj['left_gold'],price * 0.8)
        self.assertEqual(list_red_packet_obj['fact_gold'],price * 0.8)
        if red_type == 1:
            self.assertEqual(list_red_packet_obj['red_gift_id'],44)
        elif red_type == 2:
            self.assertEqual(list_red_packet_obj['red_gift_id'], 45)
        elif red_type == 3:
            self.assertEqual(list_red_packet_obj['red_gift_id'], 46)
        self.assertEqual(list_red_packet_obj['left_num'],num)
        for x in [list_red_packet_obj['diamond'],list_red_packet_obj['real_diamond'],list_red_packet_obj['left_diamond'],list_red_packet_obj['fact_diamond']]:
            self.assertEqual(x,0)
        self.assertEqual(list_red_packet_obj['red_status'], 1)
        self.assertEqual(list_red_packet_obj['name'], red_name)
        self.assertEqual(list_red_packet_obj['currency_type'],1)
        self.assertLessEqual(list_red_packet_obj['count_down_time'],60)
        self.assertLessEqual(55,list_red_packet_obj['count_down_time'])

        user_obj = user_red_packet_list[0]['user_obj']
        self.assertEqual(user_obj['id'],self.user_id)
        if red_type == 3:
            self.assertEqual(user_obj['user_rank'],3)
        else:
            self.assertEqual(user_obj['user_rank'], 1)

        self.assertEqual(user_obj['user_experience_all'],int(price * 0.2))

        intimacy_obj = user_obj['intimacy_obj']
        for x in [intimacy_obj['intimacy_experience'],intimacy_obj['intimacy_rank'],intimacy_obj['intimacy_next_experience']]:
            self.assertEqual(x,0)
        self.assertIsNone(intimacy_obj['intimacy_level_obj'])
        # 发放红包历史
        time.sleep(3)
        get_history_api = GetHistoryApi(self.login_name)
        response = get_history_api.get()
        self.assertEqual(get_history_api.get_code(),0)
        self.assertEqual(json.loads(response.content)['result']['count'],1)
        red_packet_history_list = json.loads(response.content)['result']['red_packet_history_list']
        self.assertEqual(red_packet_history_list[0]['red_packet_obj']['id'],red_package_id)
        self.assertEqual(red_packet_history_list[0]['red_packet_obj']['user_id'],int(self.user_id))
        self.assertEqual(red_packet_history_list[0]['red_packet_obj']['room_id'],int(self.room_id))
        self.assertEqual(red_packet_history_list[0]['red_packet_obj']['num'],num)
        self.assertEqual(red_packet_history_list[0]['red_packet_obj']['gold'],price)
        self.assertEqual(red_packet_history_list[0]['red_packet_obj']['real_gold'],price)
        self.assertEqual(red_packet_history_list[0]['red_packet_obj']['left_num'],num)
        self.assertEqual(red_packet_history_list[0]['red_packet_obj']['left_gold'],int(price * 0.8))
        self.assertEqual(red_packet_history_list[0]['red_packet_obj']['fact_gold'],int(price * 0.8))

        if red_type == 1:
            self.assertEqual(red_packet_history_list[0]['red_packet_obj']['red_gift_id'],44)
        elif red_type == 2:
            self.assertEqual(red_packet_history_list[0]['red_packet_obj']['red_gift_id'], 45)
        elif red_type == 3:
            self.assertEqual(red_packet_history_list[0]['red_packet_obj']['red_gift_id'], 46)
        for x in [red_packet_history_list[0]['red_packet_obj']['diamond'],red_packet_history_list[0]['red_packet_obj']['real_diamond'],red_packet_history_list[0]['red_packet_obj']['left_diamond'],list_red_packet_obj['fact_diamond']]:
            self.assertEqual(x,0)
        self.assertEqual(red_packet_history_list[0]['red_packet_obj']['red_status'], 1)
        self.assertEqual(red_packet_history_list[0]['red_packet_obj']['name'], red_name)
        self.assertEqual(red_packet_history_list[0]['red_packet_obj']['currency_type'],1)
        self.assertLessEqual(red_packet_history_list[0]['red_packet_obj']['count_down_time'],60)
        self.assertLessEqual(55,red_packet_history_list[0]['red_packet_obj']['count_down_time'])


        consumption_api = ConsumptionApi(self.login_name)
        response = consumption_api.get()
        self.assertEqual(consumption_api.get_code(),0)
        self.assertEqual(json.loads(response.content)['result']['total_page'],1)
        consume_list = json.loads(response.content)['result']['consume_list']
        self.assertEqual(len(consume_list),1)
        self.assertEqual(consume_list[0]['user_id'],self.user_id)
        self.assertIn(datetime.datetime.now().strftime("%Y-%m-%d"),consume_list[0]['create_time'])
        self.assertEqual(consume_list[0]['type'],u'4')
        self.assertEqual(consume_list[0]['gold'],price)
        self.assertEqual(consume_list[0]['corresponding_id'],0)
        self.assertEqual(consume_list[0]['corresponding_name'],u'金币')
        self.assertEqual(consume_list[0]['corresponding_num'],0)
        self.assertEqual(consume_list[0]['room_id'],self.room_id)
        self.assertEqual(consume_list[0]['status'],1)
        self.assertEqual(consume_list[0]['behavior_desc'],u'发红包')
        self.assertEqual(consume_list[0]['room_title'],MysqlOperation(room_id=self.room_id).get_room_details()['title'])
        self.assertEqual(consume_list[0]['consumption_type'],u'%s金币' % price)

        if num == 50:
            time.sleep(65)
            grab_red_package_api = GrabRedPacket(self.login_name)
            response = grab_red_package_api.get({'red_packet_id':red_package_id,'room_id':self.room_id})
            self.assertEqual(grab_red_package_api.get_code(),0)
            red_packet_log_obj = json.loads(response.content)['result']['red_packet_log_obj']
            self.assertEqual(red_packet_log_obj['red_packet_id'],red_package_id)
            self.assertEqual(red_packet_log_obj['user_id'],int(self.user_id))
            self.assertEqual(red_packet_log_obj['room_id'],int(self.room_id))

            self.assertEqual(red_packet_log_obj['get_diamond'],0)
            self.assertNotEqual(red_packet_log_obj['get_gold'],0)
            get_gold = red_packet_log_obj['get_gold']

            self.assertEqual(len(json.loads(response.content)['result']['user_red_packet_list']),0)
            self.assertEqual(json.loads(response.content)['result']['total_count'],0)

            identity_obj = json.loads(response.content)['result']['identity_obj']
            self.assertEqual(identity_obj['gold'],get_gold)
            self.assertEqual(identity_obj['diamond'],u'0')
            if red_type == 3:
                self.assertEqual(identity_obj['user_experience'], int(price * 0.2) - 100000)
            else:
                self.assertEqual(identity_obj['user_experience'], int(price * 0.2))

            gold_account_api = GoldAccountApi(self.login_name)
            response = gold_account_api.get()
            self.assertEqual(gold_account_api.get_code(),0)

            account_list = json.loads(response.content)['result']['account_list']
            self.assertEqual(len(account_list),1)
            self.assertEqual(account_list[0]['user_id'],self.user_id)
            self.assertIn(datetime.datetime.now().strftime("%Y-%m-%d"), account_list[0]['create_time'])
            self.assertEqual(account_list[0]['type'],u'2')
            self.assertEqual(account_list[0]['gold'],get_gold)

            self.assertEqual(account_list[0]['corresponding_id'], 0)
            self.assertEqual(account_list[0]['corresponding_name'], u'金币')
            self.assertEqual(account_list[0]['corresponding_num'], 0)
            self.assertEqual(account_list[0]['status'], 1)
            self.assertEqual(account_list[0]['behavior_desc'], u'抢红包')
            self.assertEqual(account_list[0]['room_title'],MysqlOperation(room_id=self.room_id).get_room_details()['title'])
            self.assertEqual(account_list[0]['consumption_type'], u'%s金币' % get_gold)
            self.assertEqual(account_list[0]['money'],0)

            get_grab_history_api = GetGrabHistoryApi(self.login_name)
            response = get_grab_history_api.get({'red_packet_id':red_package_id})
            self.assertEqual(get_grab_history_api.get_code(),0)

            red_packet_obj = json.loads(response.content)['result']['red_packet_obj']
            self.assertEqual(red_packet_obj['id'],red_package_id)
            self.assertEqual(red_packet_obj['user_id'],int(self.user_id))
            self.assertEqual(red_packet_obj['room_id'],int(self.room_id))
            self.assertEqual(red_packet_obj['num'],num)
            self.assertEqual(red_packet_obj['gold'],price)
            self.assertEqual(red_packet_obj['real_gold'],price)
            self.assertLess(red_packet_obj['left_num'],50)
            self.assertLessEqual(0,red_packet_obj['left_num'])
            self.assertEqual(red_packet_obj['fact_gold'],int(price * 0.8))
            for x in [red_packet_obj['left_gold']]:
                self.assertLess(x,price * 0.8)
                self.assertLess(0,x)
            for x in [red_packet_obj['diamond'], red_packet_obj['real_diamond'], red_packet_obj['left_diamond'],
                      red_packet_obj['fact_diamond']]:
                self.assertEqual(x, 0)
            self.assertEqual(red_packet_obj['red_status'],1)
            self.assertEqual(red_packet_obj['type'],red_type)
            self.assertEqual(red_packet_obj['status'],1)
            self.assertEqual(red_packet_obj['name'],red_name)
            self.assertEqual(red_packet_obj['count_down_time'],0)
            self.assertEqual(red_packet_obj['currency_type'],1)

            self.assertLess(0,len(json.loads(response.content)['result']['red_packet_log_list']))


