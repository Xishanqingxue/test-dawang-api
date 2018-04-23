# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.quiz_api import StopQuizApi
from settings import YULE_TEST_GAME_ANCHOR_LOGIN_NAME,YULE_TEST_USER_LOGIN_NAME

class TestStopQuizApi(BaseCase):
    """
    竞猜-停止竞猜
    """
    game_anchor_login_name = YULE_TEST_GAME_ANCHOR_LOGIN_NAME
    user_login_name = YULE_TEST_USER_LOGIN_NAME


    def test_stop_quiz_question_id_null(self):
        """
        测试请求接口问题ID为空
        :return:
        """
        stop_quiz_api = StopQuizApi(self.game_anchor_login_name)
        stop_quiz_api.get({'question_id':None})
        self.assertEqual(stop_quiz_api.get_code(),505202)
        self.assertEqual(stop_quiz_api.get_response_message(),u'问题id不能为空')

    def test_stop_quiz_question_id_error(self):
        """
        测试请求接口问题ID错误
        :return:
        """
        stop_quiz_api = StopQuizApi(self.game_anchor_login_name)
        stop_quiz_api.get({'question_id':'999'})
        self.assertEqual(stop_quiz_api.get_code(),505404)
        self.assertEqual(stop_quiz_api.get_response_message(),u'权限不足')

    def test_stop_quiz_not_anchor(self):
        """
        测试普通用户停止竞猜
        :return:
        """
        stop_quiz_api = StopQuizApi(self.user_login_name)
        stop_quiz_api.get({'question_id':'999'})
        self.assertEqual(stop_quiz_api.get_code(),505404)
        self.assertEqual(stop_quiz_api.get_response_message(),u'权限不足')