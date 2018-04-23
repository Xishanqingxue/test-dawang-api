# -*- coding:utf-8 -*-
from base.base_case import BaseCase
from api.super_visor_api import AddSuperVisorApi
from api.add_black_user_api import AddBlackUserApi
from api.noble_api import BuyNobleApi
from api.guard_api import BuyGuardApi
from api.live_api import EnterRoomApi
from utilities.mysql_helper import MysqlOperation
from utilities.redis_helper import RedisHold
import time,settings


class BlackUserAction(BaseCase):
    anchor_login_name = settings.YULE_TEST_ANCHOR_LOGIN_NAME
    anchor_id = settings.YULE_TEST_ANCHOR_ID
    high_admin_user_id = settings.YULE_TEST_USER_ID
    high_admin_user_name = settings.YULE_TEST_USER_LOGIN_NAME

    normal_admin_user_id = settings.YULE_TEST_USER_ID
    normal_admin_user_name = settings.YULE_TEST_USER_LOGIN_NAME
    room_id = settings.YULE_TEST_ROOM
    time_sleep = 0.5

    def anchor_add_black_action(self,**kwargs):
        add_super_visor = kwargs['add_super_visor']
        user_id = kwargs['user_id']
        type = kwargs['type']
        blacker_type = kwargs['blacker_type']
        is_guard = kwargs['is_guard']
        guard_id = kwargs['guard_id']
        is_noble = kwargs['is_noble']
        noble_id = kwargs['noble_id']
        user_login_name = MysqlOperation(user_id=user_id).get_user_details()['login_name']
        price = None

        if is_guard:
            if guard_id == 1:
                price = 588000
            elif guard_id == 2:
                price = 1176000
            elif guard_id == 3:
                price = 1764000
            elif guard_id == 12:
                price = 7056000
            mysql_operation = MysqlOperation(user_id=user_id)
            mysql_operation.fix_user_account(gold_num=price)
            RedisHold().clean_redis_user_detail(user_id)
            time.sleep(self.time_sleep)
            buy_guard_api = BuyGuardApi(user_login_name)
            buy_guard_api.get({'room_id': self.room_id, 'guard_id': guard_id, 'currency': 'gold'})
            self.assertEqual(buy_guard_api.get_code(), 0)
        if is_noble:
            if noble_id == 1:
                price = 24000
            elif noble_id == 2:
                price = 40000
            elif noble_id == 3:
                price = 80000
            elif noble_id == 4:
                price = 400000
            elif noble_id == 5:
                price = 800000
            elif noble_id == 6:
                price = 2400000
            elif noble_id == 7:
                price = 24000000
            mysql_operation = MysqlOperation(user_id=user_id)
            mysql_operation.fix_user_account(gold_num=price)
            RedisHold().clean_redis_user_detail(user_id)
            time.sleep(self.time_sleep)
            buy_noble_api = BuyNobleApi(user_login_name)
            buy_noble_api.get({'noble_id': noble_id, 'num': 1, 'room_id': self.room_id, 'currency': 'gold'})
            self.assertEqual(buy_noble_api.get_code(), 0)
        if add_super_visor:
            add_super_visor_api = AddSuperVisorApi(self.anchor_login_name)
            add_super_visor_api.get({'user_id': user_id, 'anchor_id': self.anchor_id, 'type': type})
            self.assertEqual(add_super_visor_api.get_code(), 0)

        add_black_user_api = AddBlackUserApi(self.anchor_login_name)
        add_black_user_api.get({'user_id': user_id, 'anchor_id': self.anchor_id,'blacker_type': blacker_type})
        if noble_id in [6,7]:
            if blacker_type == 'forbid_shout':
                self.assertEqual(add_black_user_api.get_code(), 411151)
                self.assertEqual(add_black_user_api.get_response_message(), u'权限不足，禁止喊话失败')
            elif blacker_type == 'forbid_visit':
                self.assertEqual(add_black_user_api.get_code(), 411152)
                self.assertEqual(add_black_user_api.get_response_message(), u'权限不足，踢出房间失败')
            elif blacker_type == 'forbid_speak':
                if noble_id == 7:
                    self.assertEqual(add_black_user_api.get_code(), 411150)
                    self.assertEqual(add_black_user_api.get_response_message(), u'权限不足，禁言失败')
                else:
                    self.assertEqual(add_black_user_api.get_code(), 0)
                    self.assertEqual(add_black_user_api.get_response_message(), u'操作成功')

        else:
            self.assertEqual(add_black_user_api.get_code(), 0)
            self.assertEqual(add_black_user_api.get_response_message(), u'操作成功')

        if blacker_type == 'forbid_visit':
            enter_room_api = EnterRoomApi(user_login_name)
            enter_room_api.get({'room_id': self.room_id})
            if noble_id in [6,7]:
                self.assertEqual(enter_room_api.get_code(), 0)
                self.assertEqual(enter_room_api.get_response_message(), u'操作成功')
            else:
                self.assertEqual(enter_room_api.get_code(), 402002)
                self.assertEqual(enter_room_api.get_response_message(), u'说明是禁止访问')
        else:
            if noble_id not in [6,7]:
                count = 1
                max_count = 20
                while count < max_count:
                    black_user_detail = MysqlOperation(user_id=user_id).get_black_user_details()
                    if black_user_detail == None:
                        time.sleep(self.time_sleep)
                        count += 1
                    else:
                        self.assertEqual(black_user_detail['type'], (blacker_type))
                        break
                self.assertLess(count, max_count)

    def high_admin_add_black_action(self,**kwargs):
        add_super_visor = kwargs['add_super_visor']
        user_id = kwargs['user_id']
        type = kwargs['type']
        blacker_type = kwargs['blacker_type']
        is_guard = kwargs['is_guard']
        guard_id = kwargs['guard_id']
        is_noble = kwargs['is_noble']
        noble_id = kwargs['noble_id']
        user_is_anchor = kwargs['user_is_anchor']
        user_login_name = MysqlOperation(user_id=user_id).get_user_details()['login_name']
        price = None

        add_super_visor_api = AddSuperVisorApi(self.anchor_login_name)
        add_super_visor_api.get({'user_id': self.high_admin_user_id, 'anchor_id': self.anchor_id, 'type': '60'})
        self.assertEqual(add_super_visor_api.get_code(), 0)

        if is_guard:
            if guard_id == 1:
                price = 588000
            elif guard_id == 2:
                price = 1176000
            elif guard_id == 3:
                price = 1764000
            elif guard_id == 12:
                price = 7056000
            mysql_operation = MysqlOperation(user_id=user_id)
            mysql_operation.fix_user_account(gold_num=price)
            RedisHold().clean_redis_user_detail(user_id)
            time.sleep(self.time_sleep)
            buy_guard_api = BuyGuardApi(user_login_name)
            buy_guard_api.get({'room_id': self.room_id, 'guard_id': guard_id, 'currency': 'gold'})
            self.assertEqual(buy_guard_api.get_code(), 0)
        if is_noble:
            if noble_id == 1:
                price = 24000
            elif noble_id == 2:
                price = 40000
            elif noble_id == 3:
                price = 80000
            elif noble_id == 4:
                price = 400000
            elif noble_id == 5:
                price = 800000
            elif noble_id == 6:
                price = 2400000
            elif noble_id == 7:
                price = 24000000
            mysql_operation = MysqlOperation(user_id=user_id)
            mysql_operation.fix_user_account(gold_num=price)
            RedisHold().clean_redis_user_detail(user_id)
            time.sleep(self.time_sleep)
            buy_noble_api = BuyNobleApi(user_login_name)
            buy_noble_api.get({'noble_id': noble_id, 'num': 1, 'room_id': self.room_id, 'currency': 'gold'})
            self.assertEqual(buy_noble_api.get_code(), 0)
        if add_super_visor:
            add_super_visor_api = AddSuperVisorApi(self.anchor_login_name)
            add_super_visor_api.get({'user_id': user_id, 'anchor_id': self.anchor_id, 'type':type})
            self.assertEqual(add_super_visor_api.get_code(), 0)

        def assert_forbid_type(forbid_type):
            count = 1
            max_count = 10
            while count < max_count:
                black_user_detail = MysqlOperation(user_id=user_id).get_black_user_details()
                if black_user_detail == None:
                    time.sleep(self.time_sleep)
                    count += 1
                else:
                    self.assertEqual(black_user_detail['type'], (forbid_type))
                    break
            self.assertLess(count, max_count)

        add_black_user_api = AddBlackUserApi(self.high_admin_user_name)
        add_black_user_api.get({'user_id': user_id, 'anchor_id': self.anchor_id,'blacker_type': blacker_type})
        if user_is_anchor:
            self.assertEqual(add_black_user_api.get_code(), 900012)
            self.assertEqual(add_black_user_api.get_response_message(), u'权限不足，设置失败')
        elif is_guard:
            if blacker_type == 'forbid_shout':
                self.assertEqual(add_black_user_api.get_code(), 0)
                self.assertEqual(add_black_user_api.get_response_message(), u'操作成功')
                assert_forbid_type(blacker_type)

            else:
                self.assertEqual(add_black_user_api.get_code(), 900013)
                self.assertEqual(add_black_user_api.get_response_message(), u'守护用户不能被限制拉黑和禁言')
        elif is_noble:
            if blacker_type == 'forbid_shout':
                if noble_id >= 3:
                    self.assertEqual(add_black_user_api.get_code(), 411151)
                    self.assertEqual(add_black_user_api.get_response_message(), u'权限不足，禁止喊话失败')
                else:
                    self.assertEqual(add_black_user_api.get_code(), 0)
                    self.assertEqual(add_black_user_api.get_response_message(), u'操作成功')
                    assert_forbid_type(blacker_type)
            if blacker_type == 'forbid_speak':
                if noble_id >= 5:
                    self.assertEqual(add_black_user_api.get_code(), 411150)
                    self.assertEqual(add_black_user_api.get_response_message(), u'权限不足，禁言失败')
                else:
                    self.assertEqual(add_black_user_api.get_code(), 0)
                    self.assertEqual(add_black_user_api.get_response_message(), u'操作成功')
                    assert_forbid_type(blacker_type)
            if blacker_type == 'forbid_visit':
                if noble_id >= 4:
                    self.assertEqual(add_black_user_api.get_code(), 411152)
                    self.assertEqual(add_black_user_api.get_response_message(), u'权限不足，踢出房间失败')
                else:
                    self.assertEqual(add_black_user_api.get_code(), 0)
                    self.assertEqual(add_black_user_api.get_response_message(), u'操作成功')
                    enter_room_api = EnterRoomApi(user_login_name)
                    enter_room_api.get({'room_id': self.room_id})

                    self.assertEqual(enter_room_api.get_code(), 402002)
                    self.assertEqual(enter_room_api.get_response_message(), u'说明是禁止访问')
        elif type == '60':
            self.assertEqual(add_black_user_api.get_code(), 900014)
            self.assertEqual(add_black_user_api.get_response_message(), u'目标用户管理等级较高')
        else:
            self.assertEqual(add_black_user_api.get_code(), 0)
            self.assertEqual(add_black_user_api.get_response_message(), u'操作成功')

            if blacker_type == 'forbid_visit':
                enter_room_api = EnterRoomApi(user_login_name)
                enter_room_api.get({'room_id': self.room_id})

                self.assertEqual(enter_room_api.get_code(), 402002)
                self.assertEqual(enter_room_api.get_response_message(), u'说明是禁止访问')
            else:
                assert_forbid_type(blacker_type)

    def normal_admin_add_black_action(self, **kwargs):
        add_super_visor = kwargs['add_super_visor']
        user_id = kwargs['user_id']
        type = kwargs['type']
        blacker_type = kwargs['blacker_type']
        is_guard = kwargs['is_guard']
        guard_id = kwargs['guard_id']
        is_noble = kwargs['is_noble']
        noble_id = kwargs['noble_id']
        user_is_anchor = kwargs['user_is_anchor']
        user_login_name = MysqlOperation(user_id=user_id).get_user_details()['login_name']
        price = None

        add_super_visor_api = AddSuperVisorApi(self.anchor_login_name)
        add_super_visor_api.get({'user_id': self.normal_admin_user_id, 'anchor_id': self.anchor_id, 'type': '40'})
        self.assertEqual(add_super_visor_api.get_code(), 0)

        if is_guard:
            if guard_id == 1:
                price = 588000
            elif guard_id == 2:
                price = 1176000
            elif guard_id == 3:
                price = 1764000
            elif guard_id == 12:
                price = 7056000
            mysql_operation = MysqlOperation(user_id=user_id)
            mysql_operation.fix_user_account(gold_num=price)
            RedisHold().clean_redis_user_detail(user_id)
            time.sleep(self.time_sleep)
            buy_guard_api = BuyGuardApi(user_login_name)
            buy_guard_api.get({'room_id': self.room_id, 'guard_id': guard_id, 'currency': 'gold'})
            self.assertEqual(buy_guard_api.get_code(), 0)
        if is_noble:
            if noble_id == 1:
                price = 24000
            elif noble_id == 2:
                price = 40000
            elif noble_id == 3:
                price = 80000
            elif noble_id == 4:
                price = 400000
            elif noble_id == 5:
                price = 800000
            elif noble_id == 6:
                price = 2400000
            elif noble_id == 7:
                price = 24000000
            mysql_operation = MysqlOperation(user_id=user_id)
            mysql_operation.fix_user_account(gold_num=price)
            RedisHold().clean_redis_user_detail(user_id)
            time.sleep(self.time_sleep)
            buy_noble_api = BuyNobleApi(user_login_name)
            buy_noble_api.get({'noble_id': noble_id, 'num': 1, 'room_id': self.room_id, 'currency': 'gold'})
            self.assertEqual(buy_noble_api.get_code(), 0)
        if add_super_visor:
            add_super_visor_api = AddSuperVisorApi(self.anchor_login_name)
            add_super_visor_api.get({'user_id': user_id, 'anchor_id': self.anchor_id, 'type': type})
            self.assertEqual(add_super_visor_api.get_code(), 0)

        def assert_forbid_type(forbid_type):
            count = 1
            max_count = 10
            while count < max_count:
                black_user_detail = MysqlOperation(user_id=user_id).get_black_user_details()
                if black_user_detail == None:
                    time.sleep(self.time_sleep)
                    count += 1
                else:
                    self.assertEqual(black_user_detail['type'], (forbid_type))
                    break
            self.assertLess(count, max_count)

        add_black_user_api = AddBlackUserApi(self.normal_admin_user_name)
        add_black_user_api.get({'user_id': user_id, 'anchor_id': self.anchor_id, 'blacker_type': blacker_type})
        if user_is_anchor:
            self.assertEqual(add_black_user_api.get_code(), 900012)
            self.assertEqual(add_black_user_api.get_response_message(), u'权限不足，设置失败')

        elif is_guard:
            if blacker_type == 'forbid_shout':
                self.assertEqual(add_black_user_api.get_code(), 0)
                self.assertEqual(add_black_user_api.get_response_message(), u'操作成功')
                assert_forbid_type(blacker_type)

            else:
                self.assertEqual(add_black_user_api.get_code(), 900013)
                self.assertEqual(add_black_user_api.get_response_message(), u'守护用户不能被限制拉黑和禁言')
        elif is_noble:
            if blacker_type == 'forbid_shout':
                    self.assertEqual(add_black_user_api.get_code(), 411151)
                    self.assertEqual(add_black_user_api.get_response_message(), u'权限不足，禁止喊话失败')
            if blacker_type == 'forbid_speak':
                if noble_id >= 3:
                    self.assertEqual(add_black_user_api.get_code(), 411150)
                    self.assertEqual(add_black_user_api.get_response_message(), u'权限不足，禁言失败')
                else:
                    self.assertEqual(add_black_user_api.get_code(), 0)
                    self.assertEqual(add_black_user_api.get_response_message(), u'操作成功')
                    assert_forbid_type(blacker_type)
            if blacker_type == 'forbid_visit':
                if noble_id >= 2:
                    self.assertEqual(add_black_user_api.get_code(), 411152)
                    self.assertEqual(add_black_user_api.get_response_message(), u'权限不足，踢出房间失败')
                else:
                    self.assertEqual(add_black_user_api.get_code(), 0)
                    self.assertEqual(add_black_user_api.get_response_message(), u'操作成功')
                    enter_room_api = EnterRoomApi(user_login_name)
                    enter_room_api.get({'room_id': self.room_id})

                    self.assertEqual(enter_room_api.get_code(), 402002)
                    self.assertEqual(enter_room_api.get_response_message(), u'说明是禁止访问')
        elif type in ['60','40']:
            self.assertEqual(add_black_user_api.get_code(), 900014)
            self.assertEqual(add_black_user_api.get_response_message(), u'权限不足，设置失败')
        else:
            self.assertEqual(add_black_user_api.get_code(), 0)
            self.assertEqual(add_black_user_api.get_response_message(), u'操作成功')
            if blacker_type == 'forbid_visit':
                enter_room_api = EnterRoomApi(user_login_name)
                enter_room_api.get({'room_id': self.room_id})

                self.assertEqual(enter_room_api.get_code(), 402002)
                self.assertEqual(enter_room_api.get_response_message(), u'说明是禁止访问')
            else:
                assert_forbid_type(blacker_type)

