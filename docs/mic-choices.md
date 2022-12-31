# 硬件选购建议

wukong-robot 能使用普通的麦克风正常工作。

不过，相比普通麦克风，麦克风阵列的拾音范围更大，允许隔着 wukong-robot 一段距离依然可以唤醒和交流。因此推荐选购麦克风阵列。而阵列的数量越多，效果会越好，价格也会越高。因此，您可以依据自己的经济能力选择不同阵列数量的麦克风。

以下是四款推荐考虑的一体化方案/单独的麦克风阵列模块，价格都比较亲民，可根据不同的需求选购：

* [行空板（推荐）](https://www.unihiker.com/)- 一款拥有自主知识产权的国产教学用开源硬件，采用微型计算机架构，集成LCD彩屏、WiFi蓝牙、麦克风等多种常用传感器和丰富的拓展接口，性价比、可扩展性和可玩性都相当不错。同时，其自带Linux操作系统和Jupyter Python环境，还预装了常用的Python库。
* [Google AIY Voice Kit](https://aiyprojects.withgoogle.com/voice/) - Google 的一体化音频开发板。除了本身提供了阵列麦克风外，还包含了按钮、喇叭、纸板外壳。2.0 版本还提供了树莓派 Zero 。
* [PS3 Eye](https://en.wikipedia.org/wiki/PlayStation_Eye) - PS3 淘汰的配件，包含四阵列麦克风和摄像头，免驱使用。由于是淘汰下来的配件，价格也比较便宜，可以到淘宝上找找。
* [ReSpeaker 2 Mics Pi HAT](https://www.seeedstudio.com/ReSpeaker-2-Mics-Pi-HAT.html) - 专门为树莓派打造的 2 阵列开发板，带 2 Mic 阵列，有声卡，支持外接 3.5mm 音频输出。

客观比较下四个的优劣：

- 行空板：几乎完美的一块板子，对 Python 开发很友好，直接集成了 Jupyter 和 Slot ，而且自带了麦克风和触摸屏（然而价格相比树莓派+阵列麦克风+触摸屏配件而言便宜太多），也不需要折腾配置 .asoundrc 。系统本质上是个 Debian 系统，也支持 ssh，简而言之客你只需要再搞个音箱或者买个喇叭配件就可以跑 wukong-robot 了。行空板的不足之处是相对更加小众，以至于 Porcupine 也不支持在行空板上运行；
- Google AIY Voice Kit 提供了包括阵列麦克风+喇叭+按钮+纸板外壳的一体化方案，适合没有麦克风和音响的朋友；2.0 版本还提供了树莓派 Zero ，适合连树莓派都没有的朋友，不过相应的价格也更高。不过 Google AIY Voice Kit 的安装比较繁琐，而树莓派 Zero 是 armvl6 架构，不支持 docker 安装 wukong-robot ，只能手动安装，所以需要具备一定的动手能力。由于整套设备是 Google 的，还需要有科学上网能力。另外，Pi Zero 的性能比较弱。
- PS3 Eye 同时带有麦克风和摄像头，价格更低，适用于对拾音质量要求不高、想省钱的朋友；
- ReSpeaker 2 Mics Pi HAT 为树莓派量身打造的阵列麦克风开发板，拾音质量更好，带呼吸灯，另外自带了声卡，解决了树莓派自带 3.5 mm 口电流声大的问题。适用于使用树莓派，希望有更好的拾音效果，想玩呼吸灯效果的发烧友。

## 行空板

<center>
<iframe src="//player.bilibili.com/player.html?aid=819573733&bvid=BV1mG4y1j7Fz&cid=945823463&page=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" width="80%" height="360"> </iframe>
</center>

要在行空板上运行 wukong-robot 是相对比较轻松的，当你购买好板子后，通过 USB TypeC 线把板子插上电脑的 USB 口，然后就可以 ssh 访问 10.1.2.3 进行 wukong-robot 的安装操作。

``` bash
ssh root@10.1.2.3  # 行空板的默认密码是 dfrobot
```

?> 直接访问 10.1.2.3 也可以打开行空板的内置帮助站点，可以学习掌握行空板的更多使用用法。

然后即可按照 [手动安装](/install?id=方式二：手动安装) 的指引完成手动安装。

注意到编译 `_snowboydetect.so` 的时候可以跳过，直接下载 [预编译好的 _snowboydetect.so](https://wzpan-1253537070.cos.ap-guangzhou.myqcloud.com/misc/unhiker/_snowboydetect.so) ，放到 `snowboy/` 目录下即可。

行空板的声卡默认已经配置好，你只需要给板子插好一个可用的外接音响/喇叭即可准备开始使用 wukong-robot 。无需额外再学习如何配置 .asoundrc 。但是行空板默认的麦克风采集音量设置的比较小，很难实现远场唤醒。因此可以调大一些：

### 设置录音音量

``` bash
alsamixer
```

然后按 `F4` 按钮把 Capture 的音量调到最大即可。

![调大行空板的麦克风采集音量](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/wukong-docs/unihiker_capture.png)

注意这个设置只会在当次系统运行期间生效，重启后需要重新设置 `alsamixer` 。

### 配置

记得在配置文件中打开行空板的支持：

``` yaml
# 行空板
# 需搭配行空板使用
# 展示专为行空板设计的 GUI
# 摇一摇可以实现唤醒 
# https://www.unihiker.com/
unihiker:
    enable: true
    beep: false # 是否需要开启主板的蜂鸣提示音
```

## Google AIY Voice Kit

<center>
    <iframe src="//player.bilibili.com/player.html?aid=81173082&cid=138922674&page=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" width="80%" height="360px"> </iframe>
</center>

先照着 Google AIY Voice Kit 的安装教程组建安装整个设备盒子。确保设备正常联网工作，特别是 `arecord` 、`aplay` 能正常录音和回放。

``` sh
arecord -d 3 temp.wav  # 测试录音3秒
aplay temp.wav # 播放录音看看效果
```

### 解决 Unicode 编码问题 ###

Google AIY Voice Kit 官方提供的镜像的 Locale 设置有点问题，无法很好地支持 Unicode 编码，因此建议先解决一下 Locale 问题。

编辑 /etc/locale.gen ，注释掉 `en_GB.UTF-8 UTF-8` ，反注释 `en_US.UTF-8 UTF-8`、`zh_CN.GBK GBK` 以及 `zh_CN.UTF-8 UTF-8` 。然后执行：

``` bash
sudo locale-gen
```

再在 ~/.bashrc 中追加两行内容：

``` bash
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```

再执行以下命令即可：

``` bash
source ~/.bashrc
```

### 手动安装 wukong-robot ###

参考 [手动安装](/install?id=方式二：手动安装) 教程，手动安装 wukong-robot 。

### 呼吸灯 ###

如果希望 Voice Kit 在使用 wukong-robot 的过程中有呼吸灯效果，可以如下配置：

``` yaml
# 是否展示灯光效果
# 支持 Respeaker 2 Mics 和 Google AIY Voice Kit 两种
# 必须具备相应的硬件和驱动
LED:
    enable: true
    type: aiy  # aiy: Google AIY Voice Kit; respeaker：respeaker 2Mics
```

## PS3 Eye

![PS3 Eye](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/wukong-docs/ps3-eye.jpg)

PS3 Eye 是 USB 口，可以直接插上任何带 USB 接口的主机。

* 摄像头：即插即用，配合 fswebcam 即可。
* 麦克风的配置可以参见[这篇文章](https://renatocunha.com/2012/04/playstation-eye-audio-linux/)。

## Respeaker 2 Mics Pi HAT

![Respeaker 2 Mics](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/wukong-docs/respeaker.jpg)

Respeaker 2 Mics 是专门针对树莓派的，只能插在树莓派的 GPIO 口上。

### 事前准备

如果以前配置过 `.asoundrc` ，需要将之删除：

``` sh
rm /home/pi/.asoundrc
```

### 安装驱动

``` sh
git clone https://github.com/respeaker/seeed-voicecard.git
cd seeed-voicecard
sudo ./install.sh
reboot
```

完成后可以使用 `aplay -l` 命令检查一下是否包含 `seeedvoicecard` 的播放设备。

``` sh
pi@raspberrypi:~ $ aplay -l
**** List of PLAYBACK Hardware Devices ****
card 0: seeedvoicecard [seeed-voicecard], device 0: bcm2835-i2s-wm8960-hifi wm8960-hifi-0 []
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```

### 配置

使用 `alsamixer` 进行调整：

``` sh
alsamixer
```

先重点设置 `Headphone`、`Speaker`、`Playback` 的音量，3D 也可以适当开一些。

![](https://github.com/SeeedDocument/MIC_HATv1.0_for_raspberrypi/blob/master/img/alsamixer.png?raw=true)

之后按 `F4` 键切换到录音设置界面，把 `Capture` 也开大。

完成后可以用如下方法测试下是否 ok ：

``` sh
arecord -d 3 temp.wav  # 测试录音3秒
aplay temp.wav # 播放录音看看效果
```

如果效果理想，此时可以将当前配置保存：

``` sh
sudo alsactl --file=asound.state store
```

为了避免开机音量被重置，可以将 asound.state 文件拷至 /var/lib/alsa 目录下：

``` sh
sudo cp asound.state /var/lib/alsa/
```

如果安装完后 arecord、aplay 不能正常使用，可以编写如下的 `.asoundrc` 文件：

```
pcm.!default {
        type asym
        playback.pcm {
            type plug
            slave.pcm "hw:1,0"
        }
        capture.pcm {
            type plug
            slave.pcm "hw:1,0"
        }
}

ctl.!default {
        type hw
        card 1
}
```

### 呼吸灯

如果希望 Respeaker 2 Mics 在使用 wukong-robot 的过程中有呼吸灯效果，可以如下配置：

``` bash
# 是否展示灯光效果
# 支持 Respeaker 2 Mics 和 Google AIY Voice Kit 两种
# 必须具备相应的硬件和驱动
LED:
    enable: true
    type: respeaker  # aiy: Google AIY Voice Kit; respeaker：respeaker 2Mics
```

### 3.5mm 耳机孔不发声问题

部分用户把音响插到 respeaker 2 Mics HAT 上的 3.5mm 耳机孔上后，发现没有声音输出。解决办法是把系统的声卡禁用掉。

``` bash
cd /etc/modprobe.d
sudo echo "blacklist snd_bcm2835" >> alsa-blacklist.conf
```

然后重启：

``` bash
sudo reboot
```

完成后重新设置下 .asoundrc 即可。可以看看你的设备是否只剩下 respeaker ：

``` bash
aplay -l
```

此时如果你的设备只剩下 respeaker ，那么卡号应该就是 0 。可以这么配置：

``` bash
pcm.!default {
        type asym
        playback.pcm {
            type plug
            slave.pcm "hw:0,0"
        }
        capture.pcm {
            type plug
            slave.pcm "hw:0,0"
        }
}

ctl.!default {
        type hw
        card 0
}
```

现在可以试试没有声音的问题是否解决。

### 其他技巧

如果希望利用开发板上的按钮来实现开关麦克风，可以使用 [ReSpeaker-Switcher](https://github.com/wzpan/ReSpeaker-Switcher)。

