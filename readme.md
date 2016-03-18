# mingpianer(名片儿)

## 安装依赖

pip install -r requirements.txt

另外，需要在机器上安装 redis

## 配置文件

在项目目录新建文件 `secret.json`，该文件存放配置信息，格式为 json，例子如下

```json
{
  "EMAIL_HOST": "",
  "EMAIL_PORT": ,
  "EMAIL_HOST_USER": "",
  "EMAIL_HOST_PASSWORD": "",
  "EMAIL_USE_SSL": true,
  "MY_TOKEN": "", // 由微信公共平台提供
  "MY_SCEPTER": "", // 后台管理的密码
  "REDIS_HOST": "",
  "REDIS_PORT": 5105,
  "REDIS_PASSWORD": ""
}
```

## 数据存储

执行 `python manage.py migrate` 生成数据库（默认为 sqlite）

## 使用

在微信公共平台开发配置中设置地址为 {{ yourhost }}/weixin

订阅号关注者发送 `p` 创建或修改名片，发送 `s[keyword]` 进行搜索（另，只有通过名片审核的用户可以进行搜索）

管理者访问 {{ yourhost }}/dashboard 审核名片，密码为配置文件中的 `MY_SCEPTER`

## 部署

请参照 Django 的部署方法
