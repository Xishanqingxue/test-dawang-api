# # -*- coding:utf-8 -*-
# from base_api.publish_dynamic.publish_dynamic_api import PublishDynamicApi
# from base_api.publish_dynamic.remove_dynamic_api import RemoveDynamicApi
# from base_api.publish_dynamic.get_home_page_dynamic_list_api import GetHomePageDynamicApi
# from base_api.publish_dynamic.little_red_dot_api import LittleRedDotApi
# from test_case.base_case import BaseCase
# from utilities import redis_helper
# from utilities.mysql_operation import MysqlOperation
# import json,settings
#
#
#
# class TestLittleRedDotApi(BaseCase):
#     """
#     动态小红点
#     """
#     anchor_mobile = settings.YULE_TEST_ANCHOR_LOGIN_NAME
#     anchor_id = settings.YULE_TEST_ANCHOR_ID
#     user_mobile = settings.YULE_TEST_ANCHOR_LOGIN_NAME
#     user_id = MysqlOperation(mobile=user_mobile).get_user_id()
#     pic_url = ['pic/58/c2/58c2689b7c0730d7b605cb8beeb13702_0.png']
#     video_url = ['video/e0/90/e09069c0b0792e362dd7cfbf0b0b8642.mp4']
#     content = 'Auto Test!!'
#     time_sleep = 0.3
#     dynamic_ids = []
#
#     def test_little_red_dot_api(self):
#         """
#         测试请求小红点接口成功
#         :return:
#         """
#         publish_dynamic_api = PublishDynamicApi(self.anchor_mobile)
#         publish_dynamic_api.get({'type': 2, 'image_urls': None, 'video_url': self.video_url,
#              'content': self.content, 'first_frame': self.pic_url})
#         self.assertEqual(publish_dynamic_api.get_code(), 0)
#
#         get_home_page_dynamic_list_api = GetHomePageDynamicApi(self.anchor_mobile)
#         response = get_home_page_dynamic_list_api.get({'anchor_id': self.anchor_id})
#
#         self.assertEqual(get_home_page_dynamic_list_api.get_code(), 0)
#         anchor_dynamic_list = json.loads(response.content)['result']['dynamic_list']
#         for x in anchor_dynamic_list:
#             self.dynamic_ids.append(x['id'])
#         self.assertEqual(len(anchor_dynamic_list),1)
#         dynamic_id = anchor_dynamic_list[0]['id']
#
#         redis_helper.check_anchor_dynamic(dynamic_id)
#         little_red_dot_api = LittleRedDotApi(self.user_mobile)
#         response = little_red_dot_api.get({'local_dynamic_id':int(dynamic_id)-1})
#
#         self.assertEqual(little_red_dot_api.get_code(),0)
#         self.assertEqual(json.loads(response.content)['result']['show_square_red_point'],1)
#
#         little_red_dot_api = LittleRedDotApi(self.user_mobile)
#         response = little_red_dot_api.get({'local_dynamic_id':dynamic_id})
#         self.assertEqual(little_red_dot_api.get_code(),0)
#         self.assertEqual(json.loads(response.content)['result']['show_square_red_point'],0)
#
#     def test_little_red_dot_dynamic_id_is_null(self):
#         """
#         测试请求接口动态ID为空
#         :return:
#         """
#         little_red_dot_api = LittleRedDotApi(self.user_mobile)
#         little_red_dot_api.get({'local_dynamic_id': None})
#
#         self.assertEqual(little_red_dot_api.get_code(), 450007)
#         self.assertEqual(little_red_dot_api.get_response_message(),u'动态id不能为空')
#
#     def test_little_red_dot_dynamic_id_is_error(self):
#         """
#         测试请求接口动态ID错误
#         :return:
#         """
#         little_red_dot_api = LittleRedDotApi(self.user_mobile)
#         little_red_dot_api.get({'local_dynamic_id': '781623'})
#
#         self.assertEqual(little_red_dot_api.get_code(), 450007)
#         self.assertEqual(little_red_dot_api.get_response_message(), u'动态id不能为空')
#
#
#     def tearDown(self):
#         super(TestLittleRedDotApi,self).tearDown()
#         for i in self.dynamic_ids:
#             RemoveDynamicApi(self.anchor_mobile).get({'dynamic_id': i})
