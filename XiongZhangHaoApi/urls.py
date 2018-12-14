"""XiongZhangHaoApi URL Configuration

The `urlpatterns` list routes URLs to views_dir. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views_dir
    1. Add an import:  from my_app import views_dir
    2. Add a URL to urlpatterns:  path('', views_dir.home, name='home')
Class-based views_dir
    1. Add an import:  from other_app.views_dir import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from xiongzhanghao.views_dir import login, permissions, role, user, article, img_upload, fugai_baobiao, keywords, add_fans, userStatistics, user_billing_statistics


urlpatterns = [

    url(r'^api', include('api.urls')),
    url(r'^xiaochengxu', include('baiduxiaochengxu.urls')),


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
    url(r'^user$', user.user),
    url(r'^updatePwd', user.updatePwd),

    # 文章管理
    url(r'^article/(?P<oper_type>\w+)/(?P<o_id>\d+)$', article.article_oper),
    url(r'^article', article.article),

    # 关键词管理
    url(r'^keywords/(?P<oper_type>\w+)/(?P<o_id>\d+)$', keywords.keywords_oper),
    url(r'^keywords', keywords.keywords),

    # 覆盖报表
    url(r'^fugai_baobiao/(?P<oper_type>\w+)/(?P<o_id>\d+)$', fugai_baobiao.fugai_baobiao_oper),
    url(r'^fugai_baobiao', fugai_baobiao.fugai_baobiao),

    # 上传文件
    url(r'^image_upload$', img_upload.image_upload),
    url(r'img_upload/(?P<oper_type>\w+)$', img_upload.img_upload),

    # 加粉功能
    url(r'fans/(?P<oper_type>\w+)/(?P<o_id>\d+)$', add_fans.fans_oper),
    url(r'fans', add_fans.fans),

    # 用户数据统计
    url(r'userStatistics/(?P<oper_type>\w+)/(?P<o_id>\d+)$', userStatistics.userStatistics_oper),
    url(r'userStatistics', userStatistics.userStatistics),

    # 用户计费统计
    url(r'user_billing/(?P<oper_type>\w+)/(?P<o_id>\d+)$', user_billing_statistics.user_billing_oper),
    url(r'user_billing', user_billing_statistics.user_billing),
]






