# 原神的自动签到

这个一个闲来的练手项目, 核心功能是<u>自动完成原神游戏本体的签到和米游社相关的签到任务</u>.

项目的结构参考了 [AutoMihoyoBBS](https://github.com/Womsxd/AutoMihoyoBBS) 项目.



## 基础安装

基础安装有两种方式, 一种是使用 `poetry install` 进行安装, 这个熟悉poetry的可以自行操作, 不熟悉的则可以通过一下的步骤使用原生的 `pip` 模块进行安装.

```shell
# 创建python的虚拟环境, 需求python的版本在3.6+
python -m venv genshinSignin

# 安装依赖项
pip install -r requirements.txt
```

## 使用

脚本本身提供了多样化的功能, 尤其是对多账号的情况进行了使用优化. 功能包括:

- 根据配置文件进行签到
- 当cookie失效时, 启用邮件进行通知
- 检查配置文件
- 生成配置文件
- 支持阿里云函数
- ...

### 根据配置文件进行签到

配置文件应该存放于config文件夹下, 文件名应该是 `config_[id].json` , 其中, [id] 是给该配置的名称, 笔者习惯使用姓名的首字母来命名, 即 `config_zxj.json` .

配置文件内容形如 `config.json` , 各个配置项的含义参看 [config配置项手册](https://github.com/zxjlm/GenShinSignIn/blob/main/config/README.md). 同时, 配置文件可以使用 `python main.py generaet-config` 来生成.

### 检查配置文件

使用 `python main.py --check-configs` 可以快速检查所有文件的配置信息.

![](https://cdn.jsdelivr.net/gh/zxjlm/my-static-files@master/img/截屏2021-09-26 下午9.02.26.png)



## TODO

多样化
