# -*- coding:utf-8 -*-
from base.base_api import BaseApi

class SearchQueryApi(BaseApi):
    """
    搜索
    """
    url = '/search/query'

    def build_custom_param(self, data):
        return {"keyword":data['keyword']}


class SearchRecommendApi(BaseApi):
    """
    搜索推荐列表
    """
    url = "/search/recommend"