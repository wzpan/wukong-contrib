# 脑机控制 #

从 2.0.0 版本开始，wukong-robot 加入了对 [Muse](http://choosemuse.com/) 脑机的支持，使得可以摆脱语音唤醒的限制，而使用脑部意识来触发脑机。

## Demo 

<center>
    <iframe src="//player.bilibili.com/player.html?aid=76739580&cid=131259456&page=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" width="80%" height="360px"> </iframe>
</center>

## 依赖

1. [Muse 头环](http://choosemuse.com/) 。支持目前上市的三种型号， 包括 2014 款 Muse Model MU-01、2016 款 Muse Model MU-02 及 2018 款 “Muse 2” Model MU-03 等。
2. iPhone 手机，用于连接 Muse 。
3. [Muse Monitor](https://musemonitor.com/)，用于向 wukong-robot 所在的设备传输数据。
4. 安装依赖：

``` bash
pip install python-osc
```

## 如何使用

1. 在 iPhone 上安装 Muse 的官方应用，并连接到 Muse 头环，并确保你的 iPhone 与 wukong-robot 在同一局域网下；
2. 取得你的 wukong-robot 所在电脑的局域网 ip 地址，并填入配置文件中。例如：

``` yaml
# Muse 脑机
# 推荐搭配 Muse Monitor 使用
# 并开启 OSC stream
# 同时眨眼和咬牙齿可以实现唤醒
muse:
    enable: true
    ip: '192.168.3.85'  # 请修改为本机的 ip 地址
    port: 5001          # 请修改为 OSC 的端口号
```

  如果你的 wukong-robot 用的也是 5000 端口，那么建议把 `Port` 改为另一个端口号。

3. 打开 Muse Monitor。在 setting 页里，将 wukong-robot 所在电脑的 ip 地址填入 `OSC Stream Target IP` 一栏，将你的自定义的 OSC 端口号填入 `OSC Stream Port` 一栏。

然后重新启动 wukong-robot 即可：

``` bash
python3 wukong.py
```

现在尝试咬牙 + 闭眼的动作，看看 wukong-robot 是否可以唤醒吧！
