# Generated by Django 2.2.5 on 2022-03-03 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainees', '0007_auto_20220303_1415'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainees',
            name='image',
        ),
        migrations.AlterField(
            model_name='trainees',
            name='education',
            field=models.CharField(choices=[('1', '研究生'), ('2', '本科'), ('3', '大专'), ('4', '高中'), ('5', '其他')], max_length=40, verbose_name='最高学历'),
        ),
        migrations.AlterField(
            model_name='trainees',
            name='gender',
            field=models.CharField(choices=[('man', '男'), ('woman', '女')], max_length=5, verbose_name='性别'),
        ),
        migrations.AlterField(
            model_name='trainees',
            name='id_card',
            field=models.CharField(max_length=18, unique=True, verbose_name='身份证号码'),
        ),
        migrations.AlterField(
            model_name='trainees',
            name='orientation',
            field=models.CharField(choices=[('1', '动画'), ('2', '模型'), ('3', '解算'), ('4', '灯光'), ('5', '制片')], max_length=1, verbose_name='培养方向'),
        ),
        migrations.AlterField(
            model_name='trainees',
            name='phone',
            field=models.CharField(max_length=11, unique=True, verbose_name='联系电话'),
        ),
        migrations.AlterField(
            model_name='trainees',
            name='politics_status',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='政治面貌'),
        ),
    ]
