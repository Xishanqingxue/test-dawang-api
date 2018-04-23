# -*- coding:utf-8 -*-
from base.base_log import BaseLogger
import json
import requests
import settings


logger = BaseLogger(__name__).get_logger()

class BaseApi(object):
    url = ''
    base_url = settings.API_TEST_BASE_URL
    ajax = False

    def __init__(self):
        self.response = None
        self.headers = settings.API_HEADERS
        if self.ajax:
            # AJAX类型开关，True打开，False关闭
            self.headers = settings.AJAX_HEADERS

    def api_url(self):
        """
        拼接url
        :return:
        """
        url = "{0}{1}".format(self.base_url,self.url)
        logger.info('Test Url:{0}'.format(url))
        return url

    def build_base_param(self):
        """
        构建共有入参
        :return:
        """
        return {
            "identity": "",
            "is_debug": "1",
            "client_version": settings.APP_VERSION,
            'device_id':settings.DEVICE_ID,
            'platform':'android'
        }

    def build_custom_param(self, data):
        """
        构建除共有参数外其余参数，接口封装时将该方法重写
        :param data:
        :return:
        """
        return {}

    def format_param(self,data):
        """
        合并共有参数和其他所需参数
        :param data:
        :return:
        """
        if not data:
            data = {}
        base_param = self.build_base_param()
        custom_param = self.build_custom_param(data)
        data.update(base_param)
        data.update(custom_param)
        logger.info('Param:{0}'.format(data))
        return data

    def get(self, data=None):
        """
        请求方式：GET
        :param data:
        :return:
        """
        request_data = self.format_param(data)
        s = requests.session()
        if request_data['identity']:
            s.cookies.set('identity',request_data['identity'])
        self.response = s.get(url=self.api_url(), params=request_data, headers=self.headers)
        logger.info('Headers:{0}'.format(self.response.request.headers))
        logger.info('Response:{0}'.format(self.response.text))
        return self.response

    def post(self, data=None):
        """
        请求方式：POST
        :param data:
        :return:
        """
        request_data = self.format_param(data)
        s = requests.session()
        s.cookies.set('identity',request_data['identity'])
        self.response = s.post(url=self.api_url(), params=request_data, headers=self.headers)
        logger.info('Headers:{0}'.format(self.response.request.headers))
        logger.info('Response:{0}'.format(self.response.text))
        return self.response

    def assert_status_code(self):
        """
        返回请求状态码
        :return:
        """
        if self.response:
            return self.response.status_code

    def get_code(self):
        """
        获取回参中状态码
        :return:
        """
        if self.response:
            return json.loads(self.response.text)['code']

    def get_response_message(self):
        """
        获取回参中消息
        :return:
        """
        if self.response:
            return json.loads(self.response.text)['msg']

    def get_resp_identity_obj(self):
        """
        获取回参中用户信息模块
        :return:
        """
        if self.response:
            return json.load(self.response.text)['result']['identity']
