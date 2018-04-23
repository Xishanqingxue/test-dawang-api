# # -*- coding:utf-8 -*-
# from action import SendGiftAction
# from utilities.mysql_operation import MysqlOperation
# from utilities import redis_helper
#
#
# class TestSendGift(SendGiftAction):
#     """
#     送大王豆礼物
#     """
#     gift_id = 62
#     gift_diamond = 1000
#
#     def setUp(self):
#         mysql_operation = MysqlOperation(user_id=self.user_id, anchor_id=self.anchor_id)
#         mysql_operation.fix_user_account()
#         mysql_operation.clean_send_gift().clean_user_package_gift()
#         for x in [self.user_id, self.anchor_id]:
#             MysqlOperation(user_id=x).fix_user_rank_and_experience()
#             mysql_operation.clean_user_account_log()
#             redis_helper.clean_redis_user_detail(x)
#         redis_helper.clean_redis_room_detail(self.room_id, self.anchor_id)
#
#
#     def test_send_diamond_gift_1(self):
#         """
#         送出1个大王豆礼物
#         :return:
#         """
#         test_data = {'gift_gold':0,'gift_diamond':self.gift_diamond,'gift_id':self.gift_id,'gift_num':1,'is_following':False}
#         self.send_gift_action(**test_data)
#
#     def test_send_diamond_gift_10(self):
#         """
#         送出10个大王豆礼物
#         :return:
#         """
#         test_data = {'gift_gold':0,'gift_diamond':self.gift_diamond,'gift_id':self.gift_id,'gift_num':10,'is_following':False}
#         self.send_gift_action(**test_data)
#
#     def test_send_diamond_gift_66(self):
#         """
#         送出66个大王豆礼物
#         :return:
#         """
#         test_data = {'gift_gold':0,'gift_diamond':self.gift_diamond,'gift_id':self.gift_id,'gift_num':66,'is_following':False}
#         self.send_gift_action(**test_data)
#
#     def test_send_diamond_gift_99(self):
#         """
#         送出99个大王豆礼物
#         :return:
#         """
#         test_data = {'gift_gold':0,'gift_diamond':self.gift_diamond,'gift_id':self.gift_id,'gift_num':99,'is_following':False}
#         self.send_gift_action(**test_data)
#
#     def test_send_diamond_gift_188(self):
#         """
#         送出188个大王豆礼物
#         :return:
#         """
#         test_data = {'gift_gold':0,'gift_diamond':self.gift_diamond,'gift_id':self.gift_id,'gift_num':188,'is_following':False}
#         self.send_gift_action(**test_data)
#
#     def test_send_diamond_gift_520(self):
#         """
#         送出520个大王豆礼物
#         :return:
#         """
#         test_data = {'gift_gold':0,'gift_diamond':self.gift_diamond,'gift_id':self.gift_id,'gift_num':520,'is_following':False}
#         self.send_gift_action(**test_data)
#
#     def test_send_diamond_gift_1314(self):
#         """
#         送出1314个大王豆礼物
#         :return:
#         """
#         test_data = {'gift_gold':0,'gift_diamond':self.gift_diamond,'gift_id':self.gift_id,'gift_num':1314,'is_following':False}
#         self.send_gift_action(**test_data)
#
#     def tearDown(self):
#         super(TestSendGift,self).tearDown()
#         mysql_operation = MysqlOperation(user_id=self.user_id,anchor_id=self.anchor_id)
#         mysql_operation.fix_user_account().clean_user_account_log()
#         mysql_operation.clean_send_gift().clean_user_package_gift()
#         for x in [self.user_id,self.anchor_id]:
#             MysqlOperation(user_id=x).fix_user_rank_and_experience()
#             redis_helper.clean_redis_user_detail(x)
#         redis_helper.clean_redis_room_detail(self.room_id, self.anchor_id)
