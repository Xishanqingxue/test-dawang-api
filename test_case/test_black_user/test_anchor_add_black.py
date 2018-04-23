# -*- coding:utf-8 -*-
from test_case.test_black_user.action import BlackUserAction
from utilities.redis_helper import Redis,RedisHold
from api.super_visor_api import DelSuperVisorApi
from utilities.mysql_helper import MysqlOperation
import settings


class TestAnchorAddBlackApi(BlackUserAction):
    """
    主播添加黑名单
    """
    anchor_login_name = settings.YULE_TEST_ANCHOR_LOGIN_NAME
    anchor_id = settings.YULE_TEST_ANCHOR_ID
    room_id = settings.YULE_TEST_ROOM
    user_id = '22014102'
    other_anchor_id = '20000275'
    time_sleep = 0.2

    def setUp(self,*args):
        super(TestAnchorAddBlackApi,self).setUp()
        del_super_visor_api = DelSuperVisorApi(self.anchor_login_name)
        del_super_visor_api.get({'user_id': self.user_id, 'anchor_id': self.anchor_id})
        for x in [self.user_id,self.other_anchor_id]:
            MysqlOperation(user_id=x).clean_black_user()
        Redis().clean_black_user(self.anchor_id)
        RedisHold().clean_redis_user_detail(self.user_id)

    def test_anchor_to_super_admin_forbid_shout(self):
        """
        测试主播对超管禁止喊话
        :return:
        """
        test_data = {'add_super_visor':True,'user_id':self.user_id,'type':60,'blacker_type':'forbid_shout',
                     'is_guard':None,'guard_id':None,'is_noble':None,'noble_id':None}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_super_admin_forbid_speak(self):
        """
        测试主播对超管禁言
        :return:
        """
        test_data = {'add_super_visor':True,'user_id':self.user_id,'type':60,'blacker_type':'forbid_speak',
                     'is_guard':None,'guard_id':None,'is_noble':None,'noble_id':None}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_super_admin_forbid_visit(self):
        """
        测试主播踢出超管
        :return:
        """
        test_data = {'add_super_visor':True,'user_id':self.user_id,'type':60,'blacker_type':'forbid_visit',
                     'is_guard':None,'guard_id':None,'is_noble':None,'noble_id':None}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_normal_admin_forbid_shout(self):
        """
        测试主播对普通管理禁止喊话
        :return:
        """
        test_data = {'add_super_visor': True, 'user_id': self.user_id, 'type': 40, 'blacker_type': 'forbid_shout',
                     'is_guard':None,'guard_id':None,'is_noble':None,'noble_id':None}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_normal_admin_forbid_speak(self):
        """
        测试主播对普通管理禁言
        :return:
        """
        test_data = {'add_super_visor': True, 'user_id': self.user_id, 'type': 40, 'blacker_type': 'forbid_speak',
                     'is_guard':None,'guard_id':None,'is_noble':None,'noble_id':None}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_normal_admin_forbid_visit(self):
        """
        测试主播踢出普通管理
        :return:
        """
        test_data = {'add_super_visor': True, 'user_id': self.user_id, 'type': 40, 'blacker_type': 'forbid_visit',
                     'is_guard':None,'guard_id':None,'is_noble':None,'noble_id':None}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_user_forbid_shout(self):
        """
        测试主播对普通用户禁止喊话
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_shout',
                     'is_guard':None,'guard_id':None,'is_noble':None,'noble_id':None}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_user_forbid_speak(self):
        """
        测试主播对普通用户禁言
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_speak',
                     'is_guard':None,'guard_id':None,'is_noble':None,'noble_id':None}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_user_forbid_visit(self):
        """
        测试主播踢出普通用户
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_visit',
                     'is_guard':None,'guard_id':None,'is_noble':None,'noble_id':None}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_anchor_forbid_shout(self):
        """
        测试主播对其他主播禁止喊话
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.other_anchor_id, 'type': 0, 'blacker_type': 'forbid_shout',
                     'is_guard':None,'guard_id':None,'is_noble':None,'noble_id':None}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_anchor_forbid_speak(self):
        """
        测试主播对其他主播禁言
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.other_anchor_id, 'type': 0, 'blacker_type': 'forbid_speak',
                     'is_guard':None,'guard_id':None,'is_noble':None,'noble_id':None}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_anchor_forbid_visit(self):
        """
        测试主播踢出其他主播
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.other_anchor_id, 'type': 0, 'blacker_type': 'forbid_visit',
                     'is_guard':None,'guard_id':None,'is_noble':None,'noble_id':None}
        self.anchor_add_black_action(**test_data)

    def tearDown(self,*args):
        super(TestAnchorAddBlackApi,self).tearDown()
        del_super_visor_api = DelSuperVisorApi(self.anchor_login_name)
        del_super_visor_api.get({'user_id': self.user_id, 'anchor_id': self.anchor_id})
        for x in [self.user_id,self.other_anchor_id]:
            MysqlOperation(user_id=x).clean_black_user()
        Redis().clean_black_user(self.anchor_id)
        RedisHold().clean_redis_user_detail(self.user_id)