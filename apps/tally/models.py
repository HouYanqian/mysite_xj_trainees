from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


class Personnel(models.Model):
    gender_choice = (('nan', '男'), ('nv', '女'))
    name = models.CharField(max_length=20, verbose_name='姓名')
    gender = models.CharField(max_length=3, choices=gender_choice, verbose_name='性别')
    department = models.CharField(max_length=20, verbose_name='部门')
    job = models.CharField(max_length=20, verbose_name='岗位')
    remark = models.CharField(max_length=300, blank=True, null=True, verbose_name='备注')

    def get_computer_record(self):
        # 获取使用电脑
        return self.computer_set.all()

    def get_computer_number(self):
        # 获取使用电脑编号
        computer_number = [computer.number for computer in self.get_computer_record()]

        return computer_number
        # return " ".join(product_names)
    get_computer_number.short_description = '使用电脑'

    def get_monitor_record(self):
        # 获取使用电脑
        return self.monitor_set.all()

    def get_monitor_number(self):
        # 获取使用电脑编号
        monitor_number = [monitor.number for monitor in self.get_monitor_record()]

        return monitor_number
        # return " ".join(product_names)
    get_monitor_number.short_description = '使用显示器'

    class Meta:
        verbose_name = '人员'
        verbose_name_plural = verbose_name
        unique_together = ['name']

    def __str__(self):
        return self.name


class Computer(models.Model):
    number = models.CharField(max_length=20, verbose_name='编号')
    cpu = models.CharField(max_length=50, verbose_name='cpu')
    gpu = models.CharField(max_length=50, verbose_name='显卡')
    ram = models.CharField(max_length=50, verbose_name='内存')
    hdd = models.CharField(max_length=50, verbose_name='硬盘')
    price = models.FloatField(default=0, verbose_name='价值')
    mac = models.CharField(max_length=17, blank=True, null=True, verbose_name='mac')
    ip = models.GenericIPAddressField(blank=True, null=True, verbose_name='ip')
    purchase_date = models.DateField(auto_now_add=True, verbose_name='采购日期')
    personnel = models.ForeignKey(Personnel, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='使用者')
    remark = models.CharField(max_length=300, blank=True, null=True, verbose_name='备注')

    class Meta:
        verbose_name = '主机'
        verbose_name_plural = verbose_name
        unique_together = ['number', 'mac']

    def __str__(self):
        return self.number


class Monitor(models.Model):
    number = models.CharField(max_length=20, verbose_name='编号')
    type = models.CharField(max_length=11, verbose_name='型号')
    size = models.CharField(max_length=10, verbose_name='尺寸')
    price = models.FloatField(default=0, verbose_name='价值')
    purchase_date = models.DateField(auto_now_add=True, verbose_name='采购日期')
    personnel = models.ForeignKey(Personnel, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='使用者')
    remark = models.CharField(max_length=300, blank=True, null=True, verbose_name='备注')

    class Meta:
        verbose_name = '显示器'
        verbose_name_plural = verbose_name
        unique_together = ['number']

    def __str__(self):
        return self.number


class AssetsRecord(models.Model):
    action_choice = (('nan', '男'), ('nv', '女'))
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    action = models.CharField(max_length=3, choices=action_choice, verbose_name='操作类型')
    remark = models.CharField(max_length=300, blank=True, null=True, verbose_name='操作内容')
    handler = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='操作人')

    class Meta:
        verbose_name = '操作记录'
        verbose_name_plural = verbose_name


class CheckRecord(models.Model):
    number = models.CharField(max_length=20, verbose_name='编号')
    cpu = models.CharField(max_length=50, verbose_name='cpu')
    gpu = models.CharField(max_length=50, verbose_name='显卡')
    ram = models.CharField(max_length=50, verbose_name='内存')
    hdd = models.CharField(max_length=50, verbose_name='硬盘')
    price = models.FloatField(default=0, verbose_name='价值')
    monitor = models.CharField(max_length=50, verbose_name='显示器')
    mac = models.CharField(max_length=17, blank=True, null=True, verbose_name='mac')
    ip = models.GenericIPAddressField(blank=True, null=True, verbose_name='ip')
    purchase_date = models.DateField(auto_now_add=True, verbose_name='申请日期')
    personnel = models.ForeignKey(Personnel, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='使用者')
    remark = models.CharField(max_length=300, blank=True, null=True, verbose_name='备注')
    is_check = models.BooleanField(default=False, verbose_name='是否确认')

    class Meta:
        verbose_name = '入库主机'
        verbose_name_plural = verbose_name
        unique_together = ['number', 'mac']

    def __str__(self):
        return self.number