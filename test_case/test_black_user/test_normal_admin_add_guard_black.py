# -*- coding:utf-8 -*-
from test_case.test_black_user.action import BlackUserAction
from utilities.redis_helper import Redis
from utilities.mysql_helper import MysqlOperation
from api.super_visor_api import DelSuperVisorApi
from utilities.teardown import TearDown
import settings


class TestNormalAdminAddBlackApi(BlackUserAction):
    """
    普通管理将守护添加到黑名单
    """
    anchor_login_name = settings.YULE_TEST_ANCHOR_LOGIN_NAME
    anchor_id = settings.YULE_TEST_ANCHOR_ID
    room_id = settings.YULE_TEST_ROOM
    user_id = '22014102'

    def setUp(self,*args):
        super(TestNormalAdminAddBlackApi, self).setUp(user_id=self.user_id,anchor_id=self.anchor_id)
        del_super_visor_api = DelSuperVisorApi(self.anchor_login_name)
        del_super_visor_api.get({'user_id': self.normal_admin_user_id, 'anchor_id': self.anchor_id})
        TearDown().guard_teardown(user_id=self.user_id, anchor_id=self.anchor_id)
        MysqlOperation(user_id=self.user_id).clean_black_user()
        Redis().clean_black_user(self.anchor_id)
        # RedisHold().clean_redis_user_detail(self.user_id)
        # time.sleep(self.time_sleep)

    def test_normal_admin_to_bronze_forbid_visit(self):
        """
        测试普通管理踢出青铜守护
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_visit',
                     'is_guard': True, 'guard_id': 1, 'is_noble': None, 'noble_id': None, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_bronze_forbid_shout(self):
        """
        测试普通管理将青铜守护禁止喊话
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_shout',
                     'is_guard': True, 'guard_id': 1, 'is_noble': None, 'noble_id': None, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_bronze_forbid_speak(self):
        """
        测试普通管理将青铜守护禁言
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_speak',
                     'is_guard': True, 'guard_id': 1, 'is_noble': None, 'noble_id': None, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_silver_forbid_visit(self):
        """
        测试普通管理踢出白银守护
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_visit',
                     'is_guard': True, 'guard_id': 2, 'is_noble': None, 'noble_id': None, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_silver_forbid_shout(self):
        """
        测试普通管理将白银守护禁止喊话
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_shout',
                     'is_guard': True, 'guard_id': 2, 'is_noble': None, 'noble_id': None, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_silver_forbid_speak(self):
        """
        测试普通管理将白银守护禁言
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_speak',
                     'is_guard': True, 'guard_id': 2, 'is_noble': None, 'noble_id': None, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_gold_forbid_visit(self):
        """
        测试普通管理踢出黄金守护
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_visit',
                     'is_guard': True, 'guard_id': 3, 'is_noble': None, 'noble_id': None, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_gold_forbid_shout(self):
        """
        测试普通管理将黄金守护禁止喊话
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_shout',
                     'is_guard': True, 'guard_id': 3, 'is_noble': None, 'noble_id': None, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_gold_forbid_speak(self):
        """
        测试普通管理将黄金守护禁言
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_speak',
                     'is_guard': True, 'guard_id': 3, 'is_noble': None, 'noble_id': None, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_diamond_forbid_visit(self):
        """
        测试普通管理踢出钻石守护
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_visit',
                     'is_guard': True, 'guard_id': 12, 'is_noble': None, 'noble_id': None, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_diamond_forbid_shout(self):
        """
        测试普通管理将钻石守护禁止喊话
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_shout',
                     'is_guard': True, 'guard_id': 12, 'is_noble': None, 'noble_id': None, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)

    def test_normal_admin_to_diamond_forbid_speak(self):
        """
        测试普通管理将钻石守护禁言
        :return:
        """
        test_data = {'add_super_visor': False, 'type': None, 'user_id': self.user_id, 'blacker_type': 'forbid_speak',
                     'is_guard': True, 'guard_id': 12, 'is_noble': None, 'noble_id': None, 'user_is_anchor': False}
        self.normal_admin_add_black_action(**test_data)


    def tearDown(self,*args):
        super(TestNormalAdminAddBlackApi, self).tearDown(user_id=self.user_id,anchor_id=self.anchor_id)
        del_super_visor_api = DelSuperVisorApi(self.anchor_login_name)
        del_super_visor_api.get({'user_id': self.normal_admin_user_id, 'anchor_id': self.anchor_id})
        TearDown().guard_teardown(user_id=self.user_id, anchor_id=self.anchor_id)
        MysqlOperation(user_id=self.user_id).clean_black_user()
        Redis().clean_black_user(self.anchor_id)
        # RedisHold().clean_redis_user_detail(self.user_id)
        # time.sleep(self.time_sleep)