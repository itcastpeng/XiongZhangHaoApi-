from django.db import models

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
        (2, 'PvC9'),
        (3, 'FTP')
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
    secondaryDomainName = models.CharField(verbose_name='二级域名,针对特殊用户', max_length=128, null=True, blank=True)  # 存放域名 拼接本地链接 请求到服务器
    xiongZhangHaoIndex = models.CharField(verbose_name='熊掌号主页', max_length=128, null=True, blank=True)

    deletionTime = models.DateTimeField(verbose_name='判断删除时间', null=True, blank=True) # 查询间隔时间
    user_article_result = models.TextField(verbose_name='单个用户爬取的数据', null=True, blank=True)  # 判断用户是否删除 aid title 发布时间
    # xiongzhanghaoID = models.CharField(verbose_name='熊掌号官微id', max_length=128, null=True, blank=True)
    # xiong_cookie = models.TextField(verbose_name='熊掌号cookie', null=True, blank=True) # 获取用户统计等数据
    # xiong_token = models.CharField(verbose_name='熊掌号token', max_length=32, null=True, blank=True)
    xiong_zhang_hao_user = models.CharField(verbose_name='熊掌号用户名', max_length=32, null=True, blank=True)
    xiong_zhang_hao_pwd = models.CharField(verbose_name='熊掌号密码', max_length=32, null=True, blank=True)
    xiong_zhang_hao_admin_select_time = models.DateTimeField(verbose_name='熊掌号后台查询时间', null=True, blank=True)   # 间隔时间
    fans_search_keyword = models.CharField(verbose_name='搜索关键词', max_length=64, null=True, blank=True)
    guanwang = models.CharField(verbose_name='用户官网', max_length=64, null=True, blank=True)

# 文章表
class xzh_article(models.Model):
    user = models.ForeignKey('xzh_userprofile', verbose_name='文章创建人', null=True)
    belongToUser = models.ForeignKey('xzh_userprofile', verbose_name='文章属于谁', null=True, related_name='belongToUser')
    title = models.CharField(verbose_name='文章标题', max_length=128)
    summary = models.TextField(verbose_name='文章摘要', null=True, blank=True)
    content = models.TextField(verbose_name='文章内容', null=True, blank=True)
    articlePicName = models.CharField(verbose_name='文章图片', max_length=128, null=True, blank=True)
    column_id = models.CharField(verbose_name='栏目', max_length=64, null=True, blank=True)
    create_date = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    # articlePublishedDate = models.DateField(verbose_name="文章发布时间", null=True, blank=True)
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
    DomainNameText = models.TextField(verbose_name='二级域名内容, 针对特殊用户', null=True, blank=True)  # 存放二级域名内容的字段

    is_delete = models.BooleanField(verbose_name='客户页面是否删除', default=False)
    manualRelease = models.BooleanField(verbose_name='没有兼容客户，手动发布', default=False)   # 判断是否手动发布
    select_tongji_shoulu_time = models.DateField(verbose_name='统计收录查询时间', null=True, blank=True)

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
    # article_url = models.CharField(verbose_name="匹配到的链接", max_length=256, null=True, blank=True)  # 我们发布的文章匹配到 关键词链接
    # article_rank = models.SmallIntegerField(verbose_name='匹配的链接url', null=True, blank=True)

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
    stop_check = models.BooleanField(verbose_name='是否停查', default=False)

# 覆盖报表展开详情
class xzh_fugai_baobiao_detail(models.Model):
    xzh_fugai_baobiao = models.ForeignKey('xzh_fugai_baobiao', verbose_name="覆盖表")
    link_num = models.IntegerField(verbose_name="链接数")
    cover_num = models.IntegerField(verbose_name="总覆盖")
    baobiao_url = models.TextField(verbose_name="报表地址")
    create_date = models.DateField(verbose_name="创建时间", auto_now_add=True)
    create_datetime = models.DateTimeField(verbose_name="创建时间,时分秒", auto_now_add=True)

# 熊掌号加粉
class xzh_add_fans(models.Model):
    oper_user = models.ForeignKey('xzh_userprofile', verbose_name='创建用户', related_name='xzh_add_fans_oper_user')
    belong_user = models.ForeignKey('xzh_userprofile', verbose_name='加粉用户')
    befor_add_fans = models.IntegerField(verbose_name='加粉前 粉丝数量', null=True, blank=True)
    after_add_fans = models.IntegerField(verbose_name='加粉后 粉丝数量', null=True, blank=True)
    add_fans_num = models.IntegerField(verbose_name='加粉数量', default=1)
    # xiongzhanghao_url = models.CharField(verbose_name='熊掌号官微', max_length=128, null=True, blank=True)
    # xiongzhanghaoID = models.CharField(verbose_name='熊掌号官微id', max_length=128, null=True, blank=True)
    # search_keyword = models.CharField(verbose_name='搜索关键词', max_length=64, null=True, blank=True)
    create_date = models.DateField(verbose_name="创建时间", auto_now_add=True)
    taskTimeBetween = models.DateTimeField(verbose_name="获取任务间隔", null=True, blank=True)
    status_choices = (
        (1, "未查询"),
        (2, "加粉中.."),
        (3, "加粉完成"),
        (4, "已完成"),
        (5, "异常")
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices, default=1)
    errorText = models.CharField(verbose_name='错误日志', max_length=128, null=True, blank=True)

# 缩略图  固定数据
class xzh_suoluetu(models.Model):
    man = models.CharField(verbose_name='男科缩略图', max_length=128, null=True, blank=True)
    woman = models.CharField(verbose_name='妇科缩略图', max_length=128, null=True, blank=True)

