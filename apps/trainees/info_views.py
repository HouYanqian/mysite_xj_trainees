import json
import re

from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View

from rbac.models import Role
from trainees.forms import TraineesInterviewForm, TraineesForm
from trainees.models import TraineesInterview, Trainees
from users.models import UserProfile
from utils.mixin_utils import LoginRequiredMixin
from utils.tools import id_split

User = get_user_model()


class TraineesInterviewView(LoginRequiredMixin, View):
    """
    储备生面试指标首页
    """

    def get(self, request):
        ret = dict()
        if request.GET.get('id'):
            ret['id'] = request.GET['id']
        if request.GET.get('name'):
            ret['name'] = request.GET['name']
        return render(request, 'info/trainees_interview/trainees_interview_index.html', ret)


class TraineesInterviewRecordView(LoginRequiredMixin, View):
    """
    储备生面试指标记录
    """

    def get(self, request):
        filters = dict()
        if 'key[ids]' in request.GET and request.GET['key[ids]']:
            filters["id__in"] = id_split(request.GET['key[ids]'])
        if 'key[name]' in request.GET and request.GET['key[name]']:
            search_users = UserProfile.objects.filter(name__contains=request.GET['key[name]'])
            filters['name__in'] = search_users
        trainees_interview_record = TraineesInterview.objects.filter(**filters).order_by('-id')
        res_trainees_interview_record = []
        for record in list(trainees_interview_record):
            try:
                record_url = record.name.image.url
            except ValueError:
                record_url = ''
            res_trainees_interview_record.append({
                'id': record.id,
                'name': record.name.name,
                'target_1': record.target_1,
                'target_2': record.target_2,
                'target_3': record.target_3,
                'target_4': record.target_4,
                'target_5': record.target_5,
                'target_6': record.target_6,
                'target_7': record.target_7,
                'target_8': record.target_8,
                'target_9': record.target_9,
                'target_10': record.target_10,
                'total': record.target_1 + record.target_2 + record.target_3 + record.target_4 + record.target_5 + record.target_6 + record.target_7 + record.target_8 + record.target_9 + record.target_10,
                'image': record_url,
            })

        count = len(res_trainees_interview_record)
        end_ele = int(request.GET["page"]) * int(request.GET["limit"])
        start_ele = end_ele - int(request.GET["limit"])
        limit_record = res_trainees_interview_record[start_ele:end_ele]
        res = {"code": 0, "msg": "", "count": count, "data": limit_record}

        return JsonResponse(res, safe=False)


class TraineesInterviewEditView(LoginRequiredMixin, View):
    """
    储备生面试指标编辑
    """

    def post(self, request):
        res = dict()
        if 'target' in request.POST['field']:
            try:
                value = int(request.POST['value'])
            except ValueError:
                res['status'] = 'error'
                return HttpResponse(json.dumps(res), content_type='application/json')
            if not 0 <= value <= 100:
                res['status'] = 'hint'
                return HttpResponse(json.dumps(res), content_type='application/json')

        record = get_object_or_404(TraineesInterview, pk=request.POST['id'])
        setattr(record, request.POST['field'], request.POST['value'])
        # noinspection PyBroadException
        try:
            record.save()
            res['status'] = 'success'
        except:
            res['status'] = 'error'

        return HttpResponse(json.dumps(res), content_type='application/json')


class TraineesInterviewGuideView(LoginRequiredMixin, View):
    """
    储备生面试指标添加
    """

    def get(self, request):
        ret = dict()
        if 'name_id' in request.GET and request.GET['name_id']:
            name_id = request.GET['name_id']
            trainees = get_object_or_404(User, pk=name_id)
            ret = {
                'name_id': name_id,
                'trainees': trainees,
            }
        return render(request, 'info/trainees_interview/trainees_interview_guide.html', ret)

    def post(self, request):
        res = dict()

        trainees_interview = TraineesInterview()
        trainees_interview_form = TraineesInterviewForm(request.POST, instance=trainees_interview)
        if trainees_interview_form.is_valid():
            trainees_interview_form.save()
            res['status'] = 'success'
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(trainees_interview_form.errors)
            form_errors = re.findall(pattern, errors)
            res = {
                'status': 'fail',
                'form_errors': form_errors[0]
            }

        return HttpResponse(json.dumps(res), content_type='application/json')


class TraineesInterviewUpdateView(LoginRequiredMixin, View):
    """
    储备生面试指标更改
    """

    def get(self, request):
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            trainees_interview_record = get_object_or_404(TraineesInterview, pk=request.GET['id'])
            ret["trainees_interview_record"] = trainees_interview_record
        return render(request, 'info/trainees_interview/trainees_interview_update.html', ret)

    def post(self, request):
        res = dict()
        trainees_interview = get_object_or_404(TraineesInterview, pk=request.POST['id'])
        trainees_interview_form = TraineesInterviewForm(request.POST, instance=trainees_interview)
        if trainees_interview_form.is_valid():
            trainees_interview_form.save()
            res['status'] = 'success'
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(trainees_interview_form.errors)
            form_errors = re.findall(pattern, errors)
            res = {
                'status': 'fail',
                'form_errors': form_errors[0]
            }
        return HttpResponse(json.dumps(res), content_type='application/json')


