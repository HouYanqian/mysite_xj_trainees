# Generated by Django 3.2.6 on 2021-08-24 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tally', '0024_auto_20210823_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computer',
            name='mac',
            field=models.CharField(blank=True, max_length=17, null=True, verbose_name='mac'),
        ),
    ]
