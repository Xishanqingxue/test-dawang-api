# -*- coding:utf-8 -*-
from api.send_gift_api import SendGiftApi
from base.base_case import BaseCase
from api.consumption_api import ConsumptionApi
from utilities.mysql_helper import MysqlOperation
from api.follow_api import AddFollowingApi
from api.live_api import LiveApi
from utilities.redis_helper import RedisHold
import json,time,settings


class SendGiftAction(BaseCase):
    login_name = settings.YULE_TEST_USER_LOGIN_NAME
    user_id = settings.YULE_TEST_USER_ID
    room_id = settings.YULE_TEST_ROOM
    anchor_id = settings.YULE_TEST_ANCHOR_ID
    count = 1
    max_count = 20
    time_sleep = 0.5


    def send_gift_action(self,**kwargs):
        gift_gold = kwargs['gift_gold']
        gift_diamond = kwargs['gift_diamond']
        gift_id = kwargs['gift_id']
        gift_num = kwargs['gift_num']
        is_following = kwargs['is_following']
        if gift_gold > 0:
            currency = 'gold'
        elif gift_diamond > 0:
            currency = 'diamond'
        else:
            currency = 'bag'

        if is_following:
            add_following_api = AddFollowingApi(self.login_name)
            response = add_following_api.get({'anchor_id': self.anchor_id})
            self.assertEqual(add_following_api.get_code(), 0)
            self.assertEqual(add_following_api.get_response_message(), u'操作成功')
            self.assertEqual(json.loads(response.content)['result']['identity_obj']['has_followed'], 1)

        live_api = LiveApi(self.login_name)
        response = live_api.get({'room_id': self.room_id})
        self.assertEqual(live_api.get_code(), 0)
        room_hot_num = json.loads(response.content)['result']['room_obj']['curr_hot_num']
        while self.count < self.max_count:
            mysql_operation = MysqlOperation(user_id=self.user_id)
            mysql_operation.fix_user_account(gold_num=gift_gold * gift_num, diamond_num=gift_diamond * gift_num)
            RedisHold().clean_redis_user_detail(self.user_id)
            time.sleep(self.time_sleep)
            send_gift_api = SendGiftApi(self.login_name)
            response = send_gift_api.get({'room_id': self.room_id, 'gift_id': gift_id, 'gift_count': gift_num,'currency': currency})
            if send_gift_api.get_code() == 100032:
                time.sleep(self.time_sleep)
                self.count+=1
            else:

                self.assertEqual(send_gift_api.get_code(),0)
                break
        self.assertLess(self.count,self.max_count)

        gift_details = MysqlOperation().get_gift_details(gift_id=gift_id)
        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity_obj['gold'],0)
        self.assertEqual(identity_obj['diamond'],u'0')

        user_exp = self.get_user_exp_and_rank(gift_details['add_user_experience'] * gift_num)

        self.assertEqual(identity_obj['user_experience'],user_exp['exp'])
        self.assertEqual(identity_obj['user_rank'],user_exp['rank'])

        def assert_intimacy(obj,following,gift_num):
            inti_dic = {}
            if gift_num == 1:
                inti_dic = {'intimacy_experience': 1000, 'intimacy_rank': 1, 'level': 1,'level_name': u'喜爱'}
            elif gift_num == 10:
                inti_dic = {'intimacy_experience': 0, 'intimacy_rank': 2, 'level': 1, 'level_name': u'喜爱'}
            elif gift_num == 66:
                inti_dic = {'intimacy_experience': 16000, 'intimacy_rank': 3, 'level': 1, 'level_name': u'喜爱'}
            elif gift_num == 99:
                inti_dic = {'intimacy_experience': 49000, 'intimacy_rank': 3, 'level': 1, 'level_name': u'喜爱'}
            elif gift_num == 188:
                inti_dic = {'intimacy_experience': 88000, 'intimacy_rank': 4, 'level': 1, 'level_name': u'喜爱'}
            elif gift_num == 520:
                inti_dic = {'intimacy_experience': 45000, 'intimacy_rank': 7, 'level': 1, 'level_name': u'喜爱'}
            elif gift_num == 1314:
                inti_dic = {'intimacy_experience': 214000, 'intimacy_rank': 10, 'level': 1, 'level_name': u'喜爱'}

            if following:
                self.assertEqual(obj['intimacy_experience'],inti_dic['intimacy_experience'])
                self.assertEqual(obj['intimacy_rank'],inti_dic['intimacy_rank'])
                intimacy_level_obj = obj['intimacy_level_obj']
                self.assertEqual(intimacy_level_obj['level'],inti_dic['level'])
                self.assertEqual(intimacy_level_obj['level_name'],inti_dic['level_name'])
                self.assertEqual(intimacy_level_obj['rank_start'],1)
                self.assertEqual(intimacy_level_obj['rank_end'],15)
            else:
                for x in [obj['intimacy_experience'],obj['intimacy_rank'],obj['intimacy_next_experience']]:
                    self.assertEqual(x,0)
                self.assertIsNone(obj['intimacy_level_obj'])
        intimacy_obj = identity_obj['intimacy_obj']
        assert_intimacy(intimacy_obj,is_following,gift_num)

        anchor_obj = json.loads(response.content)['result']['room_obj']['anchor_obj']
        anchor_exp = self.get_anchor_exp_and_rank(gift_details['add_anchor_experience'] * gift_num)
        self.assertEqual(anchor_obj['anchor_experience'],anchor_exp['exp'])
        self.assertEqual(anchor_obj['anchor_rank'],anchor_exp['rank'])

        live_api = LiveApi(self.login_name)
        response = live_api.get({'room_id': self.room_id})
        self.assertEqual(live_api.get_code(), 0)
        room_hot_num_after = json.loads(response.content)['result']['room_obj']['curr_hot_num']
        if gift_gold > 0:
            self.assertEqual(int(room_hot_num_after) - int(room_hot_num),gift_gold * gift_num)
        if gift_diamond > 0:
            self.assertEqual(int(room_hot_num_after) - int(room_hot_num), gift_diamond / 10 * gift_num)

        consumption_api = ConsumptionApi(self.login_name)
        response = consumption_api.get()
        self.assertEqual(consumption_api.get_code(),0)
        consume_list = json.loads(response.content)['result']['consume_list'][0]
        self.assertEqual(consume_list['user_id'],self.user_id)
        self.assertEqual(consume_list['type'],u'1')
        self.assertEqual(consume_list['gold'],(gift_gold * gift_num))
        self.assertEqual(consume_list['corresponding_id'],gift_id)
        self.assertEqual(consume_list['corresponding_name'],MysqlOperation().get_gift_details(gift_id)['name'])
        self.assertEqual(consume_list['corresponding_num'],gift_num)
        self.assertEqual(consume_list['room_id'],self.room_id)
        self.assertEqual(consume_list['status'],1)
        self.assertEqual(consume_list['behavior_desc'],u'送礼')
        self.assertEqual(consume_list['room_title'],MysqlOperation(room_id=self.room_id).get_room_details()['title'])
        self.assertEqual(consume_list['consumption_type'],u'%s金币' % (gift_gold * gift_num))


    def get_user_exp_and_rank(self,exp_all):
        if exp_all < 50000:
            user_rank = 1
            return {"exp": exp_all, "rank": user_rank}
        if exp_all >= 50000 and exp_all < 100000:
            user_rank = 2
            user_exp = exp_all - 50000
            return {"exp":user_exp,"rank":user_rank}
        if exp_all >= 100000 and exp_all < 150000:
            user_rank = 3
            user_exp = exp_all - 100000
            return {"exp":user_exp,"rank":user_rank}
        if exp_all >= 150000 and exp_all < 200000:
            user_rank = 4
            user_exp = exp_all - 150000
            return {"exp":user_exp,"rank":user_rank}
        if 250000 > exp_all >= 200000:
            user_rank = 5
            user_exp = exp_all - 200000
            return {"exp":user_exp,"rank":user_rank}
        if 300000 > exp_all >= 250000:
            user_rank = 6
            user_exp = exp_all - 250000
            return {"exp":user_exp,"rank":user_rank}
        if 400000 > exp_all >= 300000:
            user_rank = 7
            user_exp = exp_all - 300000
            return {"exp":user_exp,"rank":user_rank}
        if 500000 > exp_all >= 400000:
            user_rank = 8
            user_exp = exp_all - 400000
            return {"exp":user_exp,"rank":user_rank}
        if 750000 > exp_all >= 500000:
            user_rank = 9
            user_exp = exp_all - 500000
            return {"exp":user_exp,"rank":user_rank}
        if 1000000 > exp_all >= 750000:
            user_rank = 10
            user_exp = exp_all - 750000
            return {"exp":user_exp,"rank":user_rank}
        if 2000000 > exp_all >= 1000000:
            user_rank = 11
            user_exp = exp_all - 1000000
            return {"exp":user_exp,"rank":user_rank}
        if exp_all >= 2000000:
            user_rank = 12
            user_exp = exp_all - 2000000
            return {"exp":user_exp,"rank":user_rank}

    def get_anchor_exp_and_rank(self,exp_all):
        if exp_all < 50000:
            anchor_rank = 1
            return {"exp": exp_all, "rank": anchor_rank}
        if exp_all >= 50000 and exp_all < 500000:
            anchor_rank = 2
            anchor_exp = exp_all - 50000
            return {"exp":anchor_exp,"rank":anchor_rank}
        if exp_all >= 500000 and exp_all < 1000000:
            anchor_rank = 4
            anchor_exp = exp_all - 500000
            return {"exp": anchor_exp, "rank": anchor_rank}
        if exp_all >= 1000000:
            anchor_rank = 5
            anchor_exp = exp_all - 1000000
            return {"exp": anchor_exp, "rank": anchor_rank}