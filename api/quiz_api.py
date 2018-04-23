# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi


class GetQuestionsApi(LoginBaseApi):
    """
    获取问题列表
    """
    url = '/quiz/getquestion'

    def build_custom_param(self, data):
        return {'room_id': data['room_id']}


class QuizApi(LoginBaseApi):
    """
    竞猜
    """
    url = '/quiz/quiz'

    def build_custom_param(self, data):
        return {'question_id': data['question_id'], 'gold': data['gold'],'option':data['option']}


class SetAnswerApi(LoginBaseApi):
    """
    设置答案
    """
    url = '/quiz/setAnswer'

    def build_custom_param(self, data):
        return {'question_id': data['question_id'],'option':data['option']}


class SetQuestionsApi(LoginBaseApi):
    """
    添加题目到题库
    """
    url = '/quiz/setQuestions'

    def build_custom_param(self, data):
        return {'room_id': data['room_id'], 'question': data['question'],'option_a':data['option_a'],'option_b':data['option_b']}


class StartQuizApi(LoginBaseApi):
    """
    开始竞猜
    """
    url = '/quiz/startQuiz'


    def build_custom_param(self, data):
        return {'room_id':data['room_id'],'question_bank_ids':data['question_bank_ids']}


class StopQuizApi(LoginBaseApi):
    """
    停止竞猜
    """
    url = '/quiz/stopQuiz'

    def build_custom_param(self, data):
        return {'question_id':data['question_id']}