class TraineesInterviewDelView(LoginRequiredMixin, View):
    """
    储备生面试指标删除
    """

    def post(self, request):
        ret = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            # id_list = map(int, request.POST.get('id').split(','))
            id_list = eval(request.POST.get('id'))
            if isinstance(id_list, int):
                id_list = [id_list]
            TraineesInterview.objects.filter(id__in=id_list).delete()
            ret['result'] = True
        return HttpResponse(json.dumps(ret), content_type='application/json')


class TraineesView(LoginRequiredMixin, View):
    """
    储备生基本信息首页
    """

    def get(self, request):
        ret = dict()
        if request.GET.get('id'):
            ret['id'] = request.GET['id']
        if request.GET.get('username'):
            ret['username'] = request.GET['username']
        if request.GET.get('name'):
            ret['name'] = request.GET['name']
        return render(request, 'info/trainees/trainees_index.html', ret)


class TraineesRecordView(LoginRequiredMixin, View):
    """
    储备生基本信息记录
    """

    def get(self, request):
        filters = dict()
        if 'key[ids]' in request.GET and request.GET['key[ids]']:
            filters["id__in"] = id_split(request.GET['key[ids]'])
        if 'key[name]' in request.GET and request.GET['key[name]']:
            search_users = UserProfile.objects.filter(name__contains=request.GET['key[name]'])
            filters['name__in'] = search_users
        trainees_record = Trainees.objects.filter(**filters).order_by('-id')
        res_record = []
        for record in list(trainees_record):
            try:
                record_url = record.name.image.url
            except ValueError:
                record_url = ''
            res_record.append({
                'id': record.id,
                'name': record.name.name,
                'orientation': record.get_orientation_display(),
                'lot': record.lot,
                'entry_date': record.entry_date.strftime('%Y-%m-%d'),
                'gender': record.gender,
                'nation': record.nation,
                'age': record.age,
                'politics_status': record.politics_status,
                'height': record.height,
                'weight': record.weight,
                'school': record.school,
                'major': record.major,
                'education': record.get_education_display(),
                'phone': record.phone,
                'id_card': record.id_card[:6]+'***',
                'address': record.address,
                'education_experience': record.education_experience.strip(','),
                'family_member': record.family_member.strip(','),
                'emergency_contact': record.emergency_contact.strip(','),
                'remark': record.remark,
                'image': record_url,
            })

        count = len(res_record)
        end_ele = int(request.GET["page"]) * int(request.GET["limit"])
        start_ele = end_ele - int(request.GET["limit"])
        limit_record = res_record[start_ele:end_ele]
        res = {"code": 0, "msg": "", "count": count, "data": limit_record}

        return JsonResponse(res, safe=False)


class TraineesEditView(LoginRequiredMixin, View):
    """
    储备生基本信息编辑
    """

    def post(self, request):
        res = dict()
        record = get_object_or_404(Trainees, pk=request.POST['id'])
        setattr(record, request.POST['field'], request.POST['value'])
        # noinspection PyBroadException
        try:
            record.save()
            res['status'] = 'success'
        except:
            res['status'] = 'error'

        return HttpResponse(json.dumps(res), content_type='application/json')


class TraineesUpdateView(LoginRequiredMixin, View):
    """
    储备生基本信息更改
    """

    def get(self, request):
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            trainees_info_record = get_object_or_404(Trainees, pk=request.GET['id'])
            ret["trainees_info_record"] = trainees_info_record
        return render(request, 'info/trainees/trainees_update.html', ret)

    def post(self, request):
        res = dict()
        trainees = get_object_or_404(Trainees, pk=request.POST['id'])
        trainees_form = TraineesForm(request.POST, instance=trainees)
        if trainees_form.is_valid():
            trainees_form.save()
            res['status'] = 'success'
            user = UserProfile.objects.get(id=request.POST['name'])
            user.name = request.POST.get('rename')
            user.save()

        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(trainees_form.errors)
            form_errors = re.findall(pattern, errors)
            res = {
                'status': 'fail',
                'form_errors': form_errors[0]
            }

        return HttpResponse(json.dumps(res), content_type='application/json')


class TraineesDelView(LoginRequiredMixin, View):
    """
    储备生基本信息删除
    """

    def post(self, request):
        ret = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            # id_list = map(int, request.POST.get('id').split(','))
            id_list = eval(request.POST.get('id'))
            if isinstance(id_list, int):
                id_list = [id_list]
            Trainees.objects.filter(id__in=id_list).delete()
            ret['result'] = True
        return HttpResponse(json.dumps(ret), content_type='application/json')
