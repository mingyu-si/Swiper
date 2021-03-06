"""swiper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from user import apis as user_api
from social import apis as social_api

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^api/user/get_vcode', user_api.get_vcode),
    url(r'^api/user/submit_vcode', user_api.submit_vcode),
    url(r'^api/user/show_profile', user_api.show_profile),
    url(r'^api/user/modify_prodile', user_api.modify_prodile),
    url(r'^api/user/upload_avator', user_api.upload_avator),
    url(r'^api/social/rcmd_user', social_api.rcmd_user),
    url(r'^api/social/like', social_api.like),
    url(r'^api/social/superlike_someone', social_api.superlike_someone),
    url(r'^api/social/dislike', social_api.dislike),
    url(r'^api/social/rewind', social_api.rewind),
]
