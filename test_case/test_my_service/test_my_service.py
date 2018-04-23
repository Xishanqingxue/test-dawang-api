# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.my_service_api import MyServiceApi
import json,settings

class TestMyService(BaseCase):
    """
    客服帮助
    """
    login_name = settings.YULE_TEST_USER_LOGIN_NAME

    def test_my_service_success(self):
        """
        测试接口返回H5页面地址正常
        :return:
        """
        my_service_api = MyServiceApi(login_name = self.login_name)
        response = my_service_api.get()
        self.assertEqual(my_service_api.get_code(),0)
        self.assertEqual(my_service_api.get_response_message(),u"操作成功")

        result = json.loads(response.content)['result']
        self.assertEqual(result['app_service_url'],u'/h5/service')

