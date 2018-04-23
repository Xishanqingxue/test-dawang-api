# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.guard_api import BuyGuardApi,MyGuardApi
from utilities.mysql_helper import MysqlOperation
from api.live_api import LiveApi
from api.follow_api import AddFollowingApi
from api.consumption_api import ConsumptionApi
from api.live_api import EnterRoomApi
from utilities.redis_helper import RedisHold
import json,time,settings,datetime


class GuardAction(BaseCase):
    login_name = settings.YULE_TEST_USER_LOGIN_NAME
    user_id = settings.YULE_TEST_USER_ID
    time_sleep = 0.2
    room_id = settings.YULE_TEST_ROOM
    anchor_id = settings.YULE_TEST_ANCHOR_ID


    def action(self,**kwargs):
        guard_price = 0
        guard_id = kwargs['guard_id']
        user_rank = kwargs['user_rank']
        sun_max_num = kwargs['sun_max_num']
        anchor_rank = kwargs['anchor_rank']
        following = kwargs['following']
        expire_time_num = None
        guard_rank = None

        if guard_id == 1:
            guard_price = 588000
        elif guard_id == 2:
            guard_price = 1176000
        elif guard_id == 3:
            guard_price = 1764000
        elif guard_id == 6:
            guard_price = 3528000
        elif guard_id == 12:
            guard_price = 7056000
        elif guard_id == 13:
            guard_price = 14112000
        mysql_operation = MysqlOperation(user_id=self.user_id)
        mysql_operation.fix_user_account(gold_num=guard_price)
        RedisHold().clean_redis_user_detail(self.user_id)
        time.sleep(self.time_sleep)

        live_api = LiveApi(self.login_name)
        response = live_api.get({'room_id':self.room_id})
        self.assertEqual(live_api.get_code(),0)
        room_hot_num = json.loads(response.content)['result']['room_obj']['curr_hot_num']

        if following:
            add_following_api = AddFollowingApi(self.login_name)
            response = add_following_api.get({'anchor_id': self.anchor_id})
            self.assertEqual(add_following_api.get_code(), 0)
            self.assertEqual(add_following_api.get_response_message(), u'操作成功')
            self.assertEqual(json.loads(response.content)['result']['identity_obj']['has_followed'], 1)

        buy_guard_api = BuyGuardApi(self.login_name)
        response = buy_guard_api.get({'room_id': self.room_id, 'guard_id': guard_id, 'currency': 'gold'})

        self.assertEqual(buy_guard_api.get_code(),0)

        guard_list = json.loads(response.content)['result']['guard_list']
        self.assertEqual(len(guard_list),1)
        self.assertEqual(guard_list[0]['user_rank'],user_rank)
        self.assertEqual(guard_list[0]['user_experience_all'],guard_price)
        self.assertEqual(guard_list[0]['sun_resumed_time'],180)
        self.assertEqual(guard_list[0]['sun_max_num'],sun_max_num)

        user_guard_obj = guard_list[0]['user_guard_obj']
        self.assertEqual(user_guard_obj['user_id'],(self.user_id))
        def assert_guard_obj(obj,guard_id):
            if guard_id == 1:
                guard_rank = 1
                expire_time_num = range(28,32)
                self.assertEqual(user_guard_obj['guard_rank'], guard_rank)
                self.assertIn(user_guard_obj['rest_time_int'], expire_time_num)
                expire_time_num_format = []
                for x in expire_time_num:
                    expire_time_num_format.append(u'{0}天'.format(x))
                self.assertIn(user_guard_obj['rest_time_str'], expire_time_num_format)

            elif guard_id == 2:
                guard_rank = 2
                expire_time_num = range(59,63)
                self.assertEqual(user_guard_obj['guard_rank'], guard_rank)
                self.assertIn(user_guard_obj['rest_time_int'], expire_time_num)
                expire_time_num_format = []
                for x in expire_time_num:
                    expire_time_num_format.append(u'{0}天'.format(x))
                self.assertIn(user_guard_obj['rest_time_str'], expire_time_num_format)
            elif guard_id in [3, 6]:
                guard_rank = 3
                self.assertEqual(user_guard_obj['guard_rank'], guard_rank)
                if guard_id == 3:
                    expire_time_num = range(89,94)
                    self.assertIn(user_guard_obj['rest_time_int'], expire_time_num)
                    expire_time_num_format = []
                    for x in expire_time_num:
                        expire_time_num_format.append(u'{0}天'.format(x))
                    self.assertIn(user_guard_obj['rest_time_str'], expire_time_num_format)
                elif guard_id == 6:
                    expire_time_num = range(183,187)
                    self.assertIn(user_guard_obj['rest_time_int'], expire_time_num)
                    expire_time_num_format = []
                    for x in expire_time_num:
                        expire_time_num_format.append(u'{0}天'.format(x))
                    self.assertIn(user_guard_obj['rest_time_str'], expire_time_num_format)
            elif guard_id in [12, 13]:
                guard_rank = 4
                self.assertEqual(user_guard_obj['guard_rank'], guard_rank)
                if guard_id == 12:
                    expire_time_num = range(369,373)
                    self.assertIn(user_guard_obj['rest_time_int'], expire_time_num)
                    expire_time_num_format = []
                    for x in expire_time_num:
                        expire_time_num_format.append(u'{0}天'.format(x))
                    self.assertIn(user_guard_obj['rest_time_str'], expire_time_num_format)
                elif guard_id == 13:
                    expire_time_num = range(739,745)
                    self.assertIn(user_guard_obj['rest_time_int'], expire_time_num)
                    expire_time_num_format = []
                    for x in expire_time_num:
                        expire_time_num_format.append(u'{0}天'.format(x))
                    self.assertIn(user_guard_obj['rest_time_str'], expire_time_num_format)

        assert_guard_obj(obj=user_guard_obj,guard_id=guard_id)


        intimacy_obj = guard_list[0]['intimacy_obj']

        def assert_intimacy(obj,following,guard_id,identity=False):
            inti_dic = {}
            if guard_id == 1:
                inti_dic = {'intimacy_experience': 113000, 'intimacy_rank': 7, 'level': 1,'level_name': u'喜爱'}
            elif guard_id == 2:
                inti_dic = {'intimacy_experience': 76000, 'intimacy_rank': 10, 'level': 1, 'level_name': u'喜爱'}
            elif guard_id == 3:
                inti_dic = {'intimacy_experience': 264000, 'intimacy_rank': 11, 'level': 1, 'level_name': u'喜爱'}
            elif guard_id == 6:
                inti_dic = {'intimacy_experience': 528000, 'intimacy_rank': 13, 'level': 1, 'level_name': u'喜爱'}
            elif guard_id == 12:
                inti_dic = {'intimacy_experience': 56000, 'intimacy_rank': 15, 'level': 1, 'level_name': u'喜爱'}
            elif guard_id == 13:
                inti_dic = {'intimacy_experience': 112000, 'intimacy_rank': 17, 'level': 2, 'level_name': u'真爱'}

            if following:
                self.assertEqual(obj['intimacy_experience'],inti_dic['intimacy_experience'])
                self.assertEqual(obj['intimacy_rank'],inti_dic['intimacy_rank'])
                intimacy_level_obj = obj['intimacy_level_obj']
                self.assertEqual(intimacy_level_obj['level'],inti_dic['level'])
                self.assertEqual(intimacy_level_obj['level_name'],inti_dic['level_name'])
                if guard_id == 13:
                    self.assertEqual(intimacy_level_obj['rank_start'], 16)
                    self.assertEqual(intimacy_level_obj['rank_end'], 30)
                else:
                    self.assertEqual(intimacy_level_obj['rank_start'],1)
                    self.assertEqual(intimacy_level_obj['rank_end'],15)
            else:
                if identity:
                    self.assertEqual(obj['intimacy_experience'],0)
                    self.assertEqual(obj['intimacy_rank'],1)
                    self.assertEqual(obj['intimacy_next_experience'],10000)
                    self.assertEqual(obj['intimacy_level_obj']['level'],1)
                    self.assertEqual(obj['intimacy_level_obj']['level_name'],u'喜爱')
                    self.assertEqual(obj['intimacy_level_obj']['rank_start'],1)
                    self.assertEqual(obj['intimacy_level_obj']['rank_end'],15)
                else:
                    self.assertEqual(obj['intimacy_experience'], 0)
                    self.assertEqual(obj['intimacy_rank'], 0)
                    self.assertEqual(obj['intimacy_next_experience'], 0)
                    self.assertIsNone(obj['intimacy_level_obj'])

        assert_intimacy(intimacy_obj,following,guard_id)

        identity_obj = json.loads(response.content)['result']['identity_obj']
        identity_user_guard_obj = identity_obj['user_guard_obj']
        self.assertEqual(identity_user_guard_obj['user_id'],(self.user_id))
        assert_guard_obj(obj=identity_user_guard_obj, guard_id=guard_id)

        identity_intimacy_obj = json.loads(response.content)['result']['identity_obj']['intimacy_obj']
        assert_intimacy(identity_intimacy_obj,following,guard_id,identity=True)

        if following:
            self.assertEqual(identity_obj['has_followed'],1)
        else:
            self.assertEqual(identity_obj['has_followed'], 0)

        anchor_obj = json.loads(response.content)['result']['room_obj']['anchor_obj']
        self.assertEqual(anchor_obj['id'],self.anchor_id)
        self.assertEqual(anchor_obj['anchor_rank'],anchor_rank)
        self.assertEqual(anchor_obj['sun_resumed_time'],180)
        self.assertEqual(anchor_obj['sun_max_num'],50)

        live_api = LiveApi(self.login_name)
        response = live_api.get({'room_id': self.room_id})
        self.assertEqual(live_api.get_code(), 0)
        room_hot_num_after_buy = json.loads(response.content)['result']['room_obj']['curr_hot_num']

        self.assertEqual(room_hot_num_after_buy - room_hot_num,guard_price)

        consumption_api = ConsumptionApi(self.login_name)
        response = consumption_api.get()
        self.assertEqual(consumption_api.get_code(),0)
        self.assertEqual(len(json.loads(response.content)['result']['consume_list']),1)
        consume_list = json.loads(response.content)['result']['consume_list'][0]
        self.assertEqual(consume_list['user_id'],self.user_id)
        self.assertEqual(consume_list['type'],u'3')
        self.assertEqual(consume_list['gold'],guard_price)
        self.assertEqual(consume_list['corresponding_id'],guard_id)
        self.assertEqual(consume_list['corresponding_name'],u'守护')
        self.assertEqual(consume_list['corresponding_num'],1)
        self.assertEqual(consume_list['room_id'],self.room_id)
        self.assertEqual(consume_list['status'],1)
        self.assertEqual(consume_list['behavior_desc'],u'购买守护')
        self.assertEqual(consume_list['room_title'],MysqlOperation(room_id=self.room_id).get_room_details()['title'])
        self.assertEqual(consume_list['consumption_type'],u'%s金币' % guard_price)

        my_guard_api = MyGuardApi(self.login_name)
        response = my_guard_api.get()

        self.assertEqual(my_guard_api.get_code(),0)
        guard_list = json.loads(response.content)['result']['guard_list']
        self.assertEqual(len(guard_list),1)
        self.assertEqual(guard_list[0]['anchor_id'],self.anchor_id)
        if guard_id == 1:
            guard_rank = 1
            expire_time_num = 31
        elif guard_id == 2:
            guard_rank = 2
            expire_time_num = 62
        elif guard_id in [3, 6]:
            guard_rank = 3
            if guard_id == 3:
                expire_time_num = 93
            elif guard_id == 6:
                expire_time_num = 186
        elif guard_id in [12, 13]:
            guard_rank = 4
            if guard_id == 12:
                expire_time_num = 372
            elif guard_id == 13:
                expire_time_num = 744
        expire_time = (datetime.datetime.now() + datetime.timedelta(days=+expire_time_num)).strftime("%Y-%m-%d")
        self.assertIn(expire_time,guard_list[0]['expire_time'])
        self.assertEqual(guard_list[0]['guard_rank'],guard_rank)

        room_obj = guard_list[0]['room_obj']
        self.assertEqual(room_obj['id'],self.room_id)
        self.assertEqual(room_obj['room_type'],1)
        self.assertEqual(room_obj['room_style'],1)
        self.assertEqual(room_obj['room_style_extend'],0)
        guard_list_anchor_obj = room_obj['anchor_obj']
        self.assertEqual(guard_list_anchor_obj['id'],self.anchor_id)
        self.assertEqual(guard_list_anchor_obj['anchor_rank'],anchor_rank)
        if guard_id in [1,2,3,12]:

            enter_room_api = EnterRoomApi(self.login_name)
            response = enter_room_api.get({'room_id':self.room_id})
            self.assertEqual(enter_room_api.get_code(),0)

            ani_obj = json.loads(response.content)['result']['enter_room_message']['msg']['obj']['ani_obj']
            self.assertEqual(ani_obj['ani_type'],u'entry_guard')
            if guard_id == 1:
                self.assertEqual(ani_obj['ani_id'],1)
            elif guard_id == 2:
                self.assertEqual(ani_obj['ani_id'], 2)
            elif guard_id == 3:
                self.assertEqual(ani_obj['ani_id'], 3)
            elif guard_id == 12:
                self.assertEqual(ani_obj['ani_id'], 4)
            self.assertEqual(ani_obj['ani_num'],0)
            self.assertIsNone(ani_obj['category_type'])


    def renew_action(self,**kwargs):
        guard_price = kwargs['guard_price']
        first_guard_id = kwargs['first_guard_id']
        second_guard_id = kwargs['second_guard_id']
        following = kwargs['following']
        user_rank = kwargs['user_rank']
        sun_max_num = kwargs['sun_max_num']
        anchor_rank = kwargs['anchor_rank']
        guard_rank = kwargs['guard_rank']
        expire_time_num = kwargs['expire_time_num']

        mysql_operation = MysqlOperation(user_id=self.user_id)
        mysql_operation.fix_user_account(gold_num=guard_price)
        RedisHold().clean_redis_user_detail(self.user_id)
        time.sleep(self.time_sleep)

        buy_guard_api = BuyGuardApi(self.login_name)
        buy_guard_api.get({'room_id': self.room_id, 'guard_id': first_guard_id, 'currency': 'gold'})
        self.assertEqual(buy_guard_api.get_code(),0)
        time.sleep(0.5)
        renew_buy_guard = BuyGuardApi(self.login_name)
        response = renew_buy_guard.get({'room_id': self.room_id, 'guard_id': second_guard_id, 'currency': 'gold'})
        self.assertEqual(renew_buy_guard.get_code(), 0)

        guard_list = json.loads(response.content)['result']['guard_list']
        self.assertEqual(len(guard_list), 1)
        self.assertEqual(guard_list[0]['user_rank'], user_rank)
        self.assertEqual(guard_list[0]['user_experience_all'], guard_price)
        self.assertEqual(guard_list[0]['sun_resumed_time'], 180)
        self.assertEqual(guard_list[0]['sun_max_num'], sun_max_num)

        user_guard_obj = guard_list[0]['user_guard_obj']
        self.assertEqual(user_guard_obj['user_id'], (self.user_id))
        self.assertEqual(user_guard_obj['guard_rank'], guard_rank)
        self.assertIn(user_guard_obj['rest_time_int'], expire_time_num)
        expire_time_num_format = []
        for x in expire_time_num:
            expire_time_num_format.append(u'{0}天'.format(x))
        self.assertIn(user_guard_obj['rest_time_str'], expire_time_num_format)

        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity_obj['user_rank'],user_rank)
        self.assertEqual(identity_obj['gold'],0)
        self.assertEqual(identity_obj['diamond'],u'0')
        self.assertEqual(identity_obj['sun_max_num'],sun_max_num)
        self.assertEqual(identity_obj['has_followed'], 0)

        identity_user_guard_obj = identity_obj['user_guard_obj']
        self.assertEqual(identity_user_guard_obj['user_id'], (self.user_id))
        self.assertEqual(identity_user_guard_obj['guard_rank'], guard_rank)
        self.assertIn(identity_user_guard_obj['rest_time_int'], expire_time_num)
        expire_time_num_format = []
        for x in expire_time_num:
            expire_time_num_format.append(u'{0}天'.format(x))
        self.assertIn(identity_user_guard_obj['rest_time_str'], expire_time_num_format)

        anchor_obj = json.loads(response.content)['result']['room_obj']['anchor_obj']
        self.assertEqual(anchor_obj['anchor_rank'], anchor_rank)
        self.assertEqual(anchor_obj['sun_resumed_time'], 180)
        self.assertEqual(anchor_obj['sun_max_num'], 50)

