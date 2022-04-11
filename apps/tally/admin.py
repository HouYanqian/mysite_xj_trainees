import re

from django.contrib import admin, messages
from django.contrib.admin import helpers
from django.contrib.admin.utils import model_ngettext
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.response import TemplateResponse

from .forms import ComputerForm
from .models import Computer, Monitor, Personnel, AssetsRecord, CheckRecord


class ComputerAdmin(admin.ModelAdmin):
    list_display = ['id', 'number', 'cpu', 'gpu', 'ram', 'hdd', 'price', 'ip', 'mac', 'purchase_date', 'personnel',
                    'personnel_department', 'remark']
    list_filter = ['cpu', 'gpu', 'ram', 'hdd', 'price', 'personnel__department', 'purchase_date']
    search_fields = ['number', 'cpu', 'gpu', 'ram', 'hdd', 'price', 'personnel__name', 'personnel__department', 'remark']
    list_editable = ['remark']

    def personnel_department(self, obj):
        if obj.personnel:
            return obj.personnel.department
        else:
            return '-'
    personnel_department.short_description = '部门'


class MonitorAdmin(admin.ModelAdmin):
    list_display = ['id', 'number', 'type', 'size', 'price', 'purchase_date', 'personnel', 'remark']
    list_filter = ['type', 'size', 'price', 'purchase_date']
    search_fields = ['number', 'type', 'size', 'price', 'remark']
    list_editable = ['remark']


class PersonnelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'gender', 'department', 'job', 'get_computer_number', 'get_monitor_number', 'remark']
    list_filter = ['gender', 'department', 'job']
    search_fields = ['name', 'gender', 'department', 'job', 'remark']
    list_editable = ['remark']
    list_display_links = ['name']


class AssetsRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'add_time', 'action', 'remark', 'handler']
    list_filter = ['add_time', 'action']
    search_fields = ['id', 'action', 'remark', 'handler']


class CheckRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'number', 'cpu', 'gpu', 'ram', 'hdd', 'ip', 'mac', 'purchase_date', 'price',
                    'monitor', 'personnel_department', 'personnel', 'is_check', 'remark']
    search_fields = ['number', 'monitor', 'personnel__department', 'personnel__name', 'remark',
                     'cpu', 'gpu', 'ram', 'hdd', 'ip', 'mac']
    list_filter = ['is_check', 'personnel__department', 'cpu', 'gpu', 'ram', 'hdd', 'purchase_date']
    list_editable = ['is_check', 'remark']
    actions = ['check_action']

    # list_select_related = ['personnel']

    def personnel_department(self, obj):
        if obj.personnel:
            return obj.personnel.department
        else:
            return '-'

    personnel_department.short_description = '部门'

    # def check_action(self, request, queryset):
    #     queryset.update(is_check=True)
    # check_action.short_description = "确认所选的 入库主机"

    def check_action(self, request, queryset):
        queryset = queryset.filter(is_check=False)
        if not queryset:
            msg = "选中的条目皆为已确认过的条目。"
            self.message_user(request, msg, messages.WARNING)
            return None
        if request.POST.get('post'):
            n = queryset.count()
            if n:
                for obj in queryset:
                    computer_record = Computer.objects.filter(mac=obj.mac)
                    if computer_record:
                        computer_record = computer_record.first()
                    else:
                        computer_record = Computer()
                        computer_record.save()
                    computer_record.number = obj.number
                    computer_record.cpu = obj.cpu
                    computer_record.gpu = obj.gpu
                    computer_record.ram = obj.ram
                    computer_record.hdd = obj.hdd
                    computer_record.price = obj.price
                    computer_record.mac = obj.mac
                    computer_record.ip = obj.ip
                    computer_record.personnel = obj.personnel
                    computer_record.remark = obj.remark
                    computer_record.purchase_date = obj.purchase_date
                    computer_record.save()
                    monitor_list = re.split('[,;:，；： ]', obj.monitor)
                    monitor_type = ''
                    monitor_type_record = None
                    for monitor in monitor_list:
                        if len(monitor) == 7:
                            monitor_type = monitor
                            monitor_type_records = MonitorList.objects.filter(name=monitor)
                            if monitor_type_records:
                                monitor_type_record = monitor_type_records.first()
                        elif len(monitor) > 7:
                            monitor_record = Monitor.objects.filter(number__contains=monitor)

                            if monitor_record:
                                monitor_record = monitor_record.first()
                            if not monitor_record:
                                monitor_record = Monitor()
                            monitor_record.personnel = obj.personnel
                            monitor_record.number = monitor
                            monitor_record.type = monitor_type
                            if monitor_type_record:
                                monitor_record.size = monitor_type_record.size
                            monitor_record.save()

                self.message_user(request, "成功确认 %(count)d %(items)s." % {
                    "count": n, "items": model_ngettext(self.opts, n)
                }, messages.SUCCESS)

            if 'submit' in request.POST:
                queryset.update(is_check=True)
            elif 'submitDel' in request.POST:
                queryset.delete()
            return None

        title = '你确定吗？'
        objects_name = model_ngettext(queryset)
        selected_objects, model_count, perms_needed, protected = self.get_deleted_objects(queryset, request)
        opts = self.model._meta
        # app_label = opts.app_label
        context = {
            **self.admin_site.each_context(request),
            'title': title,
            'objects_name': str(objects_name),
            'selected_objects': [selected_objects],
            'model_count': dict(model_count).items(),
            'queryset': queryset,
            'perms_lacking': perms_needed,
            'protected': protected,
            'opts': opts,
            'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
            'media': self.media,
            'action': 'check_action',
        }
        request.current_app = self.admin_site.name
        return TemplateResponse(request, "admin/check_action.html", context)
    check_action.short_description = '确认所选的 入库主机'

    # class data_src_form(forms.forms.Form):
    #     _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    #     data_src = forms.ModelChoiceField(DataSrc.objects)


admin.site.register(Computer, ComputerAdmin)
admin.site.register(Monitor, MonitorAdmin)
admin.site.register(Personnel, PersonnelAdmin)
admin.site.register(AssetsRecord, AssetsRecordAdmin)
admin.site.register(CheckRecord, CheckRecordAdmin)

admin.site.site_header = '储备生管理系统'  # 此处设置页面显示标题
admin.site.site_title = '储备生管理系统'  # 此处设置页面头部标题
