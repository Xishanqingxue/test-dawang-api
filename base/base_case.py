# -*- coding:utf-8 -*-
from unittest import TestCase
from api.image_code_api import ImageCodeApi
from api.send_sms_code_api import SendSmsCodeApi
from api.register_api import RegisterApi
from utilities.redis_helper import Redis, RedisHold
from utilities.mysql_helper import MysqlOperation
from base.base_log import BaseLogger
from base.base_helper import generate_random_nickname
import time
import json

logger = BaseLogger(__name__).get_logger()


#
# class BaseCase(TestCase):
#     """
#     1、手机号在上层继承该类时重新定义
#     2、随机生成一个默认5个汉字的用户昵称，也可重新定义指定昵称
#     """
#     user_mobile = ''
#     init_user=False
#     nickname = generate_random_nickname(words=5)
#     api_id = ''
#     test_module = ''
#
#     @classmethod
#     def setUpClass(cls):
#         """
#         类方法：初始化新用户信息(注册流程)
#         :param init:
#         :return:
#         """
#         count = 1
#         max_count = 10
#         if cls.init_user:
#             logger.info('Initializing the user.')
#             ImageCodeApi().get()
#             image_code = Redis().get_image_captcha()
#             logger.info('Image code is {0}.'.format(image_code))
#
#             send_sms_code_api = SendSmsCodeApi()
#             resp = send_sms_code_api.get({'type': 'register', 'phone': cls.user_mobile,'check_code': image_code})
#             try:
#                 assert send_sms_code_api.get_resp_code() == 0
#             except AssertionError:
#                 logger.error('Send sms code failed.')
#                 logger.error('Send sms api response:{0}'.format(json.loads(resp.content)))
#             logger.info('Send sms code successful.')
#             sms_code = None
#             while count < max_count:
#                 sms_code = MysqlOperation(mobile=cls.user_mobile).get_sms_code()
#                 if sms_code:
#                     break
#                 else:
#                     time.sleep(0.5)
#                     count+=1
#             assert count < max_count
#             logger.info('Sms code is {0}.'.format(sms_code))
#
#             try:
#                 register_api = RegisterApi()
#                 resp = register_api.get({'login_name': cls.user_mobile, 'code': sms_code,'nickname': cls.nickname})
#                 assert register_api.get_resp_code() == 0
#                 logger.info('User initialization is successful.')
#             except AssertionError:
#                 logger.error('User initialization failed.')
#                 logger.error('Register api response:{0}'.format(json.loads(resp.content)))
#         else:
#             logger.info('There is no need to initialize user information.')
#         time.sleep(0.5)
#
#     @classmethod
#     def tearDownClass(cls):
#         """
#         类方法：清除用户信息
#         :return:
#         """
#         logger.info('Deleting user information.')
#         user_id = MysqlOperation(mobile=cls.user_mobile).get_user_id()
#         MysqlOperation(user_id=user_id,mobile=cls.user_mobile).delete_user()
#         RedisHold().clean_redis_user_detail(user_id)
#         logger.info('Delete user information complete.')
#         time.sleep(0.5)


class BaseCase(TestCase):


    def init_user_and_room(self, user_id, anchor_id):
        """
        初始化用户信息或房间信息
        :param user_id:
        :param room_id:
        :return:
        """
        if user_id:
            logger.info('正在初始化用户信息...')
            if isinstance(user_id, (str, int)):
                MysqlOperation(user_id=user_id).fix_user_account().fix_user_rank_and_experience(). \
                    clean_user_exp_log().clean_user_account_log().clean_user_intimacy_rank().clean_user_contribution()
                RedisHold().clean_redis_user_detail(user_id)
            elif isinstance(user_id, (list, tuple, set)):
                for i in user_id:
                    MysqlOperation(user_id=i).fix_user_account().fix_user_rank_and_experience(). \
                        clean_user_exp_log().clean_user_account_log().clean_user_intimacy_rank().clean_user_contribution()
                    RedisHold().clean_redis_user_detail(i)
            logger.info('初始化用户信息完成!')
        else:
            logger.info('无需初始化用户信息!')

        if anchor_id:
            logger.info('正在初始化主播信息...')
            if isinstance(anchor_id, (str, int)):
                MysqlOperation(anchor_id=anchor_id,
                               user_id=anchor_id).fix_anchor_rank_and_exp().clean_user_account_log()
                RedisHold().clean_redis_user_detail(anchor_id)
            elif isinstance(anchor_id, (list, tuple, set)):
                for i in anchor_id:
                    MysqlOperation(anchor_id=anchor_id,
                                   user_id=anchor_id).fix_anchor_rank_and_exp().clean_user_account_log()
                    RedisHold().clean_redis_user_detail(i)
            logger.info('初始化主播信息完成!')
        else:
            logger.info('无需初始化主播信息!')

    def setUp(self, user_id=None, anchor_id=None):
        """
        用例执行前初始化用户或房间信息
        :param user_id:
        :param room_id:
        :return:
        """
        logger.info('正在执行用例SetUp...')
        self.init_user_and_room(user_id, anchor_id)

    def tearDown(self, user_id=None, anchor_id=None):
        """
        用例执行完成后初始化用户或房间信息
        :param user_id:
        :param room_id:
        :return:
        """
        logger.info('正在执行用例TearDown...')
        self.init_user_and_room(user_id, anchor_id)