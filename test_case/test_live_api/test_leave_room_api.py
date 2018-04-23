# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.live_api import LeaveAnchorRoomApi
import json,settings


class TestLeaveAnchorRoomApi(BaseCase):
    """
    离开直播间
    """
    login_name = settings.YULE_TEST_USER_LOGIN_NAME
    room_id = settings.YULE_TEST_ROOM

    def test_leave_anchor_room(self):
        """
        测试正常请求接口
        :return:
        """
        leave_anchor_room_api = LeaveAnchorRoomApi(self.login_name)
        response = leave_anchor_room_api.get({'room_id':self.room_id})

        self.assertEqual(leave_anchor_room_api.get_code(),0)
        self.assertEqual(leave_anchor_room_api.get_response_message(),u'操作成功')

        self.assertIsNotNone(json.loads(response.content)['result']['identity_obj']['identity'])
        self.assertIsNotNone(json.loads(response.content)['result']['identity_obj']['user_sign'])


    def test_leave_anchor_room_id_is_error(self):
        """
        测试请求接口房间ID不存在
        :return:
        """
        leave_anchor_room_api = LeaveAnchorRoomApi(self.login_name)
        leave_anchor_room_api.get({'room_id': str(self.room_id) + '1'})

        self.assertEqual(leave_anchor_room_api.get_code(), 402004)
        self.assertEqual(leave_anchor_room_api.get_response_message(), u'获取直播间数据错误:直播间不存在')


    def test_leave_anchor_room_id_is_null(self):
        """
        测试请求接口房间ID为空
        :return:
        """
        leave_anchor_room_api = LeaveAnchorRoomApi(self.login_name)
        leave_anchor_room_api.get({'room_id': ''})

        self.assertEqual(leave_anchor_room_api.get_code(), 402000)
        self.assertEqual(leave_anchor_room_api.get_response_message(), u'房间ID不能为空')


