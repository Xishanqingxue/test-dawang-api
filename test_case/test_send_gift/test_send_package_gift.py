# -*- coding:utf-8 -*-
from api.send_gift_api import SendGiftApi
from base.base_case import BaseCase
from api.live_api import LiveApi
from api.follow_api import AddFollowingApi
from utilities.redis_helper import RedisHold
import json,time,settings
from utilities.teardown import TearDown


class TestSendPackageGift(BaseCase):
    """
    送背包礼物
    """
    login_name = settings.YULE_TEST_USER_LOGIN_NAME
    user_id = settings.YULE_TEST_USER_ID
    room_id = settings.YULE_TEST_ROOM
    anchor_id = settings.YULE_TEST_ANCHOR_ID
    count = 1
    max_count = 20
    time_sleep = 0.5
    package_gift_id = 1009

    def setUp(self, *args):
        super(TestSendPackageGift, self).setUp(user_id=self.user_id, anchor_id=self.anchor_id)
        TearDown().send_gift_teardown(login_name=self.login_name, anchor_id=self.anchor_id, user_id=self.user_id,
                                      room_id=self.room_id)
        time.sleep(self.time_sleep)


    def test_send_package_gift_success(self):
        """
        测试送出为你伴舞礼物
        :return:
        """
        add_following_api = AddFollowingApi(self.login_name)
        add_following_api.get({'anchor_id': self.anchor_id})
        self.assertEqual(add_following_api.get_code(), 0)
        self.assertEqual(add_following_api.get_response_message(), u'操作成功')

        live_api = LiveApi(self.login_name)
        response = live_api.get({'room_id': self.room_id})
        self.assertEqual(live_api.get_code(), 0)
        room_hot_num = json.loads(response.content)['result']['room_obj']['curr_hot_num']

        RedisHold().add_user_package_gift(self.user_id,gift_id=self.package_gift_id,gift_num=1)
        time.sleep(self.time_sleep)

        send_gift_api = SendGiftApi(self.login_name)
        response = send_gift_api.get({'room_id': self.room_id, 'gift_id': self.package_gift_id, 'gift_count': 1,'currency': 'bag'})

        self.assertEqual(send_gift_api.get_code(),0)
        self.assertEqual(json.loads(response.content)['result']['identity_obj']['gold'],0)
        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity_obj['gold'],0)
        self.assertEqual(identity_obj['user_rank'],3)
        self.assertEqual(identity_obj['user_experience'],0)
        intimacy_obj = identity_obj['intimacy_obj']
        self.assertEqual(intimacy_obj['intimacy_rank'],4)
        self.assertEqual(intimacy_obj['intimacy_experience'],0)
        intimacy_level_obj = intimacy_obj['intimacy_level_obj']
        self.assertEqual(intimacy_level_obj['level'],1)

        anchor_obj = json.loads(response.content)['result']['room_obj']['anchor_obj']
        self.assertEqual(anchor_obj['anchor_rank'],2)
        self.assertEqual(anchor_obj['anchor_experience'],50000)

        time.sleep(self.time_sleep)

        live_api = LiveApi(self.login_name)
        response = live_api.get({'room_id': self.room_id})
        self.assertEqual(live_api.get_code(), 0)
        room_hot_num_after_send = json.loads(response.content)['result']['room_obj']['curr_hot_num']

        self.assertEqual(room_hot_num_after_send - room_hot_num,100000)


    def tearDown(self,*args):
        super(TestSendPackageGift,self).tearDown(user_id=self.user_id,anchor_id=self.anchor_id)
        TearDown().send_gift_teardown(login_name=self.login_name,anchor_id=self.anchor_id, user_id=self.user_id,room_id=self.room_id)
        time.sleep(self.time_sleep)