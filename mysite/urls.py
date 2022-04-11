"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import include
from django.views.static import serve

from mysite import settings
from rbac.views import RoleView, RoleUpdateView
from trainees.views import GuideView
from users.views import LoginView, LogoutView, ChangePwdView, UploadImgView
from trainees import views
from reckondate import views as views_reckondate

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^welcome/', views.IndexWelcomeView.as_view(), name="welcome"),
    # 用户登录
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^users/change_pwd', ChangePwdView.as_view(), name="change_pwd"),
    url(r'^users/upload_img', UploadImgView.as_view(), name="upload_img"),

    url(r'^trainees/', include('trainees.urls', namespace='trainees')),
    url(r'^attendance/', include('attendance.urls', namespace='attendance')),
    url(r'^rbac/', include('rbac.urls', namespace='rbac')),

    url(r'^pub/trainees_guide', GuideView.as_view(), name="pub-trainees_guide"),
    url(r'^test', views.TestView.as_view(), name="test"),

    url(r'^other/reckon_date/$', views_reckondate.ReckonDateView.as_view(), name="other-reckon_date"),
    url(r'^other/reckon_date/record', views_reckondate.ReckonDateRecordView.as_view(), name="other-reckon_date-record"),
    url(r'^other/reckon_date/add', views_reckondate.ReckonDateAddView.as_view(), name="other-reckon_date-add"),
    url(r'^other/reckon_date/change', views_reckondate.ReckonDateChangeView.as_view(), name="other-reckon_date-change"),
    url(r'^other/reckon_date/update', views_reckondate.ReckonDateUpdateView.as_view(), name="other-reckon_date-update"),
    url(r'^other/reckon_date/del', views_reckondate.ReckonDateDelView.as_view(), name="other-reckon_date-del"),
    url(r'^other/reckon_date/history', views_reckondate.ReckonDateHistoryView.as_view(),
        name="other-reckon_date-history"),

    url(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})

]
