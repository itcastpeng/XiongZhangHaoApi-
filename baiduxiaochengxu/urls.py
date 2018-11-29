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
from baiduxiaochengxu.views_dir import login, user,  article, program
from baiduxiaochengxu.xiaochengxu_view import xzx_article, xzx_program, xzx_user
urlpatterns = [
    # ==============================================后台=====================================================
    # 登录
    url(r'login$', login.login),

    # 用户管理
    url(r'user/(?P<oper_type>\w+)/(?P<o_id>\d+)$', user.user_oper),
    url(r'user$', user.user),

    # 文章管理
    url(r'article/(?P<oper_type>\w+)/(?P<o_id>\d+)$', article.article_oper),
    url(r'article', article.article),

    # 栏目管理
    url(r'program/(?P<oper_type>\w+)/(?P<o_id>\d+)$', program.program_oper),
    url(r'program', program.program),


    # =============================================小程序========================================================

    # 文章管理
    url(r'xzx_article', xzx_article.article),

    # 栏目管理
    url(r'xzx_program', xzx_program.program),

    # 用户管理
    url(r'xzx_user', xzx_user.user),
]







