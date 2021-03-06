# Generated by Django 3.2.6 on 2021-08-25 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tally', '0026_computerapplyrecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=20, verbose_name='编号')),
                ('cpu', models.CharField(max_length=50, verbose_name='cpu')),
                ('gpu', models.CharField(max_length=50, verbose_name='显卡')),
                ('ram', models.CharField(max_length=50, verbose_name='内存')),
                ('hdd', models.CharField(max_length=50, verbose_name='硬盘')),
                ('price', models.FloatField(default=0, verbose_name='价值')),
                ('monitor', models.CharField(max_length=50, verbose_name='显示器')),
                ('mac', models.CharField(blank=True, max_length=17, null=True, verbose_name='mac')),
                ('ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='ip')),
                ('purchase_date', models.DateField(auto_now_add=True, verbose_name='采购日期')),
                ('remark', models.CharField(blank=True, max_length=300, null=True, verbose_name='备注')),
                ('is_check', models.BooleanField(default=False, verbose_name='是否确认')),
                ('personnel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tally.personnel', verbose_name='使用者')),
            ],
            options={
                'verbose_name': '入库主机',
                'verbose_name_plural': '入库主机',
                'unique_together': {('number', 'mac')},
            },
        ),
        migrations.DeleteModel(
            name='ComputerApplyRecord',
        ),
    ]
