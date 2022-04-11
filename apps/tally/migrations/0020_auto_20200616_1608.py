# Generated by Django 3.0.6 on 2020-06-16 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tally', '0019_auto_20200615_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tallyrecord',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='tallyrecord',
            name='tally_type',
            field=models.CharField(choices=[('in', '进货'), ('out', '出货')], default='out', max_length=3, verbose_name='进出货'),
        ),
    ]