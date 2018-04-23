# -*- coding:utf-8 -*-
from test_case.test_black_user.action import BlackUserAction
from utilities.redis_helper import Redis,RedisHold
from api.super_visor_api import DelSuperVisorApi
from utilities.mysql_helper import MysqlOperation
import settings


class TestHighAdminAddBlackApi(BlackUserAction):
    """
    高管添加黑名单
    """
    anchor_login_name = settings.YULE_TEST_ANCHOR_LOGIN_NAME
    anchor_id = settings.YULE_TEST_ANCHOR_ID
    room_id = settings.YULE_TEST_ROOM
    user_id = '22014102'
    other_anchor_id = '20000275'

    def setUp(self,*args):
        super(TestHighAdminAddBlackApi,self).setUp()
        for x in [self.user_id,self.high_admin_user_id]:
            del_super_visor_api = DelSuperVisorApi(self.anchor_login_name)
            del_super_visor_api.get({'user_id': x, 'anchor_id': self.anchor_id})
        for x in [self.user_id,self.other_anchor_id]:
            MysqlOperation(user_id=x).clean_black_user()
        Redis().clean_black_user(self.anchor_id)
        RedisHold().clean_redis_user_detail(self.user_id)
        # time.sleep(self.time_sleep)

    def test_high_admin_to_anchor_forbid_visit(self):
        """
        测试高管踢出主播
        :return:
        """
        test_data = {'add_super_visor': False, 'type':None,'user_id': self.anchor_id, 'blacker_type': 'forbid_visit',
                     'is_guard':False,'guard_id':None,'is_noble':None,'noble_id':None,'user_is_anchor':True}
        self.high_admin_add_black_action(**test_data)

    def test_high_admin_to_anchor_forbid_shout(self):
        """
        测试高管对主播禁止喊话
        :return:
        """
        test_data = {'add_super_visor': False, 'type':None,'user_id': self.anchor_id, 'blacker_type': 'forbid_shout',
                     'is_guard':False,'guard_id':None,'is_noble':None,'noble_id':None,'user_is_anchor':True}
        self.high_admin_add_black_action(**test_data)

    def test_high_admin_to_anchor_forbid_speak(self):
        """
        测试高管对主播禁言
        :return:
        """
        test_data = {'add_super_visor': False, 'type':None,'user_id': self.anchor_id, 'blacker_type': 'forbid_speak',
                     'is_guard':False,'guard_id':None,'is_noble':None,'noble_id':None,'user_is_anchor':True}
        self.high_admin_add_black_action(**test_data)

    def test_high_admin_to_user_forbid_visit(self):
        """
        测试高管踢出普通用户
        :return:
        """
        test_data = {'add_super_visor': False,'type':None, 'user_id': self.user_id, 'blacker_type': 'forbid_visit',
                     'is_guard':False,'guard_id':None,'is_noble':None,'noble_id':None,'user_is_anchor':False}
        self.high_admin_add_black_action(**test_data)

    def test_high_admin_to_user_forbid_shout(self):
        """
        测试高管对普通用户禁止喊话
        :return:
        """
        test_data = {'add_super_visor': False,'type':None, 'user_id': self.user_id, 'blacker_type': 'forbid_shout',
                     'is_guard':False,'guard_id':None,'is_noble':None,'noble_id':None,'user_is_anchor':False}
        self.high_admin_add_black_action(**test_data)

    def test_high_admin_to_user_forbid_speak(self):
        """
        测试高管对普通用户禁言
        :return:
        """
        test_data = {'add_super_visor': False,'type':None, 'user_id': self.user_id, 'blacker_type': 'forbid_speak',
                     'is_guard':False,'guard_id':None,'is_noble':None,'noble_id':None,'user_is_anchor':False}
        self.high_admin_add_black_action(**test_data)

    # def test_high_admin_to_high_admin_forbid_visit(self):
    #     test_data = {'add_super_visor': True, 'type':'60','user_id': self.user_id, 'blacker_type': 'forbid_visit',
    #                  'is_guard':False,'guard_id':None,'is_noble':None,'noble_id':None,'user_is_anchor':False}
    #     self.high_admin_add_black_action(**test_data)
    #
    # def test_high_admin_to_high_admin_forbid_shout(self):
    #     test_data = {'add_super_visor': True,'type':'60', 'user_id': self.user_id, 'blacker_type': 'forbid_shout',
    #                  'is_guard':False,'guard_id':None,'is_noble':None,'noble_id':None,'user_is_anchor':False}
    #     self.high_admin_add_black_action(**test_data)
    #
    # def test_high_admin_to_high_admin_forbid_speak(self):
    #     test_data = {'add_super_visor': True,'type':'60', 'user_id': self.user_id, 'blacker_type': 'forbid_speak',
    #                  'is_guard':False,'guard_id':None,'is_noble':None,'noble_id':None,'user_is_anchor':False}
    #     self.high_admin_add_black_action(**test_data)

    def test_high_admin_to_normal_admin_forbid_visit(self):
        """
        测试高管踢出普通管理
        :return:
        """
        test_data = {'add_super_visor': True, 'type':'40','user_id': self.user_id, 'blacker_type': 'forbid_visit',
                     'is_guard':False,'guard_id':None,'is_noble':None,'noble_id':None,'user_is_anchor':False}
        self.high_admin_add_black_action(**test_data)

    def test_high_admin_to_normal_admin_forbid_shout(self):
        """
        测试高管对普通管理禁止喊话
        :return:
        """
        test_data = {'add_super_visor': True,'type':'40', 'user_id': self.user_id, 'blacker_type': 'forbid_shout',
                     'is_guard':False,'guard_id':None,'is_noble':None,'noble_id':None,'user_is_anchor':False}
        self.high_admin_add_black_action(**test_data)

    def test_high_admin_to_normal_admin_forbid_speak(self):
        """
        测试高管对普通管理禁言
        :return:
        """
        test_data = {'add_super_visor': True,'type':'40', 'user_id': self.user_id, 'blacker_type': 'forbid_speak',
                     'is_guard':False,'guard_id':None,'is_noble':None,'noble_id':None,'user_is_anchor':False}
        self.high_admin_add_black_action(**test_data)

    def test_high_admin_to_other_anchor_forbid_visit(self):
        """
        测试高管踢出其他主播
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.other_anchor_id, 'blacker_type': 'forbid_visit',
                     'is_guard': False, 'guard_id': None, 'is_noble': None, 'noble_id': None, 'user_is_anchor': False}
        self.high_admin_add_black_action(**test_data)

    def test_high_admin_to_other_anchor_forbid_shout(self):
        """
        测试高管对其他主播禁止喊话
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.other_anchor_id, 'blacker_type': 'forbid_shout',
                     'is_guard': False, 'guard_id': None, 'is_noble': None, 'noble_id': None, 'user_is_anchor': False}
        self.high_admin_add_black_action(**test_data)

    def test_high_admin_to_other_anchor_forbid_speak(self):
        """
        测试高管对其他主播禁言
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.other_anchor_id, 'blacker_type': 'forbid_speak',
                     'is_guard': False, 'guard_id': None, 'is_noble': None, 'noble_id': None, 'user_is_anchor': False}
        self.high_admin_add_black_action(**test_data)


    def tearDown(self,*args):
        super(TestHighAdminAddBlackApi,self).tearDown()
        for x in [self.user_id,self.high_admin_user_id]:
            del_super_visor_api = DelSuperVisorApi(self.anchor_login_name)
            del_super_visor_api.get({'user_id': x, 'anchor_id': self.anchor_id})
        for x in [self.user_id,self.other_anchor_id]:
            MysqlOperation(user_id=x).clean_black_user()
        Redis().clean_black_user(self.anchor_id)
        RedisHold().clean_redis_user_detail(self.user_id)
        # time.sleep(self.time_sleep)