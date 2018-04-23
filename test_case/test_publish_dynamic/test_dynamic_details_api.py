# -*- coding:utf-8 -*-
from api.publish_dynamic_api import RemoveDynamicApi,PublishDynamicApi,GetHomePageDynamicApi,GetDynamicDetailApi
from base.base_case import BaseCase
from utilities.redis_helper import Redis
import json,settings

class TestDynamicDetailsApi(BaseCase):
    """
    动态详情
    """
    anchor_mobile = settings.YULE_TEST_ANCHOR_LOGIN_NAME
    anchor_id = settings.YULE_TEST_ANCHOR_ID
    user_mobile = settings.YULE_TEST_ANCHOR_LOGIN_NAME
    room_id = settings.YULE_TEST_ROOM
    user_id = settings.YULE_TEST_USER_ID
    pic_url = ['pic/58/c2/58c2689b7c0730d7b605cb8beeb13702_0.png']
    video_url = ['video/e0/90/e09069c0b0792e362dd7cfbf0b0b8642.mp4']
    content = 'Auto Test!!'
    dynamic_ids = []

    def test_get_dynamic_details(self):
        """
        测试动态详情接口
        :return:
        """
        # 发动态
        publish_dynamic_api = PublishDynamicApi(self.anchor_mobile)
        publish_dynamic_api.get({'type': 2, 'image_urls': None, 'video_url': self.video_url,
             'content': self.content, 'first_frame': self.pic_url})

        self.assertEqual(publish_dynamic_api.get_code(), 0)
        # 校验主播自己的个人主页里面是否显示该动态
        get_home_page_dynamic_list_api = GetHomePageDynamicApi(self.anchor_mobile)
        response = get_home_page_dynamic_list_api.get({'anchor_id': self.anchor_id})
        self.assertEqual(get_home_page_dynamic_list_api.get_code(), 0)
        anchor_dynamic_list = json.loads(response.content)['result']['dynamic_list']
        for x in anchor_dynamic_list:
            self.dynamic_ids.append(x['id'])
        self.assertEqual(len(anchor_dynamic_list), 1)
        dynamic_id = anchor_dynamic_list[0]['id']
        # 审核动态
        Redis().check_anchor_dynamic(dynamic_id)
        # 动态详细
        get_dynamic_detail_api = GetDynamicDetailApi(self.user_mobile)
        response = get_dynamic_detail_api.get({'dynamic_id':dynamic_id})

        self.assertEqual(get_dynamic_detail_api.get_code(), 0)
        self.assertEqual(json.loads(response.content)['result']['has_upvoted'],0)

        anchor_dynamic = json.loads(response.content)['result']['dynamic_obj']
        self.assertEqual(anchor_dynamic['user_id'], self.anchor_id)
        self.assertEqual(anchor_dynamic['image_urls'], u'')
        self.assertIn((self.video_url[0]), anchor_dynamic['video_url'])
        self.assertEqual(anchor_dynamic['upvote_num'], 0)

        self.assertEqual(anchor_dynamic['content'], self.content)
        self.assertEqual(anchor_dynamic['status'], 1)
        self.assertEqual(anchor_dynamic['has_followed'], 0)
        self.assertEqual(anchor_dynamic['show_red_point'], 0)
        self.assertEqual(anchor_dynamic['reason'], u'')
        self.assertIsNotNone(anchor_dynamic['first_frame'])
        self.assertEqual(anchor_dynamic['is_upvote_by_me'], 0)
        self.assertEqual(anchor_dynamic['create_time_str'], u'刚刚')
        self.assertEqual(anchor_dynamic['type'], 2)
        self.assertIsNotNone(anchor_dynamic['small_head_url'])
        self.assertEqual(anchor_dynamic['room_id'], int(self.room_id))
        self.assertIsNotNone(anchor_dynamic['first_frame'])

        share_list = anchor_dynamic['share_list']
        self.assertIsNotNone(share_list['share_title'])
        self.assertIsNotNone(share_list['share_content'])
        self.assertEqual(share_list['share_url'], u'https://yl.t.dwtv.tv/h5share/dynamic/dynamic_id/#####')


    def test_dynamic_id_is_null(self):
        """
        测试请求接口动态ID为空
        :return:
        """
        get_dynamic_detail_api = GetDynamicDetailApi(self.user_mobile)
        get_dynamic_detail_api.post({'dynamic_id': None})

        self.assertEqual(get_dynamic_detail_api.get_code(), 450007)
        self.assertEqual(get_dynamic_detail_api.get_response_message(),u'动态id不能为空')

    def test_dynamic_id_is_error(self):
        """
        测试请求接口动态ID不存在
        :return:
        """
        get_dynamic_detail_api = GetDynamicDetailApi(self.user_mobile)
        get_dynamic_detail_api.post({'dynamic_id': 9090999})

        self.assertEqual(get_dynamic_detail_api.get_code(), 450010)
        self.assertEqual(get_dynamic_detail_api.get_response_message(),u'动态不存在')


    def tearDown(self,*args):
        super(TestDynamicDetailsApi,self).tearDown()
        for i in self.dynamic_ids:
            RemoveDynamicApi(self.anchor_mobile).get({'dynamic_id': i})