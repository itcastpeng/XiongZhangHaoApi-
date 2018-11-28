from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab

app = Celery(
    broker='redis://redis_host:6379/4',
    # broker='redis://127.0.0.1:6379/0',
    backend='redis://redis_host:6379/4',
    # backend='redis://127.0.0.1:6379/0',
    include=['XiongZhangHaoApi_celery.tasks'],

)
app.conf.enable_utc = False
app.conf.timezone = "Asia/Shanghai"
CELERYD_FORCE_EXECV = True    # 非常重要,有些情况下可以防止死锁
CELERYD_MAX_TASKS_PER_CHILD = 100    # 每个worker最多执行万100个任务就会被销毁，可防止内存泄露
app.conf.beat_schedule = {
    # 1分钟一次
    # 生成二级域名
    'specialUserGenerateThePage':{
        'task':'XiongZhangHaoApi_celery.tasks.specialUserGenerateThePage',
        # 'schedule':30                                   # 秒
        'schedule': crontab("*/1", '*', '*', '*', '*'),  # 此处跟 linux 中 crontab 的格式一样
        # 'schedule': crontab("5", '9, 11', '*', '*', '*'),  # 9点一次  11点一次
        # 'schedule': crontab(hour=8, minute=30),
    },

    # 初始化覆盖报表数据
    'init_fugai_baobiao':{
        'task': 'XiongZhangHaoApi_celery.tasks.init_fugai_baobiao',
        'schedule': crontab("*/10", '*', '*', '*', '*'),
    },


    # 提交熊掌号
    'celerySubmitXiongZhangHao':{
        'task': 'XiongZhangHaoApi_celery.tasks.celerySubmitXiongZhangHao',
        'schedule': crontab("*/10", '*', '*', '*', '*'),  # 此处跟 linux 中 crontab 的格式一样
    },

    # 更新覆盖报表详情数据
    'update_fugai_baobiao_detail':{
        'task': 'XiongZhangHaoApi_celery.tasks.update_fugai_baobiao_detail',
        'schedule': crontab("*/10", '*', '*', '*', '*'),  # 此处跟 linux 中 crontab 的格式一样
    },

    # 判断文章是否被删除   #每一小时执行一次
    'selectDeleteQuery':{
        'task': 'XiongZhangHaoApi_celery.tasks.selectDeleteQuery',
        'schedule': crontab("*/60", '*', '*', '*', '*'),  # 此处跟 linux 中 crontab 的格式一样
    },

    # 定时刷新 粉丝量 60s
    'queryFollowersNum':{
        'task': 'XiongZhangHaoApi_celery.tasks.queryFollowersNum',
        # 'schedule': crontab("*/60", '*', '*', '*', '*'),  # 此处跟 linux 中 crontab 的格式一样
        'schedule':60
    },

}
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
