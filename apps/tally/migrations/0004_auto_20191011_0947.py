# Generated by Django 2.1.4 on 2019-10-11 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tally', '0003_auto_20191011_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='产品型号'),
        ),
    ]
