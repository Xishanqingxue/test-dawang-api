# -*- coding:utf-8 -*-
from unittest import TestCase
from api.red_package_api import SendRedPacketApi
import settings


class TestSendRedPacketApi(TestCase):
    """
    发红包
    """
    user_login_name = settings.YULE_TEST_USER_LOGIN_NAME
    room_id = settings.YULE_TEST_ROOM
    user_id = settings.YULE_TEST_USER_ID


    def test_send_red_packet_conf_id_is_null(self):
        """
        测试请求接口红包商品ID为空
        :return:
        """
        send_red_packet_api = SendRedPacketApi(self.user_login_name)
        send_red_packet_api.get({'conf_id': '','room_id': self.room_id,'num': 50,'currency':'gold'})

        self.assertEqual(send_red_packet_api.get_code(),505017)
        self.assertEqual(send_red_packet_api.get_response_message(),u'配置id不能为空')


    def test_send_red_packet_room_id_is_null(self):
        """
        测试请求接口房间ID为空
        :return:
        """
        send_red_packet_api = SendRedPacketApi(self.user_login_name)
        send_red_packet_api.get({'conf_id': 1,'room_id': '','num': 50,'currency':'gold'})

        self.assertEqual(send_red_packet_api.get_code(),402000)
        self.assertEqual(send_red_packet_api.get_response_message(),u'房间ID不能为空')

    def test_send_red_packet_num_is_null(self):
        """
        测试请求接口红包数量为空
        :return:
        """
        send_red_packet_api = SendRedPacketApi(self.user_login_name)
        send_red_packet_api.get({'conf_id': 1,'room_id': self.room_id,'num': '','currency':'gold'})

        self.assertEqual(send_red_packet_api.get_code(),505016)
        self.assertEqual(send_red_packet_api.get_response_message(),u'请选择红包份数')

    def test_send_red_packet_conf_id_is_error(self):
        """
        测试请求接口红包商品ID错误
        :return:
        """
        send_red_packet_api = SendRedPacketApi(self.user_login_name)
        send_red_packet_api.get({'conf_id': '111','room_id': self.room_id,'num': 50,'currency':'gold'})
        self.assertEqual(send_red_packet_api.get_code(),10112)
        self.assertEqual(send_red_packet_api.get_response_message(),u'参数异常')

    def test_send_red_packet_num_is_error(self):
        """
        测试请求接口红包数量错误
        :return:
        """
        send_red_packet_api = SendRedPacketApi(self.user_login_name)
        send_red_packet_api.get({'conf_id': 1,'room_id': self.room_id,'num': '33','currency':'gold'})

        self.assertEqual(send_red_packet_api.get_code(),10112)
        self.assertEqual(send_red_packet_api.get_response_message(),u'参数异常')