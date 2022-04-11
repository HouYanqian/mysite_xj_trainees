from django.conf.urls import url

from trainees import organiztion_views
from trainees import info_views
from trainees.views import GuideView

app_name = '[trainees]'

urlpatterns = [
    # 人员管理
    url(r'^organization/personnel/$', organiztion_views.PersonnelView.as_view(), name="organization-personnel-index"),
    url(r'^organization/personnel/record', organiztion_views.PersonnelRecordView.as_view(), name="organization-personnel-record"),
    url(r'^organization/personnel/edit', organiztion_views.PersonnelEditView.as_view(), name="organization-personnel-edit"),
    url(r'^organization/personnel/add', organiztion_views.PersonnelAddView.as_view(), name="organization-personnel-add"),
    url(r'^organization/personnel/update', organiztion_views.PersonnelUpdateView.as_view(), name="organization-personnel-update"),
    url(r'^organization/personnel/del', organiztion_views.PersonnelDelView.as_view(), name="organization-personnel-del"),

    # 面试指标
    url(r'^info/interview/$', info_views.TraineesInterviewView.as_view(), name="info-interview-index"),
    url(r'^info/interview/record', info_views.TraineesInterviewRecordView.as_view(), name="info-interview-record"),
    url(r'^info/interview/edit', info_views.TraineesInterviewEditView.as_view(), name="info-interview-edit"),
    url(r'^info/interview/guide', info_views.TraineesInterviewGuideView.as_view(), name="info-interview-guide"),
    url(r'^info/interview/update', info_views.TraineesInterviewUpdateView.as_view(), name="info-interview-update"),
    url(r'^info/interview/del', info_views.TraineesInterviewDelView.as_view(), name="info-interview-del"),

    # 基本信息
    url(r'^info/info/$', info_views.TraineesView.as_view(), name="info-info-index"),
    url(r'^info/info/record', info_views.TraineesRecordView.as_view(), name="info-info-record"),
    url(r'^info/info/edit', info_views.TraineesEditView.as_view(), name="info-info-edit"),
    url(r'^info/info/update', info_views.TraineesUpdateView.as_view(), name="info-info-update"),
    url(r'^info/info/del', info_views.TraineesDelView.as_view(), name="info-info-del"),
]
