from django.db import models


#
# # 公司表
# class xzh_company(models.Model):
#     name = models.CharField(verbose_name="公司名称", max_length=128)
#     create_date = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
#     oper_user = models.ForeignKey('xzh_userprofile', verbose_name="创建用户", related_name='company_userprofile')
#

# 角色表
class xzh_role(models.Model):
    name = models.CharField(verbose_name="角色名称", max_length=128)
    create_date = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    oper_user = models.ForeignKey('xzh_userprofile', verbose_name="创建用户", related_name='role_user')
    permissions = models.ManyToManyField('xzh_permissions', verbose_name="拥有权限")


# 权限表
class xzh_permissions(models.Model):
    name = models.CharField(verbose_name="权限名称", max_length=128)
    title = models.CharField(verbose_name="权限标题", max_length=128)
    pid = models.ForeignKey('self', verbose_name="父级权限", null=True, blank=True)
    create_date = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    oper_user = models.ForeignKey('xzh_userprofile', verbose_name="创建用户", related_name='permissions_user')


# 用户表
class xzh_userprofile(models.Model):
    username = models.CharField(verbose_name="用户账号", max_length=128)
    password = models.CharField(verbose_name="用户密码", max_length=128)
    token = models.CharField(verbose_name="token值", max_length=128)
    oper_user = models.ForeignKey('xzh_userprofile', verbose_name="创建用户", related_name='userprofile_self', null=True, blank=True)

    create_date = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    status_choices = (
        (1, '启用'),
        (2, '不启用'),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)

    role = models.ForeignKey('xzh_role', verbose_name='所属角色', null=True, blank=True)
    # company = models.ForeignKey('xzh_company', verbose_name='所属公司', null=True, blank=True)      # 超级管理员没有所属公司
    set_avator = models.CharField(verbose_name='头像', default='http://api.zhugeyingxiao.com/statics/imgs/setAvator.jpg', max_length=128)

    website_backstage_choices = (
        (1, '织梦'),
    )
    website_backstage = models.SmallIntegerField(verbose_name='网站后台类型', choices=website_backstage_choices, default=1)
    website_backstage_url = models.CharField(verbose_name='客户后台网站地址', max_length=128, null=True, blank=True)
    website_backstage_username = models.CharField(verbose_name='客户后台账号', max_length=64, null=True, blank=True)
    website_backstage_password = models.CharField(verbose_name='客户后台密码', max_length=64, null=True, blank=True)
    is_debug = models.BooleanField(verbose_name='是否调试', default=False) # 为True 才可以发布文章
    cookies = models.TextField(verbose_name='cookies', null=True, blank=True)
    column_all = models.TextField(verbose_name='所有栏目', null=True, blank=True)
    website_backstage_token = models.CharField(verbose_name='熊掌号token', max_length=64, null=True, blank=True)
    website_backstage_appid = models.CharField(verbose_name='熊掌号appid', max_length=64, null=True, blank=True)

    userType_choices = (
        (1,'普通用户'),
        (2,'特殊用户')
    )
    userType = models.SmallIntegerField(verbose_name='用户类型', default=1)
    secondaryDomainName = models.CharField(verbose_name='二级域名,针对特殊用户', max_length=128, null=True, blank=True)
    xiongZhangHaoIndex = models.CharField(verbose_name='熊掌号主页', max_length=128, null=True, blank=True)

    deletionTime = models.DateTimeField(verbose_name='判断删除时间', null=True, blank=True) # 查询间隔时间
    user_article_result = models.TextField(verbose_name='单个用户爬取的数据', null=True, blank=True)  # 判断用户是否删除 aid title 发布时间

