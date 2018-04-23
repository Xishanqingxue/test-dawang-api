# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.guard_api import GuardProductListApi
import json

class TestGuardProductListApi(BaseCase):
    """
    守护商品列表
    """


    def test_guard_product_list(self):
        """
        测试请求守护商品列表
        :return:
        """
        guard_product_api = GuardProductListApi()
        response = guard_product_api.get()

        self.assertEqual(guard_product_api.get_code(),0)

        guards_product_list = json.loads(response.content)['result']['guards_product_list']

        guard_ids = [i['id'] for i in guards_product_list]
        self.assertEqual(guard_ids,[1,2,3,6,12,13])
        guard_name = [i['name'] for i in guards_product_list]
        guard_content = [i['content'] for i in guards_product_list]
        for name in [guard_name,guard_content]:
            self.assertEqual(name,[u'1个月守护',u'2个月守护',u'3个月守护',u'6个月守护',u'1年守护',u'2年守护'])

        guard_price = [i['price'] for i in guards_product_list]
        self.assertEqual(guard_price,[588000,1176000,1764000,3528000,7056000,14112000])

        guard_time = [i['effect_time'] for i in guards_product_list]
        self.assertEqual(guard_time,[1,2,3,6,12,24])

        order_id = [i['order_id'] for i in guards_product_list]
        self.assertEqual(order_id,[1,2,3,4,5,6])

        guard_rank = [i['guard_rank'] for i in guards_product_list]
        self.assertEqual(guard_rank,[1,2,3,3,4,4])

        send_gift_add_intimacy_ratio = [i['privilege_config']['send_gift_add_intimacy_ratio'] for i in guards_product_list]
        self.assertEqual(send_gift_add_intimacy_ratio,[1.5, 1.5, 1.5, 1.5, 2, 2])

        send_sun_add_intimacy_ratio = [i['privilege_config']['send_sun_add_intimacy_ratio'] for i in  guards_product_list]
        self.assertEqual(send_sun_add_intimacy_ratio, [1.5, 2, 2.5, 2.5, 3, 3])

        show_flag = [i['privilege_config']['show_flag'] for i in  guards_product_list]
        self.assertEqual(show_flag, [1, 1, 1, 1, 1, 1])

        chat_rgb = [i['privilege_config']['chat_rgb'] for i in  guards_product_list]
        self.assertEqual(chat_rgb, [u'#9ec0f3', u'#9ec0f3', u'#288ddb', u'#288ddb', u'#288ddb', u'#288ddb'])

        shout_rgb = [i['privilege_config']['shout_rgb'] for i in  guards_product_list]
        self.assertEqual(shout_rgb, [u'#a2c7fa', u'#a2c7fa', u'#a2c7fa', u'#a2c7fa', u'#a2c7fa', u'#a2c7fa'])
