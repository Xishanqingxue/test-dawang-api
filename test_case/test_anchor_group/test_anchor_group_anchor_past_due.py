# # -*- coding:utf-8 -*-
# from test_case.base_case import BaseCase
# from base_api.buy_guard import BuyGuardApi
# from base_api.anchor_group.open_anchor_group_api import OpenAnchorGroupApi
# from base_api.anchor_group.add_anchor_to_group_api import AddAnchorToGroupApi
# from base_api.anchor_group.my_anchor_group_logs_api import MyAnchorGroupLogsApi
# from base_api.anchor_group.my_anchor_group_list_api import MyAnchorGroupListApi
# from utilities import redis_helper
# from utilities.mysql_operation import MysqlOperation
# from settings import YULE_TEST_ANCHOR_ID as anchor_id,YULE_TEST_ROOM as room_id
# import json, time
# from settings import YULE_TEST_USER_LOGIN_NAME,YULE_TEST_USER_ID
#
# class TestAnchorGroupPastDueApi(BaseCase):
#     """
#     主播团主播到期
#     """
#     user_login_name = YULE_TEST_USER_LOGIN_NAME
#     user_id = YULE_TEST_USER_ID
#     user_rank = 12
#     user_experience_all = 3000000
#     count = 1
#     max_count = 20
#     time_sleep = 0.2
#
#     def setUp(self):
#         user_id = self.user_id
#         mysql_operation = MysqlOperation(user_id=user_id)
#         redis_helper.clean_anchor_group(user_id, anchor_id=anchor_id)
#         for i in [user_id, anchor_id]:
#             redis_helper.clean_redis_user_detail(i)
#             MysqlOperation(user_id=i).clean_user_anchor_group().clean_user_account_log()
#         mysql_operation.fix_user_rank_and_experience()
#         mysql_operation.fix_user_account()
#         redis_helper.clean_user_buy_guard(user_id, anchor_id)
#         redis_helper.clean_redis_user_detail(user_id)
#         redis_helper.clean_redis_room_detail(room_id, anchor_id)
#
#     def test_anchor_group_anchor_past_due(self):
#         """
#         测试主播团中主播到期后自动脱离主播团
#         :return:
#         """
#         user_id = self.user_id
#         while self.count < self.max_count:
#             mysql_operation = MysqlOperation(user_id=user_id)
#             mysql_operation.fix_user_rank_and_experience(user_rank=self.user_rank, experience_all=self.user_experience_all)
#             mysql_operation.fix_user_account(gold_num=100000)
#             redis_helper.clean_redis_user_detail(self.user_id)
#             # 开通主播团
#             open_anchor_group_api = OpenAnchorGroupApi(self.user_login_name)
#             open_anchor_group_api.get()
#             if open_anchor_group_api.get_code() == 200502:
#                 time.sleep(self.time_sleep)
#                 self.count+=1
#             else:
#                 self.assertEqual(open_anchor_group_api.get_code(), 0)
#                 break
#         self.assertLess(self.count,self.max_count)
#         # 购买守护
#         while self.count < self.max_count:
#             mysql_operation = MysqlOperation(user_id=user_id)
#             mysql_operation.fix_user_rank_and_experience(user_rank=self.user_rank,
#                                                          experience_all=self.user_experience_all)
#             mysql_operation.fix_user_account(gold_num=1226000)
#             redis_helper.clean_redis_user_detail(self.user_id)
#             buy_guard_api = BuyGuardApi(self.user_login_name)
#             guard_response = buy_guard_api.get({'room_id': room_id, 'guard_id': '2','currency':'gold'})
#             if buy_guard_api.get_code() == 100032:
#                 time.sleep(self.time_sleep)
#                 self.count+=1
#             else:
#                 self.assertEqual(buy_guard_api.get_code(), 0)
#                 self.assertEqual(json.loads(guard_response.content)['result']['identity_obj']['user_guard_obj']['guard_rank'], 2)
#                 time.sleep(3)
#                 # 将主播纳入主播团
#                 add_anchor_to_group_api = AddAnchorToGroupApi(self.user_login_name)
#                 add_anchor_to_group_api.get({'anchor_id': anchor_id, 'position': 1,'grab_flag': 0,'change_flag': 0})
#                 self.assertEqual(add_anchor_to_group_api.get_code(), 0)
#                 time.sleep(2)
#                 my_anchor_group_list_api = MyAnchorGroupListApi(self.user_login_name)
#                 list_response = my_anchor_group_list_api.get()
#                 self.assertEqual(my_anchor_group_list_api.get_code(), 0)
#                 self.assertEqual(json.loads(list_response.content)['result']['anchor_group_obj']['owend_anchor_count'],1)
#
#                 now_time = time.time() + 30
#                 redis_helper.set_anchor_group_anchor_end_time(anchor_id,now_time)
#                 time.sleep(600)
#                 my_anchor_group_list_api = MyAnchorGroupListApi(self.user_login_name)
#                 list_response = my_anchor_group_list_api.get()
#                 self.assertEqual(my_anchor_group_list_api.get_code(), 0)
#                 self.assertEqual(json.loads(list_response.content)['result']['anchor_group_obj']['owend_anchor_count'],0)
#
#                 my_anchor_group_logs_api = MyAnchorGroupLogsApi(self.user_login_name)
#                 logs_response = my_anchor_group_logs_api.get()
#                 my_anchor_group_logs_list = json.loads(logs_response.content)['result']['anchor_group_log_list']
#                 self.assertEqual(my_anchor_group_logs_api.get_code(),0)
#
#                 self.assertEqual(len(my_anchor_group_logs_list),2)
#                 self.assertIn(u'在驻留时间到期后自动脱离主播团',my_anchor_group_logs_list[0]['content'])
#                 break
#         self.assertLess(self.count,self.max_count)
#
#     def tearDown(self):
#         user_id = self.user_id
#         mysql_operation = MysqlOperation(user_id=user_id)
#         mysql_operation.clean_user_anchor_group()
#         redis_helper.clean_anchor_group(user_id, anchor_id=anchor_id)
#         for i in [user_id, anchor_id]:
#             redis_helper.clean_redis_user_detail(i)
#             MysqlOperation(user_id=i).clean_user_anchor_group().clean_user_account_log()
#         mysql_operation.fix_user_rank_and_experience()
#         mysql_operation.fix_user_account()
#         redis_helper.clean_user_buy_guard(user_id, anchor_id)
#         redis_helper.clean_redis_user_detail(user_id)
#         redis_helper.clean_redis_room_detail(room_id, anchor_id)
