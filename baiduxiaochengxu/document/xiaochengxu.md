

#### 登录 说明
```
http请求：POST
http请求url：http://127.0.0.1:8003/xiaochengxu/login

参数                      请求方式           必须                     说明
username                    POST            是                       用户名
password                    POST            是                       用户密码
```

#### 用户管理 添加说明
``` 
http请求：PSOT
http请求url:http://127.0.0.1:8003/xiaochengxu/user/add/0?user_id=1&timestamp=123&rand_str=e43ad72eb271958a26328f4a81af3812
参数                      请求方式           必须                     说明
username                 用户名称            是                     用户名称   
role_id                 角色ID              是                     角色ID
password                密码                是                     用户密码

返回说明 （正常时返回的json数据 示例）
{
    "msg": "添加成功",
    "data": {},
    "code": 200
}
```

#### 用户管理 修改说明
``` 
http请求：PSOT
http请求url:http://127.0.0.1:8003/xiaochengxu/user/update/4?user_id=1&timestamp=123&rand_str=e43ad72eb271958a26328f4a81af3812
参数                      请求方式           必须                     说明
username                 用户名称            是                     用户名称   
role_id                 角色ID              是                     角色ID

返回说明 （正常时返回的json数据 示例）
{
    "msg": "修改成功",
    "data": {},
    "code": 200
}
``` 

#### 用户管理 删除说明
``` 
http请求：PSOT
http请求url:http://127.0.0.1:8003/xiaochengxu/user/delete/4?user_id=1&timestamp=123&rand_str=e43ad72eb271958a26328f4a81af3812
参数                      请求方式           必须                     说明

返回说明 （正常时返回的json数据 示例）
{
    "msg": "删除成功",
    "data": {},
    "code": 200
}
```

#### 用户管理 查询说明
``` 
http请求：GET
http请求url:http://127.0.0.1:8003/xiaochengxu/user?user_id=1&timestamp=123&rand_str=e43ad72eb271958a26328f4a81af3812
参数                      请求方式           必须                     说明

返回说明 （正常时返回的json数据 示例）
{
    "code": 200,
    "msg": "查询成功",
    "data": {
        "ret_data": [
            {
                "id": 3,
                "username": "赵欣鹏1",
                "create_date": "2018-11-26T20:09:09",
                "role_name": "超级管理员",
                "oper_user_id": 1,
                "oper_user": "赵欣鹏",
                "role": 1
            },
            {
                "id": 1,
                "username": "赵欣鹏",
                "create_date": "2018-11-26T17:15:47",
                "role_name": "超级管理员",
                "oper_user_id": 1,
                "oper_user": "赵欣鹏",
                "role": 1
            }
        ]
    }
}
```


#### 栏目管理 添加说明
```
http请求：POST
http请求url:http://127.0.0.1:8003/xiaochengxu/user?user_id=1&timestamp=123&rand_str=e43ad72eb271958a26328f4a81af3812
参数                      请求方式           必须                     说明
program_name                POST            是                   栏目名称
program_teyp                POST            是                   栏目类型
program_text                POST            否                   如果栏目类型为1列表型 该字段为空 类型为2单页型 该字段: 单页内容有值

返回说明 （正常时返回的json数据 示例）
{
    "data": {},
    "code": 200,
    "msg": "添加成功"
}
```

#### 栏目管理 修改说明
```
http请求：POST
http请求url:http://127.0.0.1:8003/xiaochengxu/program/update/2?user_id=1&timestamp=123&rand_str=e43ad72eb271958a26328f4a81af3812
参数                      请求方式           必须                     说明
program_name                POST            是                   栏目名称
program_teyp                POST            是                   栏目类型
program_text                POST            否                   如果栏目类型为1列表型 该字段为空 类型为2单页型 该字段: 单页内容有值

返回说明 （正常时返回的json数据 示例）
{
    "data": {},
    "code": 200,
    "msg": "修改成功"
}
```

#### 栏目管理 删除说明
```
http请求：POST
http请求url:http://127.0.0.1:8003/xiaochengxu/program/delete/2?user_id=1&timestamp=123&rand_str=e43ad72eb271958a26328f4a81af3812
参数                      请求方式           必须                     说明

返回说明 （正常时返回的json数据 示例）
{
    "data": {},
    "code": 200,
    "msg": "删除成功"
}
```

#### 栏目管理 查询说明
```
http请求：POST
http请求url:http://127.0.0.1:8003/xiaochengxu/program?user_id=1&timestamp=123&rand_str=e43ad72eb271958a26328f4a81af3812
参数                      请求方式           必须                     说明

返回说明 （正常时返回的json数据 示例）
{
    "data": {
        "ret_data": [
            {
                "belongUser": "赵欣鹏",
                "create_date": "2018-11-28 14:17:45",
                "program_type_id": 1,
                "program_type": "列表页",
                "belongUser_id": 1,
                "id": 1,
                "program_name": "栏目1"
            }
        ],
        "type_list": [
            [
                1,
                "列表页"
            ],
            [
                2,
                "单页"
            ]
        ]
    },
    "msg": "查询成功",
    "code": 200
}
```


#### 文章管理 添加说明
```
http请求：POST
http请求url:http://127.0.0.1:8003/xiaochengxu/article/add/0?user_id=1&timestamp=123&rand_str=e43ad72eb271958a26328f4a81af3812
参数                      请求方式           必须                     说明
title                       POST            是                   文章标题
content                     POST            是                   文章内容    
belongToUser_id             POST            是                   文章归属人
article_program_id          POST            是                   文章归属栏目

返回说明 （正常时返回的json数据 示例）
{
    "data": {},
    "msg": "添加成功",
    "code": 200
}
```

#### 文章管理 修改说明
```
http请求：POST
http请求url:http://127.0.0.1:8003/xiaochengxu/article/update/3?user_id=1&timestamp=123&rand_str=e43ad72eb271958a26328f4a81af3812
参数                      请求方式           必须                     说明
title                       POST            是                   文章标题
content                     POST            是                   文章内容    
belongToUser_id             POST            是                   文章归属人
article_program_id          POST            是                   文章归属栏目

{
    "data": {},
    "msg": "修改成功",
    "code": 200
}  "code": 200
```

#### 文章管理 删除说明
```
http请求：POST
http请求url:http://127.0.0.1:8003/xiaochengxu/article/delete/2?user_id=1&timestamp=123&rand_str=e43ad72eb271958a26328f4a81af3812
参数                      请求方式           必须                     说明

{
    "data": {},
    "msg": "删除成功",
    "code": 200
}
```

#### 文章管理 查询说明
```
http请求：GET
http请求url:http://127.0.0.1:8003/xiaochengxu/article?user_id=1&timestamp=123&rand_str=e43ad72eb271958a26328f4a81af3812
参数                      请求方式           必须                     说明

{
    "msg": "查询成功",
    "code": 200,
    "data": {
        "ret_data": [
            {
                "title": "标题阿达是",
                "id": 3,
                "user_name": "赵欣鹏",
                "content": "内容阿萨德",
                "create_date": "2018-11-28 14:58:58",
                "belongToUser_id": 3,
                "belongToUser_name": "赵欣鹏1",
                "user_id": 1
            },
            {
                "title": "标题",
                "id": 1,
                "user_name": "赵欣鹏",
                "content": "内容",
                "create_date": "2018-11-26 20:12:09",
                "belongToUser_id": 3,
                "belongToUser_name": "赵欣鹏1",
                "user_id": 1
            }
        ]
    }
}
```
















