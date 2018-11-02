from django.conf.urls import url, include
from django.contrib import admin
from xiongzhanghao.views_dir import login, company, permissions, role, user


urlpatterns = [
    # 登录
    url(r'^login$', login.login),

    # 公司管理
    url(r'^company/(?P<oper_type>\w+)/(?P<o_id>\d+)$', company.company_oper),
    url(r'^company', company.company),

    # 权限管理
    url(r'^permissions/(?P<oper_type>\w+)/(?P<o_id>\d+)$', permissions.permissions_oper),
    url(r'^permissions$', permissions.permissions),

    # 角色管理
    url(r'^role/(?P<oper_type>\w+)/(?P<o_id>\d+)$', role.role_oper),
    url(r'^role$', role.role),

    # 用户管理
    url(r'^user/(?P<oper_type>\w+)/(?P<o_id>\d+)$', user.user_oper),
    url(r'^user$', user.user),


]







