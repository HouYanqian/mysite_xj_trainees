# Generated by Django 3.0.6 on 2020-06-05 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0003_auto_20191017_1021'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menu',
            options={'verbose_name': '权限', 'verbose_name_plural': '权限'},
        ),
        migrations.AlterField(
            model_name='menu',
            name='title',
            field=models.CharField(max_length=32, unique=True, verbose_name='权限名'),
        ),
    ]