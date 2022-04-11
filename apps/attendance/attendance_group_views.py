import datetime
import json
import re

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View

from users.models import UserProfile
from utils.date_calculate import shift_strptime
from .forms import AttendanceGroupForm
from .models import AttendanceGroup
from utils.mixin_utils import LoginRequiredMixin
from utils.tools import id_split


class AttendanceGroupView(LoginRequiredMixin, View):
    """
    考勤组首页
    """
    def get(self, request):
        ret = dict()
        if request.GET.get('id'):
            ret['id'] = request.GET['id']
        if request.GET.get('title'):
            ret['title'] = request.GET['title']
        return render(request, 'attendance/attendance_group/attendance_group_index.html', ret)


class AttendanceGroupRecordView(LoginRequiredMixin, View):
    """
    考勤组管理记录
    """
    def get(self, request):
        filters = dict()
        if 'key[ids]' in request.GET and request.GET['key[ids]']:
            filters["id__in"] = id_split(request.GET['key[ids]'])
        if 'key[title]' in request.GET and request.GET['key[title]']:
            filters['title__contains'] = request.GET['key[title]']
        attendance_group_record = AttendanceGroup.objects.filter(**filters).order_by('-id')
        res_attendance_group_record = []
        for record in list(attendance_group_record):
            personnel_count = 0
            if record.personnel.all():
                personnel_count = record.personnel.all().count()

            res_attendance_group_record.append({
                'id': record.id,
                'title': record.title,
                'personnel': personnel_count,
                'shift': record.shift,
            })

        count = len(res_attendance_group_record)
        end_ele = int(request.GET["page"]) * int(request.GET["limit"])
        start_ele = end_ele - int(request.GET["limit"])
        limit_record = res_attendance_group_record[start_ele:end_ele]
        res = {"code": 0, "msg": "", "count": count, "data": limit_record}

        return JsonResponse(res, safe=False)


class AttendanceGroupEditView(LoginRequiredMixin, View):
    """
    考勤组管理编辑
    """
    def post(self, request):
        res = dict()
        record = get_object_or_404(AttendanceGroup, pk=request.POST['id'])
        setattr(record, request.POST['field'], request.POST['value'])
        try:
            record.save()
            res['status'] = 'success'
        except:
            res['status'] = 'error'

        return HttpResponse(json.dumps(res), content_type='application/json')


class AttendanceGroupAddView(LoginRequiredMixin, View):
    """
    考勤组管理添加
    """
    def get(self, request):
        trainees_personnel_record = UserProfile.objects.filter(roles__title="储备生")
        personnel_data = []
        for record in list(trainees_personnel_record):
            personnel_data.append({
                'value': record.id,
                'title': record.name,
            })

        return render(request, 'attendance/attendance_group/attendance_group_add.html', {
            'personnel_data': personnel_data
        })

    def post(self, request):
        res = dict()
        attendance_group = AttendanceGroup()
        # 获取两个排班
        get_post_shift1 = request.POST.get('shift1')
        get_post_shift2 = request.POST.get('shift2')
        # 时间有效判定
        if get_post_shift1:
            start_time1, end_time1 = shift_strptime(get_post_shift1)
            if start_time1 >= end_time1:
                res = {
                    'status': 'fail',
                    'form_errors': '"班次1"上班时间需小于下班时间'
                }
                return HttpResponse(json.dumps(res), content_type='application/json')
            if get_post_shift2:
                start_time2, end_time2 = get_post_shift1.split(' - ')
                if start_time2 <= end_time1:
                    res = {
                        'status': 'fail',
                        'form_errors': '"班次2"上班时间需大于"班次1"下班时间'
                    }
                    return HttpResponse(json.dumps(res), content_type='application/json')
                elif start_time2 >= end_time2:
                    res = {
                        'status': 'fail',
                        'form_errors': '"班次2"上班时间需小于下班时间'
                    }
                    return HttpResponse(json.dumps(res), content_type='application/json')
                get_post_shift1 = ", ".join((get_post_shift1,  get_post_shift2))
            attendance_group.shift = get_post_shift1
        form = AttendanceGroupForm(request.POST, instance=attendance_group)
        if form.is_valid():
            form.save()

            get_post_personnel = request.POST.get('personnel')
            if get_post_personnel:
                personnel_ids = eval(get_post_personnel)
                # 清楚人员所在其他考勤组
                for search_attendance_group in AttendanceGroup.objects.all():
                    search_attendance_group.personnel.remove(*personnel_ids)
                attendance_group.personnel.add(*personnel_ids)

            res['status'] = 'success'
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(form.errors)
            form_errors = re.findall(pattern, errors)
            res = {
                'status': 'fail',
                'form_errors': form_errors[0]
            }

        return HttpResponse(json.dumps(res), content_type='application/json')


