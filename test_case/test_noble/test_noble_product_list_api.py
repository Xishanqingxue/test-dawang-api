# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.noble_api import NobleListApi
import json


class TestNobleListApi(BaseCase):
    """
    贵族商品列表
    """
    continue_diamond_num = [24000, 40000, 80000, 400000, 800000, 2400000, 24000000]
    recharge_diamond_num = [9000, 15000, 30000, 150000, 300000, 900000, 9000000]
    noble_price = [30000, 50000, 100000, 500000, 1000000, 3000000, 30000000]
    show_flag = 1
    shout_font = [u'蓝色',u'蓝色',u'蓝色',u'橘色',u'橘色',u'橘色',u'紫色']
    noble_name = [u'骑士',u'男爵',u'子爵',u'伯爵',u'侯爵',u'公爵',u'帝王']
    sun_recovery_multiple = [0, 0, 0, 0, 1, 1, 1]
    sign_reward_ratio = [2, 2, 2, 3, 3, 3, 3]
    task_reward_ratio = [0, 2, 2, 2, 3, 3, 3]
    private_chat = [0, 0, 0, 1, 1, 1, 1]
    anti_tickout_from_room = [40, 60, 60, 88, 88, 99, 99]
    anti_forbid_speak_in_room = [40, 40, 60, 60, 88, 88, 99]
    anti_forbid_speak_to_all = [60, 60, 88, 88, 88, 99, 99]

    def test_noble_product_list_api(self):
        """
        测试请求贵族商品列表
        :return:
        """
        noble_list_api = NobleListApi()
        response = noble_list_api.get()
        self.assertEqual(noble_list_api.get_code(),0)
        self.assertEqual(noble_list_api.get_response_message(),u'操作成功')
        noble_list = json.loads(response.content)['result']['noble_list']
        self.assertEqual(len(noble_list),7)

        # 校验贵族钻石价格
        continue_diamond_num = []
        for i in noble_list:
            a = i['continue_recharge_reward_config']
            continue_diamond_num.append(a[0]['num'])
        self.assertEqual(self.continue_diamond_num,continue_diamond_num)

        recharge_diamond_num = []
        for i in noble_list:
            a = i['recharge_reward_config']
            recharge_diamond_num.append(a[0]['num'])
        self.assertEqual(self.recharge_diamond_num,recharge_diamond_num)

        # 校验贵族名称
        noble_name = [i['name'] for i in noble_list]
        self.assertEqual(noble_name,self.noble_name)

        # 校验贵族金币价格
        noble_price = [i['price'] for i in noble_list]
        self.assertEqual(noble_price, self.noble_price)

        open_discout = []
        for i in noble_list:
            open_discout.append(i['open_discout'])

        for i in open_discout:
            self.assertEqual(i,u'0.8')

        renew_discout = []
        for i in noble_list:
            renew_discout.append(i['renew_discout'])

        for i in renew_discout:
            self.assertEqual(i,u'0.6')

        # 校验所有贵族是否显示贵族图标
        noble_is_show_flag = []
        for i in noble_list:
            privilege_config = i['privilege_config']
            noble_is_show_flag.append(privilege_config['show_flag'])
        for flag in noble_is_show_flag:
            self.assertEqual(flag,1)

        # 校验贵族喊话颜色
        noble_shout_font = []
        for i in noble_list:
            privilege_config = i['privilege_config']
            noble_shout_font.append(privilege_config['shout_font'])
        self.assertEqual(self.shout_font,noble_shout_font)

        # 校验贵族太阳恢复倍数
        sun_recovery_multiple = []
        for i in noble_list:
            privilege_config = i['privilege_config']
            sun_recovery_multiple.append(privilege_config['sun_recovery_multiple'])
        self.assertEqual(self.sun_recovery_multiple,sun_recovery_multiple)

        # 校验贵族签到奖励倍率
        sign_reward_ratio = []
        for i in noble_list:
            privilege_config = i['privilege_config']
            sign_reward_ratio.append(privilege_config['sign_reward_ratio'])
        self.assertEqual(self.sign_reward_ratio, sign_reward_ratio)

        # 校验贵族任务奖励倍率
        task_reward_ratio = []
        for i in noble_list:
            privilege_config = i['privilege_config']
            task_reward_ratio.append(privilege_config['task_reward_ratio'])
        self.assertEqual(self.task_reward_ratio, task_reward_ratio)

        # 校验贵族是否可以私聊
        private_chat = []
        for i in noble_list:
            privilege_config = i['privilege_config']
            private_chat.append(privilege_config['private_chat'])
        self.assertEqual(self.private_chat, private_chat)

        anti_tickout_from_room = []
        for i in noble_list:
            privilege_config = i['privilege_config']
            anti_tickout_from_room.append(privilege_config['anti_tickout_from_room'])
        self.assertEqual(self.anti_tickout_from_room, anti_tickout_from_room)

        anti_forbid_speak_in_room = []
        for i in noble_list:
            privilege_config = i['privilege_config']
            anti_forbid_speak_in_room.append(privilege_config['anti_forbid_speak_in_room'])
        self.assertEqual(self.anti_forbid_speak_in_room, anti_forbid_speak_in_room)

        anti_forbid_speak_to_all = []
        for i in noble_list:
            privilege_config = i['privilege_config']
            anti_forbid_speak_to_all.append(privilege_config['anti_forbid_speak_to_all'])
        self.assertEqual(self.anti_forbid_speak_to_all, anti_forbid_speak_to_all)
