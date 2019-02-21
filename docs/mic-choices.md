# 麦克风选购建议

wukong-robot 能配合普通的麦克风正常工作。

不过，相比普通麦克风，麦克风阵列的拾音范围更大，允许隔着叮当一段距离依然可以唤醒和交流。因此推荐选购麦克风阵列。而阵列的数量越多，效果会越好，价格也会越高。因此，您可以依据自己的经济能力选择不同阵列数量的麦克风。

以下是两款推荐考虑的麦克风阵列模块，价格都在百元以内，比较亲民：

* PS3 Eye - PS3 淘汰的配件，包含四阵列麦克风和摄像头，免驱使用。由于是淘汰下来的配件，价格也比较便宜，可以到淘宝上找找。
* ReSpeaker 2 Mics Pi HAT - 专门为树莓派打造的 2 阵列开发板，带 2 Mic 阵列，有声卡，支持外接 3.5mm 音频输出。

客观比较下两个的优劣：

- PS3 Eye 同时带有麦克风和摄像头，价格更低，适用于对拾音质量要求不高、想省钱的朋友；
- ReSpeaker 2 Mics Pi HAT 为树莓派量身打造的阵列麦克风开发板，拾音质量更好，带呼吸灯，另外自带了声卡，解决了树莓派自带 3.5 mm 口电流声大的问题。适用于使用树莓派，希望有更好的拾音效果，想玩呼吸灯效果的发烧友。

## PS3 Eye 安装配置

PS3 Eye 是 USB 口，可以直接插上任何带 USB 接口的主机。

* 摄像头：即插即用，配合 fswebcam 即可。
* 麦克风的配置可以参见[这篇文章](http://renatocunha.com/blog/2012/04/playstation-eye-audio-linux/)。

## Respeaker 2 Mics Pi HAT

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

如果希望 Respeaker 2 Mics 在使用 wukong-robot 的过程中有呼吸灯效果，可以打个呼吸灯补丁。

``` bash
cd wukong-robot 的根路径
git cherry-pick c12ca91
```

不过每次更新了 wukong-robot 后，这个补丁的效果会丢失，只需重新打一次补丁即可。

### 其他技巧

如果希望利用开发板上的按钮来实现开关麦克风，可以使用 [ReSpeaker-Switcher](https://github.com/wzpan/ReSpeaker-Switcher)。
