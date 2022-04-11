from django.conf.urls import url

from attendance import attendance_group_views, attendance_record_views

app_name = '[attendance]'

urlpatterns = [
    # 考勤组管理
    url(r'^attendance_group/$', attendance_group_views.AttendanceGroupView.as_view(), name="attendance_group-index"),
    url(r'^attendance_group/record', attendance_group_views.AttendanceGroupRecordView.as_view(),
        name="attendance_group-record"),
    url(r'^attendance_group/edit', attendance_group_views.AttendanceGroupEditView.as_view(),
        name="attendance_group-edit"),
    url(r'^attendance_group/add', attendance_group_views.AttendanceGroupAddView.as_view(), name="attendance_group-add"),
    url(r'^attendance_group/update', attendance_group_views.AttendanceGroupUpdateView.as_view(),
        name="attendance_group-update"),
    url(r'^attendance_group/del', attendance_group_views.AttendanceGroupDelView.as_view(), name="attendance_group-del"),

    # 考勤记录
    url(r'^attendance_record/add', attendance_record_views.AttendanceRecordAddView.as_view(), name="attendance_record-add"),
]
