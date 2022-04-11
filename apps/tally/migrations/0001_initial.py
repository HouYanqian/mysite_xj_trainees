# Generated by Django 2.1.4 on 2019-09-28 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TallyRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('use_date', models.DateField(verbose_name='日期')),
                ('number', models.CharField(max_length=10, verbose_name='单号')),
                ('client_name', models.CharField(max_length=20, verbose_name='客户名称')),
                ('product_name', models.CharField(max_length=50, verbose_name='产品名称')),
                ('unit', models.CharField(max_length=10, verbose_name='单位')),
                ('quantity', models.FloatField(default=0, verbose_name='数量')),
                ('unit_price', models.FloatField(default=0, verbose_name='单价')),
                ('returned_money', models.FloatField(default=0, verbose_name='回款金额')),
                ('returned_money_remark', models.CharField(max_length=300, verbose_name='回款备注')),
                ('transport_expenses', models.FloatField(default=0, verbose_name='运输费用')),
                ('unloading_expenses', models.FloatField(default=0, verbose_name='装卸费用')),
                ('remark', models.CharField(max_length=300, verbose_name='备注')),
            ],
        ),
    ]
