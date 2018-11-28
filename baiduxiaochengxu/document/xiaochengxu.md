

#### 登录 说明
```
http请求：POST
http请求url：http://127.0.0.1:8003/xiaochengxu/login

参数                      请求方式           必须                     说明
username                    POST            是                       用户名
password                    POST            是                       用户密码
```

#### 角色管理 查询说明
``` 
http请求：GET
http请求url:http://127.0.0.1:8003/xiaochengxu/role?user_id=1&timestamp=123&rand_str=e43ad72eb271958a26328f4a81af3812

返回说明 （正常时返回的json数据 示例）
      
{
    "code":200,
    "msg":"查询成功",
    "data":{
        "ret_data":[
            {
                "id":1,
                "create_date":"2018-11-26 17:16:08",
                "permissionsData":"[{"expand": true, "id": 12, "title": "\u7528\u6237\u7ba1\u7406", "children": [{"expand": true, "id": 32, "title": "\u7528\u6237\u9996\u9875", "checked": false}], "checked": false}, {"expand": true, "id": 35, "title": "\u89d2\u8272\u7ba1\u7406", "children": [{"expand": true, "id": 36, "title": "\u89d2\u8272\u9996\u9875", "checked": false}], "checked": false}, {"expand": true, "id": 37, "title": "\u6743\u9650\u7ba1\u7406", "children": [{"expand": true, "id": 38, "title": "\u6743\u9650\u7ba1\u7406", "checked": false}], "checked": false}, {"expand": true, "id": 39, "title": "\u6587\u7ae0\u7ba1\u7406", "children": [{"expand": true, "id": 40, "title": "\u6587\u7ae0\u9996\u9875", "checked": false}], "checked": false}]",
                "name":"超级管理员",
                "oper_user__username":"赵欣鹏"
            }
        ],
        "data_count":1
    }
}
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






