


#### 文章管理 查询说明
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