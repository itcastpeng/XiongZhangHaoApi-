



#### 角色管理 添加说明
``` 
http请求：POST
http请求url：http://127.0.0.1:8000/xiong/role/add/0?user_id=1&timestamp=123&rand_str=7e0fc6b6833ebe0347ab6a5945d519ea&company_id=1
参数                      请求方式           必须                     说明
company_id                  GET             是                       公司ID
name                        POST            是                       角色名称
permissionsList             POST            是                       权限 可选多个 [1,2,3]数组格式

返回说明 （正常时返回的json数据 示例）
{
    "data": {
        "testCase": 40
    },
    "msg": "添加成功",
    "code": 200
}
```

#### 角色管理 修改说明
``` 
http请求：POST
http请求url:http://127.0.0.1:8000/xiong/role/update/8?user_id=1&timestamp=123&rand_str=7e0fc6b6833ebe0347ab6a5945d519ea
参数                      请求方式           必须                     说明
name                        POST            否                     角色名称  
permissionsList             POST            否                     权限 可选多个 [1,2,3]数组格式

返回说明 （正常时返回的json数据 示例）
{
    "data": {},
    "msg": "修改成功",
    "code": 200
}
```

#### 角色管理 删除说明
``` 
http请求：POST
http请求url:http://127.0.0.1:8000/xiong/role/delete/32?user_id=1&timestamp=123&rand_str=7e0fc6b6833ebe0347ab6a5945d519ea
参数                      请求方式           必须                     说明

返回说明 （正常时返回的json数据 示例）
{
    "data": {},
    "msg": "删除成功",
    "code": 200
}
```

#### 角色管理 查询说明
``` 
http请求：GET
http请求url:http://127.0.0.1:8000/xiong/role?user_id=1&timestamp=123&rand_str=7e0fc6b6833ebe0347ab6a5945d519ea&company_id=1

返回说明 （正常时返回的json数据 示例）
{
    "msg": "查询成功",
    "data": {
        "ret_data": [
            {
                "id": 1,
                "create_date": "2018-11-02 10:16:39",
                "oper_user__username": "赵欣鹏",
                "permissionsData": "[]",
                "name": "管理员"
            }
        ],
        "data_count": 1
    },
    "code": 200
}
```

#### 用户管理 添加说明
``` 
http请求：PSOT
http请求url:http://127.0.0.1:8001/api/testCaseDetaile/sendTheRequest/0?user_id=10&rand_str=2be6ba2fa87950c7fb15c5c358722408&timestamp=1534157927644
参数                      请求方式           必须                     说明
username                 用户名称            是                     用户名称   
role_id                 角色ID              是                     角色ID
company_id              公司ID              是                     公司ID
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
http请求url:http://127.0.0.1:8000/xiong/user/update/5?user_id=1&timestamp=123&rand_str=7e0fc6b6833ebe0347ab6a5945d519ea&company_id=1&role_id=1
参数                      请求方式           必须                     说明
username                 用户名称            是                     用户名称   
role_id                 角色ID              是                     角色ID
company_id              公司ID              是                     公司ID

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
http请求url:http://127.0.0.1:8000/xiong/user/delete/5?user_id=1&timestamp=123&rand_str=7e0fc6b6833ebe0347ab6a5945d519ea&company_id= 1
参数                      请求方式           必须                     说明

返回说明 （正常时返回的json数据 示例）
{
    "msg": "删除成功",
    "data": {},
    "code": 200
}
```

#### 用户管理 删除说明
``` 
http请求：GET
http请求url:http://127.0.0.1:8000/xiong/user?user_id=1&timestamp=123&rand_str=7e0fc6b6833ebe0347ab6a5945d519ea&company_id=1&role_id=1
参数                      请求方式           必须                     说明

返回说明 （正常时返回的json数据 示例）
{
    "code": 200,
    "msg": "查询成功",
    "data": {
        "data_count": 2,
        "ret_data": [
            {
                "username": "测试",
                "status": 2,
                "role_name": "管理员",
                "role_id": 1,
                "company_name": "公司",
                "company_id": 1,
                "get_status_display": "不启用",
                "create_date": "2018-11-02 10:32:20",
                "id": 2,
                "oper_user__username": "赵欣鹏"
            },
            {
                "username": "赵欣鹏",
                "status": 1,
                "role_name": "管理员",
                "role_id": 1,
                "company_name": "公司",
                "company_id": 1,
                "get_status_display": "启用",
                "create_date": "2018-11-02 10:15:20",
                "id": 1,
                "oper_user__username": "赵欣鹏"
            }
        ]
    }
}
```

#### 权限管理 添加说明
``` 
http请求：POST
http请求url:http://127.0.0.1:8000/xiong/permissions/add/0?user_id=1&timestamp=123&rand_str=7e0fc6b6833ebe0347ab6a5945d519ea
参数                      请求方式           必须                     说明
name                       POST             是                     权限名称
title                      POST            是                      权限标题           
pid_id                     POST             是                       父级权限

返回说明 （正常时返回的json数据 示例）
{
    "code": 200,
    "msg": "添加成功",
    "data": {}
}
```

#### 权限管理 修改说明
``` 
http请求：POST
http请求url:http://127.0.0.1:8000/xiong/permissions/update/3?user_id=1&timestamp=123&rand_str=7e0fc6b6833ebe0347ab6a5945d519ea
参数                      请求方式           必须                     说明
name                       POST             是                     权限名称
title                      POST            是                      权限标题           
pid_id                     POST             是                       父级权限

返回说明 （正常时返回的json数据 示例）
{
    "code": 200,
    "msg": "修改成功",
    "data": {}
}
```

