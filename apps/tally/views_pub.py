import json
import re

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from tally.forms import PersonnelForm, CheckRecordForm
from tally.models import Computer, Personnel, CheckRecord


class RukuView(View):
    """
    入库
    """

    def get(self, request):
        ret = dict()
        if 'mac' in request.GET and request.GET['mac']:
            # 优先取确认记录、主机记录中的值
            check_records = CheckRecord.objects.filter(mac=request.GET['mac'])
            computer_records = Computer.objects.filter(mac=request.GET['mac'])
            if check_records:
                cur_computer = check_records.first()
                ret['number'] = cur_computer.number
                ret['monitor_num'] = cur_computer.monitor.split(':')[0]
                ret['personnel_id'] = cur_computer.personnel_id
            elif computer_records:
                cur_computer = computer_records.first()
                ret['number'] = cur_computer.number
                if cur_computer.personnel:
                    ret['monitor_num'] = ', '.join(cur_computer.personnel.get_monitor_number())
                ret['personnel_id'] = cur_computer.personnel_id

        if request.GET.get('cpu'):
            ret['cpu'] = request.GET['cpu']
        if request.GET.get('gpu'):
            ret['gpu'] = request.GET['gpu']
        if request.GET.get('ram'):
            ret['ram'] = request.GET['ram']
        if request.GET.get('hdd'):
            ret['hdd'] = request.GET['hdd']
        if request.GET.get('ip'):
            ret['ip'] = request.GET['ip']
        if request.GET.get('mac'):
            ret['mac'] = request.GET['mac']
        if request.GET.get('monitor'):
            monitor_list = MonitorList.objects.all()
            for monitor in request.GET.get('monitor').split('; '):
                if len(monitor) == 7:
                    monitor_record = monitor_list.filter(name=monitor)
                    if monitor_record:
                        monitor_record = monitor_record.first()
                        ret['monitor'] = [monitor, monitor_record.type, monitor_record.size]
                    else:
                        ret['monitor'] = [monitor, '未识别', '未识别']

        personnel = Personnel.objects.all()
        ret['personnel'] = personnel

        return render(request, 'pub/ruku.html', ret)

    def post(self, request):
        res = {'status': 'fail'}
        check_record = CheckRecord()
        if 'mac' in request.POST and request.POST['mac']:
            check_record_record = CheckRecord.objects.filter(mac=request.POST['mac'])
            if check_record_record:
                check_record = check_record_record.first()
        if 'monitor' in request.POST and request.POST['monitor']:
            if 'monitor_type' in request.POST and request.POST['monitor_type']:
                check_record.monitor = "%s: %s" % (request.POST['monitor'], request.POST['monitor_type'])

        check_record_form = CheckRecordForm(request.POST, instance=check_record)
        if check_record_form.is_valid():
            check_record_form.save()
            res['status'] = 'success'
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(check_record_form.errors)
            record_form_errors = re.findall(pattern, errors)
            res['record_form_errors'] = record_form_errors[0]
        return HttpResponse(json.dumps(res), content_type='application/json')


class PersonnelAddView(View):
    """
    新增人员
    """
    def get(self, request):
        ret = dict()
        return render(request, 'pub/personnel_add.html', ret)

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
            record_form_errors = re.findall(pattern, errors)
            res = {
                'status': 'fail',
                'record_form_errors': record_form_errors[0]
            }
        return HttpResponse(json.dumps(res), content_type='application/json')
