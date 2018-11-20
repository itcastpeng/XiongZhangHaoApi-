"""XiongZhangHaoApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from xiongzhanghao.views_dir import login, company, permissions, role, user, article, img_upload, fugai_baobiao, keywords

urlpatterns = [
    # 登录
    url(r'^login$', login.login),

    # # 公司管理
    # url(r'^company/(?P<oper_type>\w+)/(?P<o_id>\d+)$', company.company_oper),
    # url(r'^company', company.company),

    # 权限管理
    url(r'^permissions/(?P<oper_type>\w+)/(?P<o_id>\d+)$', permissions.permissions_oper),
    url(r'^permissions$', permissions.permissions),

    # 角色管理
    url(r'^role/(?P<oper_type>\w+)/(?P<o_id>\d+)$', role.role_oper),
    url(r'^role$', role.role),

    # 用户管理
    url(r'^user/(?P<oper_type>\w+)/(?P<o_id>\d+)$', user.user_oper),
    url(r'^userGetCookieOper/(?P<oper_type>\w+)$', user.userGetCookieOper),   # 获取栏目及cookie
    url(r'^user$', user.user),

    # 文章管理
    url(r'^article/(?P<oper_type>\w+)/(?P<o_id>\d+)$', article.article_oper),
    url(r'^articleScriptOper/(?P<oper_type>\w+)$', article.articleScriptOper), # 文章操作 审核 提交熊掌号 发布文章
    url(r'^article', article.article),

    # 关键词管理
    url(r'^keywords/(?P<oper_type>\w+)/(?P<o_id>\d+)$', keywords.keywords_oper),
    url(r'^keywords', keywords.keywords),

    # 覆盖报表
    url(r'^fugai_baobiao/(?P<oper_type>\w+)/(?P<o_id>\d+)$', fugai_baobiao.fugai_baobiao_oper),
    url(r'^fugai_baobiao', fugai_baobiao.fugai_baobiao),

    # 上传文件
    url(r'^image_upload', img_upload.image_upload),


]







