# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.quiz_api import SetQuestionsApi,StartQuizApi,GetQuestionsApi,StopQuizApi,SetAnswerApi,QuizApi
from api.consumption_api import ConsumptionApi,GoldAccountApi
from utilities.mysql_helper import MysqlOperation
from utilities.redis_helper import Redis,RedisHold
from settings import YULE_TEST_GAME_ANCHOR_LOGIN_NAME,YULE_TEST_GAME_ANCHOR_ID,YULE_TEST_GAME_ROOM
from settings import YULE_TEST_USER_LOGIN_NAME,YULE_TEST_USER_ID
import json,time,datetime

class TestQuizConsumptionApi(BaseCase):
    """
    竞猜-消费记录/获取记录
    """
    game_anchor_login_name = YULE_TEST_GAME_ANCHOR_LOGIN_NAME
    game_anchor_id = YULE_TEST_GAME_ANCHOR_ID
    game_room = YULE_TEST_GAME_ROOM
    questions = u'自动化测试添加题目。'
    option_a = u'选项A'
    option_b = u'选项B'
    user_login_name = YULE_TEST_USER_LOGIN_NAME
    user_id = YULE_TEST_USER_ID
    user_login_name_two = '13381078888'
    user_id_two = '22017151'
    time_sleep = 0.3

    def test_quiz_win(self):
        """
        测试竞猜消费记录和金币获取记录
        :return:
        """
        set_questions_api = SetQuestionsApi(self.game_anchor_login_name)
        set_questions_api.get({'room_id': self.game_room, 'question': self.questions, 'option_a': self.option_a,
             'option_b': self.option_b})
        self.assertEqual(set_questions_api.get_code(), 0)

        db_questions = MysqlOperation(room_id=self.game_room).get_questions()
        self.assertEqual(len(db_questions),1)
        question_ids = []
        for x in db_questions:
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
        quiz_api.get({'question_id': quiz_questions_id, 'gold': '50000', 'option': 'A'})
        self.assertEqual(quiz_api.get_code(), 0)

        mysql_operation = MysqlOperation(user_id=self.user_id_two)
        mysql_operation.fix_user_account(gold_num=20000)
        RedisHold().clean_redis_user_detail(self.user_id_two)
        time.sleep(self.time_sleep)

        quiz_api = QuizApi(self.user_login_name_two)
        quiz_api.get({'question_id': quiz_questions_id, 'gold': '20000', 'option': 'B'})
        self.assertEqual(quiz_api.get_code(), 0)

        get_questions_api = GetQuestionsApi(self.game_anchor_login_name)
        response = get_questions_api.get({'room_id': self.game_room})
        self.assertEqual(get_questions_api.get_code(), 0)

        question_list = json.loads(response.content)['result']['question_list']
        self.assertEqual(len(question_list), 1)
        question_obj = json.loads(response.content)['result']['question_list'][0]
        self.assertEqual(int(question_obj['id']), int(quiz_questions_id))
        self.assertEqual(question_obj['room_id'], self.game_room)
        self.assertEqual(question_obj['question'], self.questions)
        self.assertEqual(question_obj['total_pool'], 70000)
        self.assertEqual(question_obj['init_pool'], u'0')
        self.assertEqual(question_obj['currency'], u'gold')
        self.assertEqual(question_obj['status'], u'1')
        self.assertEqual(question_obj['my_result'], 0)
        self.assertIsNone(question_obj['result'])

        options = question_obj['options']
        self.assertEqual(options['A']['odds'], u'1.4')
        self.assertEqual(options['A']['option_amount'], u'50000')
        self.assertEqual(options['A']['user_amount'], 0)
        self.assertEqual(options['A']['persent'], 0.025)

        self.assertEqual(options['B']['odds'], u'3.5')
        self.assertEqual(options['B']['option_amount'], u'20000')
        self.assertEqual(options['B']['user_amount'], 0)
        self.assertEqual(options['B']['persent'], 0.01)

        stop_quiz_api = StopQuizApi(self.game_anchor_login_name)
        stop_quiz_api.get({'question_id':quiz_questions_id})
        self.assertEqual(stop_quiz_api.get_code(),0)

        get_questions_api = GetQuestionsApi(self.game_anchor_login_name)
        response = get_questions_api.get({'room_id': self.game_room})
        self.assertEqual(get_questions_api.get_code(), 0)

        self.assertEqual(json.loads(response.content)['result']['question_list'][0]['status'],2)
        now_time_format = datetime.datetime.now().strftime("%Y-%m-%d")
        self.assertIn(now_time_format, json.loads(response.content)['result']['question_list'][0]['end_time'])

        set_answer_api = SetAnswerApi(self.game_anchor_login_name)
        response = set_answer_api.get({'question_id': quiz_questions_id,'option':'A'})
        self.assertEqual(set_answer_api.get_code(),0)
        question_obj = json.loads(response.content)['result']['question_obj']
        self.assertEqual(question_obj['status'],3)
        self.assertEqual(question_obj['result'],u'A')
        time.sleep(2)
        consum_api = ConsumptionApi(self.user_login_name)
        response = consum_api.get()
        self.assertEqual(consum_api.get_code(),0)
        consume_list = json.loads(response.content)['result']['consume_list']
        self.assertEqual(len(consume_list),1)

        self.assertEqual(consume_list[0]['user_id'],self.user_id)
        self.assertIn(now_time_format,consume_list[0]['create_time'])
        self.assertEqual(consume_list[0]['type'],u'101')
        self.assertEqual(consume_list[0]['gold'],50000)
        self.assertEqual(consume_list[0]['corresponding_id'],quiz_questions_id)
        self.assertEqual(consume_list[0]['corresponding_name'],u'A')
        self.assertEqual(consume_list[0]['corresponding_num'],0)
        self.assertEqual(consume_list[0]['room_id'],self.game_room)
        self.assertEqual(consume_list[0]['status'],1)
        self.assertEqual(consume_list[0]['behavior_desc'],u'竞猜下注')
        self.assertEqual(consume_list[0]['consumption_type'],u'50000金币')

        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity_obj['gold'],70000)
        self.assertEqual(identity_obj['diamond'],u'0')

        consum_api = ConsumptionApi(self.user_login_name_two)
        response = consum_api.get()
        self.assertEqual(consum_api.get_code(),0)
        consume_list = json.loads(response.content)['result']['consume_list']
        self.assertEqual(len(consume_list),1)

        self.assertEqual(consume_list[0]['user_id'],self.user_id_two)
        self.assertIn(now_time_format,consume_list[0]['create_time'])
        self.assertEqual(consume_list[0]['type'],u'101')
        self.assertEqual(consume_list[0]['gold'],20000)
        self.assertEqual(consume_list[0]['corresponding_id'],quiz_questions_id)
        self.assertEqual(consume_list[0]['corresponding_name'],u'B')
        self.assertEqual(consume_list[0]['corresponding_num'],0)
        self.assertEqual(consume_list[0]['room_id'],self.game_room)
        self.assertEqual(consume_list[0]['status'],1)
        self.assertEqual(consume_list[0]['behavior_desc'],u'竞猜下注')
        self.assertEqual(consume_list[0]['consumption_type'],u'20000金币')

        identity_obj = json.loads(response.content)['result']['identity_obj']
        self.assertEqual(identity_obj['gold'],0)
        self.assertEqual(identity_obj['diamond'],u'0')

        gold_account_api = GoldAccountApi(self.user_login_name)
        response = gold_account_api.get()
        self.assertEqual(gold_account_api.get_code(),0)
        account_list = json.loads(response.content)['result']['account_list']
        self.assertEqual(len(account_list),1)
        self.assertEqual(account_list[0]['user_id'],self.user_id)
        self.assertEqual(account_list[0]['type'],u'102')
        self.assertEqual(account_list[0]['gold'],70000)

        self.assertEqual(account_list[0]['corresponding_id'],quiz_questions_id)
        self.assertEqual(account_list[0]['corresponding_name'],u'A')
        self.assertEqual(account_list[0]['corresponding_num'],0)
        self.assertEqual(account_list[0]['status'],1)
        self.assertEqual(account_list[0]['money'],0)
        self.assertEqual(account_list[0]['behavior_desc'],u'竞猜奖励')
        self.assertEqual(account_list[0]['consumption_type'],u'70000金币')
        self.assertEqual(account_list[0]['room_id'],self.game_room)


        gold_account_api = GoldAccountApi(self.user_login_name_two)
        response = gold_account_api.get()
        self.assertEqual(gold_account_api.get_code(),0)
        account_list = json.loads(response.content)['result']['account_list']
        self.assertEqual(len(account_list),0)

    def tearDown(self,*args):
        super(TestQuizConsumptionApi,self).tearDown(user_id=[self.user_id,self.user_id_two])
        mysql_operation = MysqlOperation(room_id=self.game_room)
        quiz_question = mysql_operation.get_quiz_questions()
        quiz_question_ids = [x['id'] for x in quiz_question]
        mysql_operation.clean_questions()
        Redis().clean_quiz_questions(room_id=self.game_room,question_ids=quiz_question_ids)
        # for x in [self.user_id,self.user_id_two]:
        #     MysqlOperation(user_id=x).fix_user_account().clean_user_account_log()
        #     RedisHold().clean_redis_user_detail(x)
        # time.sleep(0.5)