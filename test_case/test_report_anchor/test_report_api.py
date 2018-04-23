# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.report_anchor_api import ReportUserApi
from utilities.mysql_helper import MysqlOperation
import settings,time
from utilities.teardown import TearDown

class TestReportUserApi(BaseCase):
    """
    举报主播
    """
    user_mobile = settings.YULE_TEST_USER_LOGIN_NAME
    user_id = settings.YULE_TEST_USER_ID
    anchor_id = settings.YULE_TEST_ANCHOR_ID
    reason = u'人身攻击'

    def test_report_user_success(self):
        """
        测试举报主播成功
        :return:
        """
        report_user_api = ReportUserApi(self.user_mobile)
        report_user_api.get({'to_user_id': self.anchor_id,'reason': self.reason})
        self.assertEqual(report_user_api.get_code(),0)
        count = 1
        max_count = 20
        while count < max_count:
            report = MysqlOperation(user_id=self.user_id,anchor_id=self.anchor_id).get_user_report_details()
            if report:
                self.assertEqual(report['reason'], self.reason)
                break
            else:
                time.sleep(0.5)
                count+=1
        self.assertLess(count,max_count)

    def test_report_user_to_user_id_is_null(self):
        """
        测试请求接口主播ID为空
        :return:
        """
        report_user_api = ReportUserApi(self.user_mobile)
        report_user_api.get({'to_user_id': None,'reason': self.reason})
        self.assertEqual(report_user_api.get_code(),402005)
        self.assertEqual(report_user_api.get_response_message(),u'主播ID不能为空')


    def test_report_user_reason_is_null(self):
        """
        测试去请求接口举报原因为空
        :return:
        """
        report_user_api = ReportUserApi(self.user_mobile)
        report_user_api.get({'to_user_id': self.anchor_id,'reason': None})

        self.assertEqual(report_user_api.get_code(),402022)
        self.assertEqual(report_user_api.get_response_message(),u'举报原因不能为空')

    def tearDown(self,*args):
        super(TestReportUserApi,self).tearDown()
        TearDown().report_anchor(self.user_id)