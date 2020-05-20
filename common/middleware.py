from django.utils.deprecation import MiddlewareMixin

from common import error
from libs.http import render_json


class AuthMiddleware(MiddlewareMixin):
    '''检查用户登入状态中间件'''
    white_list = [
        '/api/user/get_vcode',
        '/api/user/submit_vcode',
    ]

    def process_request(self, request):
        # 检查当前的请求是否在白名单中
        if request.path in self.white_list:

            # 检查用户是否登入
            uid = request.session.get('uid')
            if not uid:
                return render_json(error.LOGIN_REQUIRED)
            else:
                request.uid = uid
