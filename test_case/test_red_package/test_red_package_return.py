# # -*- coding:utf-8 -*-
# from test_case.base_case import BaseCase
# from base_api.red_package.send_red_package_api import SendRedPacketApi
# from base_api.gold_account_api import GoldAccountApi
# from utilities.mysql_operation import MysqlOperation
# from utilities import redis_helper
# import time,json,settings,datetime
#
#
#
# class TestRedPackageReturn(BaseCase):
#     """
#     红包过期后返还
#     """
#     login_name = settings.YULE_TEST_USER_LOGIN_NAME
#     user_id = settings.YULE_TEST_USER_ID
#     room_id = settings.YULE_TEST_ROOM
#     anchor_id=settings.YULE_TEST_ANCHOR_ID
#     time_sleep = 2
#
#     def setUp(self):
#         super(TestRedPackageReturn, self).tearDown()
#         red_packet_ids = MysqlOperation(room_id=self.room_id).get_red_packet_ids()
#         MysqlOperation(room_id=self.room_id).clean_red_packet()
#         MysqlOperation(user_id=self.user_id, anchor_id=self.anchor_id).clean_send_gift()
#         for i in red_packet_ids:
#             redis_helper.clean_red_packet(self.room_id, i['id'])
#         redis_helper.clean_redis_room_detail(self.room_id, self.anchor_id)
#         for x in [self.user_id, self.anchor_id]:
#             MysqlOperation(user_id=x).fix_user_rank_and_experience().clean_user_account_log()
#             redis_helper.clean_redis_user_detail(x)
#         time.sleep(self.time_sleep)
#
#     def test_send_red_packet_gold_return(self):
#         """
#         测试红包过期后将剩余金币返还给用户
#         :return:
#         """
#         mysql_operation = MysqlOperation(user_id=self.user_id)
#         mysql_operation.fix_user_account(gold_num=50000)
#         redis_helper.clean_redis_user_detail(self.user_id)
#         time.sleep(self.time_sleep)
#         # 发红包
#         send_red_packet_api = SendRedPacketApi(self.login_name)
#         response = send_red_packet_api.get({'conf_id': 1, 'room_id': self.room_id, 'num': 50, 'currency': 'gold'})
#         self.assertEqual(send_red_packet_api.get_code(), 0)
#         red_packet_id= json.loads(response.content)['result']['red_packet_obj']['id']
#         time.sleep(5)
#         red_packet_end_time = time.time() + 30
#         MysqlOperation().fix_red_packet_end_time(red_packet_id,red_packet_end_time)
#         redis_helper.set_red_packet_end_time(self.room_id,red_packet_id,red_packet_end_time)
#         count = 1
#         max_count = 30
#         while count < max_count:
#             user_gold = MysqlOperation(user_id=self.user_id).get_user_account_details()['gold']
#             if user_gold == 0:
#                 time.sleep(self.time_sleep)
#                 count+=1
#             else:
#                 self.assertLessEqual(user_gold,400000)
#                 self.assertLess(0,user_gold)
#                 break
#         self.assertLess(count,max_count)
#
#         gold_account_api = GoldAccountApi(self.login_name)
#         response = gold_account_api.get()
#         self.assertEqual(gold_account_api.get_code(), 0)
#
#         account_list = json.loads(response.content)['result']['account_list']
#         self.assertEqual(len(account_list), 1)
#         self.assertEqual(account_list[0]['user_id'], self.user_id)
#         self.assertIn(datetime.datetime.now().strftime("%Y-%m-%d"), account_list[0]['create_time'])
#         self.assertEqual(account_list[0]['type'], u'3')
#         self.assertNotEqual(account_list[0]['gold'], 0)
#
#         self.assertEqual(account_list[0]['corresponding_id'], 107009)
#         self.assertEqual(account_list[0]['corresponding_name'], u'')
#         self.assertEqual(account_list[0]['corresponding_num'], 0)
#         self.assertEqual(account_list[0]['status'], 1)
#         self.assertEqual(account_list[0]['behavior_desc'], u'过期红包返还')
#         self.assertEqual(account_list[0]['room_title'], MysqlOperation(room_id=self.room_id).get_room_details()['title'])
#         self.assertEqual(account_list[0]['consumption_type'], u'%s金币' % account_list[0]['gold'])
#         self.assertEqual(account_list[0]['money'], 0)
#
#
#
#     def tearDown(self):
#         super(TestRedPackageReturn,self).tearDown()
#         red_packet_ids = MysqlOperation(room_id=self.room_id).get_red_packet_ids()
#         MysqlOperation(room_id=self.room_id).clean_red_packet()
#         MysqlOperation(user_id=self.user_id,anchor_id=self.anchor_id).clean_send_gift()
#         for i in red_packet_ids:
#             redis_helper.clean_red_packet(self.room_id,i['id'])
#         redis_helper.clean_redis_room_detail(self.room_id, self.anchor_id)
#         for x in [self.user_id,self.anchor_id]:
#             MysqlOperation(user_id=x).fix_user_rank_and_experience().clean_user_account_log()
#             redis_helper.clean_redis_user_detail(x)
#         time.sleep(self.time_sleep)