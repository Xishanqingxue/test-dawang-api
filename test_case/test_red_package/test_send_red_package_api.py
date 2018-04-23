# -*- coding:utf-8 -*-
from test_case.test_red_package.action import Action
import time
from utilities.teardown import TearDown


class TestSendRedPackageApi(Action):
    """
    红包
    """

    def setUp(self,*args):
        super(TestSendRedPackageApi,self).setUp(user_id=self.user_id,anchor_id=self.anchor_id)
        TearDown().send_red_package_teardown(room_id=self.room_id,user_id=self.user_id,anchor_id=self.anchor_id)

    def test_send_welfare_50(self):
        """
        测试发送50个福利包/发红包历史/可抢红包列表/抢红包/抢红包历史
        :return:
        """
        test_data = {'price':50000,'conf_id':1,'num':50}
        self.send_action(**test_data)

    def test_send_welfare_100(self):
        """
        测试发送100个福利包/发红包历史/可抢红包列表
        :return:
        """
        test_data = {'price':50000,'conf_id':1,'num':100}
        self.send_action(**test_data)

    def test_send_welfare_200(self):
        """
        测试发送200个福利包/发红包历史/可抢红包列表
        :return:
        """
        test_data = {'price':50000,'conf_id':1,'num':200}
        self.send_action(**test_data)

    def test_send_tyrant_50(self):
        """
        测试发送50个土豪包/发红包历史/可抢红包列表/抢红包/抢红包历史
        :return:
        """
        test_data = {'price': 100000, 'conf_id': 2, 'num': 50}
        self.send_action(**test_data)

    def test_send_tyrant_100(self):
        """
        测试发送100个土豪包/发红包历史/可抢红包列表
        :return:
        """
        test_data = {'price': 100000, 'conf_id': 2, 'num': 100}
        self.send_action(**test_data)

    def test_send_tyrant_200(self):
        """
        测试发送200个土豪包/发红包历史/可抢红包列表
        :return:
        """
        test_data = {'price': 100000, 'conf_id': 2, 'num': 200}
        self.send_action(**test_data)

    def test_send_extreme_50(self):
        """
        测试发送50个至尊包/发红包历史/可抢红包列表/抢红包/抢红包历史
        :return:
        """
        test_data = {'price': 588000, 'conf_id': 3, 'num': 50}
        self.send_action(**test_data)

    def test_send_extreme_100(self):
        """
        测试发送100个至尊包/发红包历史/可抢红包列表
        :return:
        """
        test_data = {'price': 588000, 'conf_id': 3, 'num': 100}
        self.send_action(**test_data)

    def test_send_extreme_200(self):
        """
        测试发送200个至尊包/发红包历史/可抢红包列表
        :return:
        """
        test_data = {'price': 588000, 'conf_id': 3, 'num': 200}
        self.send_action(**test_data)

    def tearDown(self,*args):
        super(TestSendRedPackageApi,self).tearDown(user_id=self.user_id,anchor_id=self.anchor_id)
        TearDown().send_red_package_teardown(room_id=self.room_id, user_id=self.user_id, anchor_id=self.anchor_id)