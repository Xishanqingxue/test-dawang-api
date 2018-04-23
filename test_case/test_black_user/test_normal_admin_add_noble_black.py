# -*- coding:utf-8 -*-
from test_case.test_black_user.action import BlackUserAction
from utilities.redis_helper import Redis
from utilities.mysql_helper import MysqlOperation
from api.super_visor_api import DelSuperVisorApi
import settings


class TestNormalAdminAddBlackApi(BlackUserAction):
    """
    测试普通管理将贵族添加到黑名单
    """
    anchor_login_name = settings.YULE_TEST_ANCHOR_LOGIN_NAME
    anchor_id = settings.YULE_TEST_ANCHOR_ID
    room_id = settings.YULE_TEST_ROOM
    user_id = '22014102'

    def setUp(self,*args):
        super(TestNormalAdminAddBlackApi, self).setUp(self.user_id)
        del_super_visor_api = DelSuperVisorApi(self.anchor_login_name)
        del_super_visor_api.get({'user_id': self.high_admin_user_id, 'anchor_id': self.anchor_id})
        MysqlOperation(user_id=self.user_id).clean_user_noble().clean_black_user()
        # RedisHold().clean_redis_user_detail(self.user_id)
        Redis().clean_black_user(self.anchor_id)
        # time.sleep(self.time_sleep)

    def test_normal_admin_to_knight_forbid_visit(self):
        """
        测试普通管理踢出骑士
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_visit',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 1, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_knight_forbid_shout(self):
        """
        测试普通管理对骑士禁止喊话
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_shout',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 1, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_knight_forbid_speak(self):
        """
        测试普通管理对骑士禁言
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_speak',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 1, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_baron_forbid_visit(self):
        """
        测试普通管理踢出男爵
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_visit',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 2, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_baron_forbid_shout(self):
        """
        测试普通管理对男爵禁止喊话
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_shout',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 2, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_baron_forbid_speak(self):
        """
        测试普通管理对男爵禁言
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_speak',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 2, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_viscount_forbid_visit(self):
        """
        测试普通管理踢出子爵
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_visit',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 3, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_viscount_forbid_shout(self):
        """
        测试普通管理对子爵禁止喊话
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_shout',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 3, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_viscount_forbid_speak(self):
        """
        测试普通管理对子爵禁言
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_speak',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 3, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_earl_forbid_visit(self):
        """
        测试普通管理踢出伯爵
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_visit',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 4, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_earl_forbid_shout(self):
        """
        测试普通管理对伯爵禁止喊话
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_shout',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 4, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_earl_forbid_speak(self):
        """
        测试普通管理对伯爵禁言
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_speak',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 4, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_marquis_forbid_visit(self):
        """
        测试普通管理踢出侯爵
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_visit',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 5, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_marquis_forbid_shout(self):
        """
        测试普通管理对侯爵禁止喊话
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_shout',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 5, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_marquis_forbid_speak(self):
        """
        测试普通管理对侯爵禁言
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_speak',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 5, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_duck_forbid_visit(self):
        """
        测试普通管理踢出公爵
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_visit',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 6, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_duck_forbid_shout(self):
        """
        测试普通管理对公爵禁止喊话
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_shout',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 6, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_duck_forbid_speak(self):
        """
        测试普通管理对公爵禁言
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_speak',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 6, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_monarch_forbid_visit(self):
        """
        测试普通管理踢出帝王
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_visit',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 7, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_monarch_forbid_shout(self):
        """
        测试普通管理对帝王禁止喊话
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_shout',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 7, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_monarch_forbid_speak(self):
        """
        测试普通管理对帝王禁言
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_speak',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 7, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def tearDown(self,*args):
        super(TestNormalAdminAddBlackApi, self).tearDown(self.user_id)
        del_super_visor_api = DelSuperVisorApi(self.anchor_login_name)
        del_super_visor_api.get({'user_id': self.high_admin_user_id, 'anchor_id': self.anchor_id})
        MysqlOperation(user_id=self.user_id).clean_user_noble().clean_black_user()
        # RedisHold().clean_redis_user_detail(self.user_id)
        Redis().clean_black_user(self.anchor_id)
        # time.sleep(self.time_sleep)