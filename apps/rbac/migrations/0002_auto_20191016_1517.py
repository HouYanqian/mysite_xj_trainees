# Generated by Django 2.1.4 on 2019-10-16 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='code',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='icon',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='is_top',
        ),
    ]
