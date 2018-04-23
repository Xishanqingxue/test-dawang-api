# -*- coding:utf-8 -*-
from api.publish_dynamic_api import PublishDynamicApi,RemoveDynamicApi,GetHomePageDynamicApi,GetSquareDynamicApi,GetDynamicDetailApi,UpvoteApi
from base.base_case import BaseCase
from utilities.redis_helper import Redis
import json,settings



class TestDynamicUpvoteApi(BaseCase):
    """
    动态点赞
    """
    anchor_mobile = settings.YULE_TEST_ANCHOR_LOGIN_NAME
    anchor_id = settings.YULE_TEST_ANCHOR_ID
    room_id = settings.YULE_TEST_ROOM
    user_mobile = settings.YULE_TEST_USER_LOGIN_NAME
    other_user_mobile = '13511110003'
    pic_url = ['pic/58/c2/58c2689b7c0730d7b605cb8beeb13702_0.png']
    video_url = ['video/e0/90/e09069c0b0792e362dd7cfbf0b0b8642.mp4']
    content = 'Auto Test!!'
    dynamic_ids = []

    def test_dynamic_upvote(self):
        """
        测试动态点赞成功
        :return:
        """
        # 发布动态
        publish_dynamic_api = PublishDynamicApi(self.anchor_mobile)
        publish_dynamic_api.get({'type': 2, 'image_urls': None, 'video_url': self.video_url,
             'content': self.content, 'first_frame': self.pic_url})
        self.assertEqual(publish_dynamic_api.get_code(), 0)
        # 验证个人主页中动态信息
        get_home_page_dynamic_list_api = GetHomePageDynamicApi(self.anchor_mobile)
        response = get_home_page_dynamic_list_api.get({'anchor_id':self.anchor_id})

        self.assertEqual(get_home_page_dynamic_list_api.get_code(),0)
        anchor_dynamic_list = json.loads(response.content)['result']['dynamic_list']
        for x in anchor_dynamic_list:
            self.dynamic_ids.append(x['id'])
        self.assertEqual(anchor_dynamic_list[0]['upvote_num'],0)
        self.assertEqual(anchor_dynamic_list[0]['is_upvote_by_me'],0)
        dynamic_id = json.loads(response.content)['result']['dynamic_list'][0]['id']

        Redis().check_anchor_dynamic(dynamic_id)
        # 验证广场页面动态信息
        get_square_dynamic_api = GetSquareDynamicApi(self.user_mobile)
        response= get_square_dynamic_api.get()
        self.assertEqual(get_square_dynamic_api.get_code(),0)
        dynamic_list = json.loads(response.content)['result']['dynamic_list']
        self.assertEqual(dynamic_list[0]['id'],dynamic_id)
        self.assertEqual(dynamic_list[0]['upvote_num'],0)
        self.assertEqual(dynamic_list[0]['status'],1)
        self.assertEqual(dynamic_list[0]['is_upvote_by_me'],0)
        # 点赞
        upvote_api = UpvoteApi(self.user_mobile)
        upvote_api.get({'dynamic_id':dynamic_id})

        self.assertEqual(upvote_api.get_code(),0)
        # 校验点赞
        get_home_page_dynamic_list_api = GetHomePageDynamicApi(self.anchor_mobile)
        response = get_home_page_dynamic_list_api.get({'anchor_id': self.anchor_id})

        self.assertEqual(get_home_page_dynamic_list_api.get_code(), 0)
        self.assertEqual(json.loads(response.content)['result']['dynamic_list'][0]['upvote_num'],1)
        self.assertEqual(json.loads(response.content)['result']['dynamic_list'][0]['is_upvote_by_me'],0)
        self.assertEqual(json.loads(response.content)['result']['dynamic_list'][0]['status'],1)

        get_square_dynamic_api = GetSquareDynamicApi(self.user_mobile)
        response = get_square_dynamic_api.get()
        self.assertEqual(get_square_dynamic_api.get_code(), 0)
        dynamic_list = json.loads(response.content)['result']['dynamic_list']
        self.assertEqual(dynamic_list[0]['id'], dynamic_id)
        self.assertEqual(dynamic_list[0]['upvote_num'], 1)

        get_dynamic_detail_api = GetDynamicDetailApi(self.user_mobile)
        response = get_dynamic_detail_api.get({'dynamic_id': dynamic_id})

        self.assertEqual(get_dynamic_detail_api.get_code(), 0)
        dynamic_obj = json.loads(response.content)['result']['dynamic_obj']
        self.assertEqual(dynamic_obj['upvote_num'],1)
        self.assertEqual(dynamic_obj['is_upvote_by_me'],1)

    def test_dynamic_upvote_again(self):
        """
        测试两次请求点赞接口取消点赞
        :return:
        """
        publish_dynamic_api = PublishDynamicApi(self.anchor_mobile)
        publish_dynamic_api.get(
            {'type': 2, 'image_urls': None, 'video_url': self.video_url,
             'content': self.content, 'first_frame': self.pic_url})
        self.assertEqual(publish_dynamic_api.get_code(), 0)

        get_home_page_dynamic_list_api = GetHomePageDynamicApi(self.anchor_mobile)
        response = get_home_page_dynamic_list_api.get({'anchor_id':self.anchor_id})

        self.assertEqual(get_home_page_dynamic_list_api.get_code(),0)
        anchor_dynamic_list = json.loads(response.content)['result']['dynamic_list']
        for x in anchor_dynamic_list:
            self.dynamic_ids.append(x['id'])
        dynamic_id = anchor_dynamic_list[0]['id']

        Redis().check_anchor_dynamic(dynamic_id)
        # 点赞
        upvote_api = UpvoteApi(self.user_mobile)
        upvote_api.get({'dynamic_id':dynamic_id})
        self.assertEqual(upvote_api.get_code(),0)

        upvote_api = UpvoteApi(self.user_mobile)
        upvote_api.get({'dynamic_id':dynamic_id})
        self.assertEqual(upvote_api.get_code(),0)
        # 校验点赞
        get_home_page_dynamic_list_api = GetHomePageDynamicApi(self.anchor_mobile)
        response = get_home_page_dynamic_list_api.get({'anchor_id': self.anchor_id})
        self.assertEqual(get_home_page_dynamic_list_api.get_code(), 0)
        dynamic_obj = json.loads(response.content)['result']['dynamic_list'][0]
        self.assertEqual(dynamic_obj['upvote_num'],0)
        self.assertEqual(dynamic_obj['status'],1)
        self.assertEqual(dynamic_obj['is_upvote_by_me'],0)

        get_square_dynamic_api = GetSquareDynamicApi(self.user_mobile)
        response = get_square_dynamic_api.get()
        self.assertEqual(get_square_dynamic_api.get_code(), 0)
        dynamic_list = json.loads(response.content)['result']['dynamic_list']
        self.assertEqual(dynamic_list[0]['id'], dynamic_id)
        self.assertEqual(dynamic_list[0]['upvote_num'], 0)
        self.assertEqual(dynamic_list[0]['is_upvote_by_me'],0)

        get_dynamic_detail_api = GetDynamicDetailApi(self.user_mobile)
        response = get_dynamic_detail_api.get({'dynamic_id': dynamic_id})

        self.assertEqual(get_dynamic_detail_api.get_code(), 0)
        dynamic_obj = json.loads(response.content)['result']['dynamic_obj']
        self.assertEqual(dynamic_obj['upvote_num'], 0)
        self.assertEqual(dynamic_obj['is_upvote_by_me'], 0)


    def test_dynamic_upvote_other_user(self):
        """
        测试多个用户点赞
        :return:
        """
        publish_dynamic_api = PublishDynamicApi(self.anchor_mobile)
        publish_dynamic_api.get(
            {'type': 2, 'image_urls': None, 'video_url': self.video_url,
             'content': self.content, 'first_frame': self.pic_url})
        self.assertEqual(publish_dynamic_api.get_code(), 0)

        get_home_page_dynamic_list_api = GetHomePageDynamicApi(self.anchor_mobile)
        response = get_home_page_dynamic_list_api.get({'anchor_id':self.anchor_id})

        self.assertEqual(get_home_page_dynamic_list_api.get_code(),0)
        anchor_dynamic_list = json.loads(response.content)['result']['dynamic_list']
        for x in anchor_dynamic_list:
            self.dynamic_ids.append(x['id'])
        dynamic_id = anchor_dynamic_list[0]['id']

        Redis().check_anchor_dynamic(dynamic_id)
        # 点赞
        upvote_api = UpvoteApi(self.user_mobile)
        upvote_api.get({'dynamic_id':dynamic_id})
        self.assertEqual(upvote_api.get_code(),0)

        upvote_api = UpvoteApi(self.other_user_mobile)
        upvote_api.get({'dynamic_id':dynamic_id})
        self.assertEqual(upvote_api.get_code(),0)
        # 校验点赞
        get_home_page_dynamic_list_api = GetHomePageDynamicApi(self.anchor_mobile)
        response = get_home_page_dynamic_list_api.get({'anchor_id': self.anchor_id})
        self.assertEqual(get_home_page_dynamic_list_api.get_code(), 0)
        dynamic_obj = json.loads(response.content)['result']['dynamic_list'][0]
        self.assertEqual(dynamic_obj['upvote_num'],2)
        self.assertEqual(dynamic_obj['status'],1)
        self.assertEqual(dynamic_obj['is_upvote_by_me'],0)
        get_square_dynamic_api = GetSquareDynamicApi(self.user_mobile)
        response = get_square_dynamic_api.get()
        self.assertEqual(get_square_dynamic_api.get_code(), 0)
        dynamic_list = json.loads(response.content)['result']['dynamic_list']
        self.assertEqual(dynamic_list[0]['id'], dynamic_id)
        self.assertEqual(dynamic_list[0]['upvote_num'], 2)
        self.assertEqual(dynamic_list[0]['is_upvote_by_me'],1)

        get_dynamic_detail_api = GetDynamicDetailApi(self.user_mobile)
        response = get_dynamic_detail_api.get({'dynamic_id': dynamic_id})

        self.assertEqual(get_dynamic_detail_api.get_code(), 0)
        dynamic_obj = json.loads(response.content)['result']['dynamic_obj']
        self.assertEqual(dynamic_obj['upvote_num'], 2)
        self.assertEqual(dynamic_obj['is_upvote_by_me'], 1)


    def test_upvote_dynamic_id_is_null(self):
        """
        测试请求接口动态ID为空
        :return:
        """
        upvote_api = UpvoteApi(self.user_mobile)
        upvote_api.get({'dynamic_id': None})
        self.assertEqual(upvote_api.get_code(), 450006)
        self.assertEqual(upvote_api.get_response_message(),u'请求信息出错')

    def tearDown(self,*args):
        super(TestDynamicUpvoteApi,self).tearDown()
        for i in self.dynamic_ids:
            RemoveDynamicApi(self.anchor_mobile).get({'dynamic_id': i})

