# -*- coding:utf-8 -*-
from api.publish_dynamic_api import PublishDynamicApi,GetHomePageDynamicApi,DynamicReportApi,RemoveDynamicApi
from base.base_case import BaseCase
from utilities.redis_helper import Redis
from utilities.mysql_helper import MysqlOperation
import json,settings,random,time

class TestDynamicReportApi(BaseCase):
    """
    举报动态
    """
    anchor_mobile = settings.YULE_TEST_ANCHOR_LOGIN_NAME
    anchor_id = settings.YULE_TEST_ANCHOR_ID
    user_mobile = settings.YULE_TEST_USER_LOGIN_NAME
    user_id = settings.YULE_TEST_USER_ID
    pic_url = ['pic/58/c2/58c2689b7c0730d7b605cb8beeb13702_0.png']
    video_url = ['video/e0/90/e09069c0b0792e362dd7cfbf0b0b8642.mp4']
    content = 'Auto Test!!'
    dynamic_ids = []
    reason = u'广告诈骗' + str(random.randint(10,99))

    def test_dynamic_report(self):
        """
        测试举报动态成功
        :return:
        """
        publish_dynamic_api = PublishDynamicApi(self.anchor_mobile)
        publish_dynamic_api.get({'type': 2, 'image_urls': None, 'video_url': self.video_url,
             'content': self.content, 'first_frame': self.pic_url})
        self.assertEqual(publish_dynamic_api.get_code(), 0)

        get_home_page_dynamic_list_api = GetHomePageDynamicApi(self.anchor_mobile)
        response = get_home_page_dynamic_list_api.get({'anchor_id': self.anchor_id})

        self.assertEqual(get_home_page_dynamic_list_api.get_code(), 0)
        anchor_dynamic_list = json.loads(response.content)['result']['dynamic_list']
        for x in anchor_dynamic_list:
            self.dynamic_ids.append(x['id'])
        self.assertEqual(len(anchor_dynamic_list), 1)
        dynamic_id = anchor_dynamic_list[0]['id']
        Redis().check_anchor_dynamic(dynamic_id)

        dynamic_report_api = DynamicReportApi(self.user_mobile)
        dynamic_report_api.get({'dynamic_id':dynamic_id,'reason':self.reason})

        self.assertEqual(dynamic_report_api.get_code(), 0)
        time.sleep(5)

        db_reason = MysqlOperation(user_id=self.user_id,anchor_id=self.anchor_id).get_user_dynamic_report_reason()
        self.assertEqual(db_reason,self.reason)


    def test_dynamic_report_dynamic_id_is_null(self):
        """
        测试请求接口动态ID为空
        :return:
        """
        dynamic_report_api = DynamicReportApi(self.user_mobile)
        dynamic_report_api.get({'dynamic_id': None, 'reason': self.reason})

        self.assertEqual(dynamic_report_api.get_code(), 450007)
        self.assertEqual(dynamic_report_api.get_response_message(),u'动态id不能为空')


    def test_dynamic_report_reason_is_null(self):
        """
        测试请求接口举报原因为空
        :return:
        """
        publish_dynamic_api = PublishDynamicApi(self.anchor_mobile)
        publish_dynamic_api.get(
            {'type': 2, 'image_urls': None, 'video_url': self.video_url,
             'content': self.content, 'first_frame': self.pic_url})

        self.assertEqual(publish_dynamic_api.get_code(), 0)

        get_home_page_dynamic_list_api = GetHomePageDynamicApi(self.anchor_mobile)
        response = get_home_page_dynamic_list_api.get({'anchor_id': self.anchor_id})
        self.assertEqual(get_home_page_dynamic_list_api.get_code(), 0)
        anchor_dynamic_list = json.loads(response.content)['result']['dynamic_list']
        for x in anchor_dynamic_list:
            self.dynamic_ids.append(x['id'])
        self.assertEqual(len(anchor_dynamic_list), 1)
        dynamic_id = anchor_dynamic_list[0]['id']
        Redis().check_anchor_dynamic(dynamic_id)

        dynamic_report_api = DynamicReportApi(self.user_mobile)
        dynamic_report_api.get({'dynamic_id':dynamic_id,'reason':None})
        self.assertEqual(dynamic_report_api.get_code(), 450008)
        self.assertEqual(dynamic_report_api.get_response_message(),u'举报原因不能为空')

    def tearDown(self,*args):
        super(TestDynamicReportApi,self).tearDown()
        for i in self.dynamic_ids:
            RemoveDynamicApi(self.anchor_mobile).get({'dynamic_id': i})
