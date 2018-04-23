# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.task_api import TaskListApi
import settings,json

class TestGetTaskListApi(BaseCase):
    """
    我的任务
    """
    login_name = settings.YULE_TEST_USER_LOGIN_NAME



    def test_get_task_list_success(self):
        """
        测试我的任务列表
        :return:
        """
        task_list_api = TaskListApi(self.login_name)
        response = task_list_api.get()
        self.assertEqual(task_list_api.get_code(),0)
        task_list = json.loads(response.content)['result']['task_list']
        self.assertEqual(len(task_list),4)
        task_name = []
        for x in task_list:
            task_name.append(x['task_name'])
        self.assertEqual(task_name,[u'绑定手机',u'充值',u'分享',u'送礼'])

        task_type = []
        for x in task_list:
            task_type.append(x['task_type'])
        self.assertEqual(task_type, [u'once', u'daily', u'daily', u'daily'])

        task_behavior = []
        for x in task_list:
            task_behavior.append(x['task_behavior'])
        self.assertEqual(task_behavior, [u'bind_mobile', u'recharging', u'share_to_sns', u'send_gift'])

        task_desc = []
        for x in task_list:
            task_desc.append(x['task_desc'])
        self.assertEqual(task_desc, [u'绑定手机号送5000大王豆', u'充值送288大王豆', u'分享三次送88大王豆', u'送任意金额的礼物送500经验'])

        task_num = []
        for x in task_list:
            task_num.append(x['task_num'])
        self.assertEqual(task_num, [1, 1, 3, 1])

        unit = []
        for x in task_list:
            unit.append(x['unit'])
        self.assertEqual(unit, [u'大王豆', u'大王豆', u'大王豆', u'经验'])

        for x in task_list:
            if x['task_name'] == u'绑定手机':
                self.assertEqual(x['task_award_config'][0]['type'],u'diamond')
                self.assertEqual(x['task_award_config'][0]['id'],0)
                self.assertEqual(x['task_award_config'][0]['num'],5000)
            elif x['task_name'] == u'充值':
                self.assertEqual(x['task_award_config'][0]['type'], u'diamond')
                self.assertEqual(x['task_award_config'][0]['id'], 0)
                self.assertEqual(x['task_award_config'][0]['num'], 288)
            elif x['task_name'] == u'分享':
                self.assertEqual(x['task_award_config'][0]['type'], u'diamond')
                self.assertEqual(x['task_award_config'][0]['id'], 0)
                self.assertEqual(x['task_award_config'][0]['num'], 88)
            elif x['task_name'] == u'送礼':
                self.assertEqual(x['task_award_config'][0]['type'], u'exp')
                self.assertEqual(x['task_award_config'][0]['id'], 0)
                self.assertEqual(x['task_award_config'][0]['num'], 500)