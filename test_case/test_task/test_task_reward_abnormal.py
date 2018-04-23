# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.task_api import GetTaskRewardApi

class TestTaskApi(BaseCase):
    """
    领取任务奖励
    """
    user_name = '13877776666'

    def test_get_task_reward_behavior_error(self):
        """
        测试请求领取任务奖励接口任务类型错误
        :return:
        """
        get_task_reward_api = GetTaskRewardApi(self.user_name)
        get_task_reward_api.get({'behavior':'abcd'})

        self.assertEqual(get_task_reward_api.get_code(),430001)
        self.assertEqual(get_task_reward_api.get_response_message(),u'任务不存在')

    def test_get_task_reward_behavior_null(self):
        """
        测试请求领取任务奖励接口任务类型为空
        :return:
        """
        get_task_reward_api = GetTaskRewardApi(self.user_name)
        get_task_reward_api.get({'behavior': None})

        self.assertEqual(get_task_reward_api.get_code(), 430004)
        self.assertEqual(get_task_reward_api.get_response_message(), u'任务类型不能为空')