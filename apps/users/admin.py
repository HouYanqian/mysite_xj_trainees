from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy

from users.models import UserProfile
# Register your models here.


class UserProfileAdmin(UserAdmin):
    list_display = ['username', 'name', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'last_login']
    fieldsets = (
        (None, {'fields': ['username', 'password', 'name', 'email', 'roles', 'image']}),

        ('状态', {'fields': ['is_superuser', 'is_staff', 'is_active']}),

        (gettext_lazy('Important dates'), {'fields': ['last_login', 'date_joined']}),
    )
    # 分栏显示


admin.site.register(UserProfile, UserProfileAdmin)
