# -*- coding:utf-8 -*-
from api import login_api
from base.base_api import BaseApi
import settings

class LoginBaseApi(BaseApi):

    def __init__(self, login_name,password=settings.PUBLIC_PASSWORD ,*args, **kwargs):
        super(LoginBaseApi, self).__init__(*args,**kwargs)
        self.password = password
        self.login_name = login_name

    def build_base_param(self):
        base_param = super(LoginBaseApi, self).build_base_param()
        identity = login_api.LoginApi().login(self.login_name, self.password, only_get_identity=True)
        base_param['identity'] = identity
        return base_param


