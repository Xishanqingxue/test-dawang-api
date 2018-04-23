# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.super_visor_api import AddSuperVisorApi,DelSuperVisorApi
from utilities.mysql_helper import MysqlOperation
import json,settings




class TestSuperVisorApi(BaseCase):
    """
    房间内设置管理
    """
    anchor_login_name = settings.YULE_TEST_ANCHOR_LOGIN_NAME
    anchor_id = settings.YULE_TEST_ANCHOR_ID
    user_login_name = '15899999999'
    user_id = '22013806'


    def test_super_visor_high_admin(self):
        """
        测试设置高级管理成功
        :return:
        """
        add_super_visor_api = AddSuperVisorApi(self.anchor_login_name)
        add_super_visor_api.get({'user_id': self.user_id, 'anchor_id': self.anchor_id, 'type':'60'})

        self.assertEqual(add_super_visor_api.get_code(),0)
        self.assertEqual(add_super_visor_api.get_response_message(),u'操作成功')

        super_visor_details = MysqlOperation(user_id=self.user_id).get_anchor_room_supervisor_details()
        self.assertEqual(super_visor_details['is_advance_admin'],1)

    def test_super_visor_normal_admin(self):
        """
        测试设置普通管理成功
        :return:
        """
        add_super_visor_api = AddSuperVisorApi(self.anchor_login_name)
        add_super_visor_api.get({'user_id': self.user_id, 'anchor_id': self.anchor_id, 'type':'40'})

        self.assertEqual(add_super_visor_api.get_code(),0)
        self.assertEqual(add_super_visor_api.get_response_message(),u'操作成功')

        super_visor_details = MysqlOperation(user_id=self.user_id).get_anchor_room_supervisor_details()
        self.assertEqual(super_visor_details['is_normal_admin'],1)

    def test_super_visor_user_id_null(self):
        """
        测试请求接口用户ID为空
        :return:
        """
        add_super_visor_api = AddSuperVisorApi(self.anchor_login_name)
        add_super_visor_api.get({'user_id': None, 'anchor_id': self.anchor_id, 'type':'40'})

        self.assertEqual(add_super_visor_api.get_code(),801020)
        self.assertEqual(add_super_visor_api.get_response_message(),u'用户id不能为空')

    def test_super_visor_anchor_id_null(self):
        """
        测试请求接口主播ID为空
        :return:
        """
        add_super_visor_api = AddSuperVisorApi(self.anchor_login_name)
        add_super_visor_api.get({'user_id': self.user_id, 'anchor_id': None, 'type':'40'})

        self.assertEqual(add_super_visor_api.get_code(),402005)
        self.assertEqual(add_super_visor_api.get_response_message(),u'主播ID不能为空')

    def test_super_visor_type_null(self):
        """
        测试请求接口管理员类型为空
        :return:
        """
        add_super_visor_api = AddSuperVisorApi(self.anchor_login_name)
        add_super_visor_api.get({'user_id': self.user_id, 'anchor_id': self.anchor_id, 'type': None})

        self.assertEqual(add_super_visor_api.get_code(), 411127)
        self.assertEqual(add_super_visor_api.get_response_message(), u'管理员类型不能为空')

    def test_super_visor_user_id_error(self):
        """
        测试请求接口用户ID错误
        :return:
        """
        add_super_visor_api = AddSuperVisorApi(self.anchor_login_name)
        add_super_visor_api.get({'user_id': self.user_id + '123', 'anchor_id': self.anchor_id, 'type':'40'})

        self.assertEqual(add_super_visor_api.get_code(),801027)
        self.assertEqual(add_super_visor_api.get_response_message(),u'用户信息不存在')

    def test_super_visor_anchor_id_error(self):
        """
        测试请求接口主播ID错误
        :return:
        """
        add_super_visor_api = AddSuperVisorApi(self.anchor_login_name)
        add_super_visor_api.get({'user_id': self.user_id, 'anchor_id': self.anchor_id + '123', 'type':'40'})

        self.assertEqual(add_super_visor_api.get_code(),801017)
        self.assertEqual(add_super_visor_api.get_response_message(),u'房间信息不存在')

    def test_super_visor_type_error(self):
        """
        测试请求接口管理员类型错误
        :return:
        """
        add_super_visor_api = AddSuperVisorApi(self.anchor_login_name)
        add_super_visor_api.get({'user_id': self.user_id, 'anchor_id': self.anchor_id, 'type': '123'})

        self.assertEqual(add_super_visor_api.get_code(), 900003)
        self.assertEqual(add_super_visor_api.get_response_message(), u'管理员类型异常')

    def tearDown(self,*args):
        super(TestSuperVisorApi,self).tearDown()
        del_super_visor_api = DelSuperVisorApi(self.anchor_login_name)
        del_super_visor_api.get({'user_id': self.user_id, 'anchor_id': self.anchor_id})