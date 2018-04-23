# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.quiz_api import SetQuestionsApi,StartQuizApi,GetQuestionsApi,QuizApi,StopQuizApi,SetAnswerApi
from utilities.mysql_helper import MysqlOperation
from utilities.redis_helper import Redis,RedisHold
from settings import YULE_TEST_GAME_ANCHOR_LOGIN_NAME,YULE_TEST_GAME_ANCHOR_ID,YULE_TEST_GAME_ROOM
from settings import YULE_TEST_USER_LOGIN_NAME,YULE_TEST_USER_ID
import json,time,datetime

class TestQuizApi(BaseCase):
    """
    竞猜-下注
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
    other_anchor_login_name = '15118174857'
    other_anchor_id = '20047778'


    def test_quiz_success(self):
        """
        测试下注成功
        :return:
        """
        set_questions_api = SetQuestionsApi(self.game_anchor_login_name)
        set_questions_api.get({'room_id': self.game_room, 'question': self.questions, 'option_a': self.option_a,
             'option_b': self.option_b})
        self.assertEqual(set_questions_api.get_code(), 0)

        question_ids = []
        for x in MysqlOperation(room_id=self.game_room).get_questions():
            question_ids.append(x['id'])
        question_ids_json = json.dumps(question_ids)

        start_quiz_api = StartQuizApi(self.game_anchor_login_name)
        start_quiz_api.get({'room_id':self.game_room,'question_bank_ids':question_ids_json})
        self.assertEqual(start_quiz_api.get_code(),0)

        quiz_questions_id = MysqlOperation(room_id=self.game_room).get_quiz_questions()[0]['id']

        mysql_operation = MysqlOperation(user_id=self.user_id)
        mysql_operation.fix_user_account(gold_num=50000)
        RedisHold().clean_redis_user_detail(self.user_id)
        time.sleep(self.time_sleep)

        quiz_api = QuizApi(self.user_login_name)
        response = quiz_api.get({'question_id': quiz_questions_id, 'gold': '20000','option':'A'})
        self.assertEqual(quiz_api.get_code(),0)

        question_obj = json.loads(response.content)['result']['question_obj']
        self.assertEqual(int(question_obj['id']),int(quiz_questions_id))
        self.assertEqual(question_obj['room_id'],self.game_room)
        self.assertEqual(question_obj['question'],self.questions)
        self.assertEqual(question_obj['total_pool'],20000)
        self.assertEqual(question_obj['init_pool'],u'0')
        self.assertEqual(question_obj['currency'],u'gold')
        self.assertEqual(question_obj['status'],u'1')
        self.assertEqual(question_obj['my_result'],0)
        self.assertIsNone(question_obj['result'])

        get_questions_api = GetQuestionsApi(self.user_login_name)
        response = get_questions_api.get({'room_id': self.game_room})
        self.assertEqual(get_questions_api.get_code(),0)
        question_list = json.loads(response.content)['result']['question_list']
        self.assertEqual(len(question_list),1)
        question_obj = json.loads(response.content)['result']['question_list'][0]
        self.assertEqual(int(question_obj['id']), int(quiz_questions_id))
        self.assertEqual(question_obj['room_id'], self.game_room)
        self.assertEqual(question_obj['question'], self.questions)
        self.assertEqual(question_obj['total_pool'], 20000)
        self.assertEqual(question_obj['init_pool'], u'0')
        self.assertEqual(question_obj['currency'], u'gold')
        self.assertEqual(question_obj['status'], u'1')
        self.assertEqual(question_obj['my_result'], 0)
        self.assertIsNone(question_obj['result'])

        options = question_obj['options']
        self.assertEqual(options['A']['odds'],u'1.0')
        self.assertEqual(options['A']['option_amount'],u'20000')
        self.assertEqual(options['A']['user_amount'],u'20000')
        self.assertEqual(options['A']['persent'],0.01)

        self.assertEqual(options['B']['odds'], u'1.0')
        self.assertEqual(options['B']['option_amount'], u'0')
        self.assertEqual(options['B']['user_amount'], u'0')
        self.assertEqual(options['B']['persent'], 0)

        quiz_api = QuizApi(self.user_login_name)
        response = quiz_api.get({'question_id': quiz_questions_id, 'gold': '30000', 'option': 'B'})
        self.assertEqual(quiz_api.get_code(), 0)

        question_obj = json.loads(response.content)['result']['question_obj']
        self.assertEqual(int(question_obj['id']), int(quiz_questions_id))
        self.assertEqual(question_obj['room_id'], self.game_room)
        self.assertEqual(question_obj['question'], self.questions)
        self.assertEqual(question_obj['total_pool'], 50000)
        self.assertEqual(question_obj['init_pool'], u'0')
        self.assertEqual(question_obj['currency'], u'gold')
        self.assertEqual(question_obj['status'], u'1')
        self.assertEqual(question_obj['my_result'], 0)
        self.assertIsNone(question_obj['result'])

        get_questions_api = GetQuestionsApi(self.user_login_name)
        response = get_questions_api.get({'room_id': self.game_room})
        self.assertEqual(get_questions_api.get_code(), 0)
        question_list = json.loads(response.content)['result']['question_list']
        self.assertEqual(len(question_list), 1)
        question_obj = json.loads(response.content)['result']['question_list'][0]
        self.assertEqual(int(question_obj['id']), int(quiz_questions_id))
        self.assertEqual(question_obj['room_id'], self.game_room)
        self.assertEqual(question_obj['question'], self.questions)
        self.assertEqual(question_obj['total_pool'], 50000)
        self.assertEqual(question_obj['init_pool'], u'0')
        self.assertEqual(question_obj['currency'], u'gold')
        self.assertEqual(question_obj['status'], u'1')
        self.assertEqual(question_obj['my_result'], 0)
        self.assertIsNone(question_obj['result'])

        options = question_obj['options']
        self.assertEqual(options['A']['odds'], u'2.5')
        self.assertEqual(options['A']['option_amount'], u'20000')
        self.assertEqual(options['A']['user_amount'], u'20000')
        self.assertEqual(options['A']['persent'], 0.01)

        self.assertEqual(options['B']['odds'], u'1.6')
        self.assertEqual(options['B']['option_amount'], u'30000')
        self.assertEqual(options['B']['user_amount'], u'30000')
        self.assertEqual(options['B']['persent'], 0.015)

    def test_quiz_failed(self):
        """
        测试单次下注超过9位数
        :return:
        """
        set_questions_api = SetQuestionsApi(self.game_anchor_login_name)
        set_questions_api.get({'room_id': self.game_room, 'question': self.questions, 'option_a': self.option_a,
             'option_b': self.option_b})
        self.assertEqual(set_questions_api.get_code(), 0)

        question_ids = []
        for x in MysqlOperation(room_id=self.game_room).get_questions():
            question_ids.append(x['id'])
        question_ids_json = json.dumps(question_ids)

        start_quiz_api = StartQuizApi(self.game_anchor_login_name)
        start_quiz_api.get({'room_id':self.game_room,'question_bank_ids':question_ids_json})
        self.assertEqual(start_quiz_api.get_code(),0)

        quiz_questions_id = MysqlOperation(room_id=self.game_room).get_quiz_questions()[0]['id']

        mysql_operation = MysqlOperation(user_id=self.user_id)
        mysql_operation.fix_user_account(gold_num=5000000000)
        RedisHold().clean_redis_user_detail(self.user_id)
        time.sleep(self.time_sleep)

        quiz_api = QuizApi(self.user_login_name)
        quiz_api.get({'question_id': quiz_questions_id, 'gold': '5000000000','option':'A'})
        self.assertEqual(quiz_api.get_code(),505227)
        self.assertEqual(quiz_api.get_response_message(),u'单笔投注超过限额')

    def test_quiz_success_9(self):
        """
        测试投注金额8位数成功
        :return:
        """
        set_questions_api = SetQuestionsApi(self.game_anchor_login_name)
        set_questions_api.get({'room_id': self.game_room, 'question': self.questions, 'option_a': self.option_a,
             'option_b': self.option_b})
        self.assertEqual(set_questions_api.get_code(), 0)

        question_ids = []
        for x in MysqlOperation(room_id=self.game_room).get_questions():
            question_ids.append(x['id'])
        question_ids_json = json.dumps(question_ids)

        start_quiz_api = StartQuizApi(self.game_anchor_login_name)
        start_quiz_api.get({'room_id':self.game_room,'question_bank_ids':question_ids_json})
        self.assertEqual(start_quiz_api.get_code(),0)

        quiz_questions_id = MysqlOperation(room_id=self.game_room).get_quiz_questions()[0]['id']

        mysql_operation = MysqlOperation(user_id=self.user_id)
        mysql_operation.fix_user_account(gold_num=99999999)
        RedisHold().clean_redis_user_detail(self.user_id)
        time.sleep(self.time_sleep)

        quiz_api = QuizApi(self.user_login_name)
        response = quiz_api.get({'question_id': quiz_questions_id, 'gold': '99999999','option':'A'})
        self.assertEqual(quiz_api.get_code(),0)

        question_obj = json.loads(response.content)['result']['question_obj']
        self.assertEqual(int(question_obj['id']),int(quiz_questions_id))
        self.assertEqual(question_obj['room_id'],self.game_room)
        self.assertEqual(question_obj['question'],self.questions)
        self.assertEqual(question_obj['total_pool'],99999999)
        self.assertEqual(question_obj['init_pool'],u'0')
        self.assertEqual(question_obj['currency'],u'gold')
        self.assertEqual(question_obj['status'],u'1')
        self.assertEqual(question_obj['my_result'],0)
        self.assertIsNone(question_obj['result'])

        get_questions_api = GetQuestionsApi(self.user_login_name)
        response = get_questions_api.get({'room_id': self.game_room})
        self.assertEqual(get_questions_api.get_code(),0)
        question_list = json.loads(response.content)['result']['question_list']
        self.assertEqual(len(question_list),1)
        question_obj = json.loads(response.content)['result']['question_list'][0]
        self.assertEqual(int(question_obj['id']), int(quiz_questions_id))
        self.assertEqual(question_obj['room_id'], self.game_room)
        self.assertEqual(question_obj['question'], self.questions)
        self.assertEqual(question_obj['total_pool'], 99999999)
        self.assertEqual(question_obj['init_pool'], u'0')
        self.assertEqual(question_obj['currency'], u'gold')
        self.assertEqual(question_obj['status'], u'1')
        self.assertEqual(question_obj['my_result'], 0)
        self.assertIsNone(question_obj['result'])

        options = question_obj['options']
        self.assertEqual(options['A']['odds'],u'1.0')
        self.assertEqual(options['A']['option_amount'],u'99999999')
        self.assertEqual(options['A']['user_amount'],u'99999999')
        self.assertEqual(options['A']['persent'],0.98)

        self.assertEqual(options['B']['odds'], u'1.0')
        self.assertEqual(options['B']['option_amount'], u'0')
        self.assertEqual(options['B']['user_amount'], u'0')
        self.assertEqual(options['B']['persent'], 0)


    def test_quiz_question_id_null(self):
        """
        测试请求下注接口问题ID为空
        :return:
        """
        quiz_api = QuizApi(self.user_login_name)
        quiz_api.get({'question_id': None, 'gold': 10000, 'option': 'A'})
        self.assertEqual(quiz_api.get_code(), 505202)
        self.assertEqual(quiz_api.get_response_message(),u'问题id不能为空')

    def test_quiz_question_id_error(self):
        """
        测试请求下注接口问题ID不存在
        :return:
        """
        mysql_operation = MysqlOperation(user_id=self.user_id)
        mysql_operation.fix_user_account(gold_num=10000)
        RedisHold().clean_redis_user_detail(self.user_id)
        time.sleep(self.time_sleep)

        quiz_api = QuizApi(self.user_login_name)
        quiz_api.get({'question_id': '999', 'gold': 10000, 'option': 'A'})
        self.assertEqual(quiz_api.get_code(), 505207)
        self.assertEqual(quiz_api.get_response_message(),u'竞猜题目不存在')

    def test_quiz_gold_null(self):
        """
        测试请求下注接口下注金额为空
        :return:
        """
        quiz_api = QuizApi(self.user_login_name)
        quiz_api.get({'question_id': '123', 'gold': None, 'option': 'A'})
        self.assertEqual(quiz_api.get_code(), 505204)
        self.assertEqual(quiz_api.get_response_message(),u'竞猜数额不能为空')

    def test_quiz_gold_error(self):
        """
        测试请求下注接口下注金额为字符串
        :return:
        """
        quiz_api = QuizApi(self.user_login_name)
        quiz_api.get({'question_id': '123', 'gold': 'abc', 'option': 'A'})
        self.assertEqual(quiz_api.get_code(), 100032)
        self.assertEqual(quiz_api.get_response_message(), u'账户金币不足')

    def test_quiz_gold_is_negative(self):
        """
        测试请求下注接口下注金额为负数
        :return:
        """
        quiz_api = QuizApi(self.user_login_name)
        quiz_api.get({'question_id': '123', 'gold': -100, 'option': 'A'})
        self.assertEqual(quiz_api.get_code(), 505205)
        self.assertEqual(quiz_api.get_response_message(), u'竞猜数额不正确')

    def test_quiz_gold_is_0(self):
        """
        测试请求下注接口下注金额为0
        :return:
        """
        quiz_api = QuizApi(self.user_login_name)
        quiz_api.get({'question_id': '123', 'gold': 0, 'option': 'A'})
        self.assertEqual(quiz_api.get_code(), 100032)
        self.assertEqual(quiz_api.get_response_message(), u'账户金币不足')

    def test_quiz_option_null(self):
        """
        测试请求下注接口竞猜选项为空
        :return:
        """
        quiz_api = QuizApi(self.user_login_name)
        quiz_api.get({'question_id': '123', 'gold': 10000, 'option': None})
        self.assertEqual(quiz_api.get_code(), 505206)
        self.assertEqual(quiz_api.get_response_message(),u'竞猜选项不能为空')

    def test_quiz_option_error(self):
        """
        测试请求下注接口竞猜选项错误
        :return:
        """
        set_questions_api = SetQuestionsApi(self.game_anchor_login_name)
        set_questions_api.get({'room_id': self.game_room, 'question': self.questions, 'option_a': self.option_a,
                               'option_b': self.option_b})
        self.assertEqual(set_questions_api.get_code(), 0)

        question_ids = []
        for x in MysqlOperation(room_id=self.game_room).get_questions():
            question_ids.append(x['id'])
        question_ids_json = json.dumps(question_ids)

        start_quiz_api = StartQuizApi(self.game_anchor_login_name)
        start_quiz_api.get({'room_id': self.game_room, 'question_bank_ids': question_ids_json})
        self.assertEqual(start_quiz_api.get_code(), 0)

        quiz_questions_id = MysqlOperation(room_id=self.game_room).get_quiz_questions()[0]['id']

        mysql_operation = MysqlOperation(user_id=self.user_id)
        mysql_operation.fix_user_account(gold_num=10000)
        RedisHold().clean_redis_user_detail(self.user_id)
        time.sleep(self.time_sleep)

        quiz_api = QuizApi(self.user_login_name)
        quiz_api.get({'question_id': quiz_questions_id, 'gold': 10000, 'option': 'C'})
        self.assertEqual(quiz_api.get_code(), 505208)
        self.assertEqual(quiz_api.get_response_message(), u'竞猜选项不存在')

    def test_quiz_gold_low(self):
        """
        测试请求下注接口金币不足
        :return:
        """
        set_questions_api = SetQuestionsApi(self.game_anchor_login_name)
        set_questions_api.get({'room_id': self.game_room, 'question': self.questions, 'option_a': self.option_a,
                               'option_b': self.option_b})
        self.assertEqual(set_questions_api.get_code(), 0)

        question_ids = []
        for x in MysqlOperation(room_id=self.game_room).get_questions():
            question_ids.append(x['id'])
        question_ids_json = json.dumps(question_ids)

        start_quiz_api = StartQuizApi(self.game_anchor_login_name)
        start_quiz_api.get({'room_id': self.game_room, 'question_bank_ids': question_ids_json})
        self.assertEqual(start_quiz_api.get_code(), 0)

        quiz_questions_id = MysqlOperation(room_id=self.game_room).get_quiz_questions()[0]['id']

        quiz_api = QuizApi(self.user_login_name)
        quiz_api.get({'question_id': quiz_questions_id, 'gold': 10000, 'option': 'A'})
        self.assertEqual(quiz_api.get_code(), 100032)
        self.assertEqual(quiz_api.get_response_message(), u'账户金币不足')

    def test_quiz_stop_last_not_set_answer(self):
        """
        测试停止竞猜未设置答案进行下注
        :return:
        """
        set_questions_api = SetQuestionsApi(self.game_anchor_login_name)
        set_questions_api.get({'room_id': self.game_room, 'question': self.questions, 'option_a': self.option_a,
                               'option_b': self.option_b})
        self.assertEqual(set_questions_api.get_code(), 0)

        question_ids = []
        for x in MysqlOperation(room_id=self.game_room).get_questions():
            question_ids.append(x['id'])
        question_ids_json = json.dumps(question_ids)

        start_quiz_api = StartQuizApi(self.game_anchor_login_name)
        start_quiz_api.get({'room_id': self.game_room, 'question_bank_ids': question_ids_json})
        self.assertEqual(start_quiz_api.get_code(), 0)

        quiz_questions_id = MysqlOperation(room_id=self.game_room).get_quiz_questions()[0]['id']

        mysql_operation = MysqlOperation(user_id=self.user_id)
        mysql_operation.fix_user_account(gold_num=50000)
        RedisHold().clean_redis_user_detail(self.user_id)
        time.sleep(self.time_sleep)

        stop_quiz_api = StopQuizApi(self.game_anchor_login_name)
        stop_quiz_api.get({'question_id': quiz_questions_id})
        self.assertEqual(stop_quiz_api.get_code(), 0)

        get_questions_api = GetQuestionsApi(self.game_anchor_login_name)
        response = get_questions_api.get({'room_id': self.game_room})
        self.assertEqual(get_questions_api.get_code(), 0)

        self.assertEqual(json.loads(response.content)['result']['question_list'][0]['status'], 2)
        now_time_format = datetime.datetime.now().strftime("%Y-%m-%d")
        self.assertIn(now_time_format, json.loads(response.content)['result']['question_list'][0]['end_time'])


        quiz_api = QuizApi(self.user_login_name)
        quiz_api.get({'question_id': quiz_questions_id, 'gold': '20000', 'option': 'A'})
        self.assertEqual(quiz_api.get_code(), 505209)
        self.assertEqual(quiz_api.get_response_message(),u'对不起，管理员已停止该竞猜，快去竞猜下一个题目吧')

    def test_quiz_stop_last_and_set_answer(self):
        """
        测试停止竞猜并且设置答案进行下注
        :return:
        """
        set_questions_api = SetQuestionsApi(self.game_anchor_login_name)
        set_questions_api.get({'room_id': self.game_room, 'question': self.questions, 'option_a': self.option_a,
                               'option_b': self.option_b})
        self.assertEqual(set_questions_api.get_code(), 0)

        question_ids = []
        for x in MysqlOperation(room_id=self.game_room).get_questions():
            question_ids.append(x['id'])
        question_ids_json = json.dumps(question_ids)

        start_quiz_api = StartQuizApi(self.game_anchor_login_name)
        start_quiz_api.get({'room_id': self.game_room, 'question_bank_ids': question_ids_json})
        self.assertEqual(start_quiz_api.get_code(), 0)

        quiz_questions_id = MysqlOperation(room_id=self.game_room).get_quiz_questions()[0]['id']

        mysql_operation = MysqlOperation(user_id=self.user_id)
        mysql_operation.fix_user_account(gold_num=50000)
        RedisHold().clean_redis_user_detail(self.user_id)
        time.sleep(self.time_sleep)

        stop_quiz_api = StopQuizApi(self.game_anchor_login_name)
        stop_quiz_api.get({'question_id': quiz_questions_id})
        self.assertEqual(stop_quiz_api.get_code(), 0)

        get_questions_api = GetQuestionsApi(self.game_anchor_login_name)
        response = get_questions_api.get({'room_id': self.game_room})
        self.assertEqual(get_questions_api.get_code(), 0)

        self.assertEqual(json.loads(response.content)['result']['question_list'][0]['status'], 2)
        now_time_format = datetime.datetime.now().strftime("%Y-%m-%d")
        self.assertIn(now_time_format, json.loads(response.content)['result']['question_list'][0]['end_time'])

        set_answer_api = SetAnswerApi(self.game_anchor_login_name)
        response = set_answer_api.get({'question_id': quiz_questions_id, 'option': u'A'})
        self.assertEqual(set_answer_api.get_code(), 0)
        question_obj = json.loads(response.content)['result']['question_obj']
        self.assertEqual(question_obj['status'], 3)
        self.assertEqual(question_obj['result'], u'A')


        quiz_api = QuizApi(self.user_login_name)
        quiz_api.get({'question_id': quiz_questions_id, 'gold': '20000', 'option': 'A'})
        self.assertEqual(quiz_api.get_code(), 505209)
        self.assertEqual(quiz_api.get_response_message(),u'对不起，管理员已停止该竞猜，快去竞猜下一个题目吧')

    def test_anchor_quiz_me(self):
        """
        测试主播无法投注自己房间得题目
        :return:
        """
        set_questions_api = SetQuestionsApi(self.game_anchor_login_name)
        set_questions_api.get({'room_id': self.game_room, 'question': self.questions, 'option_a': self.option_a,
                               'option_b': self.option_b})
        self.assertEqual(set_questions_api.get_code(), 0)

        question_ids = []
        for x in MysqlOperation(room_id=self.game_room).get_questions():
            question_ids.append(x['id'])
        question_ids_json = json.dumps(question_ids)

        start_quiz_api = StartQuizApi(self.game_anchor_login_name)
        start_quiz_api.get({'room_id': self.game_room, 'question_bank_ids': question_ids_json})
        self.assertEqual(start_quiz_api.get_code(), 0)

        quiz_questions_id = MysqlOperation(room_id=self.game_room).get_quiz_questions()[0]['id']

        mysql_operation = MysqlOperation(user_id=self.game_anchor_id)
        mysql_operation.fix_user_account(gold_num=20000)
        RedisHold().clean_redis_user_detail(self.game_anchor_id)
        time.sleep(self.time_sleep)

        quiz_api = QuizApi(self.game_anchor_login_name)
        quiz_api.get({'question_id': quiz_questions_id, 'gold': '20000', 'option': 'A'})
        self.assertEqual(quiz_api.get_code(), 505226)
        self.assertEqual(quiz_api.get_response_message(),u'主播不能对自己直播间的问题进行投注')

    def test_anchor_quiz_other_room(self):
        """
        测试主播投注其他房间得题目
        :return:
        """
        set_questions_api = SetQuestionsApi(self.game_anchor_login_name)
        set_questions_api.get({'room_id': self.game_room, 'question': self.questions, 'option_a': self.option_a,
                               'option_b': self.option_b})
        self.assertEqual(set_questions_api.get_code(), 0)

        question_ids = []
        for x in MysqlOperation(room_id=self.game_room).get_questions():
            question_ids.append(x['id'])
        question_ids_json = json.dumps(question_ids)

        start_quiz_api = StartQuizApi(self.game_anchor_login_name)
        start_quiz_api.get({'room_id': self.game_room, 'question_bank_ids': question_ids_json})
        self.assertEqual(start_quiz_api.get_code(), 0)

        quiz_questions_id = MysqlOperation(room_id=self.game_room).get_quiz_questions()[0]['id']

        mysql_operation = MysqlOperation(user_id=self.other_anchor_id)
        mysql_operation.fix_user_account(gold_num=20000)
        RedisHold().clean_redis_user_detail(self.other_anchor_id)
        time.sleep(self.time_sleep)

        quiz_api = QuizApi(self.other_anchor_login_name)
        quiz_api.get({'question_id': quiz_questions_id, 'gold': '20000', 'option': 'A'})
        self.assertEqual(quiz_api.get_code(), 0)

        get_questions_api = GetQuestionsApi(self.user_login_name)
        response = get_questions_api.get({'room_id': self.game_room})
        self.assertEqual(get_questions_api.get_code(), 0)
        question_list = json.loads(response.content)['result']['question_list']
        self.assertEqual(len(question_list), 1)
        question_obj = json.loads(response.content)['result']['question_list'][0]
        self.assertEqual(int(question_obj['id']), int(quiz_questions_id))
        self.assertEqual(question_obj['room_id'], self.game_room)
        self.assertEqual(question_obj['question'], self.questions)
        self.assertEqual(question_obj['total_pool'], 20000)
        self.assertEqual(question_obj['init_pool'], u'0')
        self.assertEqual(question_obj['currency'], u'gold')
        self.assertEqual(question_obj['status'], u'1')
        self.assertEqual(question_obj['my_result'], 0)
        self.assertIsNone(question_obj['result'])

        options = question_obj['options']
        self.assertEqual(options['A']['odds'], u'1.0')
        self.assertEqual(options['A']['option_amount'], u'20000')
        self.assertEqual(options['A']['user_amount'], 0)
        self.assertEqual(options['A']['persent'], 0.01)

        self.assertEqual(options['B']['odds'], u'1.0')
        self.assertEqual(options['B']['option_amount'], u'0')
        self.assertEqual(options['B']['user_amount'], 0)
        self.assertEqual(options['B']['persent'], 0)

    def tearDown(self,*args):
        super(TestQuizApi,self).tearDown(user_id=self.user_id)
        mysql_operation = MysqlOperation(room_id=self.game_room)
        quiz_question = mysql_operation.get_quiz_questions()
        quiz_question_ids = [x['id'] for x in quiz_question]
        mysql_operation.clean_questions()
        Redis().clean_quiz_questions(room_id=self.game_room,question_ids=quiz_question_ids)
        # MysqlOperation(user_id=self.user_id).fix_user_account().clean_user_account_log()
        # RedisHold().clean_redis_user_detail(self.user_id)
        # time.sleep(self.time_sleep)