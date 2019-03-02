# 运行 #

``` bash
python3 wukong.py
```

第一次启动时将提示你是否要到用户目录下创建一个配置文件，输入 `y` 即可。

然后通过唤醒词 “孙悟空” 唤醒 wukong-robot 进行交互（该唤醒词可自定义）。

要让 wukong-robot 暂时屏蔽离线监听，可以在配置文件中设置 `hotword_switch` 为 true：

``` yaml
# 勿扰模式，该时间段内自动进入睡眠，避免监听
do_not_bother:
    ...
    hotword_switch: false  # 是否使用唤醒词开关唤醒模式
    ...
```

此外，wukong-robot 默认在运行期间还会启动一个后台管理端，提供了远程对话、查看修改配置、查看 log 等能力。

- 默认地址：http://localhost:5000
- 默认账户名：wukong
- 默认密码：wukong@2019

建议正式使用时修改用户名和密码，以免泄漏隐私。

## 后台运行 ##

直接在终端中启动 wukong-robot ，等关掉终端后 wukong-robot 的进程可能就没了。

要想在后台保持运行 wukong-robot ，可以在 [tmux](http://blog.jobbole.com/87278/) 或 supervisor 中运行。

## 外网可访问 ##

要在外网访问你家中的 wukong-robot ，可以参考 [使用技巧 - 在家访问家中的 wukong-robot](tips?id=_4-在外网访问家中的-wukong-robot)。

## 其他使用技巧 ##

可以参考 [使用技巧](tips) 。
