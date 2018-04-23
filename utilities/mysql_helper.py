# -*- coding:utf-8 -*-
import base.base_mysql as base_mysql
import re
import json



class MysqlGet(object):

    def get_user_id(self,user_mobile):
        # 获取用户ID
        user_id = base_mysql.execute('select id from dw_user where login_name=%s',params=(user_mobile))
        return user_id['id']

    def get_user_details(self,user_mobile):
        # 获取用户账户信息
        user_id = self.get_user_id(user_mobile)
        details = base_mysql.execute('select * from dw_user where id=%s', params=(user_id))
        return details

    def get_user_account_details(self,user_mobile):
        user_id = self.get_user_id(user_mobile)
        details = base_mysql.execute('select * from dw_user_account where user_id=%s',params=(user_id))
        return details

    def get_sms_code(self,mobile):
        # 获取短信验证码
        code = base_mysql.execute('select code from send_sms_code where mobile=%s order by send_time desc',params=(mobile))
        return code['code']

    def get_black_user_details(self,user_mobile):
        # 获取用户黑名单信息
        user_id = self.get_user_id(user_mobile)
        details = base_mysql.execute('select * from black_user where user_id=%s order by create_time',params=(user_id))
        return details

    def get_user_report_details(self,user_id,anchor_id):
        # 获取用户举报信息
        details = base_mysql.execute('select * from report where from_user_id=%s and to_user_id=%s',params=(user_id, anchor_id))
        return details

    def get_user_update_nick_log(self,user_mobile):
        # 获取用户修改昵称日志
        user_id = self.get_user_id(user_mobile)
        details = base_mysql.execute('select * from user_nickname_log where userid=%s order by create_time desc',params=(user_id))
        return details

    def get_anchor_dynamic_ids(self,anchor_id):
        # 获取主播发布的动态id
        ids = base_mysql.execute('select id from user_dynamic where user_id=%s and status!=-1', params=(anchor_id),is_fetchone=False)
        return ids

    def get_user_dynamic_report_reason(self,user_id,anchor_id):
        # 获取用户举报动态信息
        reason = base_mysql.execute('select reason from dynamic_report where report_user_id=%s and be_reported_user_id=%s order by id desc',params=(user_id, anchor_id))
        return reason['reason']

    def get_user_package_gift(self, user_mobile,gift_id):
        # 获取用户背包礼物详情
        user_id = self.get_user_id(user_mobile)
        packet_gift = base_mysql.execute('select * from user_package where user_id=%s and tool_id=%s',params=(user_id, gift_id))
        return packet_gift

    def get_tip_details(self,anchor_id):
        # 获取直播间内公告内容
        details = base_mysql.execute('select * from tips where id=%s', params=(anchor_id))
        return details

    def get_anchor_room_supervisor_details(self,user_mobile):
        # 获取直播间内管理员列表
        user_id = self.get_user_id(user_mobile)
        details = base_mysql.execute('select * from anchor_room_supervisor where user_id=%s', params=(user_id))
        return details

    def get_gift_details(self,gift_id):
        # 获取单个礼物详情
        details = base_mysql.execute('select * from gift where id=%s', params=(gift_id))
        return details

    def get_room_details(self,room_id):
        # 获取直播间信息
        details = base_mysql.execute('select * from anchor_room where id=%s', params=(room_id))
        return details

    def get_room_share_details(self,room_id):
        # 获取直播间分享语信息
        details = base_mysql.execute('select * from anchor_room_share where room_id=%s', params=(room_id))
        return details

    def get_week_star_anchor(self,anchor_id):
        # 获取主播端收到礼物列表
        details = base_mysql.execute('select * from week_star_anchor where anchor_id=%s order by id desc', params=(anchor_id))
        return details

    def get_week_star_user(self,user_mobile):
        # 获取用户端收到礼物列表
        user_id = self.get_user_id(user_mobile)
        details = base_mysql.execute('select * from week_star_user where user_id=%s order by id desc', params=(user_id))
        return details


    def get_user_contribution_details(self, user_mobile,guard=False):
        # 获取用户贡献值详情
        user_id = self.get_user_id(user_mobile)
        if guard:
            details = base_mysql.execute('select * from user_contribution where user_id=%s and behavior=%s',params=(user_id, 'behavior_buy_guard_fruit'))
            return details
        else:
            details = base_mysql.execute('select * from user_contribution where user_id=%s order by id desc', params=(user_id))
            return details

    def get_doll_details(self,doll_id):
        # 获取娃娃商品详情
        details = base_mysql.execute('select * from doll where id=%s', params=(doll_id))
        return details

    def get_red_packet_ids(self,room_id):
        # 获取房间内所有红包id
        red_packet_ids = base_mysql.execute('select id from act_red_packet where room_id=%s',params=(room_id),is_fetchone=False)
        return red_packet_ids

    def get_diamond_product_info(self,platform):
        # 获取银币商品信息
        info = base_mysql.execute('select * from pay_diamond_info where platform=%s and status=1', params=(platform),db='live_pay', is_fetchone=False)
        return info

    def get_machine_rule(self,type_id=6):
        # 获取规则
        rule = base_mysql.execute('select * from document where type=%s', params=(type_id))
        return rule

    def get_user_dawang_roulette_stake(self,uid):
        # 获取转盘抽奖记录中大王直播记录ID
        stake_id = base_mysql.execute('select id from game_roulette_user_stake where uid=%s and type=2',params=(uid))
        return stake_id['id']

    def get_notice_details(self):
        # 获取公告
        details = base_mysql.execute('select * from notice where status=1')
        return details

    def get_banner_content(self,id):
        # 获取频道banner的列表信息
        banner_list= base_mysql.execute('select * from dw_channel_config where id=%s',params=(id))
        return banner_list['banner_content']

    def get_platform_upgrade_details(self,channel_id,pname="com.dawang.live"):
        details = base_mysql.execute('select * from platform_upgrade where channel_id=%s and pname=%s',params=(channel_id,pname))
        return details

    def get_questions(self,room_id):
        questions = base_mysql.execute('select * from jc_question_bank where room_id=%s',params=(room_id),is_fetchone=False)
        return questions

    def get_quiz_questions(self,room_id):
        quiz_questions = base_mysql.execute('select * from jc_quiz_question where room_id=%s',params=(room_id),is_fetchone=False)
        return quiz_questions

    def get_coinpusher_report(self,room_id):
        """
        获取推币机问题反馈信息
        :return:
        """
        details = base_mysql.execute('select * from coinpusher_report where room_id=%s',params=(room_id),is_fetchone=False)
        return details


