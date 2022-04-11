import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View

from rbac.models import Role, Menu
from utils.mixin_utils import LoginRequiredMixin
from utils.model_tools import get_role_permissions_trees


class RoleView(LoginRequiredMixin, View):
    """
    角色管理首页
    """

    def get(self, request):
        ret = dict()
        role_records = Role.objects.all()
        ret['role_records'] = role_records
        return render(request, 'rbac/role_index.html', ret)


class RoleUpdateView(LoginRequiredMixin, View):
    """
    角色管理
    """

    def get(self, request):
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            role_record = get_object_or_404(Role, pk=request.GET['id'])
            ret["role_record"] = role_record
            ret["role_record_permissions"] = [menu.id for menu in role_record.permissions.all()]

            role_permissions_trees = get_role_permissions_trees()
            ret["role_permissions_trees"] = role_permissions_trees

        return render(request, 'rbac/role_update.html', ret)

    def post(self, request):
        res = dict()

        role = get_object_or_404(Role, pk=request.POST['id'])
        permissions_list = []
        for post_key in request.POST:
            if post_key == 'title':
                setattr(role, post_key, request.POST[post_key])
                role.save()
            elif 'layuiTreeCheck' in post_key:
                permissions_list.append(request.POST[post_key])
        if permissions_list:
            role.permissions.set(permissions_list)
        else:
            role.permissions.clear()
        res['status'] = 'success'
        return HttpResponse(json.dumps(res), content_type='application/json')


class MenuAddView(LoginRequiredMixin, View):
    """
    角色管理菜单新增
    """

    def post(self, request):
        res = {'status': 'fail'}
        parent = get_object_or_404(Menu, pk=request.POST['parent_id'])
        get_title = request.POST.get('title')

        if get_title:
            url = '/temp'
            if parent.url:
                url = parent.url + url
            menu = Menu(title=get_title, url=url, parent=parent)
            try:
                menu.save()
                res['id'] = menu.id
                res['status'] = 'success'
            except:
                res['form_errors'] = '菜单名重复'

        return HttpResponse(json.dumps(res), content_type='application/json')


class MenuEditView(LoginRequiredMixin, View):
    """
    角色管理菜单编辑
    """
    def get(self, request):
        record = get_object_or_404(Menu, pk=request.GET['id'])
        ret = {
            'url': record.url
        }
        return HttpResponse(json.dumps(ret), content_type='application/json')

    def post(self, request):
        res = dict()
        record = get_object_or_404(Menu, pk=request.POST['id'])
        setattr(record, request.POST['field'], request.POST['value'])
        try:
            record.save()
            res['status'] = 'success'
        except:
            res['status'] = 'error'

        return HttpResponse(json.dumps(res), content_type='application/json')


class MenuDelView(LoginRequiredMixin, View):
    """
    角色管理菜单删除
    """

    def post(self, request):
        ret = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            id_list = eval(request.POST.get('id'))
            if isinstance(id_list, int):
                id_list = [id_list]
            Menu.objects.filter(id__in=id_list).delete()
            ret['result'] = True
        return HttpResponse(json.dumps(ret), content_type='application/json')
