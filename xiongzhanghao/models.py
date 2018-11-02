from django.db import models



# 公司表
class xzh_company(models.Model):
    name = models.CharField(verbose_name="公司名称", max_length=128)
    create_date = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    oper_user = models.ForeignKey('xzh_userprofile', verbose_name="创建用户", related_name='company_userprofile')


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
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)

    role = models.ForeignKey('xzh_role', verbose_name='所属角色', null=True, blank=True)
    company = models.ForeignKey('xzh_company', verbose_name='所属公司', null=True, blank=True)      # 超级管理员没有所属公司
    set_avator = models.CharField(verbose_name='头像', default='http://api.zhugeyingxiao.com/statics/imgs/setAvator.jpg', max_length=128)

    # userid = models.CharField(verbose_name="企业微信id", max_length=64, null=True, blank=True)

#公众号-文章表
class zgld_article(models.Model):
    user = models.ForeignKey('xzh_userprofile', verbose_name='文章作者', null=True)
    company = models.ForeignKey('xzh_company',verbose_name='文章所属公司',null=True)
    title = models.CharField(verbose_name='文章标题', max_length=128)
    summary = models.CharField(verbose_name='文章摘要', max_length=255)
    status_choices = ( (1,'已发'),
                       (2,'未发'),
                     )
    status = models.SmallIntegerField(default=2, verbose_name='文章状态', choices=status_choices)
    source_choices = ( (1,'原创'),
                       (2,'转载'),
                     )
    source = models.SmallIntegerField(default=1, verbose_name='文章来源', choices=source_choices)
    content = models.TextField(verbose_name='文章内容', null=True)
    cover_picture  = models.CharField(verbose_name="封面图片URL",max_length=128)
    read_count = models.IntegerField(verbose_name="文章阅读数量",default=0)
    forward_count = models.IntegerField(verbose_name="文章转发个数",default=0)
    comment_count = models.IntegerField(default=0,verbose_name="被评论数量")
    insert_ads = models.TextField(verbose_name='插入广告语',null=True)
    qrcode_url = models.CharField(verbose_name="二维码URL", max_length=128, null=True)
    create_date = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)
