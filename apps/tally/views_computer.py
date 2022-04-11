import json
import re

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View

from tally.forms import ComputerForm
from tally.models import Computer, Personnel
from utils.mixin_utils import LoginRequiredMixin
from utils.tools import id_split


class ComputerView(LoginRequiredMixin, View):
    """
    主机管理
    """

    def get(self, request):
        ret = dict()
        if request.GET.get('id'):
            ret['id'] = request.GET['id']
        if request.GET.get('number'):
            ret['number'] = request.GET['number']
        if request.GET.get('cpu'):
            ret['cpu'] = request.GET['cpu']
        if request.GET.get('gpu'):
            ret['gpu'] = request.GET['gpu']
        if request.GET.get('ram'):
            ret['ram'] = request.GET['ram']
        if request.GET.get('hdd'):
            ret['hdd'] = request.GET['hdd']
        if request.GET.get('date'):
            ret['date'] = request.GET['date']
        if request.GET.get('personnel'):
            ret['personnel'] = request.GET['personnel']

        return render(request, 'computer/computer_index.html', ret)


class ComputerRecordView(LoginRequiredMixin, View):
    """
    主机记录
    """
    def get(self, request):
        filters = dict()
        if 'key[ids]' in request.GET and request.GET['key[ids]']:
            filters["id__in"] = id_split(request.GET['key[ids]'])
        if 'key[number]' in request.GET and request.GET['key[number]']:
            filters['number__contains'] = request.GET['key[number]']
        if 'key[cpu]' in request.GET and request.GET['key[cpu]']:
            filters['cpu__contains'] = request.GET['key[cpu]']
        if 'key[gpu]' in request.GET and request.GET['key[gpu]']:
            filters['gpu__contains'] = request.GET['key[gpu]']
        if 'key[ram]' in request.GET and request.GET['key[ram]']:
            filters['ram__contains'] = request.GET['key[ram]']
        if 'key[hdd]' in request.GET and request.GET['key[hdd]']:
            filters['memory__hdd'] = request.GET['key[hdd]']
        if 'key[date_range]' in request.GET and request.GET['key[date_range]']:
            try:
                filters["purchase_date__gte"], filters["purchase_date__lte"] \
                    = request.GET['key[date_range]'].split(" - ")
            except ValueError:
                print("输入日期格式不正确")
        if 'key[personnel]' in request.GET and request.GET['key[personnel]']:
            if request.GET['key[personnel]'] == '*':
                filters['personnel__isnull'] = False
            elif request.GET['key[personnel]'] == '-':
                filters['personnel__isnull'] = True
            else:
                filters['personnel__name__contains'] = request.GET['key[personnel]']
        computer_record = Computer.objects.filter(**filters).order_by('-id')
        res_computer_record = []
        for record in list(computer_record):
            if record.personnel:
                personnel = record.personnel.name
            else:
                personnel = ''
            res_computer_record.append({
                'id': record.id,
                'number': record.number,
                'cpu': record.cpu,
                'gpu': record.gpu,
                'ram': record.ram,
                'hdd': record.hdd,
                'price': record.price,
                'purchase_date': record.purchase_date,
                'personnel': personnel,
                'remark': record.remark,
            })

        count = len(res_computer_record)
        end_ele = int(request.GET["page"]) * int(request.GET["limit"])
        start_ele = end_ele - int(request.GET["limit"])
        limit_record = res_computer_record[start_ele:end_ele]
        res = {"code": 0, "msg": "", "count": count, "data": limit_record}

        return JsonResponse(res, safe=False)


class ComputerEditView(LoginRequiredMixin, View):
    """
    主机编辑
    """
    def post(self, request):
        res = dict()
        product = get_object_or_404(Computer, pk=request.POST['id'])
        setattr(product, request.POST['field'], request.POST['value'])
        # noinspection PyBroadException
        try:
            product.save()
            res['status'] = 'success'
        except:
            res['status'] = 'error'

        return HttpResponse(json.dumps(res), content_type='application/json')


class ComputerAddView(LoginRequiredMixin, View):
    """
    主机添加
    """
    def get(self, request):
        ret = dict()
        personnel = Personnel.objects.all()
        ret['personnel'] = personnel

        return render(request, 'computer/computer_add.html', ret)

    def post(self, request):
        res = dict()
        computer = Computer()
        computer_form = ComputerForm(request.POST, instance=computer)
        if computer_form.is_valid():
            computer_form.save()
            res['status'] = 'success'
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(computer_form.errors)
            tally_record_form_errors = re.findall(pattern, errors)
            res = {
                'status': 'fail',
                'tally_record_form_errors': tally_record_form_errors[0]
            }
        return HttpResponse(json.dumps(res), content_type='application/json')


class ComputerUpdateView(LoginRequiredMixin, View):
    """
    主机更改
    """
    def get(self, request):
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            computer_record = get_object_or_404(Computer, pk=request.GET['id'])
            ret["personnel"] = Personnel.objects.all()
            ret["computer_record"] = computer_record
        return render(request, 'computer/computer_update.html', ret)

    def post(self, request):
        res = dict()
        computer_record = get_object_or_404(Computer, pk=request.POST['id'])
        computer_record_form = ComputerForm(request.POST, instance=computer_record)
        if computer_record_form.is_valid():
            computer_record_form.save()
            res['status'] = 'success'
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(computer_record_form.errors)
            tally_record_form_errors = re.findall(pattern, errors)
            res = {
                'status': 'fail',
                'tally_record_form_errors': tally_record_form_errors[0]
            }
        return HttpResponse(json.dumps(res), content_type='application/json')


class ComputerDelView(LoginRequiredMixin, View):
    """
    主机删除
    """
    def post(self, request):
        ret = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            # id_list = map(int, request.POST.get('id').split(','))
            id_list = eval(request.POST.get('id'))
            if isinstance(id_list, int):
                id_list = [id_list]
            Computer.objects.filter(id__in=id_list).delete()
            ret['result'] = True
        return HttpResponse(json.dumps(ret), content_type='application/json')