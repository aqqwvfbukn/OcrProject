from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


"""登录验证中间件"""
class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 排除那些不需要登录就能访问的页面
        # request.path_info 获取当前用户请求的url ， /login/
        if request.path_info in ['/login_code/','/send_message/']:
            return

        # 读取当前用户的session信息，如果能读取，说明已经登录过，就可以继续向后走
        info_dict = request.session.get('info')
        if info_dict:
            return

        # 没有登录过，重新回到登录页面
        return redirect('/login_code/')