# 公众号-文章表
class xzh_article(models.Model):
    user = models.ForeignKey('xzh_userprofile', verbose_name='文章创建人', null=True)
    belongToUser = models.ForeignKey('xzh_userprofile', verbose_name='文章属于谁', null=True, related_name='belongToUser')
    title = models.CharField(verbose_name='文章标题', max_length=128)
    summary = models.TextField(verbose_name='文章摘要', null=True, blank=True)
    content = models.TextField(verbose_name='文章内容', null=True, blank=True)
    articlePicName = models.CharField(verbose_name='文章图片', max_length=128, null=True, blank=True)
    column_id = models.CharField(verbose_name='栏目', max_length=64, null=True, blank=True)
    create_date = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    article_status_choices = (
        (1, '发布中'),
        (2, '发布成功, 待审核'),
        (3, '发布失败'),
        (4, '审核成功, 提交中'),
        (5, '已完成'),
        (6, '特殊用户, 生成页面中'),
    )
    article_status = models.SmallIntegerField(verbose_name='文章状态',choices=article_status_choices, default=1)
    back_url = models.CharField(verbose_name='回链地址', max_length=128, null=True, blank=True)
    note_content = models.CharField(verbose_name='错误备注', max_length=256, default='无')
    send_time = models.DateTimeField(verbose_name='定时发送文章', null=True, blank=True)
    aid = models.IntegerField(verbose_name='文章发布id', null=True, blank=True)
    is_audit = models.BooleanField(verbose_name='是否审核', default=False)
    DomainNameText = models.TextField(verbose_name='二级域名内容, 针对特殊用户', null=True, blank=True)

    is_delete = models.BooleanField(verbose_name='客户页面是否删除', default=False)
    manualRelease = models.BooleanField(verbose_name='没有兼容客户，手动发布', default=False)

# 关键词表
class xzh_keywords(models.Model):
    user = models.ForeignKey('xzh_userprofile', verbose_name="所属用户")
    keywords = models.CharField(verbose_name="关键词", max_length=128)
    create_date = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    get_date = models.DateTimeField(verbose_name="获取时间", null=True, blank=True)     # 该时间控制每个词在5分钟之内只被查询一次
    select_date = models.DateTimeField(verbose_name="查询时间", null=True, blank=True)


# 关键词覆盖表
class xzh_keywords_detail(models.Model):
    xzh_keywords = models.ForeignKey('xzh_keywords', verbose_name="关键词")
    url = models.CharField(verbose_name="匹配到的链接", max_length=256)
    rank = models.SmallIntegerField(verbose_name="排名")
    create_date = models.DateField(verbose_name="创建时间", auto_now_add=True)


# 覆盖报表
class xzh_fugai_baobiao(models.Model):
    user = models.ForeignKey('xzh_userprofile', verbose_name="所属用户")
    keywords_num = models.IntegerField(verbose_name="关键词总数")

    status_choices = (
        (1, "查询中"),
        (2, "查询完成"),
    )
    status = models.SmallIntegerField(verbose_name="查询状态", default=1, choices=status_choices)

    today_cover = models.IntegerField(verbose_name="今日覆盖")
    total_cover = models.IntegerField(verbose_name="总覆盖")
    publish_num = models.IntegerField(verbose_name="总发布篇数")
    create_date = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)


# 覆盖报表展开详情
class xzh_fugai_baobiao_detail(models.Model):
    xzh_fugai_baobiao = models.ForeignKey('xzh_fugai_baobiao', verbose_name="覆盖表")
    link_num = models.IntegerField(verbose_name="链接数")
    cover_num = models.IntegerField(verbose_name="总覆盖")
    baobiao_url = models.TextField(verbose_name="报表地址")
    create_date = models.DateField(verbose_name="创建时间", auto_now_add=True)

# 判断客户后台是否删除了文章 该表存取客户后台aid 和 标题
# class xzh_customer_background_background_is_deleted(models.Model):
#     user_background = models.ForeignKey('xzh_userprofile', verbose_name='文章归属人', null=True)
#     aid = models.IntegerField(verbose_name='aid')
#     title = models.CharField(verbose_name='标题', max_length=64)
#     releaseTime = models.DateField(verbose_name='发布时间', null=True, blank=True)






