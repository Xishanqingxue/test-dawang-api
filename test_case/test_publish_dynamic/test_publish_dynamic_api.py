# -*- coding:utf-8 -*-
from api.publish_dynamic_api import PublishDynamicApi,RemoveDynamicApi,GetHomePageDynamicApi
from base.base_case import BaseCase
import json,settings


class TestPublishDynamicApi(BaseCase):
    """
    发布动态
    """
    anchor_mobile = settings.YULE_TEST_ANCHOR_LOGIN_NAME
    anchor_id = settings.YULE_TEST_ANCHOR_ID
    room_id = settings.YULE_TEST_ROOM
    pic_url = ['pic/58/c2/58c2689b7c0730d7b605cb8beeb13702_0.png']
    video_url = ['video/e0/90/e09069c0b0792e362dd7cfbf0b0b8642.mp4']
    content = 'Auto Test!!'
    dynamic_ids = []

    def test_publish_dynamic_video(self):
        """
        测试发布视频动态
        :return:
        """
        publish_dynamic_api = PublishDynamicApi(self.anchor_mobile)
        publish_dynamic_api.get({'type': 2, 'image_urls': None, 'video_url': self.video_url, 'content': self.content,
                                 'first_frame': self.pic_url})

        self.assertEqual(publish_dynamic_api.get_code(), 0)

        get_home_page_dynamic_list_api = GetHomePageDynamicApi(self.anchor_mobile)
        response = get_home_page_dynamic_list_api.get({'anchor_id': self.anchor_id})
        self.assertEqual(get_home_page_dynamic_list_api.get_code(), 0)

        anchor_dynamic_list = json.loads(response.content)['result']['dynamic_list']
        for x in anchor_dynamic_list:
            self.dynamic_ids.append(x['id'])

        self.assertEqual(len(anchor_dynamic_list), 1)

        anchor_dynamic = json.loads(response.content)['result']['dynamic_list'][0]
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

    def test_publish_dynamic_pic_url_is_null(self):
        """
        测试请求接口动态图片为空
        :return:
        """
        publish_dynamic_api = PublishDynamicApi(self.anchor_mobile)
        publish_dynamic_api.get({'type': 1, 'image_urls': None, 'video_url': None,
             'content': None, 'first_frame': None})
        self.assertEqual(publish_dynamic_api.get_code(), 450004)
        self.assertEqual(publish_dynamic_api.get_response_message(),u'请上传动态中的图片')

    def test_publish_dynamic_video_url_is_null(self):
        """
        测试请求接口视频为空
        :return:
        """
        publish_dynamic_api = PublishDynamicApi(self.anchor_mobile)
        publish_dynamic_api.get({'type': 2, 'image_urls': None, 'video_url': None,
             'content': None, 'first_frame': None})
        self.assertEqual(publish_dynamic_api.get_code(), 450005)
        self.assertEqual(publish_dynamic_api.get_response_message(),u'请上传动态中的视频')

    def test_publish_dynamic_first_frame_is_null(self):
        """
        测试请求接口第一帧图片为空
        :return:
        """
        publish_dynamic_api = PublishDynamicApi(self.anchor_mobile)
        publish_dynamic_api.get({'type': 2, 'image_urls': None, 'video_url': self.video_url,
             'content': None, 'first_frame': None})
        self.assertEqual(publish_dynamic_api.get_code(), 450005)
        self.assertEqual(publish_dynamic_api.get_response_message(),u'请上传动态中的视频')

    def test_publish_dynamic_type_null(self):
        """
        测试请求接口动态类型为空
        :return:
        """
        publish_dynamic_api = PublishDynamicApi(self.anchor_mobile)
        publish_dynamic_api.get({'type': None, 'image_urls': None, 'video_url': self.video_url,
             'content': None, 'first_frame': None})
        self.assertEqual(publish_dynamic_api.get_code(), 450001)
        self.assertEqual(publish_dynamic_api.get_response_message(),u'上传文件类型不能为空')

    def test_publish_dynamic_type_error(self):
        """
        测试请求接口动态类型错误
        :return:
        """
        publish_dynamic_api = PublishDynamicApi(self.anchor_mobile)
        publish_dynamic_api.get({'type': 55, 'image_urls': None, 'video_url': self.video_url,
             'content': None, 'first_frame': None})
        self.assertEqual(publish_dynamic_api.get_code(), 450001)
        self.assertEqual(publish_dynamic_api.get_response_message(),u'上传文件类型不能为空')

    def tearDown(self,*args):
        super(TestPublishDynamicApi, self).tearDown()
        for i in self.dynamic_ids:
            RemoveDynamicApi(self.anchor_mobile).get({'dynamic_id': i})
