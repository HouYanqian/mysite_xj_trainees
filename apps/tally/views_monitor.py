import json
import re

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View

from tally.forms import MonitorForm
from tally.models import Monitor, Personnel
from utils.mixin_utils import LoginRequiredMixin
from utils.tools import id_split


class MonitorView(LoginRequiredMixin, View):
    """
    显示器管理
    """

    def get(self, request):
        ret = dict()
        if request.GET.get('id'):
            ret['id'] = request.GET['id']
        if request.GET.get('number'):
            ret['number'] = request.GET['number']
        if request.GET.get('cpu'):
            ret['type'] = request.GET['type']
        if request.GET.get('gpu'):
            ret['size'] = request.GET['size']
        if request.GET.get('date'):
            ret['date'] = request.GET['date']
        if request.GET.get('personnel'):
            ret['personnel'] = request.GET['personnel']

        return render(request, 'monitor/monitor_index.html', ret)


class MonitorRecordView(LoginRequiredMixin, View):
    """
    显示器记录
    """
    def get(self, request):
        filters = dict()
        if 'key[ids]' in request.GET and request.GET['key[ids]']:
            filters["id__in"] = id_split(request.GET['key[ids]'])
        if 'key[number]' in request.GET and request.GET['key[number]']:
            filters['number__contains'] = request.GET['key[number]']
        if 'key[type]' in request.GET and request.GET['key[type]']:
            filters['type__contains'] = request.GET['key[type]']
        if 'key[size]' in request.GET and request.GET['key[size]']:
            filters['size__contains'] = request.GET['key[size]']
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
        monitor_record = Monitor.objects.filter(**filters).order_by('-id')
        res_monitor_record = []
        for record in list(monitor_record):
            if record.personnel:
                personnel = record.personnel.name
            else:
                personnel = ''
            res_monitor_record.append({
                'id': record.id,
                'number': record.number,
                'type': record.type,
                'size': record.size,
                'price': record.price,
                'purchase_date': record.purchase_date,
                'personnel': personnel,
                'remark': record.remark,
            })

        count = len(res_monitor_record)
        end_ele = int(request.GET["page"]) * int(request.GET["limit"])
        start_ele = end_ele - int(request.GET["limit"])
        limit_record = res_monitor_record[start_ele:end_ele]
        res = {"code": 0, "msg": "", "count": count, "data": limit_record}

        return JsonResponse(res, safe=False)


class MonitorEditView(LoginRequiredMixin, View):
    """
    显示器编辑
    """
    def post(self, request):
        res = dict()
        product = get_object_or_404(Monitor, pk=request.POST['id'])
        setattr(product, request.POST['field'], request.POST['value'])
        # noinspection PyBroadException
        try:
            product.save()
            res['status'] = 'success'
        except:
            res['status'] = 'error'

        return HttpResponse(json.dumps(res), content_type='application/json')


class MonitorAddView(LoginRequiredMixin, View):
    """
    显示器添加
    """
    def get(self, request):
        ret = dict()
        personnel = Personnel.objects.all()
        ret['personnel'] = personnel

        return render(request, 'monitor/monitor_add.html', ret)

    def post(self, request):
        res = dict()
        monitor = Monitor()
        monitor_form = MonitorForm(request.POST, instance=monitor)
        if monitor_form.is_valid():
            monitor_form.save()
            res['status'] = 'success'
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(monitor_form.errors)
            tally_record_form_errors = re.findall(pattern, errors)
            res = {
                'status': 'fail',
                'tally_record_form_errors': tally_record_form_errors[0]
            }
        return HttpResponse(json.dumps(res), content_type='application/json')


class MonitorUpdateView(LoginRequiredMixin, View):
    """
    显示器更改
    """
    def get(self, request):
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            monitor_record = get_object_or_404(Monitor, pk=request.GET['id'])
            ret["personnel"] = Personnel.objects.all()
            ret["monitor_record"] = monitor_record
        return render(request, 'monitor/monitor_update.html', ret)

    def post(self, request):
        res = dict()
        monitor_record = get_object_or_404(Monitor, pk=request.POST['id'])
        monitor_record_form = MonitorForm(request.POST, instance=monitor_record)
        if monitor_record_form.is_valid():
            monitor_record_form.save()
            res['status'] = 'success'
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(monitor_record_form.errors)
            tally_record_form_errors = re.findall(pattern, errors)
            res = {
                'status': 'fail',
                'tally_record_form_errors': tally_record_form_errors[0]
            }
        return HttpResponse(json.dumps(res), content_type='application/json')


class MonitorDelView(LoginRequiredMixin, View):
    """
    显示器删除
    """
    def post(self, request):
        ret = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            # id_list = map(int, request.POST.get('id').split(','))
            id_list = eval(request.POST.get('id'))
            if isinstance(id_list, int):
                id_list = [id_list]
            Monitor.objects.filter(id__in=id_list).delete()
            ret['result'] = True
        return HttpResponse(json.dumps(ret), content_type='application/json')