from django.db import models
from django.contrib.auth.models import AbstractUser

from rbac.models import Role


class UserProfile(AbstractUser):
    name = models.CharField(max_length=20, default="", verbose_name="姓名")
    roles = models.ManyToManyField("rbac.Role", verbose_name="角色", blank=True)
    image = models.ImageField(upload_to='user/%Y-%m-%d/', blank=True, null=True, verbose_name='头像')


    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name
