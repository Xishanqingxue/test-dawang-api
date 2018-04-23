# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.login_server_api import LoginServerApi
import json


class TestHomeLoginServer(BaseCase):
    """
    初始化
    """
    def test_login_server_api(self):
        """
        测试请求初始化接口成功
        :return:
        """
        login_server_api = LoginServerApi()
        response = login_server_api.get({'platform': 'android'})
        self.assertEqual(login_server_api.get_code(), 0)
        result = json.loads(response.content)['result']
        self.assertEqual(result['rename_cost_gold'],20000)
        self.assertEqual(result['session_id'],u'')
        self.assertEqual(result['home_url'],u'')
        self.assertEqual(result['active_url'],u'/Index/active')
        self.assertEqual(result['channel_url'],u'/Index/channel')
        self.assertEqual(result['exchange_url'],u'/Index/exchange')
        self.assertEqual(result['show_wwj_baby'],1)
        self.assertEqual(result['show_exchange_shop'],1)
        self.assertIsNotNone(result['h5_animation_url'])
        self.assertEqual(result['rank_url'],u'/h5ranklist/all')
        self.assertEqual(result['exchange_ratio'],10)

        guest_config = result['guest_config']
        self.assertEqual(guest_config['guest_sun'],10)
        self.assertEqual(guest_config['guest_chat'],10)

        share_config = result['share_config']
        self.assertEqual(share_config['share_title'],u'要想生活有意思，必须发现点乐子！')
        self.assertEqual(share_config['share_content'],u'<#####>正在大王直播，也许会有惊喜等着你~来跟我一起感受欢乐时光吧')
        self.assertEqual(share_config['share_url'],u'http://h5.t.dwtv.tv/share/live/#####')

        server_config = result['server_config']
        self.assertEqual(server_config['img_server'],u'https://pic.t.dwtv.tv/files')
        self.assertEqual(server_config['socket_domain'],u'chat.t.dwtv.tv')
        self.assertEqual(server_config['socket_port'],u'80')
        self.assertEqual(server_config['upload_header_url'],u'http://pic.t.dwtv.tv/base/uploadHeads.shtml')
        self.assertEqual(server_config['game_hall_server'],u'https://hall.game.dwtv.tv/enter/gamecenter')
        self.assertEqual(server_config['game_entry_server'],u'https://static.t.dwtv.tv/h5/gameshell/game_shell.html')

        show_advert_info = result['show_advert_info']
        self.assertIsNotNone(show_advert_info['image'])
        self.assertIsNone(show_advert_info['url'])
        self.assertEqual(show_advert_info['title'],u'shsfdhh')

        live_icon_bg_color = result['live_icon_bg_color']
        self.assertEqual(len(live_icon_bg_color),2)
        self.assertEqual(live_icon_bg_color['mobile_live']['color'],u'#a151cb')
        self.assertEqual(live_icon_bg_color['mobile_live']['name'],u'移动直播')
        self.assertEqual(live_icon_bg_color['live']['color'],u'#a151cb')
        self.assertEqual(live_icon_bg_color['live']['name'],u'直播中')

        guard_obj_list = result['guard_obj_list']
        self.assertEqual(len(guard_obj_list),6)

        noble_obj_list = result['noble_obj_list']
        self.assertEqual(len(noble_obj_list),7)

        plat_signin_gift_list = result['plat_signin_gift_list']
        self.assertEqual(len(plat_signin_gift_list),7)


