# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi
import settings


class DoshareTaskApi(LoginBaseApi):
    """
    完成分享任务
    """
    url = '/task/dosharetask'



class GetTaskRewardApi(LoginBaseApi):
    """
    获取任务奖励
    """
    url = '/task/gettaskreward'

    def build_custom_param(self, data):
        return {'behavior':data['behavior']}
    

class TaskListApi(LoginBaseApi):
    """
    获取任务列表
    """
    url = '/task/tasklist'
    
    
class TaskNoticeApi(LoginBaseApi):
    """
    任务红点显示
    """
    url = '/task/tasknotice'