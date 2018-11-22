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
from api.views_dir import select_keywords_cover, generateThePage, getCookieAndColumn, articleScriptOper, \
    theScheduler, init_fugai_baobiao, init_fugai_detail, selectDeleteQuery

urlpatterns = [

    # # 权限管理
    # url(r'^permissions/(?P<oper_type>\w+)/(?P<o_id>\d+)$', permissions.permissions_oper),
    # url(r'^permissions$', permissions.permissions),

    # 调度器 分配任务
    url(r'theScheduler$', theScheduler.theScheduler),

    # 查关键词覆盖
    url(r'select_keywords_cover$', select_keywords_cover.select_keywords_cover),

    # 二级域名
    url(r'SearchSecondary/(?P<article_id>\d+)$', generateThePage.SearchSecondaryDomainName),  # 查询二级域名
    url(r'specialUserGenerateThePage$', generateThePage.specialUserGenerateThePage),  # 生成二级域名

    # 获取栏目及cookie
    url(r'userGetCookieOper/(?P<oper_type>\w+)$', getCookieAndColumn.userGetCookieOper),

    # 文章脚本操作
    url(r'articleScriptOper/(?P<oper_type>\w+)$', articleScriptOper.articleScriptOper), # 文章操作 审核 提交熊掌号 发布文章

    # 初始化覆盖报表中的数据
    url(r'init_fugai_baobiao$', init_fugai_baobiao.init_fugai_baobiao),

    # 更新覆盖报表详情数据
    url(r'statisticalReports$', init_fugai_detail.statisticalReports),

    # 查询客户网站该文章是否删除 做出提示
    url(r'deleteQuery', selectDeleteQuery.deleteQuery),

]







