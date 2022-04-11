from django.db import models


class Menu(models.Model):
    """
    权限
    """
    title = models.CharField(max_length=32, unique=True, verbose_name='权限名')
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name='父菜单', on_delete=models.CASCADE)
    url = models.CharField(max_length=128, null=True, blank=True)
    icon = models.CharField(max_length=20, null=True, blank=True, verbose_name='图标')

    def __str__(self):
        title_list = [self.title]
        p = self.parent
        while p:
            title_list.insert(0, p.title)
            p = p.parent
        return '-'.join(title_list)

    class Meta:
        verbose_name = '权限'
        verbose_name_plural = verbose_name

    @classmethod
    def getMenuByRequestUrl(self, url):
        ret = dict(menu=Menu.objects.get(url=url))
        return ret


class Role(models.Model):
    """
    角色：绑定权限
    """
    title = models.CharField(max_length=32, verbose_name='角色名')
    permissions = models.ManyToManyField("Menu", blank=True, verbose_name='拥有权限')

    def get_user_list(self):
        return self.userprofile_set.all()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = verbose_name
