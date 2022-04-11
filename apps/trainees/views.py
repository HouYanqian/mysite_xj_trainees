import datetime
import json
import re

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
# from django.urls import reverse
from django.views.generic.base import View

from rbac.models import Role
from trainees.forms import TraineesForm
from trainees.models import Trainees
from users.models import UserProfile
from utils.mixin_utils import LoginRequiredMixin
from utils.model_tools import attendance_record_cur_status

User = get_user_model()


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        cur_user = request.user
        if cur_user.roles.filter(title='储备生'):
            try:
                cur_user.trainees
            except:
                return render(request, 'pub/trainees_guide.html')
                # return HttpResponseRedirect(reverse('pub-trainees_guide'))    # 改变url
        return render(request, 'index.html')


class IndexWelcomeView(View):
    """
    首页
    """

    def get(self, request):
        ret = dict()
        if request.user.roles.filter(title='教务总监'):
            personnel_record = Role.objects.get(title='储备生').get_user_list()

            new_personnel_count = 0
            trainees_interview_count = 0
            trainees_info_count = 0
            scheduling_count = 0

            for record in personnel_record:
                uncatalogued = False
                try:
                    if record.traineesinterview:
                        trainees_interview_count += 1
                except:
                    uncatalogued = True
                try:
                    if record.trainees:
                        trainees_info_count += 1
                except:
                    uncatalogued = True
                if uncatalogued:
                    new_personnel_count += 1

            ret = {
                'new_personnel_count': new_personnel_count,
                'trainees_interview_count': trainees_interview_count,
                'trainees_info_count': trainees_info_count,
                'scheduling_count': scheduling_count,
            }
            return render(request, 'welcome/teachers.html', ret)
        elif request.user.roles.filter(title='储备生'):
            user = request.user
            # 如果没有当天打卡记录则从排版中新增空白记录
            attendance_record, status = attendance_record_cur_status(user)
            ret = {
                'attendance_record': attendance_record,
                'status': status,
            }

            return render(request, 'welcome/students.html', ret)
        else:
            return render(request, 'welcome.html', ret)


class GuideView(View):
    def post(self, request):
        res = dict()
        trainees = Trainees()
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


class TestView(View):
    def get(self, request):
        return render(request, 'test.html')
