from django.contrib import admin

from .models import Menu, Role


class MenuAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'url', 'parent']
    list_filter = ['parent']
    search_fields = ['id', 'title', 'url']
    list_editable = ['url']


class RoleAdmin(admin.ModelAdmin):
    list_display = ['title']


admin.site.register(Menu, MenuAdmin)
admin.site.register(Role, RoleAdmin)