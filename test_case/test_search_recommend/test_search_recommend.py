# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.search_api import SearchRecommendApi
import json, settings


class TestSearchRecommend(BaseCase):
    """
    搜索推荐
    """

    def test_search_recommend(self):
        """
        测试请求接口成功
        :return:
        """
        search_recommend = SearchRecommendApi()
        response = search_recommend.get()
        self.assertEqual(search_recommend.get_code(), 0)
        recommend_list = json.loads(response.content)['result']['recommend_list']
        self.assertEqual(len(recommend_list), 10)
