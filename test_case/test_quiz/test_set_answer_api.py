# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.quiz_api import SetQuestionsApi,StartQuizApi,StopQuizApi,SetAnswerApi
from utilities.mysql_helper import MysqlOperation
from utilities.redis_helper import Redis
from settings import YULE_TEST_GAME_ANCHOR_LOGIN_NAME,YULE_TEST_GAME_ANCHOR_ID,YULE_TEST_GAME_ROOM
from settings import YULE_TEST_USER_LOGIN_NAME,YULE_TEST_USER_ID
import json,time

class TestSetAnswerApi(BaseCase):
    """
    竞猜-设置答案
    """
    game_anchor_login_name = YULE_TEST_GAME_ANCHOR_LOGIN_NAME
    game_anchor_id = YULE_TEST_GAME_ANCHOR_ID
    game_room = YULE_TEST_GAME_ROOM
    questions = u'自动化测试添加题目。'
    option_a = u'选项A'
    option_b = u'选项B'
    time_sleep = 0.3
    user_login_name = YULE_TEST_USER_LOGIN_NAME
    user_id = YULE_TEST_USER_ID

    def test_set_answer_question_id_null(self):
        """
        测试请求接口问题ID为空
        :return:
        """
        set_answer_api = SetAnswerApi(self.game_anchor_login_name)
        set_answer_api.get({'question_id': None,'option':1})
        self.assertEqual(set_answer_api.get_code(),505202)
        self.assertEqual(set_answer_api.get_response_message(),u'问题id不能为空')

    def test_set_answer_question_id_error(self):
        """
        测试请求接口问题ID错误
        :return:
        """
        set_answer_api = SetAnswerApi(self.game_anchor_login_name)
        set_answer_api.get({'question_id': '999','option':'A'})
        self.assertEqual(set_answer_api.get_code(),505207)
        self.assertEqual(set_answer_api.get_response_message(),u'竞猜题目不存在')

    def test_set_answer_option_null(self):
        """
        测试请求接口选项为空
        :return:
        """
        set_questions_api = SetQuestionsApi(self.game_anchor_login_name)
        set_questions_api.get({'room_id': self.game_room, 'question': self.questions, 'option_a': self.option_a,
                               'option_b': self.option_b})
        self.assertEqual(set_questions_api.get_code(), 0)

        db_questions = MysqlOperation(room_id=self.game_room).get_questions()
        self.assertEqual(len(db_questions), 1)
        question_ids = []
        for x in db_questions:
            question_ids.append(x['id'])
        question_ids_json = json.dumps(question_ids)

        start_quiz_api = StartQuizApi(self.game_anchor_login_name)
        start_quiz_api.get({'room_id': self.game_room, 'question_bank_ids': question_ids_json})
        self.assertEqual(start_quiz_api.get_code(), 0)

        quiz_questions_id = MysqlOperation(room_id=self.game_room).get_quiz_questions()[0]['id']

        stop_quiz_api = StopQuizApi(self.game_anchor_login_name)
        stop_quiz_api.get({'question_id': quiz_questions_id})
        self.assertEqual(stop_quiz_api.get_code(), 0)

        set_answer_api = SetAnswerApi(self.game_anchor_login_name)
        set_answer_api.get({'question_id': quiz_questions_id, 'option': None})
        self.assertEqual(set_answer_api.get_code(), 505206)
        self.assertEqual(set_answer_api.get_response_message(), u'竞猜选项不能为空')

    def test_set_answer_not_stop_quiz(self):
        """
        测试未停止竞猜设置答案
        :return:
        """
        set_questions_api = SetQuestionsApi(self.game_anchor_login_name)
        set_questions_api.get({'room_id': self.game_room, 'question': self.questions, 'option_a': self.option_a,
                               'option_b': self.option_b})
        self.assertEqual(set_questions_api.get_code(), 0)

        db_questions = MysqlOperation(room_id=self.game_room).get_questions()
        self.assertEqual(len(db_questions), 1)
        question_ids = []
        for x in db_questions:
            question_ids.append(x['id'])
        question_ids_json = json.dumps(question_ids)

        start_quiz_api = StartQuizApi(self.game_anchor_login_name)
        start_quiz_api.get({'room_id': self.game_room, 'question_bank_ids': question_ids_json})
        self.assertEqual(start_quiz_api.get_code(), 0)

        quiz_questions_id = MysqlOperation(room_id=self.game_room).get_quiz_questions()[0]['id']

        set_answer_api = SetAnswerApi(self.game_anchor_login_name)
        set_answer_api.get({'question_id': quiz_questions_id, 'option': u'A'})
        self.assertEqual(set_answer_api.get_code(), 505210)
        self.assertEqual(set_answer_api.get_response_message(), u'请先停止竞猜再设置结果')

    def test_set_answer_option_again(self):
        """
        测试重复设置答案
        :return:
        """
        set_questions_api = SetQuestionsApi(self.game_anchor_login_name)
        set_questions_api.get({'room_id': self.game_room, 'question': self.questions, 'option_a': self.option_a,
                               'option_b': self.option_b})
        self.assertEqual(set_questions_api.get_code(), 0)

        db_questions = MysqlOperation(room_id=self.game_room).get_questions()
        self.assertEqual(len(db_questions), 1)
        question_ids = []
        for x in db_questions:
            question_ids.append(x['id'])
        question_ids_json = json.dumps(question_ids)

        start_quiz_api = StartQuizApi(self.game_anchor_login_name)
        start_quiz_api.get({'room_id': self.game_room, 'question_bank_ids': question_ids_json})
        self.assertEqual(start_quiz_api.get_code(), 0)

        quiz_questions_id = MysqlOperation(room_id=self.game_room).get_quiz_questions()[0]['id']

        stop_quiz_api = StopQuizApi(self.game_anchor_login_name)
        stop_quiz_api.get({'question_id': quiz_questions_id})
        self.assertEqual(stop_quiz_api.get_code(), 0)

        set_answer_api = SetAnswerApi(self.game_anchor_login_name)
        response = set_answer_api.get({'question_id': quiz_questions_id, 'option': 'A'})
        self.assertEqual(set_answer_api.get_code(), 0)
        question_obj = json.loads(response.content)['result']['question_obj']
        self.assertEqual(question_obj['status'], 3)
        self.assertEqual(question_obj['result'], u'A')

        set_answer_api = SetAnswerApi(self.game_anchor_login_name)
        set_answer_api.get({'question_id': quiz_questions_id, 'option': 'A'})
        self.assertEqual(set_answer_api.get_code(),505211)
        self.assertEqual(set_answer_api.get_response_message(),u'已经设置过竞猜结果了')

    def tearDown(self,*args):
        super(TestSetAnswerApi,self).tearDown()
        mysql_operation = MysqlOperation(room_id=self.game_room)
        quiz_question = mysql_operation.get_quiz_questions()
        quiz_question_ids = [x['id'] for x in quiz_question]
        mysql_operation.clean_questions()
        Redis().clean_quiz_questions(room_id=self.game_room,question_ids=quiz_question_ids)
        # time.sleep(0.5)