# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.user_noticelist_api import UserNoticeList
from utilities.mysql_helper import MysqlOperation
import json

class TestNoticeListApi(BaseCase):
    """
    公告
    """

    def test_notice_list_success(self):
        """
        测试获取公告列表成功
        :return:
        """
        notice_list_api = UserNoticeList()
        response = notice_list_api.get()
        self.assertEqual(notice_list_api.get_code(),0)
        self.assertEqual(notice_list_api.get_response_message(),u"操作成功")

        db_notice_details = MysqlOperation().get_notice_details()

        notice_list = json.loads(response.content)['result']['notice_list']
        self.assertEqual(notice_list[0]['title'], db_notice_details['title'])
        self.assertEqual(notice_list[0]['content'], db_notice_details['content'])
        self.assertEqual(notice_list[0]['url'], u'/api/notice/getnoticecontent/6.html')
        self.assertEqual(notice_list[0]['status'], 1)
        self.assertEqual(notice_list[0]['publish_type'], 0)
        self.assertEqual(notice_list[0]['publish_value'], u'')
