import datetime
import json
import re

import chinese_calendar
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views import View

from reckondate.forms import PersonnelForm
from reckondate.models import Personnel, ChangeRecord
from utils.date_calculate import week_day_zh, holiday_zh
from utils.mixin_utils import LoginRequiredMixin
from utils.tools import id_split


class ReckonDateView(LoginRequiredMixin, View):
    """
    排班日期
    """

    def get(self, request):
        ret = dict()

        now = datetime.datetime.now()
        next_month = now.replace(day=28) + datetime.timedelta(days=4)
        start_date = datetime.datetime(now.year, now.month, 1)
        end_date = next_month - datetime.timedelta(days=next_month.day)
        if request.GET.get('date') and request.GET['date']:
            date_start, date_end = request.GET['date'].split(" - ")
            start_date = datetime.datetime.strptime(date_start, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(date_end, '%Y-%m-%d')

        ret['date'] = "%s - %s" % (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        diff_date = end_date - start_date
        if diff_date.days > 200:
            return render(request, 'reckon_date/reckon_date_index.html', ret)

        ret['period'] = []
        while start_date <= end_date:
            ret['period'].append(start_date)
            start_date += datetime.timedelta(days=1)

        return render(request, 'reckon_date/reckon_date_index.html', ret)


class ReckonDateRecordView(LoginRequiredMixin, View):
    """
    排班日期记录
    """
    def get(self, request):
        filters = dict()
        if 'key[ids]' in request.GET and request.GET['key[ids]']:
            filters["id__in"] = id_split(request.GET['key[ids]'])
        if 'key[name]' in request.GET and request.GET['key[name]']:
            filters['name__contains'] = request.GET['key[name]']
        all_personnel = Personnel.objects.filter(**filters)
        res_record = []

        for personnel in all_personnel:
            personnel_data = dict()
            personnel_data['id'] = personnel.id
            personnel_data['name'] = personnel.name
            start_date = personnel.start_date
            personnel_data['start_date'] = personnel.start_date.strftime('%Y/%m/%d')
            today = datetime.datetime.now().date()
            personnel_change_record = [date[0] for date in personnel.get_change_record().values_list('date')]
            part_days = 23
            past_days = 0
            remain_days = 0

            for part in range(1, 7):
                count = 1
                while part_days >= count:
                    cur_date = start_date.strftime('%m/%d')
                    try:
                        is_holiday, detail = chinese_calendar.get_holiday_detail(start_date)
                    except NotImplementedError:
                        if start_date.isoweekday() > 5:
                            is_holiday, detail = True, None
                        else:
                            is_holiday, detail = False, None
                    if start_date in personnel_change_record:
                        if is_holiday:
                            is_holiday = False
                        else:
                            is_holiday = True
                            detail = '调休'
                    if is_holiday:
                        if detail:
                            personnel_data[cur_date] = detail
                            if holiday_zh.get(detail):
                                personnel_data[cur_date] = holiday_zh.get(detail)
                        else:
                            personnel_data[cur_date] = week_day_zh[start_date.weekday()]

                    else:
                        personnel_data[cur_date] = '%s-%s' % (part, count)
                        count += 1
                        if start_date < today:
                            past_days += 1
                            personnel_data[cur_date] += '_past'
                        elif start_date == today:
                            personnel_data[cur_date] += '_today'
                        elif start_date > today:
                            remain_days += 1
                    start_date += datetime.timedelta(days=1)
                personnel_data['start_date'] = '%s(%s)' % (personnel.start_date.strftime('%Y/%m/%d'), past_days)
                personnel_data['end_date'] = '%s(%s)' % (start_date.strftime('%Y/%m/%d'), remain_days)

            res_record.append(personnel_data)
        count = len(res_record)
        end_ele = int(request.GET["page"]) * int(request.GET["limit"])
        start_ele = end_ele - int(request.GET["limit"])
        limit_record = res_record[start_ele:end_ele]
        res = {"code": 0, "msg": "", "count": count, "data": limit_record}

        return JsonResponse(res, safe=False)


class ReckonDateAddView(LoginRequiredMixin, View):
    """
    排班人员添加
    """
    def get(self, request):
        ret = dict()
        return render(request, 'reckon_date/reckon_date_add.html', ret)

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


class ReckonDateChangeView(LoginRequiredMixin, View):
    def post(self, request):
        res = dict()
        res['status'] = 'fail'

        if request.POST.get('id') and request.POST['id']:
            personnel = Personnel.objects.filter(id=request.POST['id'])
            if personnel:
                personnel = personnel.first()
                if request.POST.get('date') and request.POST['date']:
                    month, day = request.POST['date'].split('/')
                    month = int(month)
                    day = int(day)
                    if month < personnel.start_date.month:
                        year = personnel.start_date.year + 1
                    else:
                        year = personnel.start_date.year
                    date = datetime.date(year, month, day)
                    change_record = ChangeRecord.objects.filter(personnel_id=request.POST['id'], date=date)
                    if change_record:
                        change_record.delete()
                        res['status'] = 'success'
                    else:
                        change_record = ChangeRecord()
                        change_record.personnel_id = request.POST['id']
                        change_record.date = date
                        change_record.save()
                        res['status'] = 'success'

        return HttpResponse(json.dumps(res), content_type='application/json')


class ReckonDateUpdateView(LoginRequiredMixin, View):
    """
    排班人员更改
    """
    def get(self, request):
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            personnel_record = get_object_or_404(Personnel, pk=request.GET['id'])
            ret["personnel"] = Personnel.objects.all()
            ret["personnel_record"] = personnel_record
        return render(request, 'reckon_date/reckon_date_update.html', ret)

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


class ReckonDateDelView(LoginRequiredMixin, View):
    """
    排班人员删除
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


class ReckonDateHistoryView(LoginRequiredMixin, View):
    """
    排班人员历史
    """
    def get(self, request):
        ret = dict(result=False)
        if 'id' in request.GET and request.GET['id']:
            personnel = get_object_or_404(Personnel, pk=request.GET['id'])
            personnel_data = []
            start_date = personnel.start_date

            today = datetime.datetime.now().date()
            personnel_change_record = [date[0] for date in personnel.get_change_record().values_list('date')]
            part_days = 23
            past_days = 0
            remain_days = 0

            for part in range(1, 7):
                part = {
                    'start_date': start_date,
                    'personnel_change_record': []
                }
                count = 1
                while part_days >= count:
                    try:
                        is_holiday, detail = chinese_calendar.get_holiday_detail(start_date)
                    except NotImplementedError:
                        if start_date.isoweekday() > 5:
                            is_holiday, detail = True, None
                        else:
                            is_holiday, detail = False, None
                    if start_date in personnel_change_record:
                        if is_holiday:
                            is_holiday = False
                            if detail:
                                part["personnel_change_record"].append([start_date, detail + '-出勤'])
                            else:
                                part["personnel_change_record"].append([start_date, '周末-出勤'])
                        else:
                            is_holiday = True
                            part["personnel_change_record"].append([start_date, '工作日-调休'])

                    if not is_holiday:
                        count += 1
                        if start_date < today:
                            past_days += 1
                        elif start_date == today:
                            part["personnel_change_record"].append([start_date, '今日'])
                        elif start_date > today:
                            remain_days += 1
                    start_date += datetime.timedelta(days=1)
                personnel_data.append(part)
            if personnel_data:
                ret = {
                    'past_days': past_days,
                    'remain_days': remain_days,
                    'personnel_data': personnel_data,
                    'personnel_end_date': start_date,
                    'result': True,
                }

        return render(request, 'reckon_date/reckon_date_history.html', ret)

