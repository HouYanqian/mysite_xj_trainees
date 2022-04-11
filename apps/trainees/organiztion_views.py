import json

from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View

from rbac.models import Role
from users.models import UserProfile
from utils.mixin_utils import LoginRequiredMixin
from utils.tools import id_split

User = get_user_model()


class PersonnelView(LoginRequiredMixin, View):
    """
    人员管理首页
    """

    def get(self, request):
        ret = dict()
        if request.GET.get('id'):
            ret['id'] = request.GET['id']
        if request.GET.get('username'):
            ret['username'] = request.GET['username']
        if request.GET.get('name'):
            ret['name'] = request.GET['name']
        return render(request, 'organization/personnel/personnel_index.html', ret)


class PersonnelRecordView(LoginRequiredMixin, View):
    """
    人员管理记录
    """
    def get(self, request):
        filters = dict()
        if 'key[ids]' in request.GET and request.GET['key[ids]']:
            filters["id__in"] = id_split(request.GET['key[ids]'])
        if 'key[username]' in request.GET and request.GET['key[username]']:
            filters['username__contains'] = request.GET['key[username]']
        if 'key[name]' in request.GET and request.GET['key[name]']:
            filters['name__contains'] = request.GET['key[name]']
        personnel_record = Role.objects.get(title='储备生').get_user_list().filter(**filters).order_by('-id')
        res_personnel_record = []
        for record in list(personnel_record):
            try:
                trainees_interview = record.traineesinterview.add_time.date()
                # trainees_interview = record.traineesinterview_set.all().first().add_time
            except:
                trainees_interview = '未录入'
            try:
                trainees_info = record.trainees.add_time.date()
            except:
                trainees_info = '未录入'
            attendance_group = record.attendancegroup_set.all().first()
            if attendance_group:
                attendance_group = attendance_group.title
            else:
                attendance_group = '未加入'

            res_personnel_record.append({
                'id': record.id,
                'username': record.username,
                'name': record.name,
                'trainees_interview': trainees_interview,
                'trainees_info': trainees_info,
                'attendance_group': attendance_group,
            })

        count = len(res_personnel_record)
        end_ele = int(request.GET["page"]) * int(request.GET["limit"])
        start_ele = end_ele - int(request.GET["limit"])
        limit_record = res_personnel_record[start_ele:end_ele]
        res = {"code": 0, "msg": "", "count": count, "data": limit_record}

        return JsonResponse(res, safe=False)


class PersonnelEditView(LoginRequiredMixin, View):
    """
    人员管理编辑
    """
    def post(self, request):
        res = dict()
        product = get_object_or_404(User, pk=request.POST['id'])
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
    人员管理添加
    """
    def get(self, request):
        return render(request, 'organization/personnel/personnel_add.html')

    def post(self, request):
        res = {'status': 'fail'}
        username = request.POST.get('username')
        if UserProfile.objects.filter(username=username):
            res['form_errors'] = '用户名重复'
        else:
            if username:
                default_pwd = '123456'
                User.objects.create_user(username=username, password=default_pwd)
                new_user = UserProfile.objects.get(username=username)
                new_user.name = username
                new_user.roles.add(Role.objects.get(title='储备生'))
                new_user.save()
                res['status'] = 'success'
            else:
                res['form_errors'] = '用户名重复不能为空'

        return HttpResponse(json.dumps(res), content_type='application/json')


class PersonnelUpdateView(LoginRequiredMixin, View):
    """
    人员管理更改
    """
    def get(self, request):
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            personnel_record = get_object_or_404(User, pk=request.GET['id'])
            ret["username"] = personnel_record.username
        return render(request, 'organization/personnel/personnel_update.html', ret)

    def post(self, request):
        res = {'status': 'fail'}
        res['form_errors'] = '禁止更改用户名'
        return HttpResponse(json.dumps(res), content_type='application/json')


class PersonnelDelView(LoginRequiredMixin, View):
    """
    人员管理删除
    """
    def post(self, request):
        ret = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            # id_list = map(int, request.POST.get('id').split(','))
            id_list = eval(request.POST.get('id'))
            if isinstance(id_list, int):
                id_list = [id_list]
            User.objects.filter(id__in=id_list).delete()
            ret['result'] = True
        return HttpResponse(json.dumps(ret), content_type='application/json')