class MysqlFix(MysqlGet):

    def fix_user_status(self,user_mobile,status):
        # 修改用户账户状态
        base_mysql.execute('update user set status=%s where login_name=%s',params=(status,user_mobile))
        return self

    def fix_user_password(self,user_mobile,password='eb4f76fecca2893c1036dd0779698cd9'):
        # 修改用户密码
        user_id = self.get_user_id(user_mobile)
        base_mysql.execute('update dw_user set password=%s where id=%s',params=(password,user_id))
        return self

    def fix_user_bind_mobile(self,login_name=None,mobile_phone=None,phone_confirm=0,user_id=None):
        # 修改用户绑定手机号
        base_mysql.execute('update dw_user set login_name=%s,mobilephone=%s,phone_confirm=%s where id=%s',params=(login_name,mobile_phone,phone_confirm,user_id))
        return self

    def fix_user_account(self,user_mobile,gold_num=0,diamond_num=0):
        # 修改用户账户余额
        user_id = self.get_user_id(user_mobile)
        details = base_mysql.execute('select * from dw_user_account where user_id=%s',params=(user_id))
        if details:
            base_mysql.execute('update dw_user_account set gold=%s,diamond=%s where user_id=%s', params=(gold_num, diamond_num, user_id))
        else:
            base_mysql.execute('insert into dw_user_account VALUES (NULL,%s,0,0,0,0)',params=(user_id))
            base_mysql.execute('update dw_user_account set gold=%s,diamond=%s where user_id=%s', params=(gold_num, diamond_num, user_id))
        return self

    def fix_user_rank_and_experience(self, user_mobile,user_rank=1,experience_all=0):
        # 修改用户经验值和军衔
        user_id = self.get_user_id(user_mobile)
        base_mysql.execute('update dw_user set user_rank=%s,user_experience_all=%s,user_experience=0 where id=%s',params=(user_rank, experience_all, user_id))
        return self

    def fix_anchor_group_gold(self,user_mobile,gold_num=0):
        # 修改主播团金库余额
        user_id = self.get_user_id(user_mobile)
        base_mysql.execute('update anchor_group set gold=%s where user_id=%s', params=(gold_num, user_id))
        return self

    def fix_user_nickname(self,user_mobile,nickname):
        # 修改用户昵称
        user_id = self.get_user_id(user_mobile)
        base_mysql.execute('update dw_user set nickname=%s where id=%s',params=(nickname,user_id))
        return self

    def fix_user_update_nick_num(self,user_mobile,rename_num=1):
        # 修改用户免费修改昵称次数
        user_id = self.get_user_id(user_mobile)
        base_mysql.execute('update dw_user set left_rename_num=%s where id=%s', params=(rename_num, user_id))
        return self

    def fix_user_sun_num(self,user_mobile,sun_num=0):
        # 修改用户太阳数量
        user_id = self.get_user_id(user_mobile)
        base_mysql.execute('update dw_user set sun_num=%s where id=%s', params=(sun_num,user_id))
        return self

    def fix_dynamic_comment_status(self, user_mobile,dynamic_id, status):
        # 修改动态评论状态
        user_id = self.get_user_id(user_mobile)
        base_mysql.execute('update dynamic_comment set status=%s where dynamic_id=%s and user_id=%s',params=(status, dynamic_id, user_id))

    def fix_dynamic_comment_time(self, time,comment_id):
        # 修改动态评论时间
        base_mysql.execute('update dynamic_comment set create_time=%s where id=%s', params=(time, comment_id))

    def fix_red_packet_end_time(self,red_packet_id, end_time):
        # 修改红包过期时间
        base_mysql.execute('update act_red_packet set end_time=%s where id=%s', params=(end_time, red_packet_id))

    def fix_platform_upgrade(self,strategy,platform,pname="com.dawang.live",up=True):
        #获取平台版本
        system_version = base_mysql.execute(
            "select sys_version_name from platform_upgrade where channel_id in (10180001,90010001) and pname =%s and platform=%s",
            params=(pname, platform))
        system_version = system_version['sys_version_name'][0:3]
        a = float(system_version)
        if up:
            a += 1
        else:
            a =2.4
        system_version_name = "{}.0".format(a)
        if platform == "android":
            strinfo = re.compile("\.")
            system_version_code = "1{}".format(strinfo.sub("0", system_version_name))
        else:
            strinfo = re.compile("\.")
            system_version_code = strinfo.sub("", system_version_name)
        # 修改平台更新
        base_mysql.execute('update platform_upgrade set sys_version_name=%s,sys_version_code=%s,strategy=%s where channel_id in (10180001,90010001) and pname =%s and platform=%s',
                             params=(system_version_name,system_version_code,strategy,pname,platform))
        base_mysql.execute('update platform_upgrade_strategy set sys_version_name=%s,sys_version_code=%s,strategy = %s where pname =%s and platform=%s',
                             params=(system_version_name,system_version_code,strategy,pname,platform))
        return system_version_name,int(system_version_code)


    def fix_anchor_rank_and_exp(self,anchor_id,rank=0,exp=0):
        base_mysql.execute('update dw_anchor set anchor_rank=%s,anchor_experience=0,anchor_experience_all=%s where user_id=%s',params=(rank,exp,anchor_id))
        return self




