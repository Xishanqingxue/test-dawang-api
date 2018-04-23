# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.red_package_api import RedPacketConfigApi
import settings,json

class TestGetRedPackageConfigApi(BaseCase):
    """
    红包商品列表
    """
    user_mobile = settings.YULE_TEST_USER_LOGIN_NAME
    anchor_id = settings.YULE_TEST_ANCHOR_ID
    time_sleep = 0.2

    def test_get_red_package_config(self):
        red_packet_config_api = RedPacketConfigApi(self.user_mobile)
        response = red_packet_config_api.get()

        self.assertEqual(red_packet_config_api.get_code(),0)
        redpacket_config = json.loads(response.content)['result']['redpacket_config']
        for i in redpacket_config:
            self.assertEqual(i['num'],[50,100,200])

        red_packet_gold = []
        for i in redpacket_config:
            red_packet_gold.append(i['gold'])
        self.assertEqual(red_packet_gold,[50000,100000,588000])

        type_list = []
        for i in redpacket_config:
            type_list.append(i['type'])
        self.assertEqual(type_list,[1,2,3])

        name = []
        for i in redpacket_config:
            name.append(i['name'])
        self.assertEqual(name,[u'福利包',u'土豪包',u'至尊包'])