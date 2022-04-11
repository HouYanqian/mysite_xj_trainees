import datetime
import json

from django.contrib.auth import get_user_model
from django.http import HttpResponse

from django.views import View

from utils.mixin_utils import LoginRequiredMixin
from utils.model_tools import attendance_record_cur_status

User = get_user_model()


class AttendanceRecordAddView(LoginRequiredMixin, View):
    """
    考勤组管理添加
    """
    def get(self, request):
        pass

    def post(self, request):
        res = dict()
        user = request.user
        record, status = attendance_record_cur_status(user, is_enter=True)
        if status:
            res = {
                'status': 'success',
            }

        else:
            res = {
                'status': 'fail',
                'form_errors': '上传数据异常，请勿私自上传信息！'
            }

        return HttpResponse(json.dumps(res), content_type='application/json')