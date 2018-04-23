# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi

class GetCommentListApi(LoginBaseApi):
    """
    获取评论列表
    """
    url = '/social/commentList'

    def build_custom_param(self, data):
        return {'dynamic_id':data['dynamic_id']}


class GetDynamicDetailApi(LoginBaseApi):
    """
    获取动态详情
    """
    url = '/social/getDynamicDetail'

    def build_custom_param(self, data):
        return {'dynamic_id':data['dynamic_id']}


class GetHomePageDynamicApi(LoginBaseApi):
    """
    个人主页
    """
    url = '/social/getHomepageDynamicList'

    def build_custom_param(self, data):
        return {'anchor_id':data['anchor_id']}


class GetSquareDynamicApi(LoginBaseApi):
    """
    获取广场动态列表
    """
    url = '/social/getSquareDynamic'

    def build_custom_param(self, data):
        return {}


class LittleRedDotApi(LoginBaseApi):
    """
    动态小红点
    """
    url = '/social/littleRedDot'

    def build_custom_param(self, data):
        return {'local_dynamic_id':data['local_dynamic_id']}


class PublishCommentApi(LoginBaseApi):
    """
    发表评论
    """
    url = '/social/publishComment'

    def build_custom_param(self, data):
        return {'dynamic_id': data['dynamic_id'], 'comment': data['comment'], 'reply_user_id': data['reply_user_id'],
                'type': data['type']}


class PublishDynamicApi(LoginBaseApi):
    """
    发布动态
    """
    url = '/social/publishDynamic'

    def build_custom_param(self, data):
        return {'type': data['type'], 'image_urls': data['image_urls'], 'video_url': data['video_url'],
                'content': data['content'],'first_frame':data['first_frame']}


class RemoveCommentApi(LoginBaseApi):
    """
    删除评论
    """
    url = '/social/removeComment'

    def build_custom_param(self, data):
        return {'comment_id':data['comment_id']}


class RemoveDynamicApi(LoginBaseApi):
    """
    删除动态
    """
    url = '/social/removeDynamic'

    def build_custom_param(self, data):
        return {'dynamic_id':data['dynamic_id']}


class DynamicReportApi(LoginBaseApi):
    """
    举报动态
    """
    url = '/social/dynamicReport'

    def build_custom_param(self, data):
        return {'dynamic_id':data['dynamic_id'],'reason':data['reason']}


class UpvoteApi(LoginBaseApi):
    """
    点赞
    """
    url = '/social/upvote'

    def build_custom_param(self, data):
        return {'dynamic_id':data['dynamic_id']}