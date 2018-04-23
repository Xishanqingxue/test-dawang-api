# -*- coding:utf-8 -*-
from api.follow_api import AddFollowingApi,RelieveFollowingApi,MyFollowListApi
from base.base_case import BaseCase
import json,settings


class TestFollowingApi(BaseCase):
    """
    关注
    """
    login_name = settings.YULE_TEST_USER_LOGIN_NAME
    anchor_id = settings.YULE_TEST_ANCHOR_ID

    def setUp(self,*args):
        super(TestFollowingApi,self).setUp()
        relieve_following_api = RelieveFollowingApi(self.login_name)
        relieve_following_api.get({'anchor_id': self.anchor_id})

    def test_add_following_successful(self):
        """
        测试关注主播成功/我的关注列表/取消关注成功
        :return:
        """
        # 关注主播
        add_following_api = AddFollowingApi(self.login_name)
        response = add_following_api.get({'anchor_id': self.anchor_id})
        self.assertEqual(add_following_api.get_code(), 0)
        self.assertEqual(add_following_api.get_response_message(), u'操作成功')
        self.assertEqual(json.loads(response.content)['result']['identity_obj']['has_followed'],1)

        add_following_again = AddFollowingApi(self.login_name)
        add_following_again.get({'anchor_id': self.anchor_id})
        self.assertEqual(add_following_again.get_code(),402007)
        self.assertEqual(add_following_again.get_response_message(),u'当前主播已经添加到我的关注')

        my_follow_list = MyFollowListApi(self.login_name)
        response = my_follow_list.get()
        self.assertEqual(my_follow_list.get_code(),0)
        room_list = json.loads(response.content)['result']['room_list']
        self.assertEqual(len(room_list),1)
        self.assertEqual(room_list[0]['to_user_id'],(self.anchor_id))
        self.assertEqual(room_list[0]['room_obj']['id'],(settings.YULE_TEST_ROOM))

        # 校验取消关注
        relieve_following_api = RelieveFollowingApi(self.login_name)
        response = relieve_following_api.get({'anchor_id': self.anchor_id})
        self.assertEqual(relieve_following_api.get_code(),0)
        self.assertEqual(relieve_following_api.get_response_message(),u'操作成功')
        self.assertEqual(json.loads(response.content)['result']['identity_obj']['has_followed'],0)

        my_follow_list = MyFollowListApi(self.login_name)
        response = my_follow_list.get()
        self.assertEqual(my_follow_list.get_code(), 0)
        room_list = json.loads(response.content)['result']['room_list']
        self.assertEqual(len(room_list), 0)


    def tearDown(self,*args):
        super(TestFollowingApi,self).tearDown()
        relieve_following_api = RelieveFollowingApi(self.login_name)
        relieve_following_api.get({'anchor_id': self.anchor_id})