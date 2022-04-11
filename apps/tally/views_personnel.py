import json
import re

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View

from tally.forms import PersonnelForm
from users.models import UserProfile
from utils.mixin_utils import LoginRequiredMixin
from utils.tools import id_split


class PersonnelView(LoginRequiredMixin, View):
    """
    人员管理
    """

    def get(self, request):
        ret = dict()
        if request.GET.get('id'):
            ret['id'] = request.GET['id']
        if request.GET.get('name'):
            ret['name'] = request.GET['name']
        if request.GET.get('gender'):
            ret['gender'] = request.GET['gender']
        if request.GET.get('department'):
            ret['department'] = request.GET['department']
        if request.GET.get('job'):
            ret['job'] = request.GET['job']

        return render(request, 'organization/personnel/personnel_index.html', ret)


class PersonnelRecordView(LoginRequiredMixin, View):
    """
    人员记录
    """
    def get(self, request):
        filters = dict()
        if 'key[ids]' in request.GET and request.GET['key[ids]']:
            filters["id__in"] = id_split(request.GET['key[ids]'])
        if 'key[name]' in request.GET and request.GET['key[name]']:
            filters['name__contains'] = request.GET['key[name]']
        if 'key[gender]' in request.GET and request.GET['key[gender]']:
            filters['gender'] = request.GET['key[gender]']
        if 'key[department]' in request.GET and request.GET['key[department]']:
            filters['department'] = request.GET['key[department]']
        if 'key[job]' in request.GET and request.GET['key[job]']:
            filters['job'] = request.GET['key[job]']
        personnel_record = UserProfile.objects.filter(**filters).order_by('-id')
        res_personnel_record = []
        for record in list(personnel_record):
            res_personnel_record.append({
                'id': record.id,
                'name': record.name,
                'gender': record.gender_choice,
                'department': record.department,
                'job': record.job,
                'computer': record.get_computer_number(),
                'monitor': record.get_monitor_number(),
                'remark': record.remark,
            })

        count = len(res_personnel_record)
        end_ele = int(request.GET["page"]) * int(request.GET["limit"])
        start_ele = end_ele - int(request.GET["limit"])
        limit_record = res_personnel_record[start_ele:end_ele]
        res = {"code": 0, "msg": "", "count": count, "data": limit_record}

        return JsonResponse(res, safe=False)


class PersonnelEditView(LoginRequiredMixin, View):
    """
    人员编辑
    """
    def post(self, request):
        res = dict()
        product = get_object_or_404(Personnel, pk=request.POST['id'])
        setattr(product, request.POST['field'], request.POST['value'])
        # noinspection PyBroadException
        try:
            product.save()
            res['status'] = 'success'
        except:
            res['status'] = 'error'

        return HttpResponse(json.dumps(res), content_type='application/json')


class PersonnelAddView(LoginRequiredMixin, View):
    """
    人员添加
    """
    def get(self, request):
        ret = dict()
        personnel = Personnel.objects.all()
        ret['personnel'] = personnel

        return render(request, 'personnel/personnel_add.html', ret)

    def post(self, request):
        res = dict()
        personnel = Personnel()
        personnel_form = PersonnelForm(request.POST, instance=personnel)
        if personnel_form.is_valid():
            personnel_form.save()
            res['status'] = 'success'
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(personnel_form.errors)
            tally_record_form_errors = re.findall(pattern, errors)
            res = {
                'status': 'fail',
                'tally_record_form_errors': tally_record_form_errors[0]
            }
        return HttpResponse(json.dumps(res), content_type='application/json')


class PersonnelUpdateView(LoginRequiredMixin, View):
    """
    人员更改
    """
    def get(self, request):
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            personnel_record = get_object_or_404(Personnel, pk=request.GET['id'])
            ret["personnel"] = Personnel.objects.all()
            ret["personnel_record"] = personnel_record
        return render(request, 'personnel/personnel_update.html', ret)

    def post(self, request):
        res = dict()
        personnel_record = get_object_or_404(Personnel, pk=request.POST['id'])
        personnel_record_form = PersonnelForm(request.POST, instance=personnel_record)
        if personnel_record_form.is_valid():
            personnel_record_form.save()
            res['status'] = 'success'
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(personnel_record_form.errors)
            tally_record_form_errors = re.findall(pattern, errors)
            res = {
                'status': 'fail',
                'tally_record_form_errors': tally_record_form_errors[0]
            }
        return HttpResponse(json.dumps(res), content_type='application/json')


class PersonnelDelView(LoginRequiredMixin, View):
    """
    人员删除
    """
    def post(self, request):
        ret = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            # id_list = map(int, request.POST.get('id').split(','))
            id_list = eval(request.POST.get('id'))
            if isinstance(id_list, int):
                id_list = [id_list]
            Personnel.objects.filter(id__in=id_list).delete()
            ret['result'] = True
        return HttpResponse(json.dumps(ret), content_type='application/json')