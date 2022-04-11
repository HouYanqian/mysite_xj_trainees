from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TraineesInterview(models.Model):
    """
    面试指标
    """
    name = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='姓名')
    target_1 = models.IntegerField(verbose_name='⽗⺟⼯作、身体状况')
    target_2 = models.IntegerField(verbose_name='兄妹学习、⼯作、⽣活状况')
    target_3 = models.IntegerField(verbose_name='家庭整体收⽀情况')
    target_4 = models.IntegerField(verbose_name='本⼈身体状况')
    target_5 = models.IntegerField(verbose_name='学习习惯、持续时间')
    target_6 = models.IntegerField(verbose_name='社会实践获得的收益情况和对过程的感受')
    target_7 = models.IntegerField(verbose_name='家庭诱导因素（⽗⺟管教的⼒度、⽗⺟的沟通情况）')
    target_8 = models.IntegerField(verbose_name='朋友圈影响因素（与朋友关系的密切程度、朋友的环境因素、朋友对⽣活的态度积极消极的占⽐）')
    target_9 = models.IntegerField(verbose_name='⾏业了解程度（了解的⽅式与途径、对其他⾏业了解的状况和程度）')
    target_10 = models.IntegerField(verbose_name='性格因素（表达）')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '面试指标'
        verbose_name_plural = verbose_name


class Trainees(models.Model):
    """
    基本信息
    """
    orientation_choice = (('1', '动画'), ('2', '模型'), ('3', '解算'), ('4', '灯光'), ('5', '制片'))
    gender_choice = (('man', '男'), ('woman', '女'))
    education_choice = (('1', '研究生'), ('2', '本科'), ('3', '大专'), ('4', '高中'), ('5', '其他'))
    orientation = models.CharField(max_length=1, choices=orientation_choice, verbose_name='培养方向')
    lot = models.CharField(max_length=20, verbose_name='批次')
    entry_date = models.DateField(auto_now_add=True, verbose_name='入训日期')
    name = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='姓名')
    gender = models.CharField(max_length=5, choices=gender_choice, verbose_name='性别')
    nation = models.CharField(max_length=20, verbose_name='民族')
    native = models.CharField(max_length=20, verbose_name='籍贯')
    age = models.IntegerField(verbose_name='年龄')
    politics_status = models.CharField(max_length=20, blank=True, null=True, verbose_name='政治面貌')
    height = models.IntegerField(verbose_name='身高')
    weight = models.IntegerField(verbose_name='体重')
    school = models.CharField(max_length=40, verbose_name='毕业院校')
    major = models.CharField(max_length=40, verbose_name='专业')
    education = models.CharField(max_length=40, choices=education_choice, verbose_name='最高学历')
    phone = models.CharField(max_length=11, unique=True, verbose_name='联系电话')
    id_card = models.CharField(max_length=18, unique=True, verbose_name='身份证号码')
    address = models.CharField(max_length=100, verbose_name='通讯地址')
    education_experience = models.CharField(max_length=500, verbose_name='主要教学经历')
    family_member = models.CharField(max_length=500, verbose_name='主要家庭成员')
    emergency_contact = models.CharField(max_length=500, verbose_name='紧急联系人')
    remark = models.CharField(max_length=300, blank=True, null=True, verbose_name='备注')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '基本信息'
        verbose_name_plural = verbose_name




