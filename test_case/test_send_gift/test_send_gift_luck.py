# # -*- coding:utf-8 -*-
# from base_api.send_gift_api import SendGiftApi
# from test_case.base_case import BaseCase
# from base_api.consumption_api import ConsumptionApi
# from utilities.mysql_operation import MysqlOperation
# from base_api.gold_account_api import GoldAccountApi
# from utilities import redis_helper
# import json,time,settings,datetime
#
# class TestSendGiftLuck(BaseCase):
#     """
#     送福袋礼物
#     """
#     login_name = settings.YULE_TEST_USER_LOGIN_NAME
#     user_id = settings.YULE_TEST_USER_ID
#     room_id = settings.YULE_TEST_ROOM
#     anchor_id = settings.YULE_TEST_ANCHOR_ID
#     count = 1
#     max_count = 100
#     time_sleep = 0.3
#     gift_id = 8001
#     gift_gold = 10
#     gift_num = 10
#
#     def setUp(self):
#         super(TestSendGiftLuck,self).tearDown()
#         mysql_operation = MysqlOperation(user_id=self.user_id,anchor_id=self.anchor_id)
#         mysql_operation.fix_user_account().clean_user_intimacy_rank().clean_user_account_log()
#         mysql_operation.clean_send_gift().clean_user_package_gift()
#         for x in [self.user_id,self.anchor_id]:
#             MysqlOperation(user_id=x).fix_user_rank_and_experience()
#             redis_helper.clean_redis_user_detail(x)
#         redis_helper.clean_redis_room_detail(self.room_id, self.anchor_id)
#         time.sleep(self.time_sleep)
#
#     def test_send_gift_luck(self):
#         """
#         测试送出福袋礼物暴击
#         :return:
#         """
#         gift_gold = self.gift_gold
#         gift_id = self.gift_id
#         gift_num = self.gift_num
#
#
#         while self.count < self.max_count:
#             mysql_operation = MysqlOperation(user_id=self.user_id)
#             mysql_operation.fix_user_account(gold_num=gift_gold * gift_num)
#             redis_helper.clean_redis_user_detail(self.user_id)
#             time.sleep(self.time_sleep)
#             send_gift_api = SendGiftApi(self.login_name)
#             response = send_gift_api.get({'room_id': self.room_id, 'gift_id': gift_id, 'gift_count': gift_num,'currency': 'gold'})
#             if send_gift_api.get_code() == 100032:
#                 time.sleep(self.time_sleep)
#                 self.count+=1
#             else:
#                 self.assertEqual(send_gift_api.get_code(),0)
#                 gold_account = json.loads(response.content)['result']['identity_obj']['gold']
#                 if gold_account == 0:
#                     time.sleep(self.time_sleep)
#                     self.count+=1
#                 else:
#                     #消费记录
#                     consumption_api = ConsumptionApi(self.login_name)
#                     response = consumption_api.get()
#                     self.assertEqual(consumption_api.get_code(),0)
#                     consume_list = json.loads(response.content)['result']['consume_list'][0]
#                     self.assertEqual(consume_list['user_id'], self.user_id)
#                     self.assertEqual(consume_list['type'], u'1')
#                     self.assertEqual(consume_list['gold'], self.gift_gold)
#                     self.assertEqual(consume_list['corresponding_id'], int(self.gift_id))
#                     self.assertEqual(consume_list['corresponding_name'],MysqlOperation().get_gift_details(self.gift_id)['name'])
#                     self.assertEqual(consume_list['corresponding_num'], 1)
#                     self.assertEqual(consume_list['room_id'], self.room_id)
#                     self.assertEqual(consume_list['status'], 1)
#                     self.assertEqual(consume_list['behavior_desc'], u'送礼')
#                     self.assertEqual(consume_list['room_title'],MysqlOperation(room_id=self.room_id).get_room_details()['title'])
#                     self.assertEqual(consume_list['consumption_type'], u'%s金币' % self.gift_gold)
#
#                     #验证用户金币获取记录
#                     gold_account_api = GoldAccountApi(self.login_name)
#                     response = gold_account_api.get()
#                     self.assertEqual(gold_account_api.get_code(),0)
#                     account_list = json.loads(response.content)['result']['account_list']
#                     self.assertEqual(len(account_list), 1)
#                     self.assertEqual(account_list[0]['user_id'], self.user_id)
#                     self.assertIn(datetime.datetime.now().strftime("%Y-%m-%d"), account_list[0]['create_time'])
#                     self.assertEqual(account_list[0]['type'], u'2')
#                     self.assertEqual(account_list[0]['gold'], gold_account)
#                     self.assertEqual(account_list[0]['corresponding_id'], 0)
#                     self.assertEqual(account_list[0]['corresponding_name'], u'礼物暴击')
#                     self.assertEqual(account_list[0]['corresponding_num'], 0)
#                     self.assertEqual(account_list[0]['status'], 1)
#                     self.assertEqual(account_list[0]['behavior_desc'], u'礼物暴击')
#                     self.assertEqual(account_list[0]['room_title'],MysqlOperation(room_id=self.room_id).get_room_details()['title'])
#                     self.assertEqual(account_list[0]['consumption_type'], u'%s金币' % gold_account)
#                     self.assertEqual(account_list[0]['money'], 0)
#                     break
#             self.assertLess(self.count,self.max_count)
#
#
#
#
#
#     def tearDown(self):
#         super(TestSendGiftLuck,self).tearDown()
#         mysql_operation = MysqlOperation(user_id=self.user_id,anchor_id=self.anchor_id)
#         mysql_operation.fix_user_account().clean_user_intimacy_rank().clean_user_account_log()
#         mysql_operation.clean_send_gift().clean_user_package_gift()
#         for x in [self.user_id,self.anchor_id]:
#             MysqlOperation(user_id=x).fix_user_rank_and_experience()
#             redis_helper.clean_redis_user_detail(x)
#         redis_helper.clean_redis_room_detail(self.room_id, self.anchor_id)
#         time.sleep(self.time_sleep)