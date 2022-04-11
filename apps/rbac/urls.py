from django.conf.urls import url

from rbac.views import RoleView, RoleUpdateView, MenuAddView, MenuEditView, MenuDelView

app_name = '[rbac]'

urlpatterns = [
    # 角色管理
    url(r'^role/$', RoleView.as_view(), name="role-index"),
    url(r'^role/update', RoleUpdateView.as_view(), name="role-update"),

    # 角色菜单管理
    url(r'^menu/add', MenuAddView.as_view(), name="menu-add"),
    url(r'^menu/edit', MenuEditView.as_view(), name="menu-edit"),
    url(r'^menu/del', MenuDelView.as_view(), name="menu-del"),
]
