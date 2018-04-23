# -*- coding:utf-8 -*-
from base.base_api import BaseApi
import settings


class ImageCodeApi(BaseApi):
    """
    获取图形验证码接口
    """
    url = '/user/code'
