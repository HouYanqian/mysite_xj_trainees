# Generated by Django 2.1.4 on 2019-10-11 01:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tally', '0002_auto_20190928_1717'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=20, verbose_name='客户名称')),
            ],
        ),
        migrations.CreateModel(
            name='Payee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payee_name', models.CharField(max_length=20, verbose_name='收款单位')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50, verbose_name='产品名称')),
                ('product_type', models.CharField(max_length=50, verbose_name='产品型号')),
                ('product_unit', models.CharField(max_length=10, verbose_name='单位')),
            ],
        ),
        migrations.RemoveField(
            model_name='tallyrecord',
            name='returned_money_remark',
        ),
        migrations.RemoveField(
            model_name='tallyrecord',
            name='unit',
        ),
        migrations.AddField(
            model_name='tallyrecord',
            name='has_tray',
            field=models.BooleanField(default=True, verbose_name='托盘'),
        ),
        migrations.AddField(
            model_name='tallyrecord',
            name='operating_expenses',
            field=models.FloatField(default=0, verbose_name='业务费用'),
        ),
        migrations.AddField(
            model_name='tallyrecord',
            name='storage',
            field=models.CharField(choices=[('out', '销售'), ('in', '入库')], default='out', max_length=10, verbose_name='入库'),
        ),
        migrations.AlterField(
            model_name='tallyrecord',
            name='client_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tally.Client', verbose_name='客户名称'),
        ),
        migrations.AlterField(
            model_name='tallyrecord',
            name='product_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tally.Product', verbose_name='产品名称'),
        ),
        migrations.AlterField(
            model_name='tallyrecord',
            name='remark',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='备注'),
        ),
        migrations.AddField(
            model_name='tallyrecord',
            name='payee_name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tally.Payee', verbose_name='收款单位'),
            preserve_default=False,
        ),
    ]