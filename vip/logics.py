from common import error
from user.models import User


def per_require(per_name):
    def wrapper1(view_func):
        def wrapper2(request, *args, **kwargs):
            user = User.objects.get(id=request.uid)

            # 检查用户的 VIP 是否具有某权限
            if user.vip.has_per(per_name):
                response = view_func(request, *args, **kwargs)
            else:
                raise error.PerRequired

        return wrapper2

    return wrapper1
