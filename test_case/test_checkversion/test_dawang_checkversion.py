# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.check_version_api import CheckVersionApi
from utilities.mysql_helper import MysqlOperation
import json,time


class TestDaWangCheckVersionApi(BaseCase):
    """
    检查大王娱乐版本
    """
    pname = 'com.dawang.live'
    android_channel_id = 10180001
    ios_channel_id = 90010001

    def test_android_force_update(self):
        """
        测试检查安卓强制升级
        :return:
        """
        sys_version_name,sys_version_code = MysqlOperation().fix_platform_upgrade( strategy=2,platform='android')
        time.sleep(1)
        check_version_api = CheckVersionApi()
        response = check_version_api.get({'platform': 'android', 'pname': self.pname, 'channel_id': self.android_channel_id})

        self.assertEqual(check_version_api.get_code(),0)
        self.assertEqual(json.loads(response.content)['result']['msg'],u'获取到版本信息')
        platform_info = json.loads(response.content)['result']['platform_info']
        db_info = MysqlOperation().get_platform_upgrade_details(channel_id=self.android_channel_id)
        self.assertEqual(platform_info['platform'],u'android')
        self.assertEqual(platform_info['product_id'],int(db_info['product_id']))
        self.assertEqual(platform_info['channel_id'],db_info['channel_id'])
        self.assertEqual(platform_info['channel_name'],db_info['channel_name'])
        self.assertEqual(platform_info['sys_version_name'],sys_version_name)
        self.assertEqual(platform_info['sys_version_code'],sys_version_code)
        self.assertEqual(platform_info['strategy'],2)
        self.assertEqual(platform_info['link_address'],db_info['link_address'])
        self.assertEqual(platform_info['tips'],db_info['tips'])
        self.assertEqual(platform_info['advert_tips'],db_info['advert_tips'])
        self.assertEqual(platform_info['status'],1)
        self.assertEqual(platform_info['update_time'],db_info['update_time'])
        self.assertEqual(platform_info['micro_link_address'],db_info['micro_link_address'])
        self.assertEqual(platform_info['channel_link_address'],db_info['channel_link_address'])
        self.assertEqual(platform_info['is_check_tip'],db_info['is_check_tip'])
        self.assertIsNone(json.loads(response.content)['extra'])

    def test_android_normal_update(self):
        """
        测试检测安卓普通升级
        :return:
        """
        sys_version_name, sys_version_code = MysqlOperation().fix_platform_upgrade(strategy=1,platform='android')
        time.sleep(1)
        check_version_api = CheckVersionApi()
        response = check_version_api.get({'platform': 'android', 'pname': self.pname, 'channel_id': self.android_channel_id})

        self.assertEqual(check_version_api.get_code(),0)
        self.assertEqual(json.loads(response.content)['result']['msg'],u'获取到版本信息')
        platform_info = json.loads(response.content)['result']['platform_info']
        db_info = MysqlOperation().get_platform_upgrade_details(channel_id=self.android_channel_id)
        self.assertEqual(platform_info['platform'],u'android')
        self.assertEqual(platform_info['product_id'],int(db_info['product_id']))
        self.assertEqual(platform_info['channel_id'],db_info['channel_id'])
        self.assertEqual(platform_info['channel_name'],db_info['channel_name'])
        self.assertEqual(platform_info['sys_version_name'],sys_version_name)
        self.assertEqual(platform_info['sys_version_code'],sys_version_code)
        self.assertEqual(platform_info['strategy'],1)
        self.assertEqual(platform_info['link_address'],db_info['link_address'])
        self.assertEqual(platform_info['tips'],db_info['tips'])
        self.assertEqual(platform_info['advert_tips'],db_info['advert_tips'])
        self.assertEqual(platform_info['status'],1)
        self.assertEqual(platform_info['update_time'],db_info['update_time'])
        self.assertEqual(platform_info['micro_link_address'],db_info['micro_link_address'])
        self.assertEqual(platform_info['channel_link_address'],db_info['channel_link_address'])
        self.assertEqual(platform_info['is_check_tip'],db_info['is_check_tip'])
        self.assertIsNone(json.loads(response.content)['extra'])

    def test_ios_force_update(self):
        """
        测试检测ios强制升级
        :return:
        """
        sys_version_name, sys_version_code = MysqlOperation().fix_platform_upgrade(strategy=2,platform='ios')
        time.sleep(1)
        check_version_api = CheckVersionApi()
        response = check_version_api.get({'platform': 'ios', 'pname': self.pname, 'channel_id': self.ios_channel_id})

        self.assertEqual(check_version_api.get_code(),0)
        self.assertEqual(json.loads(response.content)['result']['msg'],u'获取到版本信息')
        platform_info = json.loads(response.content)['result']['platform_info']
        db_info = MysqlOperation().get_platform_upgrade_details(channel_id=self.ios_channel_id)
        self.assertEqual(platform_info['platform'],u'ios')
        self.assertEqual(platform_info['product_id'],int(db_info['product_id']))
        self.assertEqual(platform_info['channel_id'],db_info['channel_id'])
        self.assertEqual(platform_info['channel_name'],db_info['channel_name'])
        self.assertEqual(platform_info['sys_version_name'],sys_version_name)
        self.assertEqual(platform_info['sys_version_code'],sys_version_code)
        self.assertEqual(platform_info['strategy'],2)
        self.assertEqual(platform_info['link_address'],db_info['link_address'])
        self.assertEqual(platform_info['tips'],db_info['tips'])
        self.assertEqual(platform_info['advert_tips'],db_info['advert_tips'])
        self.assertEqual(platform_info['status'],1)
        self.assertEqual(platform_info['update_time'],db_info['update_time'])
        self.assertEqual(platform_info['micro_link_address'],db_info['micro_link_address'])
        self.assertEqual(platform_info['channel_link_address'],u'')
        self.assertEqual(platform_info['is_check_tip'],db_info['is_check_tip'])
        self.assertIsNone(json.loads(response.content)['extra'])

    def test_ios_normal_update(self):
        """
        测试检测ios普通升级
        :return:
        """
        sys_version_name, sys_version_code = MysqlOperation().fix_platform_upgrade(strategy=1,platform='ios')
        time.sleep(1)
        check_version_api = CheckVersionApi()
        response = check_version_api.get({'platform': 'ios', 'pname': self.pname, 'channel_id': self.ios_channel_id})

        self.assertEqual(check_version_api.get_code(),0)
        self.assertEqual(json.loads(response.content)['result']['msg'],u'获取到版本信息')
        platform_info = json.loads(response.content)['result']['platform_info']
        db_info = MysqlOperation().get_platform_upgrade_details(channel_id=self.ios_channel_id)
        self.assertEqual(platform_info['platform'],u'ios')
        self.assertEqual(platform_info['product_id'],int(db_info['product_id']))
        self.assertEqual(platform_info['channel_id'],db_info['channel_id'])
        self.assertEqual(platform_info['channel_name'],db_info['channel_name'])
        self.assertEqual(platform_info['sys_version_name'],sys_version_name)
        self.assertEqual(platform_info['sys_version_code'],sys_version_code)
        self.assertEqual(platform_info['strategy'],1)
        self.assertEqual(platform_info['link_address'],db_info['link_address'])
        self.assertEqual(platform_info['tips'],db_info['tips'])
        self.assertEqual(platform_info['advert_tips'],db_info['advert_tips'])
        self.assertEqual(platform_info['status'],1)
        self.assertEqual(platform_info['update_time'],db_info['update_time'])
        self.assertEqual(platform_info['micro_link_address'],db_info['micro_link_address'])
        self.assertEqual(platform_info['channel_link_address'],'')
        self.assertEqual(platform_info['is_check_tip'],db_info['is_check_tip'])
        self.assertIsNone(json.loads(response.content)['extra'])

    def test_update_platform_null(self):
        """
        测试请求接口平台参数为空
        :return:
        """
        check_version_api = CheckVersionApi()
        check_version_api.get({'platform': None, 'pname': self.pname, 'channel_id': self.ios_channel_id})

        self.assertEqual(check_version_api.get_code(),401000)
        self.assertEqual(check_version_api.get_response_message(),u'缺少平台信息参数')

    def test_update_platform_error(self):
        """
        测试请求接口平台参数错误
        :return:
        """
        check_version_api = CheckVersionApi()
        check_version_api.get({'platform': '123', 'pname': self.pname, 'channel_id': self.ios_channel_id})

        self.assertEqual(check_version_api.get_code(),401000)
        self.assertEqual(check_version_api.get_response_message(),u'缺少平台信息参数')

    def test_update_pname_null(self):
        """
        测试请求接口包名为空
        :return:
        """
        check_version_api = CheckVersionApi()
        check_version_api.get({'platform': 'ios', 'pname': None, 'channel_id': self.ios_channel_id})

        self.assertEqual(check_version_api.get_code(),401001)
        self.assertEqual(check_version_api.get_response_message(),u'缺少应用包名参数')

    def test_update_pname_error(self):
        """
        测试无新版本调用接口
        :return:
        """
        check_version_api = CheckVersionApi()
        response = check_version_api.get({'platform': 'ios', 'pname': 'abc', 'channel_id': self.ios_channel_id})

        self.assertEqual(check_version_api.get_code(),0)
        self.assertEqual(json.loads(response.content)['result']['msg'],u'已经是最新版本了哦~')
        self.assertIsNone(json.loads(response.content)['result']['platform_info'])

    def test_update_channel_id_null(self):
        """
        测试请求接口渠道参数为空
        :return:
        """
        check_version_api = CheckVersionApi()
        check_version_api.get({'platform': 'ios', 'pname': self.pname, 'channel_id': None})

        self.assertEqual(check_version_api.get_code(), 401002)
        self.assertEqual(check_version_api.get_response_message(), u'缺少渠道参数')


    def tearDown(self,*args):
        super(TestDaWangCheckVersionApi,self).tearDown()
        MysqlOperation().fix_platform_upgrade(strategy=1,platform='android',up=False)
        MysqlOperation().fix_platform_upgrade(strategy=1,platform='ios',up=False)
        # time.sleep(1)