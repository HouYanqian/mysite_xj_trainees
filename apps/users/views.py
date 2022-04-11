from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from django.views.generic.base import View
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse

from .forms import LoginForm, ChangePwdForm, UploadImagForm
from utils.mixin_utils import LoginRequiredMixin

import json
import re

User = get_user_model()


class LoginView(View):
    '''
    用户登录认证，通过form表单进行输入合规验证
    '''

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'login3.html')
        else:
            return HttpResponseRedirect(reverse("index"))

    def post(self, request):
        login_form = LoginForm(request.POST)
        ret = {'status': 'fail', 'msg': ''}
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    msg = request
                    ret['status'] = 'success'
                    if request.GET.get('next'):
                        msg = request.GET['next']
                    else:
                        msg = reverse('index')
                else:
                    msg = "用户未激活！"
            else:
                msg = "用户名或密码错误！"
        else:
            msg = "用户名和密码不能够为空！"
        ret['msg'] = msg
        return HttpResponse(json.dumps(ret), content_type='application/json')


class LogoutView(View):
    '''
    用户登出
    '''

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("login"))


class ChangePwdView(LoginRequiredMixin, View):
    """
    修改用户列表中的用户密码
    """
    def post(self, request):
        user = get_object_or_404(User, pk=int(request.user.id))
        change_pwd_form = ChangePwdForm(request.POST)
        if change_pwd_form.is_valid():
            new_password = request.POST.get('password')
            user.set_password(new_password)
            user.save()
            ret = {'status': 'success'}
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(change_pwd_form.errors)
            change_pwd_form_errors = re.findall(pattern, errors)
            ret = {
                'status': 'fail',
                'change_pwd_form_errors': change_pwd_form_errors[0]
            }
        return HttpResponse(json.dumps(ret), content_type='application/json')


class UploadImgView(LoginRequiredMixin, View):
    """
    修改用户头像
    """
    def post(self, request):
        ret = dict()
        if request.POST.get('user_id'):
            user = get_object_or_404(User, pk=request.POST.get('user_id'))

            upload_image_form = UploadImagForm(request.POST, request.FILES, instance=user)
            if upload_image_form.is_valid():
                upload_image_form.save()
                ret['result'] = 'success'
            else:
                pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
                errors = str(upload_image_form.errors)
                form_errors = re.findall(pattern, errors)
                ret = {
                    'status': 'fail',
                    'change_pwd_form_errors': form_errors[0]
                }
        else:
            ret = {
                'status': 'fail',
                'change_pwd_form_errors': '用户id错误'
            }
        return HttpResponse(json.dumps(ret), content_type='application/json')
