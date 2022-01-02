# 米游社的自动签到

这个一个闲来的练手项目, 核心功能是<u>自动完成米游社相关的签到和每日任务</u>, 解除双应用签到带来的割裂感. 如存在使用问题或者功能建议, 可以在 [issue](https://github.com/zxjlm/GenShinSignIn/issues)中提出.

项目的结构参考了 [AutoMihoyoBBS](https://github.com/Womsxd/AutoMihoyoBBS) 项目, 在大佬的项目基础上做了一些个人向的修改.

## 基础安装

基础安装有两种方式, 一种是使用 `poetry install` 进行安装, 这个熟悉 poetry 的可以自行操作, 不熟悉的则可以通过一下的步骤使用原生的 `pip` 模块进行安装.

### (可选) 创建虚拟环境

```python
# 创建python的虚拟环境, 需求python的版本在3.6+
python -m venv genshinSigninVenv

# 进入虚拟环境(linux \ macos)
source ./genshinSigninVenv/bin/activate
```

### 正式安装

```shell
# 安装依赖项
pip install -r requirements.txt

# (可选) 如果需要使用自动化浏览器来处理cookie, 则需要安装内置浏览器.
playwright install firefox
```

## 使用流程

1. 完成基础安装的内容.
2. 见 [生成配置文件](#生成配置文件), 建立一份配置文件.
3. 使用 `python main.py`

## 功能说明

脚本本身提供了多样化的功能, 尤其是对多账号的情况进行了使用优化. 功能包括:

- 根据配置文件进行签到
- 当 cookie 失效时, 启用邮件进行通知
- 检查配置文件
- 生成配置文件
- 支持阿里云函数
- ...

### 根据配置文件进行签到

配置文件应该存放于 config 文件夹下, 文件名应该是 `config_[id].json` , 其中, [id] 是给该配置的名称, 笔者习惯使用姓名的首字母来命名, 即 `config_zxj.json` .

配置文件内容形如 `config.json` , 各个配置项的含义参看 [config 配置项手册](https://github.com/zxjlm/GenShinSignIn/blob/main/config/README.md). 同时, 配置文件可以使用 `python main.py generaet-config` 来生成, 更多配置文件的信息见于 [生成配置文件](#生成配置文件)

![生成配置文件](https://cdn.jsdelivr.net/gh/zxjlm/my-static-files@master/img/mainprocess.png)

### 检查配置文件

使用 `python main.py --check-configs` 可以快速检查所有文件的配置信息.

![检查配置文件](https://cdn.jsdelivr.net/gh/zxjlm/my-static-files@master/img/check-configs.png)

## 生成配置文件

配置文件有自动和手动两种方式去生成.

### 手动生成

_config_ 目录下的 _config.py_ 就是基础配置文件, 在该文件夹下创建一个名为 config\_[1].json 的文件, 然后依照配置手册修改配置项.

手动生成的配置文件, 建议在配置好之后使用 `python main.py -c` 进行一次校验.

### 自动生成

使用 `python main.py -g` 可以直接生成一份配置文件.

![自动生成配置文件](https://cdn.jsdelivr.net/gh/zxjlm/my-static-files@master/img/generate-config.png)

## 云函数

云函数无需使用服务器资源, 开箱即用, 非常方便. 现在国内的几大云服务运营商都有对应的项目服务(免费调用), 可以直接使用.

它还有一个好处就是 IP 是国内的 IP, 对国内的网络环境很友好.

笔者是阿里云重度用户, 所以这里就以阿里云为例, 腾讯云的使用方式可以看原作者 [AutoMihoyoBBS](https://github.com/Womsxd/AutoMihoyoBBS) 的项目说明.

### 阿里云

阿里云从 10 月 5 日部署开始, 到现在 1 月 2 日, 已经平稳运行大约 3 个月, 十分稳健.

1. 按照教程初始化一个[vs code](https://help.aliyun.com/document_detail/155679.html)项目.
2. 使用 git 仓库中的内容覆盖原本的内容.
3. 根据上述文本内容生成并修改配置文件.
4. 部署项目 && 测试项目.

## TODO

多样化