#### 权限管理 删除说明
``` 
http请求：POST
http请求url:http://127.0.0.1:8000/xiong/permissions/delete/2?user_id=1&timestamp=123&rand_str=7e0fc6b6833ebe0347ab6a5945d519ea

返回说明 （正常时返回的json数据 示例）
{
    "code": 200,
    "msg": "删除成功",
    "data": {}
}
```

#### 权限管理 查询说明
``` 
http请求：GET
http请求url:http://127.0.0.1:8000/xiong/permissions?user_id=1&timestamp=123&rand_str=7e0fc6b6833ebe0347ab6a5945d519ea

返回说明 （正常时返回的json数据 示例）
{
    "code": 200,
    "msg": "查询成功",
    "data": {
        "data_count": 1,
        "ret_data": [
            {
                "pid_title": "权限管理",
                "create_date": "2018-11-02 10:45:12",
                "title": "权限管理",
                "oper_user__username": "赵欣鹏",
                "name": "权限",
                "id": 1,
                "pid_id": 1
            }
        ]
    }
}
```

#### 公司管理 添加说明
``` 
http请求：POST
http请求url:http://127.0.0.1:8000/xiong/company/add/0?user_id=1&timestamp=123&rand_str=7e0fc6b6833ebe0347ab6a5945d519ea
参数                      请求方式           必须                     说明
name                    POST                是                      公司名称

返回说明 （正常时返回的json数据 示例）
{
    "code": 200,
    "msg": "添加成功",
    "data": {}
}
```

#### 公司管理 修改说明
``` 
http请求：POST
http请求url:http://127.0.0.1:8000/xiong/company/update/3?user_id=1&timestamp=123&rand_str=7e0fc6b6833ebe0347ab6a5945d519ea
参数                      请求方式           必须                     说明
name                    POST                是                      公司名称

返回说明 （正常时返回的json数据 示例）
{
    "code": 200,
    "msg": "修改成功",
    "data": {}
}
```

#### 公司管理 删除说明
``` 
http请求：POST
http请求url:http://127.0.0.1:8000/xiong/company/delete/2?user_id=1&timestamp=123&rand_str=7e0fc6b6833ebe0347ab6a5945d519ea
参数                      请求方式           必须                     说明

返回说明 （正常时返回的json数据 示例）
{
    "code": 200,
    "msg": "删除成功",
    "data": {}
}
```

#### 公司管理 查询说明
``` 
http请求：GET
http请求url:http://127.0.0.1:8000/xiong/company?user_id=1&timestamp=123&rand_str=7e0fc6b6833ebe0347ab6a5945d519ea

返回说明 （正常时返回的json数据 示例）
{
    "code": 200,
    "msg": "查询成功",
    "data": {
        "data_count": 1,
        "ret_data": [
            {
                "oper_user__username": "赵欣鹏",
                "name": "公司",
                "id": 1,
                "create_date": "2018-11-02 10:15:46"
            }
        ]
    }
}
```

#### 文章管理 添加说明
``` 
http请求：POST
http请求url:http://127.0.0.1:8000/xiong/article/add/0?user_id=1&timestamp=123&rand_str=7e0fc6b6833ebe0347ab6a5945d519ea
参数                      请求方式           必须                     说明
title                       POST            是                       文章标题
summary                     POST            是                       文章摘要
content                     POST            是                       文章内容
TheColumn                   POST            是                       栏目 （暂时随便写）

返回说明 （正常时返回的json数据 示例）
{
    "msg": "添加成功",
    "data": {},
    "code": 200
}
```


#### 文章管理 修改说明
``` 
http请求：POST
http请求url:http://127.0.0.1:8000/xiong/article/update/1?user_id=1&timestamp=123&rand_str=7e0fc6b6833ebe0347ab6a5945d519ea
参数                      请求方式           必须                     说明
title                       POST            否                       文章标题
summary                     POST            否                       文章摘要
content                     POST            否                       文章内容
TheColumn                   POST            否                       栏目 （暂时随便写）

返回说明 （正常时返回的json数据 示例）
{
    "msg": "修改成功",
    "data": {},
    "code": 200
}
```

#### 文章管理 修改说明
``` 
http请求：POST
http请求url:http://127.0.0.1:8000/xiong/article/delete/1?user_id=1&timestamp=123&rand_str=7e0fc6b6833ebe0347ab6a5945d519ea
参数                      请求方式           必须                     说明

返回说明 （正常时返回的json数据 示例）
{
    "msg": "删除成功",
    "data": {},
    "code": 200
}
```

#### 文章管理 查询说明
``` 
http请求：POST
http请求url：http://127.0.0.1:8000/xiong/article?user_id=1&timestamp=123&rand_str=7e0fc6b6833ebe0347ab6a5945d519ea

返回说明 （正常时返回的json数据 示例）
{
    "msg": "查询成功",
    "data": {
        "data_count": 1,
        "ret_data": [
            {
                "id": 5,
                "create_date": "2018-11-02T19:33:20",
                "content": "文章内容",
                "summary": "文章摘要",
                "TheColumn": "1",
                "title": "文章标题",
                "user_name": "赵欣鹏",
                "user_id": 1
            }
        ]
    },
    "code": 200
}
```




