# -*- coding:utf-8 -*-
from api.live_api import LiveApi
from utilities.mysql_helper import MysqlGet
from base.base_case import BaseCase
import json,settings


class TestLiveApi(BaseCase):
    """
    获取直播间信息
    """
    login_name = settings.YULE_TEST_USER_LOGIN_NAME
    room_id = settings.YULE_TEST_ROOM
    anchor_id = settings.YULE_TEST_ANCHOR_ID

    def setUp(self, *args):
        super(TestLiveApi,self).setUp(anchor_id=self.anchor_id)

    def test_live_api(self):
        """
        测试正常请求接口
        :return:
        """
        live_api = LiveApi(self.login_name)
        response = live_api.get({'room_id': self.room_id})
        self.assertEqual(live_api.get_code(),0)

        room_obj = json.loads(response.content)['result']['room_obj']
        self.assertEqual(room_obj['id'], self.room_id)
        self.assertEqual(room_obj['room_type'], 1)
        self.assertEqual(room_obj['room_style'], 1)
        self.assertEqual(room_obj['room_style_extend'], 0)
        self.assertIsNotNone(room_obj['max_img_path'])
        self.assertIsNotNone(room_obj['min_img_path'])
        self.assertEqual(room_obj['room_status'], 0)


        room_details =MysqlGet(room_id=self.room_id).get_room_details()
        self.assertEqual(room_obj['introduce'],room_details['introduce'])
        self.assertEqual(room_obj['notice'],room_details['notice'])
        self.assertEqual(room_obj['title'],room_details['title'])

        anchor_obj = room_obj['anchor_obj']
        self.assertEqual(anchor_obj['id'],(self.anchor_id))
        self.assertEqual(anchor_obj['anchor_rank'],1)
        self.assertEqual(anchor_obj['anchor_experience'],0)
        self.assertEqual(anchor_obj['anchor_experience_all'],0)

        welcome_tip = room_obj['welcome_tip']
        self.assertEqual(welcome_tip['tip'], u'文明直播aa123232')
        self.assertEqual(welcome_tip['link_url'], u'http://www.dawang.tv')
