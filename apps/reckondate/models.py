from django.db import models

# Create your models here.


class Personnel(models.Model):
    name = models.CharField(max_length=20, verbose_name='姓名')
    start_date = models.DateField(verbose_name='入学日期')
    remark = models.CharField(max_length=300, blank=True, null=True, verbose_name='备注')

    def get_change_record(self):
        return self.changerecord_set.all()

    class Meta:
        verbose_name = '人员'
        verbose_name_plural = verbose_name
        unique_together = ['name']

    def __str__(self):
        return self.name


class ChangeRecord(models.Model):
    type_choice = ((0, '休息'), (1, '出勤'))
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, verbose_name='姓名')
    date = models.DateField(verbose_name='日期')
    type = models.CharField(max_length=2, default=1, verbose_name='类型')

    class Meta:
        verbose_name = '调休日志'
        verbose_name_plural = verbose_name
