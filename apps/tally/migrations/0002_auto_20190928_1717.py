# Generated by Django 2.1.4 on 2019-09-28 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tally', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tallyrecord',
            name='remark',
            field=models.CharField(max_length=300, null=True, verbose_name='备注'),
        ),
        migrations.AlterField(
            model_name='tallyrecord',
            name='returned_money_remark',
            field=models.CharField(max_length=300, null=True, verbose_name='回款备注'),
        ),
    ]