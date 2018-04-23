# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi


class AddAnchorToGroupApi(LoginBaseApi):
    """
    添加主播到主播团
    """
    url = '/anchorgroup/addanchortogroup'

    def build_custom_param(self, data):
        return {'anchor_id': data['anchor_id'], 'position': data['position'], 'grab_flag': data['grab_flag'],
                'change_flag': data['change_flag']}


class AnchorGroupWithdrawApi(LoginBaseApi):
    """
    主播团提现
    """
    url = '/anchorgroup/withdraw'


class ListCanBeAddApi(LoginBaseApi):
    """
    可加入主播团的主播列表
    """
    url = '/anchorgroup/listcanbeadd'


class MyAnchorGroupApi(LoginBaseApi):
    """
    获取主播团信息
    """
    url = '/anchorgroup/myanchorgroup'


class MyAnchorGroupListApi(LoginBaseApi):
    """
    我得主播团列表
    """
    url = '/anchorgroup/myanchorgrouplist'


class MyAnchorGroupLogsApi(LoginBaseApi):
    """
    我得主播团日志列表
    """
    url = '/anchorgroup/myanchorgrouplogs'


class OpenAnchorGroupApi(LoginBaseApi):
    """
    开通主播团
    """
    url = '/anchorgroup/opengroup'