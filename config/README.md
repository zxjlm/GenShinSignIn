# Config 配置教程

## 本项目识别 config 文件的方法

读取文件夹里面的`config_*.json`文件, '\*'是通配符, 替换为你的配置文件的名称.

## json 文件的字段讲解

```python
"enable_config": true,  # 此字段的作用是是否启用这个配置文件,`bool`类型,可设置`true`(默认)和`false`

"config_version": 1,  # 此字段的作用是表明配置文件版本(不过脚本里面暂时没有用到),`int`类型

"mihoyobbs_cookies_raw": "",  # 此字段的作用存储米游社需要的 cookie 值(你填入的 cookie 里面必须带这个),`str`类型,默认为空,脚本执行成功时自动填入

"mihoyobbs": {
    "bbs_global": true,  # 作用是是否启用米游币获取,`bool`类型,可设置`true`(默认)和`false`
    "bbs_signin": true,  # 作用是是否启用讨论区自动签到,`bool`类型,可设置`true`(默认)和`false`
    "bbs_signin_list": [2, 5],  # 设置要签到的讨论区, 默认是[2,5], id 与 讨论区的关系可见于底部附录
    "bbs_view_post_0": true, # 作用是是否启用自动阅读帖子,`bool`类型,可设置`true`(默认)和`false`
    "bbs_post_up_0": true, # 作用是是否启用自动点赞帖子,`bool`类型,可设置`true`(默认)和`false`
    "bbs_post_up_cancel": true, # 作用是是否启用自动取消帖子点赞(当`bbs_post_up_0`为`false`时本设置无效),`bool`类型,可设置`true`(默认)和`false`
    "bbs_share_post_0": true # 作用是是否启用自动分享帖子,`bool`类型,可设置`true`(默认)和`false`

},

"genshin_auto_sign": true,  # 此字段的作用是是否启用原神自动签到,`bool`类型,可设置`true`(默认)和`false`

# 邮箱的配置信息可以到邮箱服务的提供方去查找, 这里给出163的配置
"mail": {   # 邮件配置, 当cookie失效时会发送通知邮件
    "receivers": [], # 接收邮件的邮箱, 可以设为多个
    "password": "", # 邮箱密码
    "user": "", # 邮箱账号
    "host": "smtp.163.com", # 邮箱host
    "port": 465  # 邮箱端口
}


```

## 讨论区的 id 对应关系

`1`对应崩坏 3

`2`对应原神

`3`对应崩坏学园 2

`4`对应未定事件簿

`5`对应大别墅
