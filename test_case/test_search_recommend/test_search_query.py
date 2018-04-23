# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.search_api import SearchQueryApi
import json

class TestSearchQuery(BaseCase):
    """
    搜索
    """

    keyword = ['123248',u'小','1234567']

    def test_search_query_esact(self):
        """
        测试准确搜索
        :return:
        """
        #准确搜索
        search_query = SearchQueryApi()
        response = search_query.get({"keyword":self.keyword[0]})
        self.assertEqual(search_query.get_code(),0)
        room_list = json.loads(response.content)['result']['room_list']
        self.assertEqual(len(room_list),1)
        self.assertEqual(room_list[0]['id'],self.keyword[0])

    def test_search_query_vague(self):
        """
        测试模糊搜索
        :return:
        """
        # 模糊搜索
        search_query = SearchQueryApi()
        response = search_query.get({"keyword": self.keyword[1]})
        self.assertEqual(search_query.get_code(), 0)
        room_list = json.loads(response.content)['result']['room_list']
        self.assertTrue(len(room_list)>=1)
        for i in range(len(room_list)):
            nickname = room_list[i]["anchor_obj"]['nickname']
            self.assertIn(self.keyword[1],nickname)

    def test_search_query_empty(self):
        """
        测试输入错误房间号搜索结果为空
        :return:
        """
        #搜索为空
        search_query = SearchQueryApi()
        response = search_query.get({"keyword":self.keyword[2]})
        self.assertEqual(search_query.get_code(),0)
        room_list = json.loads(response.content)['result']['room_list']
        self.assertEqual(len(room_list), 0)

    def test_search_query_null(self):
        """
        测试请求接口搜索内容为空
        :return:
        """
        #搜索为空
        search_query = SearchQueryApi()
        search_query.get({"keyword":None})
        self.assertEqual(search_query.get_code(),200415)
        self.assertEqual(search_query.get_response_message(),u'搜索的关键词不能为空')