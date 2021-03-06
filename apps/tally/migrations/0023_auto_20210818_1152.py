# Generated by Django 3.2.6 on 2021-08-18 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tally', '0022_auto_20210814_1218'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personnel',
            name='computer',
        ),
        migrations.RemoveField(
            model_name='personnel',
            name='monitor',
        ),
        migrations.AddField(
            model_name='computer',
            name='personnel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tally.personnel', verbose_name='使用者'),
        ),
        migrations.AddField(
            model_name='monitor',
            name='personnel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tally.personnel', verbose_name='使用者'),
        ),
        migrations.AlterField(
            model_name='computer',
            name='purchase_date',
            field=models.DateField(auto_now_add=True, verbose_name='采购日期'),
        ),
        migrations.AlterField(
            model_name='monitor',
            name='purchase_date',
            field=models.DateField(auto_now_add=True, verbose_name='采购日期'),
        ),
    ]
