import re

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render


class RbacMiddleware(MiddlewareMixin):
    """
    检查用户URL访问权限
    """
    def process_request(self, request):
        if request.user.is_authenticated:
            request_url = request.path_info
            permission_url = list(request.user.roles.values("permissions__url").distinct())
            new_permission_url = [url["permissions__url"] for url in permission_url]
            for url in settings.SAFE_URL:
                if re.match(url, request_url):
                    return None
            if request_url in new_permission_url:
                return None
            else:
                ret = dict(url=[url for url in permission_url if url is not None])
                ret['request_url'] = request_url
                return render(request, 'page404.html', ret)
        else:
            pass
