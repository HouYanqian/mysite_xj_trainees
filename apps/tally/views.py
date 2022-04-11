from django.shortcuts import render
from django.views.generic.base import View

from tally.models import Computer, Monitor
from utils.mixin_utils import LoginRequiredMixin


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'index.html')


class IndexWelcomeView(View):
    """
    首页
    """

    def get(self, request):
        computer_record = Computer.objects.all()
        monitor_record = Monitor.objects.all()
        computer_info = dict()
        computer_info['use'] = computer_record.filter(personnel__isnull=False).count()
        computer_info['repertory'] = computer_record.filter(personnel__isnull=True).count()
        monitor_info = dict()
        monitor_info['use'] = monitor_record.filter(personnel__isnull=False).count()
        monitor_info['repertory'] = monitor_record.filter(personnel__isnull=True).count()

        return render(request, 'welcome/students.html', {
            "computer_info": computer_info,
            "monitor_info": monitor_info,
        })


class TestView(View):
    def get(self, request):
        return render(request, 'test.html')
