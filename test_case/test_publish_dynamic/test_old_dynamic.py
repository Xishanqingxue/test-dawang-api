# -*- coding:utf-8 -*-
from api.publish_dynamic_api import RemoveDynamicApi,PublishDynamicApi,GetHomePageDynamicApi,GetDynamicDetailApi,GetSquareDynamicApi
from base.base_case import BaseCase
from utilities.redis_helper import Redis
from utilities.mysql_helper import MysqlOperation
import json,time,settings



class TestOldDynamicApi(BaseCase):
    """
    动态时间显示文案
    """
    anchor_mobile = settings.YULE_TEST_ANCHOR_LOGIN_NAME
    anchor_id = settings.YULE_TEST_ANCHOR_ID
    user_mobile = settings.YULE_TEST_ANCHOR_LOGIN_NAME
    user_id = MysqlOperation(mobile=user_mobile).get_user_id()
    pic_url = ['pic/58/c2/58c2689b7c0730d7b605cb8beeb13702_0.png']
    video_url = ['video/e0/90/e09069c0b0792e362dd7cfbf0b0b8642.mp4']
    content = 'Auto Test!!'
    dynamic_ids = []

    def flow_path(self,**kwargs):
        over_due_time = kwargs['over_due_time']
        hint = kwargs['hint']
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
        self.assertEqual(len(anchor_dynamic_list),1)
        dynamic_id = anchor_dynamic_list[0]['id']
        Redis().check_anchor_dynamic(dynamic_id)
        created_time = int(time.time()) - over_due_time
        Redis().fix_dynamic_created_time(dynamic_id=dynamic_id,created_time=created_time)
        time.sleep(1)

        get_square_dynamic_api = GetSquareDynamicApi(self.user_mobile)
        response = get_square_dynamic_api.get()

        self.assertEqual(get_square_dynamic_api.get_code(), 0)
        dynamic_list = json.loads(response.content)['result']['dynamic_list']
        self.assertEqual(dynamic_list[0]['create_time_str'],hint)

        get_home_page_dynamic_list_api = GetHomePageDynamicApi(self.anchor_mobile)
        response = get_home_page_dynamic_list_api.get({'anchor_id': self.anchor_id})
        self.assertEqual(get_home_page_dynamic_list_api.get_code(), 0)
        anchor_dynamic = json.loads(response.content)['result']['dynamic_list'][0]
        self.assertEqual(anchor_dynamic['create_time_str'],hint)

        get_dynamic_detail_api = GetDynamicDetailApi(self.user_mobile)
        response = get_dynamic_detail_api.get({'dynamic_id': dynamic_id})

        self.assertEqual(get_dynamic_detail_api.get_code(), 0)
        self.assertEqual(json.loads(response.content)['result']['dynamic_obj']['create_time_str'],hint)

    def test_get_square_dynamic_just_now(self):
        """
        测试发布动态时间为刚刚
        :return:
        """
        test_data = {'over_due_time':0,'hint':u'刚刚'}
        self.flow_path(**test_data)

    def test_get_square_dynamic_five_minutes_low(self):
        """
        测试发布动态时间为4分55秒前
        :return:
        """
        test_data = {'over_due_time':295,'hint':u'刚刚'}
        self.flow_path(**test_data)

    def test_get_square_dynamic_five_minutes(self):
        """
        测试发布动态时间为5分钟前
        :return:
        """
        test_data = {'over_due_time':305,'hint':u'5分钟前'}
        self.flow_path(**test_data)

    def test_get_square_dynamic_one_hour_low(self):
        """
        测试发布动态时间为59分钟前
        :return:
        """
        test_data = {'over_due_time':3585,'hint':u'59分钟前'}
        self.flow_path(**test_data)

    def test_get_square_dynamic_one_hour(self):
        """
        测试发布动态时间为1小时前
        :return:
        """
        test_data = {'over_due_time':3605,'hint':u'1小时前'}
        self.flow_path(**test_data)

    def test_get_square_dynamic_one_day_low(self):
        """
        测试发布动态时间为23小时前
        :return:
        """
        test_data = {'over_due_time':86385,'hint':u'23小时前'}
        self.flow_path(**test_data)

    def test_get_square_dynamic_one_day(self):
        """
        测试发布动态时间为1天前
        :return:
        """
        test_data = {'over_due_time':86405,'hint':u'1天前'}
        self.flow_path(**test_data)

    def test_get_square_dynamic_one_month_low(self):
        """
        测试发布动态时间为29天前
        :return:
        """
        test_data = {'over_due_time':2591985,'hint':u'29天前'}
        self.flow_path(**test_data)

    def test_get_square_dynamic_one_month(self):
        """
        测试发布动态时间为1个月前
        :return:
        """
        test_data = {'over_due_time':2592005,'hint':u'1个月前'}
        self.flow_path(**test_data)

    def test_get_square_dynamic_one_year_low(self):
        """
        测试发布动态时间为11个月前e
        :return:
        """
        test_data = {'over_due_time':31103995,'hint':u'11个月前'}
        self.flow_path(**test_data)

    def test_get_square_dynamic_one_year(self):
        """
        测试发布动态时间为12个月前
        :return:
        """
        test_data = {'over_due_time':31104005,'hint':u'12个月前'}
        self.flow_path(**test_data)

    def tearDown(self,*args):
        super(TestOldDynamicApi,self).tearDown()
        for i in self.dynamic_ids:
            RemoveDynamicApi(self.anchor_mobile).get({'dynamic_id': i})