class AttendanceGroupUpdateView(LoginRequiredMixin, View):
    """
    考勤组管理更改
    """
    def get(self, request):
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            attendance_group_record = get_object_or_404(AttendanceGroup, pk=request.GET['id'])
            ret["attendance_group_record"] = attendance_group_record

            ret['shift'] = attendance_group_record.shift.split(', ')

            trainees_personnel_record = UserProfile.objects.filter(roles__title="储备生")
            personnel_data = []
            for record in list(trainees_personnel_record):
                personnel_data.append({
                    'value': record.id,
                    'title': record.name,
                })
            ret['personnel_data'] = personnel_data
            # 已加入考勤组的名单
            record_personnel_data = [value['id'] for value in attendance_group_record.personnel.all().values('id')]
            ret['record_personnel_data'] = record_personnel_data
            get_only = request.GET.get('only')
            if get_only:
                ret['get_only'] = get_only

        return render(request, 'attendance/attendance_group/attendance_group_update.html', ret)

    def post(self, request):
        res = dict()

        attendance_group = get_object_or_404(AttendanceGroup, pk=request.POST['id'])
        # 获取两个排班
        get_post_shift1 = request.POST.get('shift1')
        get_post_shift2 = request.POST.get('shift2')
        # 时间有效判定
        if get_post_shift1:
            start_time1, end_time1 = shift_strptime(get_post_shift1)
            if start_time1 >= end_time1:
                res = {
                    'status': 'fail',
                    'form_errors': '"班次1"下班时间需大于上班时间'
                }
                return HttpResponse(json.dumps(res), content_type='application/json')
            if get_post_shift2:
                start_time2, end_time2 = shift_strptime(get_post_shift2)
                if start_time2 <= end_time1:
                    res = {
                        'status': 'fail',
                        'form_errors': '"班次2"上班时间需大于"班次1"下班时间'
                    }
                    return HttpResponse(json.dumps(res), content_type='application/json')
                elif start_time2 >= end_time2:
                    res = {
                        'status': 'fail',
                        'form_errors': '"班次2"下班时间需大于上班时间'
                    }
                    return HttpResponse(json.dumps(res), content_type='application/json')
                get_post_shift1 = ", ".join((get_post_shift1, get_post_shift2))
            attendance_group.shift = get_post_shift1

        form = AttendanceGroupForm(request.POST, instance=attendance_group)
        if form.is_valid():
            form.save()

            get_post_personnel = request.POST.get('personnel')
            if get_post_personnel:
                personnel_ids = eval(get_post_personnel)
                # 清楚人员所在其他考勤组
                for search_attendance_group in AttendanceGroup.objects.all():
                    search_attendance_group.personnel.remove(*personnel_ids)
                attendance_group.personnel.set(personnel_ids)
            else:
                attendance_group.personnel.clear()

            res['status'] = 'success'

        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(form.errors)
            form_errors = re.findall(pattern, errors)
            res = {
                'status': 'fail',
                'form_errors': form_errors[0]
            }

        return HttpResponse(json.dumps(res), content_type='application/json')


class AttendanceGroupDelView(LoginRequiredMixin, View):
    """
    考勤组管理删除
    """
    def post(self, request):
        ret = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            id_list = eval(request.POST.get('id'))
            if isinstance(id_list, int):
                id_list = [id_list]
            AttendanceGroup.objects.filter(id__in=id_list).delete()
            ret['result'] = True
        return HttpResponse(json.dumps(ret), content_type='application/json')