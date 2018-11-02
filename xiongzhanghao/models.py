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
    title = models.CharField(verbose_name='文章标题', max_length=128)
    summary = models.CharField(verbose_name='文章摘要', max_length=256)
    content = models.TextField(verbose_name='文章内容', null=True)
    TheColumn = models.CharField(verbose_name='栏目', max_length=256, null=True, blank=True)