# 用户数据统计表
class user_statistics(models.Model):
    create_date = models.DateField(verbose_name="创建时间", null=True, blank=True)
    belong_user = models.ForeignKey('xzh_userprofile', verbose_name='归属用户')
    public_num = models.IntegerField(verbose_name='发布数量', default=0)

    zhishu = models.IntegerField(verbose_name='指数', default=0)
    zhanxianliang = models.IntegerField(verbose_name='展现量', default=0)
    dianjiliang = models.IntegerField(verbose_name='点击量', default=0)

    fans_num = models.IntegerField(verbose_name='粉丝数量', default=0)
    baidu_shoulu = models.IntegerField(verbose_name='百度收录', default=0)                        # 百度收录条数
    baidu_shoulu_url = models.TextField(verbose_name='百度收录url', default='[]')                 # 百度收录 详情
    index_show = models.IntegerField(verbose_name='主页展示条数', default=0)                       # 熊掌号主页 条数 想当于收录条数
    index_show_url = models.TextField(verbose_name='主页展示的url', null=True, blank=True)        # 熊掌号主页 详情
    admin_shoulu = models.IntegerField(verbose_name='熊掌号后后台收录', default=0)                 # 熊掌号后台 收录条数
    admin_shoulu_url = models.TextField(verbose_name='熊掌号后台收录详情', null=True, blank=True)  # 熊掌号后台 收录详情

    zhoumo = models.BooleanField(verbose_name='是否为周末', default=False)

# 用户 计费
class user_billing(models.Model):
    create_date = models.DateField(verbose_name="创建时间", auto_now_add=True)
    belong_user = models.ForeignKey('xzh_userprofile', verbose_name='归属用户', related_name='user_biling_belong_user')
    create_user = models.ForeignKey('xzh_userprofile', verbose_name='创建人', null=True, blank=True)
    start_time = models.DateField(verbose_name='开始计费日期', null=True, blank=True)
    stop_time = models.DateField(verbose_name='结束计费日期', null=True, blank=True)
    billing_cycle_choices = (
        (1, '一个月'),
        (2, '二个月'),
        (3, '三个月'),
        (4, '四个月'),
        (5, '五个月'),
        (6, '六个月'),
        (7, '十二个月'),
    )
    billing_cycle = models.SmallIntegerField(verbose_name='计费周期', choices=billing_cycle_choices, default=1)
    note_text = models.TextField(verbose_name='备注', default='无')


#===============================================================百度小程序===================================================================================

# 用户表
class xcx_userprofile(models.Model):
    username = models.CharField(verbose_name="用户账号", max_length=128)
    password = models.CharField(verbose_name="用户密码", max_length=128)
    token = models.CharField(verbose_name="token值", max_length=128)
    oper_user = models.ForeignKey('xcx_userprofile', verbose_name="创建用户", related_name='userprofile_self', null=True, blank=True)

    create_date = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    status_choices = (
        (1, '启用'),
        (2, '不启用'),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)
    lunbotu = models.TextField(verbose_name='轮播图', null=True, blank=True)
    hospital_logoImg = models.CharField(verbose_name='logo图片', max_length=128, null=True, blank=True)
    hospital_phone = models.CharField(verbose_name='医院电话', max_length=32, null=True, blank=True)
    hospital_introduction = models.TextField(verbose_name='医院简介', null=True, blank=True)
    hospital_address = models.CharField(verbose_name='医院地址', max_length=128, null=True, blank=True)
    hospital_menzhen = models.CharField(verbose_name='门诊时间', max_length=128, null=True, blank=True)
    x_shaft = models.CharField(verbose_name= 'X轴', max_length=64, null=True, blank=True)
    y_shaft = models.CharField(verbose_name='Y轴', max_length=64, null=True, blank=True)

# 栏目管理
class xcx_program_management(models.Model):
    program_name = models.CharField(verbose_name='栏目名称', max_length=64)
    belongUser = models.ForeignKey('xcx_userprofile', verbose_name="创建用户", null=True, blank=True)
    program_type_choices = (
        (1, '列表页'),
        (2, '单页')
    )
    program_type = models.SmallIntegerField(verbose_name='栏目类型', choices=program_type_choices, default=1)
    program_text = models.TextField(verbose_name='单页设置内容', null=True, blank=True)    # 详情页设置内容
    create_date = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    suoluetu = models.CharField(verbose_name='缩略图', max_length=128, null=True, blank=True) # 栏目缩略图


# 文章表
class xcx_article(models.Model):
    user = models.ForeignKey('xcx_userprofile', verbose_name='文章创建人', null=True)
    belongToUser = models.ForeignKey('xcx_userprofile', verbose_name='文章属于谁', null=True, related_name='belongToUser')
    title = models.CharField(verbose_name='文章标题', max_length=128)
    content = models.TextField(verbose_name='文章内容', null=True, blank=True)
    create_date = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    article_status_choices = (
        (1, '显示'),
        (2, '不显示'),
    )
    article_status = models.SmallIntegerField(verbose_name='文章状态',choices=article_status_choices, default=1)
    article_type_choices = (
        (1, '新闻中心'),
        (2, '专家团队'),
        (3, '特色医疗'),
    )
    article_type = models.SmallIntegerField(verbose_name='文章类型', default=1, choices=article_type_choices)
    article_program = models.ForeignKey('xcx_program_management', verbose_name='归属栏目')
    suoluetu = models.CharField(verbose_name='缩略图', max_length=128, null=True, blank=True)
    article_introduction = models.CharField(verbose_name='文章简介', max_length=256, null=True, blank=True)















