# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.publish_dynamic_api import PublishCommentApi, PublishDynamicApi, GetHomePageDynamicApi, GetSquareDynamicApi, \
    GetCommentListApi, GetDynamicDetailApi, RemoveCommentApi, RemoveDynamicApi
from utilities.redis_helper import Redis
from utilities.mysql_helper import MysqlOperation
import time, json, settings


class TestPublishCommentApi(BaseCase):
    """
    动态评论
    """
    anchor_mobile = settings.YULE_TEST_ANCHOR_LOGIN_NAME
    anchor_id = settings.YULE_TEST_ANCHOR_ID
    user_mobile = '13811111112'
    user_id = '22013760'
    user_mobile_two = '13511110003'
    user_id_two = '22001448'
    no_bind_mobile_user = '15877777777'
    pic_url = ['pic/58/c2/58c2689b7c0730d7b605cb8beeb13702_0.png']
    video_url = ['video/e0/90/e09069c0b0792e362dd7cfbf0b0b8642.mp4']
    content = 'Auto Test!!'
    dynamic_ids = []

    def test_publish_comment_dynamic_id_is_null(self):
        """
        测试请求接口动态ID为空
        :return:
        """
        publish_comment_api = PublishCommentApi(self.user_mobile)
        publish_comment_api.get({'dynamic_id': None, 'comment': '测试动态评论接口', 'reply_user_id': None, 'type': 1})
        self.assertEqual(publish_comment_api.get_code(), 450007)
        self.assertEqual(publish_comment_api.get_response_message(), u'动态id不能为空')

    def test_publish_comment_dynamic_id_is_error(self):
        """
        测试请求接口动态ID错误
        :return:
        """
        publish_comment_api = PublishCommentApi(self.user_mobile)
        publish_comment_api.get({'dynamic_id': '99999', 'comment': '测试动态评论接口', 'reply_user_id': None, 'type': 1})
        self.assertEqual(publish_comment_api.get_code(), 450010)
        self.assertEqual(publish_comment_api.get_response_message(), u'动态不存在')

    def test_publish_comment_type_null(self):
        """
        测试请求接口评论类型为空
        :return:
        """
        publish_dynamic_api = PublishDynamicApi(self.anchor_mobile)
        publish_dynamic_api.get({'type': 2, 'image_urls': None, 'video_url': self.video_url,
                                 'content': self.content, 'first_frame': self.pic_url})

        self.assertEqual(publish_dynamic_api.get_code(), 0)
        # 校验主播自己的个人主页里面是否显示该动态
        get_home_page_dynamic_list_api = GetHomePageDynamicApi(self.anchor_mobile)
        response = get_home_page_dynamic_list_api.get({'anchor_id': self.anchor_id})

        self.assertEqual(get_home_page_dynamic_list_api.get_code(), 0)
        dynamic_id = json.loads(response.content)['result']['dynamic_list'][0]['id']
        self.dynamic_ids.append(dynamic_id)
        # 审核动态
        Redis().check_anchor_dynamic(dynamic_id)
        publish_comment_api = PublishCommentApi(self.user_mobile)
        publish_comment_api.get({'dynamic_id': dynamic_id, 'comment': '测试动态评论接口', 'reply_user_id': None, 'type': None})
        self.assertEqual(publish_comment_api.get_code(), 450014)
        self.assertEqual(publish_comment_api.get_response_message(), u'评论类型不正确')

    def test_publish_comment_type_error(self):
        """
        测试请求接口评论类型错误
        :return:
        """
        publish_dynamic_api = PublishDynamicApi(self.anchor_mobile)
        publish_dynamic_api.get({'type': 2, 'image_urls': None, 'video_url': self.video_url,
                                 'content': self.content, 'first_frame': self.pic_url})

        self.assertEqual(publish_dynamic_api.get_code(), 0)
        # 校验主播自己的个人主页里面是否显示该动态
        get_home_page_dynamic_list_api = GetHomePageDynamicApi(self.anchor_mobile)
        response = get_home_page_dynamic_list_api.get({'anchor_id': self.anchor_id})

        self.assertEqual(get_home_page_dynamic_list_api.get_code(), 0)
        dynamic_id = json.loads(response.content)['result']['dynamic_list'][0]['id']
        self.dynamic_ids.append(dynamic_id)
        # 审核动态
        Redis().check_anchor_dynamic(dynamic_id)
        publish_comment_api = PublishCommentApi(self.user_mobile)
        publish_comment_api.get({'dynamic_id': dynamic_id, 'comment': '测试动态评论接口', 'reply_user_id': None, 'type': 333})
        self.assertEqual(publish_comment_api.get_code(), 450014)
        self.assertEqual(publish_comment_api.get_response_message(), u'评论类型不正确')

    def test_publish_comment_comment_null(self):
        """
        测试请求接口评论内容为空
        :return:
        """
        publish_dynamic_api = PublishDynamicApi(self.anchor_mobile)
        publish_dynamic_api.get({'type': 2, 'image_urls': None, 'video_url': self.video_url,
                                 'content': self.content, 'first_frame': self.pic_url})

        self.assertEqual(publish_dynamic_api.get_code(), 0)
        # 校验主播自己的个人主页里面是否显示该动态
        get_home_page_dynamic_list_api = GetHomePageDynamicApi(self.anchor_mobile)
        response = get_home_page_dynamic_list_api.get({'anchor_id': self.anchor_id})

        self.assertEqual(get_home_page_dynamic_list_api.get_code(), 0)
        dynamic_id = json.loads(response.content)['result']['dynamic_list'][0]['id']
        self.dynamic_ids.append(dynamic_id)
        # 审核动态
        Redis().check_anchor_dynamic(dynamic_id)
        publish_comment_api = PublishCommentApi(self.user_mobile)
        publish_comment_api.get({'dynamic_id': dynamic_id, 'comment': None, 'reply_user_id': None, 'type': 333})
        self.assertEqual(publish_comment_api.get_code(), 450013)
        self.assertEqual(publish_comment_api.get_response_message(), u'评论不能为空')

    def test_publish_comment_sensitive_words(self):
        """
        测试动态评论敏感词
        :return:
        """
        publish_dynamic_api = PublishDynamicApi(self.anchor_mobile)
        publish_dynamic_api.get({'type': 2, 'image_urls': None, 'video_url': self.video_url,
                                 'content': self.content, 'first_frame': self.pic_url})

        self.assertEqual(publish_dynamic_api.get_code(), 0)
        # 校验主播自己的个人主页里面是否显示该动态
        get_home_page_dynamic_list_api = GetHomePageDynamicApi(self.anchor_mobile)
        response = get_home_page_dynamic_list_api.get({'anchor_id': self.anchor_id})

        self.assertEqual(get_home_page_dynamic_list_api.get_code(), 0)
        dynamic_id = json.loads(response.content)['result']['dynamic_list'][0]['id']
        self.dynamic_ids.append(dynamic_id)
        # 审核动态
        Redis().check_anchor_dynamic(dynamic_id)
        publish_comment_api = PublishCommentApi(self.user_mobile)
        publish_comment_api.get(
            {'dynamic_id': dynamic_id, 'comment': '习近平', 'reply_user_id': None, 'type': 1})

        self.assertEqual(publish_comment_api.get_code(), 0)

        MysqlOperation(user_id=self.user_id).fix_dynamic_comment_status(status=1, dynamic_id=dynamic_id)
        time.sleep(0.5)
        # 动态详情
        get_dynamic_detail_api = GetDynamicDetailApi(self.user_mobile)
        response = get_dynamic_detail_api.get({'dynamic_id': dynamic_id})

        self.assertEqual(get_dynamic_detail_api.get_code(), 0)
        comment_num = json.loads(response.content)['result']['dynamic_obj']['comment_num']
        self.assertEqual(comment_num, 1)

        get_comment_list_api = GetCommentListApi(self.user_mobile)
        response = get_comment_list_api.get({'dynamic_id': dynamic_id})

        self.assertEqual(get_comment_list_api.get_code(), 0)
        comment_obj_list = json.loads(response.content)['result']['comment_obj_list']
        self.assertEqual(len(comment_obj_list), 1)
        self.assertEqual(comment_obj_list[0]['comment'], u'***')

    def test_publish_comment_word_number_restriction(self):
        """
        测试动态评论内容超过字数限制
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
        dynamic_id = json.loads(response.content)['result']['dynamic_list'][0]['id']
        self.dynamic_ids.append(dynamic_id)
        # 审核动态
        Redis().check_anchor_dynamic(dynamic_id)

        publish_comment_api = PublishCommentApi(self.user_mobile)
        publish_comment_api.get(
            {'dynamic_id': dynamic_id, 'comment': '一二' * 75 + '。', 'reply_user_id': None, 'type': 1})

        self.assertEqual(publish_comment_api.get_code(), 450019)
        self.assertEqual(publish_comment_api.get_response_message(), u'超过限制的字输入无效')

        publish_comment_api = PublishCommentApi(self.user_mobile)
        publish_comment_api.get(
            {'dynamic_id': dynamic_id, 'comment': 'ab' * 75 + '.', 'reply_user_id': None, 'type': 1})
        self.assertEqual(publish_comment_api.get_code(), 450019)
        self.assertEqual(publish_comment_api.get_response_message(), u'超过限制的字输入无效')

    def test_publish_comment_success(self):
        """
        测试动态评论成功/评论详情列表
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
        dynamic_id = json.loads(response.content)['result']['dynamic_list'][0]['id']
        self.dynamic_ids.append(dynamic_id)
        # 审核动态
        Redis().check_anchor_dynamic(dynamic_id)

        publish_comment_api = PublishCommentApi(self.user_mobile)
        publish_comment_api.get({'dynamic_id': dynamic_id, 'comment': '测试动态评论接口', 'reply_user_id': None, 'type': 1})

        self.assertEqual(publish_comment_api.get_code(), 0)

        MysqlOperation(user_id=self.user_id).fix_dynamic_comment_status(status=1, dynamic_id=dynamic_id)
        time.sleep(0.5)
        # 动态详情
        get_dynamic_detail_api = GetDynamicDetailApi(self.user_mobile)
        response = get_dynamic_detail_api.get({'dynamic_id': dynamic_id})

        self.assertEqual(get_dynamic_detail_api.get_code(), 0)
        comment_num = json.loads(response.content)['result']['dynamic_obj']['comment_num']
        self.assertEqual(comment_num, 1)

        get_comment_list_api = GetCommentListApi(self.user_mobile)
        response = get_comment_list_api.get({'dynamic_id': dynamic_id})
        self.assertEqual(get_comment_list_api.get_code(), 0)
        comment_num = json.loads(response.content)['result']['comment_num']
        self.assertEqual(comment_num, 1)
        comment_obj_list = json.loads(response.content)['result']['comment_obj_list']
        self.assertEqual(len(comment_obj_list), 1)
        self.assertEqual(comment_obj_list[0]['user_id'], (self.user_id))
        self.assertEqual(comment_obj_list[0]['comment'], u'测试动态评论接口')
        self.assertEqual(comment_obj_list[0]['type'], u'1')
        self.assertEqual(comment_obj_list[0]['status'], u'1')
        self.assertEqual(comment_obj_list[0]['user_nickname'],
                         MysqlOperation(user_id=self.user_id).get_user_details()['nickname'])
        self.assertEqual(comment_obj_list[0]['create_time_str'], u'刚刚')

    def test_publish_comment_reply(self):
        """
        测试动态评论/回复/评论详情列表
        :return:
        """
        # 发动态
        publish_dynamic_api = PublishDynamicApi(self.anchor_mobile)
        publish_dynamic_api.get({'type': 2, 'image_urls': None, 'video_url': self.video_url,
                                 'content': self.content, 'first_frame': self.pic_url})

        self.assertEqual(publish_dynamic_api.get_code(), 0)

        get_home_page_dynamic_list_api = GetHomePageDynamicApi(self.anchor_mobile)
        response = get_home_page_dynamic_list_api.get({'anchor_id': self.anchor_id})

        self.assertEqual(get_home_page_dynamic_list_api.get_code(), 0)
        dynamic_id = json.loads(response.content)['result']['dynamic_list'][0]['id']
        self.dynamic_ids.append(dynamic_id)
        Redis().check_anchor_dynamic(dynamic_id)

        publish_comment_api = PublishCommentApi(self.user_mobile)
        publish_comment_api.get(
            {'dynamic_id': dynamic_id, 'comment': '测试动态评论接口', 'reply_user_id': None, 'type': 1})

        self.assertEqual(publish_comment_api.get_code(), 0)

        MysqlOperation(user_id=self.user_id).fix_dynamic_comment_status(status=1, dynamic_id=dynamic_id)
        time.sleep(0.5)

        publish_comment_api = PublishCommentApi(self.user_mobile_two)
        publish_comment_api.get(
            {'dynamic_id': dynamic_id, 'comment': '测试回复评论', 'reply_user_id': self.user_id,
             'type': 2})

        self.assertEqual(publish_comment_api.get_code(), 0)

        MysqlOperation(user_id=self.user_id_two).fix_dynamic_comment_status(status=1, dynamic_id=dynamic_id)
        time.sleep(0.5)

        get_comment_list_api = GetCommentListApi(self.user_mobile)
        response = get_comment_list_api.get({'dynamic_id': dynamic_id})

        self.assertEqual(get_comment_list_api.get_code(), 0)
        comment_num = json.loads(response.content)['result']['comment_num']
        self.assertEqual(comment_num, 2)
        comment_obj_list = json.loads(response.content)['result']['comment_obj_list']
        self.assertEqual(len(comment_obj_list), 2)
        for x in comment_obj_list:
            self.assertEqual(int(x['dynamic_id']), int(dynamic_id))
            self.assertEqual(x['status'], u'1')
            self.assertEqual(x['create_time_str'], u'刚刚')

        self.assertEqual(comment_obj_list[0]['user_id'], (self.user_id_two))
        self.assertEqual(comment_obj_list[0]['comment'], u'测试回复评论')
        self.assertEqual(comment_obj_list[0]['reply_user_id'], (self.user_id))
        self.assertEqual(comment_obj_list[0]['type'], u'2')
        self.assertEqual(comment_obj_list[0]['user_nickname'],
                         (MysqlOperation(user_id=self.user_id_two).get_user_details()['nickname']))
        self.assertEqual(comment_obj_list[0]['reply_user_nickname'],
                         (MysqlOperation(user_id=self.user_id).get_user_details()['nickname']))

        self.assertEqual(comment_obj_list[1]['user_id'], (self.user_id))
        self.assertEqual(comment_obj_list[1]['comment'], u'测试动态评论接口')
        self.assertEqual(comment_obj_list[1]['type'], u'1')
        self.assertEqual(comment_obj_list[1]['user_nickname'],
                         (MysqlOperation(user_id=self.user_id).get_user_details()['nickname']))
        self.assertEqual(comment_obj_list[1]['create_time_str'], u'刚刚')
        comment_id = comment_obj_list[0]['id']

        get_square_dynamic_api = GetSquareDynamicApi(self.user_mobile)
        response = get_square_dynamic_api.get()

        self.assertEqual(get_square_dynamic_api.get_code(), 0)
        dynamic_list = json.loads(response.content)['result']['dynamic_list']
        self.assertEqual(dynamic_list[0]['comment_num'], 2)

        get_home_page_dynamic_list_api = GetHomePageDynamicApi(self.anchor_mobile)
        response = get_home_page_dynamic_list_api.get(
            {'anchor_id': self.anchor_id})

        self.assertEqual(get_home_page_dynamic_list_api.get_code(), 0)
        comment_num = json.loads(response.content)['result']['dynamic_list'][0]['comment_num']
        self.assertEqual(comment_num, 2)

        get_comment_list_api = GetCommentListApi(self.user_mobile)
        response = get_comment_list_api.get({'dynamic_id': dynamic_id})

        self.assertEqual(get_comment_list_api.get_code(), 0)
        comment_num = json.loads(response.content)['result']['comment_num']
        self.assertEqual(comment_num, 2)
        comment_obj_list = json.loads(response.content)['result']['comment_obj_list']
        self.assertEqual(len(comment_obj_list), 2)

        remove_comment_api = RemoveCommentApi(self.user_mobile_two)
        remove_comment_api.get({'comment_id': comment_id})

        self.assertEqual(remove_comment_api.get_code(), 0)

        get_comment_list_api = GetCommentListApi(self.user_mobile)
        response = get_comment_list_api.get({'dynamic_id': dynamic_id})

        self.assertEqual(get_comment_list_api.get_code(), 0)
        comment_num = json.loads(response.content)['result']['comment_num']
        self.assertEqual(comment_num, 1)
        comment_obj_list = json.loads(response.content)['result']['comment_obj_list']
        self.assertEqual(len(comment_obj_list), 1)

        get_home_page_dynamic_list_api = GetHomePageDynamicApi(self.anchor_mobile)
        response = get_home_page_dynamic_list_api.get(
            {'anchor_id': self.anchor_id})

        self.assertEqual(get_home_page_dynamic_list_api.get_code(), 0)
        comment_num = json.loads(response.content)['result']['dynamic_list'][0]['comment_num']
        self.assertEqual(comment_num, 1)

        get_square_dynamic_api = GetSquareDynamicApi(self.user_mobile)
        response = get_square_dynamic_api.get()

        self.assertEqual(get_square_dynamic_api.get_code(), 0)
        dynamic_list = json.loads(response.content)['result']['dynamic_list']
        self.assertEqual(dynamic_list[0]['comment_num'], 1)

    def test_remove_comment(self):
        """
        测试删除评论
        :return:
        """
        publish_dynamic_api = PublishDynamicApi(self.anchor_mobile)
        publish_dynamic_api.get({'type': 2, 'image_urls': None, 'video_url': self.video_url,
                                 'content': self.content, 'first_frame': self.pic_url})

        self.assertEqual(publish_dynamic_api.get_code(), 0)

        get_home_page_dynamic_list_api = GetHomePageDynamicApi(self.anchor_mobile)
        response = get_home_page_dynamic_list_api.get({'anchor_id': self.anchor_id})

        self.assertEqual(get_home_page_dynamic_list_api.get_code(), 0)
        dynamic_id = json.loads(response.content)['result']['dynamic_list'][0]['id']
        self.dynamic_ids.append(dynamic_id)

        Redis().check_anchor_dynamic(dynamic_id)

        publish_comment_api = PublishCommentApi(self.user_mobile)
        publish_comment_api.get({'dynamic_id': dynamic_id, 'comment': '测试动态评论接口', 'reply_user_id': None, 'type': 1})

        self.assertEqual(publish_comment_api.get_code(), 0)

        MysqlOperation(user_id=self.user_id).fix_dynamic_comment_status(status=1, dynamic_id=dynamic_id)
        time.sleep(0.5)

        get_comment_list_api = GetCommentListApi(self.user_mobile)
        response = get_comment_list_api.get({'dynamic_id': dynamic_id})

        self.assertEqual(get_comment_list_api.get_code(), 0)
        comment_num = json.loads(response.content)['result']['comment_num']
        self.assertEqual(comment_num, 1)
        comment_obj_list = json.loads(response.content)['result']['comment_obj_list']
        self.assertEqual(len(comment_obj_list), 1)
        comment_id = comment_obj_list[0]['id']

        get_square_dynamic_api = GetSquareDynamicApi(self.user_mobile)
        response = get_square_dynamic_api.get()

        self.assertEqual(get_square_dynamic_api.get_code(), 0)
        dynamic_list = json.loads(response.content)['result']['dynamic_list']
        self.assertEqual(dynamic_list[0]['comment_num'], 1)

        remove_comment_api = RemoveCommentApi(self.user_mobile_two)
        remove_comment_api.get({'comment_id': comment_id})

        self.assertEqual(remove_comment_api.get_code(), 450012)
        self.assertEqual(remove_comment_api.get_response_message(), u'没有删除权限')

        remove_comment_api = RemoveCommentApi(self.user_mobile)
        remove_comment_api.get({'comment_id': comment_id})

        self.assertEqual(remove_comment_api.get_code(), 0)

        get_comment_list_api = GetCommentListApi(self.user_mobile)
        response = get_comment_list_api.get({'dynamic_id': dynamic_id})

        self.assertEqual(get_comment_list_api.get_code(), 0)
        comment_num = json.loads(response.content)['result']['comment_num']
        self.assertEqual(comment_num, 0)
        comment_obj_list = json.loads(response.content)['result']['comment_obj_list']
        self.assertEqual(len(comment_obj_list), 0)

        get_square_dynamic_api = GetSquareDynamicApi(self.user_mobile)
        response = get_square_dynamic_api.get()

        self.assertEqual(get_square_dynamic_api.get_code(), 0)
        dynamic_list = json.loads(response.content)['result']['dynamic_list']
        self.assertEqual(dynamic_list[0]['comment_num'], 0)

    def test_publish_comment_not_bind_mobile(self):
        """
        测试未绑定手机号用户不能评论动态
        :return:
        """
        publish_dynamic_api = PublishDynamicApi(self.anchor_mobile)
        publish_dynamic_api.get({'type': 2, 'image_urls': None, 'video_url': self.video_url,
                                 'content': self.content, 'first_frame': self.pic_url})

        self.assertEqual(publish_dynamic_api.get_code(), 0)

        get_home_page_dynamic_list_api = GetHomePageDynamicApi(self.anchor_mobile)
        response = get_home_page_dynamic_list_api.get({'anchor_id': self.anchor_id})

        self.assertEqual(get_home_page_dynamic_list_api.get_code(), 0)
        dynamic_id = json.loads(response.content)['result']['dynamic_list'][0]['id']
        self.dynamic_ids.append(dynamic_id)

        Redis().check_anchor_dynamic(dynamic_id)

        publish_comment_api = PublishCommentApi(self.no_bind_mobile_user)
        publish_comment_api.get({'dynamic_id': dynamic_id, 'comment': '测试动态评论接口', 'reply_user_id': None, 'type': 1})

        self.assertEqual(publish_comment_api.get_code(), 450020)
        self.assertEqual(publish_comment_api.get_response_message(), u'需要绑定手机号，才能发表评论哦')

    def tearDown(self, *args):
        super(TestPublishCommentApi, self).tearDown()
        for i in self.dynamic_ids:
            RemoveDynamicApi(self.anchor_mobile).get({'dynamic_id': i})
