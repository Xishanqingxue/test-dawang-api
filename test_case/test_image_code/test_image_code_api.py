# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.image_code_api import ImageCodeApi
from utilities.redis_helper import Redis
import settings


class TestImageCodeApi(BaseCase):
    """
    图形验证码
    """
    device_id = settings.DEVICE_ID

    def test_a_send_image_code_success(self):
        """
        获取图形验证码成功
        """
        image_code_api = ImageCodeApi()
        image_code_api.get({'device_id': self.device_id})

        image_code = Redis().get_image_captcha(self.device_id)

        self.assertIsNotNone(image_code)
        self.assertEqual(len(image_code), 4)