class MysqlOperation(MysqlFix):

    def clean_sms_code(self,user_mobile):
        # 清除短信验证码
        base_mysql.execute('delete from send_sms_code where mobile=%s', params=(user_mobile))
        return self

    def delete_user(self,user_mobile):
        # 删除用户账户信息
        user_id = self.get_user_id(user_mobile)
        self.clean_sms_code(user_mobile)
        base_mysql.execute('delete from dw_oauth where user_id=%s',params=(user_id))
        base_mysql.execute('delete from dw_user_account where user_id=%s',params=(user_id))
        base_mysql.execute('delete from dw_user_device where user_id=%s',params=(user_id))
        base_mysql.execute('delete from dw_user where id=%s', params=(user_id))
        return self

    def clean_black_user(self,user_mobile):
        # 清除用户黑名单信息
        user_id = self.get_user_id(user_mobile)
        base_mysql.execute('delete from black_user where user_id=%s',params=(user_id))
        return self

    def clean_user_follow(self,user_mobile):
        # 清除用户关注信息
        user_id = self.get_user_id(user_mobile)
        base_mysql.execute('delete from user_follow where from_user_id=%s',params=(user_id))
        return self

    def clean_user_intimacy_rank(self,user_mobile):
        # 清除用户与所有主播的亲密度
        user_id = self.get_user_id(user_mobile)
        base_mysql.execute('update user_intimacy_rank set day_num=0,week_num=0,month_num=0,all_num=0 where user_id=%s',params=(user_id))
        base_mysql.execute('delete from user_intimacy where user_id=%s',params=(user_id))
        return self

    def clean_user_contribution(self,user_mobile):
        # 清除用户贡献值
        user_id = self.get_user_id(user_mobile)
        base_mysql.execute('delete from user_contribution where user_id=%s', params=(user_id))
        base_mysql.execute('delete from user_contribution_rank where user_id=%s', params=(user_id))
        return self

    def clean_user_exp_log(self,user_mobile):
        # 清除用户经验记录
        user_id = self.get_user_id(user_mobile)
        base_mysql.execute('delete from user_exp_log where user_id=%s', params=(user_id))
        return self

    def clean_user_noble(self,user_mobile):
        # 清除用户贵族信息
        user_id = self.get_user_id(user_mobile)
        self.clean_user_contribution(user_mobile)
        base_mysql.execute('update dw_user set noble_rank=0,noble_expiretime=null where id=%s',params=(user_id))
        return self

    def clean_user_guard(self,user_mobile):
        # 清除用户守护信息
        user_id = self.get_user_id(user_mobile)
        base_mysql.execute('delete from user_guard where user_id=%s', params=(user_id))
        base_mysql.execute('delete from user_guard_log where user_id=%s', params=(user_id))
        self.clean_user_contribution()

    def clean_user_anchor_group(self,user_mobile):
        # 清除用户主播团信息
        user_id = self.get_user_id(user_mobile)
        base_mysql.execute('delete from anchor_group where user_id=%s', params=(user_id))
        base_mysql.execute('delete from anchor_group_anchor where user_id=%s', params=(user_id))
        base_mysql.execute('delete from anchor_group_rank where user_id=%s', params=(user_id))
        base_mysql.execute('delete from anchor_group_log where user_id=%s', params=(user_id))
        base_mysql.execute('delete from anchor_group_account_log where user_id=%s', params=(user_id))
        return self

    def clean_user_platform_sign(self,user_mobile):
        # 清除用户平台签到信息
        user_id = self.get_user_id(user_mobile)
        self.fix_user_account(user_mobile).clean_user_package_gift(user_mobile)
        base_mysql.execute('delete from plat_signin_log where user_id=%s', params=(user_id))

    def clean_user_report(self,user_mobile):
        # 清除用户举报信息
        user_id = self.get_user_id(user_mobile)
        base_mysql.execute('delete from report where from_user_id=%s', params=(user_id))

    def clean_user_visit_history(self,user_mobile):
        # 清除用户观看历史
        user_id = self.get_user_id(user_mobile)
        base_mysql.execute('delete from user_room_visit_record where user_id=%s', params=(user_id))

    def clean_user_task(self,user_mobile):
        # 清除用户任务信息
        user_id = self.get_user_id(user_mobile)
        base_mysql.execute('delete from user_daily_task where user_id=%s', params=(user_id))
        self.fix_user_rank_and_experience()
        return self

    def clean_exchange_log(self,user_mobile):
        # 清除用户银币兑换记录
        user_id = self.get_user_id(user_mobile)
        base_mysql.execute('delete from exchange_log where user_id=%s', params=(user_id))

    def clean_doll_log(self,user_mobile):
        # 清除用户玩娃娃机日志
        user_id = self.get_user_id(user_mobile)
        base_mysql.execute('delete from play_doll_machine_log where user_id=%s', params=(user_id))
        base_mysql.execute('delete from doll_order where user_id=%s',params=(user_id))

    def add_user_package_gift(self, user_mobile,gift_id, gift_num):
        # 添加用户背包礼物
        user_id = self.get_user_id(user_mobile)
        base_mysql.execute('insert into user_package values (NULL,%s,"gift",%s,%s)', params=(user_id, gift_id, gift_num))

    def clean_user_package_gift(self,user_mobile):
        # 清除用户背包礼物
        user_id = self.get_user_id(user_mobile)
        base_mysql.execute('update user_package set tool_num=0 where user_id=%s', params=user_id)
        return self

    def clean_dynamic_comment(self,dynamic_id):
        # 清除用户动态评论
        base_mysql.execute('delete from dynamic_comment where dynamic_id=%s', params=(dynamic_id))
        return self

    def add_new_comment(self,user_mobile, comment, dynamic_id):
        # 添加动态评论
        user_id = self.get_user_id(user_mobile)
        base_mysql.execute('insert into dynamic_comment values (NULL,%s,%s,%s,NULL,1,1,%s,NULL,NULL,NULL)',params=(dynamic_id, user_id, comment, int(time.time())))

    def clean_room_hot_num(self,room_id):
        # 清除房间热度
        base_mysql.execute('update anchor_room set curr_hot_num=0 where id=%s',params=(room_id))
        return self

    def clean_anchor_room_supervisor(self,anchor_id):
        # 删除直播间内管理
        base_mysql.execute('delete from anchor_room_supervisor where anchor_id=%s',params=(anchor_id))

    def clean_send_gift(self,user_mobile,anchor_id):
        # 清除用户送礼物信息
        user_id = self.get_user_id(user_mobile)
        self.clean_user_contribution(user_mobile)
        base_mysql.execute('delete from week_star_anchor where anchor_id=%s', params=(anchor_id))
        base_mysql.execute('delete from week_star_user where user_id=%s', params=(user_id))
        return self

    def clean_red_packet(self,room_id):
        # 清除红包相关信息
        base_mysql.execute('delete from act_red_packet where room_id=%s',params=(room_id))
        base_mysql.execute('delete from act_red_packet_log where room_id=%s',params=(room_id))

    def clean_room_rank_list(self,room_id):
        # 清除房间内排行榜
        base_mysql.execute('delete from user_contribution_rank where room_id=%s',params=room_id)

    def add_new_doll_log(self,user_mobile,room_id ,start_time, end_time, log_id=8888):
        # 添加一条抓娃娃记录
        user_id = self.get_user_id(user_mobile)
        sql = 'insert into play_doll_machine_log VALUES (%s,%s,2,%s,2,%s,%s,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL)'
        base_mysql.execute(sql, params=(log_id, user_id, room_id, end_time, start_time))

    def doll_fake_consignment(self,doll_id, post_company, post_id):
        # 修改娃娃记录状态
        base_mysql.execute('update play_doll_machine_log set status=4,post_company=%s,post_id=%s where id=%s',params=(post_company, post_id, doll_id))
        base_mysql.execute('update doll_order set status=2,post_company=%s,post_id=%s where doll_log_id_json=%s',params=(post_company, post_id, json.dumps([doll_id])))

    def clean_user_account_log(self,user_mobile):
        # 清除用户消费记录
        user_id = self.get_user_id(user_mobile)
        base_mysql.execute('delete from dw_gold_consumption_log where user_id=%s', params=(user_id))
        base_mysql.execute('delete from dw_recharge_log where user_id=%s', params=(user_id))
        return self

    def clean_user_roulette_stake(self,uid):
        # 清除用户转盘抽奖记录
        base_mysql.execute('delete from game_roulette_user_stake where uid=%s',params=(uid))

    def clean_platform_upgrade(self,sys_version_name):
        base_mysql.execute('delete from platform_upgrade_strategy where sys_version_name=%s and pname="com.dawang.live"',params=(sys_version_name))


    def clean_questions(self,room_id):
        base_mysql.execute('delete from jc_question_bank where room_id=%s',params=(room_id))
        base_mysql.execute('delete from jc_quiz_question where room_id=%s',params=(room_id))

    def clean_coinpusher_report(self,room_id):
        base_mysql.execute('delete from coinpusher_report where room_id=%s',params=(room_id))

    def clean_room_sun(self,room_id):
        # 清除房间所获得的太阳数量
        base_mysql.execute('update anchor_room set sun_num=0 where id=%s',params=(room_id))
        return self
