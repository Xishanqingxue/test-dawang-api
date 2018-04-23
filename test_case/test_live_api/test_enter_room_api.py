# -*- coding:utf-8 -*-
from api.live_api import EnterRoomApi
from utilities.mysql_helper import MysqlGet
from base.base_case import BaseCase
import json,settings


class TestEnterRoomApi(BaseCase):
    """
    进入直播间
    """
    login_name = settings.YULE_TEST_USER_LOGIN_NAME
    user_id = settings.YULE_TEST_USER_ID
    room_id = settings.YULE_TEST_ROOM
    anchor_id = settings.YULE_TEST_ANCHOR_ID

    def setUp(self, *args):
        super(TestEnterRoomApi,self).setUp(user_id=self.user_id,anchor_id=self.anchor_id)


    def test_enter_room_success(self):
        """
        测试正常请求接口
        :return:
        """
        enter_room_api = EnterRoomApi(self.login_name)
        response = enter_room_api.get({'room_id':self.room_id})
        self.assertEqual(enter_room_api.get_code(),0)

        room_obj = json.loads(response.content)['result']['room_obj']
        self.assertEqual(room_obj['id'],self.room_id)
        self.assertEqual(room_obj['room_type'],1)
        self.assertEqual(room_obj['room_style'],1)
        self.assertEqual(room_obj['room_style_extend'],0)
        self.assertIsNotNone(room_obj['max_img_path'])
        self.assertIsNotNone(room_obj['min_img_path'])
        self.assertEqual(room_obj['room_status'],0)

        room_details =MysqlGet(room_id=self.room_id).get_room_details()
        self.assertEqual(room_obj['introduce'],room_details['introduce'])
        self.assertEqual(room_obj['notice'],room_details['notice'])
        self.assertEqual(room_obj['title'],room_details['title'])

        play_url = room_obj['play_url']
        for x in [play_url['flv_play_url_raw'],play_url['flv_play_url_high'],play_url['flv_play_url_low'],play_url['hls_play_url_raw']]:
            self.assertIsNotNone(x)
        welcome_tip = room_obj['welcome_tip']
        self.assertEqual(welcome_tip['tip'],u'文明直播aa123232')
        self.assertEqual(welcome_tip['link_url'],u'http://www.dawang.tv')

        share_config = json.loads(response.content)['result']['share_config']
        self.assertIsNotNone(share_config['share_title'])
        self.assertIsNotNone(share_config['share_content'])
        self.assertEqual(share_config['share_url'],u'http://h5.t.dwtv.tv/share/live/#####')

        gift_list = json.loads(response.content)['result']['gift_list']
        gift_category_name = []
        for x in gift_list:
            gift_category_name.append(x['gift_category_obj']['name'])

        self.assertEqual(gift_category_name,[u'金币礼物',u'背包'])

        gift_category_type = []
        for x in gift_list:
            gift_category_type.append(x['gift_category_obj']['type'])

        self.assertEqual(gift_category_type, [u'gold', u'bag'])

        active_obj_list = json.loads(response.content)['result']['ship_hunter_exchage_entrance']
        self.assertEqual(active_obj_list['is_show_entrance'],1)
        self.assertEqual(active_obj_list['url'],u'/active/warship/exchangegold')

        self.assertEqual(json.loads(response.content)['result']['is_open_menu'],1)

        server_config = json.loads(response.content)['result']['server_config']
        self.assertEqual(server_config['socket_domain'],u'chat.t.dwtv.tv')
        self.assertEqual(server_config['socket_port'],u'80')
        self.assertEqual(server_config['share_title'],u'要想生活有意思，必须发现点乐子！')
        self.assertEqual(server_config['share_content'],u'<#####>正在大王直播，也许会有惊喜等着你~来跟我一起感受欢乐时光吧')
        self.assertEqual(server_config['share_url'],u'http://h5.t.dwtv.tv/share/live/#####')

        enter_room_message = json.loads(response.content)['result']['enter_room_message']
        self.assertEqual(enter_room_message['act'],u'send_group_message')
        self.assertEqual(enter_room_message['uid'],(self.user_id))
        self.assertEqual(enter_room_message['room_id'],(self.room_id))
        self.assertIsNone(enter_room_message['to_uid'])
        self.assertIsNone(enter_room_message['expire_time'])

        msg = enter_room_message['msg']
        self.assertEqual(msg['m_action'],u'system_room')
        self.assertEqual(msg['m_switch'],u'coming')
        self.assertEqual(msg['from_user_id'],u'0')
        self.assertEqual(msg['from_refer_type'],u'1')
        self.assertEqual(msg['obj']['msg_content'],u'来了')
        self.assertIsNone(msg['obj']['ani_obj'])

        user_obj = msg['user_obj']
        self.assertEqual(user_obj['id'],(self.user_id))
        self.assertEqual(user_obj['nickname'],MysqlGet(user_id=self.user_id).get_user_details()['nickname'])
        self.assertEqual(user_obj['noble_rank'],0)
        self.assertEqual(user_obj['user_rank'],1)
        self.assertEqual(user_obj['anchor_rank'],0)
        self.assertEqual(user_obj['intimacy_rank'],0)
        self.assertIsNone(user_obj['intimacy_level'])
        self.assertIsNone(user_obj['intimacy_level_name'])
        self.assertEqual(user_obj['guard_rank'],0)
        self.assertEqual(user_obj['user_type'],1)
        self.assertEqual(user_obj['is_anchor'],0)
        self.assertEqual(user_obj['small_head_url'],u'')

        self.assertEqual(json.loads(response.content)['result']['is_all_tasks_finished'],0)
        self.assertEqual(json.loads(response.content)['result']['is_show_red_packet'],1)
        self.assertEqual(json.loads(response.content)['result']['animation_source_path'],u'/flash/h5/pai/')
        self.assertIsNone(json.loads(response.content)['result']['group_head_user_obj'])

        ship_hunter_exchange_entrance = json.loads(response.content)['result']['ship_hunter_exchage_entrance']
        self.assertEqual(ship_hunter_exchange_entrance['is_show_entrance'],1)
        self.assertEqual(ship_hunter_exchange_entrance['url'],u'/active/warship/exchangegold')

    def test_enter_room_id_null(self):
        """
        测试请求接口房间ID为空
        :return:
        """
        enter_room_api = EnterRoomApi(self.login_name)
        enter_room_api.get({'room_id': None})
        self.assertEqual(enter_room_api.get_code(), 402000)
        self.assertEqual(enter_room_api.get_response_message(),u'房间ID不能为空')

    def test_enter_room_id_error(self):
        """
        测试请求接口房间ID不存在
        :return:
        """
        enter_room_api = EnterRoomApi(self.login_name)
        enter_room_api.get({'room_id': '6666'})
        self.assertEqual(enter_room_api.get_code(), 402004)
        self.assertEqual(enter_room_api.get_response_message(),u'获取直播间数据错误:直播间不存在')
