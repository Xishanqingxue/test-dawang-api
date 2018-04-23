# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.channel_banner import ChannelBanner
from utilities.mysql_helper import MysqlOperation
import json


class TestChannelBanner(BaseCase):
    """
    获取banner列表信息
    """
    def test_channel_banner_game(self):
        """
        测试电竞的内容
        :return:
        """
        channel_banner_api = ChannelBanner()
        response = channel_banner_api.get({"type":1})
        self.assertEqual(channel_banner_api.get_resp_code(),0)

        banner_list = json.loads(response.content)['result']['banner_list']
        self.assertEqual(banner_list['id'],u'0000000001')
        self.assertEqual(banner_list['name'], u'电竟')
        banner_content = json.loads(response.content)['result']['banner_list']['banner_content']
        id = json.loads(response.content)['result']['banner_list']['id']
        mysql_get = MysqlOperation()
        mysql_banner_content = json.loads(mysql_get.get_banner_content(id=id))
        self.assertEqual(len(banner_content),len(mysql_banner_content))
        for i in banner_content:
            if u'game_url' in i:
                self.assertIn(u'https://hall.game.dwtv.tv', i['game_url'])
                del i['game_url']

        #比较banner_content数组内字典是否相等
        for x in range(len(banner_content)):
            self.assertEqual(banner_content[x],mysql_banner_content[x])

    def test_channel_banner_yule(self):
        """
        测试秀场的内容
        :return:
        """
        channel_banner_api = ChannelBanner()
        response = channel_banner_api.get({"type": 2})
        self.assertEqual(channel_banner_api.get_resp_code(), 0)

        banner_list = json.loads(response.content)['result']['banner_list']
        self.assertEqual(banner_list['id'], u'0000000002')
        self.assertEqual(banner_list['name'], u'秀场')
        banner_content = json.loads(response.content)['result']['banner_list']['banner_content']
        id = json.loads(response.content)['result']['banner_list']['id']
        mysql_get = MysqlOperation()
        mysql_banner_content = json.loads(mysql_get.get_banner_content(id=id))
        self.assertEqual(len(banner_content), len(mysql_banner_content))
        for i in banner_content:
            if u'game_url' in i:
                self.assertIn(u'https://hall.game.dwtv.tv', i['game_url'])
                del i['game_url']

        # 比较banner_content数组内字典是否相等
        for x in range(len(banner_content)):
            self.assertEqual(banner_content[x], mysql_banner_content[x])

    def test_channel_banner_doll(self):
        """
        测试娃娃机的内容
        :return:
        """
        channel_banner_api = ChannelBanner()
        response = channel_banner_api.get({"type": 3})
        self.assertEqual(channel_banner_api.get_resp_code(), 0)

        banner_list = json.loads(response.content)['result']['banner_list']
        self.assertEqual(banner_list['id'], u'0000000003')
        self.assertEqual(banner_list['name'], u'娃娃机')
        banner_content = json.loads(response.content)['result']['banner_list']['banner_content']
        id = json.loads(response.content)['result']['banner_list']['id']
        mysql_get = MysqlOperation()
        mysql_banner_content = json.loads(mysql_get.get_banner_content(id=id))
        self.assertEqual(len(banner_content), len(mysql_banner_content))
        for i in banner_content:
            if u'game_url' in i:
                self.assertIn(u'https://hall.game.dwtv.tv', i['game_url'])
                del i['game_url']

        # 比较banner_content数组内字典是否相等
        for x in range(len(banner_content)):
            self.assertEqual(banner_content[x], mysql_banner_content[x])
