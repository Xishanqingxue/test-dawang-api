# -*- coding:utf-8 -*-
from test_case.test_black_user.action import BlackUserAction
from utilities.redis_helper import Redis
from utilities.mysql_helper import MysqlOperation
from utilities.teardown import TearDown
import settings


class TestAnchorAddBlackApi(BlackUserAction):
    """
    主播将守护添加到黑名单
    """
    anchor_login_name = settings.YULE_TEST_ANCHOR_LOGIN_NAME
    anchor_id = settings.YULE_TEST_ANCHOR_ID
    room_id = settings.YULE_TEST_ROOM
    user_login_name = '18744447777'
    user_id = '22014102'

    def setUp(self,*args):
        super(TestAnchorAddBlackApi,self).setUp(user_id=self.user_id,anchor_id=self.anchor_id)
        TearDown().guard_teardown(login_name=self.user_login_name, user_id=self.user_id, anchor_id=self.anchor_id)
        MysqlOperation(user_id=self.user_id).clean_black_user()
        Redis().clean_black_user(self.anchor_id)

    def test_anchor_to_bronze_forbid_visit(self):
        """
        测试主播踢出青铜守护
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_visit',
                     'is_guard':True,'guard_id':1,'is_noble':None,'noble_id':None}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_bronze_forbid_shout(self):
        """
        测试主播对青铜守护禁止喊话
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_shout',
                     'is_guard':True,'guard_id':1,'is_noble':None,'noble_id':None}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_bronze_forbid_speak(self):
        """
        测试主播对青铜守护禁言
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_speak',
                     'is_guard':True,'guard_id':1,'is_noble':None,'noble_id':None}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_silver_forbid_visit(self):
        """
        测试主播踢出白银守护
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_visit',
                     'is_guard':True,'guard_id':2,'is_noble':None,'noble_id':None}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_silver_forbid_shout(self):
        """
        测试主播对白银守护禁止喊话
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_shout',
                     'is_guard':True,'guard_id':2,'is_noble':None,'noble_id':None}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_silver_forbid_speak(self):
        """
        测试主播对白银守护禁言
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_speak',
                     'is_guard':True,'guard_id':2,'is_noble':None,'noble_id':None}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_gold_forbid_visit(self):
        """
        测试主播踢出黄金守护
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_visit',
                     'is_guard':True,'guard_id':3,'is_noble':None,'noble_id':None}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_gold_forbid_shout(self):
        """
        测试主播对黄金守护禁止喊话
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_shout',
                     'is_guard':True,'guard_id':3,'is_noble':None,'noble_id':None}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_gold_forbid_speak(self):
        """
        测试主播对黄金守护禁言
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_speak',
                     'is_guard':True,'guard_id':3,'is_noble':None,'noble_id':None}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_diamond_forbid_visit(self):
        """
        测试主播踢出钻石守护
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_visit',
                     'is_guard':True,'guard_id':12,'is_noble':None,'noble_id':None}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_diamond_forbid_shout(self):
        """
        测试主播对钻石守护禁止喊话
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_shout',
                     'is_guard':True,'guard_id':12,'is_noble':None,'noble_id':None}
        self.anchor_add_black_action(**test_data)

    def test_anchor_to_diamond_forbid_speak(self):
        """
        测试主播对钻石守护禁言
        :return:
        """
        test_data = {'add_super_visor': False, 'user_id': self.user_id, 'type': 0, 'blacker_type': 'forbid_speak',
                     'is_guard':True,'guard_id':12,'is_noble':None,'noble_id':None}
        self.anchor_add_black_action(**test_data)

    def tearDown(self,*args):
        super(TestAnchorAddBlackApi,self).tearDown(user_id=self.user_id,anchor_id=self.anchor_id)
        TearDown().guard_teardown(login_name=self.user_login_name, user_id=self.user_id, anchor_id=self.anchor_id)
        MysqlOperation(user_id=self.user_id).clean_black_user()
        Redis().clean_black_user(self.anchor_id)