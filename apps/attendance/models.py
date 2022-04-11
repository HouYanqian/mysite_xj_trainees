import datetime

from django.contrib.auth import get_user_model
from django.db import models

from utils.date_calculate import get_tomorrow

User = get_user_model()


class AttendanceGroup(models.Model):
    title = models.CharField(max_length=40, verbose_name='名称')
    personnel = models.ManyToManyField(User, verbose_name='考勤人员')
    shift = models.CharField(max_length=200, verbose_name='班次')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '考勤组'
        verbose_name_plural = verbose_name


class AttendanceRecord(models.Model):
    personnel = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='姓名')
    shift_start_time = models.DateTimeField(verbose_name='上班排班时间')
    start_time = models.DateTimeField(blank=True, null=True, verbose_name='上班打卡时间')
    shift_end_time = models.DateTimeField(verbose_name='下班排班时间')
    end_time = models.DateTimeField(blank=True, null=True, verbose_name='下班打卡时间')

    def get_start_time_status(self):
        if self.start_time:
            time_status = self.start_time.strftime("%H:%M")
            if self.start_time > self.shift_start_time:
                time_status += '迟到'
        else:
            if datetime.datetime.now() >= self.shift_end_time:
                time_status = '缺卡'
            else:
                time_status = '未打卡'
        return time_status

    def get_end_time_status(self):
        if self.end_time:
            time_status = self.end_time.strftime("%H:%M")
            if self.end_time < self.shift_end_time:
                time_status += '早退'
        else:
            tomorrow = get_tomorrow(self.shift_end_time)

            if datetime.datetime.now() >= tomorrow:
                time_status = '缺卡'
            else:
                time_status = '未打卡'
        return time_status

    def duration(self):
        if self.start_time and self.end_time:
            timedelta = self.end_time - self.start_time
            hours = round(timedelta.seconds / 60, 1)
        else:
            hours = 0
        return hours

    def __str__(self):
        return self.personnel.name + "的考勤记录"

    class Meta:
        verbose_name = '考勤组'
        verbose_name_plural = verbose_name


