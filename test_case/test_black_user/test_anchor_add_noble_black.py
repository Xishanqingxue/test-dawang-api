# -*- coding:utf-8 -*-
from test_case.test_black_user.action import BlackUserAction
from utilities.redis_helper import Redis
from utilities.mysql_helper import MysqlOperation
import settings


class TestAnchorAddBlackApi(BlackUserAction):
    """
    主播将贵族添加到黑名单
    """
    anchor_login_name = settings.YULE_TEST_ANCHOR_LOGIN_NAME
    anchor_id = settings.YULE_TEST_ANCHOR_ID
    room_id = settings.YULE_TEST_ROOM
    user_id = '22014102'
    # time_sleep = 0.5

    def setUp(self,*args):
        super(TestAnchorAddBlackApi, self).setUp(user_id=self.user_id,anchor_id=self.anchor_id)
        MysqlOperation(user_id=self.user_id).clean_user_noble().clean_black_user()
        Redis().clean_black_user(self.anchor_id)
        # time.sleep(self.time_sleep)

    def test_anchor_to_knight_forbid_visit(self):
        """
        测试主播踢出骑士
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_visit',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 1}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_knight_forbid_shout(self):
        """
        测试主播对骑士禁止喊话
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_shout',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 1}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_knight_forbid_speak(self):
        """
        测试主播对骑士禁言
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_speak',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 1}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_baron_forbid_visit(self):
        """
        测试主播踢出男爵
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_visit',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 2}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_baron_forbid_shout(self):
        """
        测试主播对男爵禁止喊话
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_shout',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 2}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_baron_forbid_speak(self):
        """
        测试主播对男爵禁言
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_speak',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 2}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_viscount_forbid_visit(self):
        """
        测试主播踢出子爵
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_visit',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 3}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_viscount_forbid_shout(self):
        """
        测试主播对子爵禁止喊话
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_shout',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 3}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_viscount_forbid_speak(self):
        """
        测试主播对子爵禁言
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_speak',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 3}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_earl_forbid_visit(self):
        """
        测试主播踢出伯爵
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_visit',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 4}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_earl_forbid_shout(self):
        """
        测试主播对伯爵禁止喊话
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_shout',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 4}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_earl_forbid_speak(self):
        """
        测试主播对伯爵禁言
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_speak',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 4}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_marquis_forbid_visit(self):
        """
        测试主播踢出侯爵
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_visit',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 5}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_marquis_forbid_shout(self):
        """
        测试主播对侯爵禁止喊话
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_shout',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 5}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_marquis_forbid_speak(self):
        """
        测试主播对侯爵禁言
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_speak',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 5}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_duck_forbid_visit(self):
        """
        测试主播踢出公爵
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_visit',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 6}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_duck_forbid_shout(self):
        """
        测试主播对公爵禁止喊话
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_shout',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 6}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_duck_forbid_speak(self):
        """
        测试主播对公爵禁言
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_speak',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 6}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_monarch_forbid_visit(self):
        """
        测试主播踢出帝王
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_visit',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 7}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_monarch_forbid_shout(self):
        """
        测试主播对帝王禁止喊话
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_shout',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 7}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_monarch_forbid_speak(self):
        """
        测试主播对帝王禁言
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_speak',
                     'is_guard': False, 'guard_id': None, 'is_noble': True, 'noble_id': 7}
        self.anchor_add_black_action(**test_data)

    def tearDown(self,*args):
        super(TestAnchorAddBlackApi, self).tearDown(user_id=self.user_id,anchor_id=self.anchor_id)
        MysqlOperation(user_id=self.user_id).clean_user_noble().clean_black_user()
        Redis().clean_black_user(self.anchor_id)
        # time.sleep(self.time_sleep)