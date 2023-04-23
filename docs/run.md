# 运行 #

## 运行前声卡检查和设置

!> 重要的事情说三遍！请确保麦克风和音响配置正确再启动 wukong-robot ！<br/> 重要的事情说三遍！请确保麦克风和音响配置正确再启动 wukong-robot ！ <br/> 重要的事情说三遍！请确保麦克风和音响配置正确再启动 wukong-robot ！

### Mac 系统

Mac 系统的配置比较简单，在【系统偏好设置】→【声音】里调整输入和输出即可。

调节完之后，可以测试一下录音：

``` bash
rec test.wav
```

将启动 sox 提供的录音工具，随便说点什么，然后按 `Ctrl-C` 结束录音。

之后播放一下录音：

``` bash
play test.wav
```

如果可以正常播放，则说明配置正常。可以[运行 wukong-robot](/run?id=运行-wukong-robot) 了。

### Linux 系统（包括树莓派）

而对于 Linux 系统，则往往需要对声卡进行一下设置。配置麦克风和音响是新用户在 Linux 下使用 wukong-robot 过程中最容易卡住的环节。

?> 如果您使用的是行空板，请参见 [行空板](/mic-choices?id=行空板) 配置教程，无需阅读本节设置。

?> 如果您使用的是 PS3 eye，请参见 [这篇文章](https://renatocunha.com/2012/04/playstation-eye-audio-linux/) 配置教程，无需阅读本节设置。

?> 如果您使用的是 ReSpeaker 2 Mic HAT，请参见 [ReSpeaker 2-Mics Pi HAT](/mic-choices?id=respeaker-2-mics-pi-hat) 配置教程，无需阅读本节设置。

#### 1. 检查声卡配置

测试一下录音：

``` bash
arecord test.wav
```

将启动 alsa 进行录音。随便说点什么，然后按 `Ctrl-C` 结束录音。

之后播放一下录音：

``` bash
aplay test.wav
```

如果可以正常播放，则说明配置正常。可以[运行 wukong-robot](/run?id=运行-wukong-robot) 。如果不能，则参考下面的步骤进行配置。

在配置前，首先确保已接好麦克风和音响。

#### 2. 配置声卡


##### 获得声卡编号和设备编号

查看当前已接入的所有录音设备：

``` bash
arecord -l
```

得到的结果类似这样：

``` bash
pi@raspberrypi:~$ arecord -l
**** List of CAPTURE Hardware Devices ****
card 1: Set [C-Media USB Headphone Set], device 0: USB Audio [USB Audio]
  Subdevices: 0/1
  Subdevice #0: subdevice #0
card 2: Device [USB PnP Sound Device], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```

上面的结果说明当前接入了两个录音设备，选择你要使用的录音设备，并记下声卡编号（或名字）和设备编号。例如，我希望使用 `USB PnP Sound Device` 这个设备，则声卡编号为 2 （声卡名为 `Device`），设备编号为 0 。

类似的方法获取音响的声卡编号和设备编号：

``` bash
aplay -l
```

结果类似这样：

``` bash
pi@raspberrypi:~$ aplay -l
**** List of PLAYBACK Hardware Devices ****
card 0: ALSA [bcm2835 ALSA], device 0: bcm2835 ALSA [bcm2835 ALSA]
  Subdevices: 8/8
  Subdevice #0: subdevice #0
  Subdevice #1: subdevice #1
  Subdevice #2: subdevice #2
  Subdevice #3: subdevice #3
  Subdevice #4: subdevice #4
  Subdevice #5: subdevice #5
  Subdevice #6: subdevice #6
  Subdevice #7: subdevice #7
card 0: ALSA [bcm2835 ALSA], device 1: bcm2835 ALSA [bcm2835 IEC958/HDMI]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 1: Set [C-Media USB Headphone Set], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 2: Device [USB PnP Sound Device], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```

上面的结果说明当前接入了三个播放设备，其中 card 0 是树莓派自带的声卡，如果您是使用 AUX 3.5 口外接的音响/或耳机，那么应该使用 card 0；card 1 和 card 2 则是其他的设备。记下您要使用的声卡编号和设备编号。

##### 配置 .asoundrc

首先创建 `~/.asoundrc` ：

``` bash
cp $HOME/.asoundrc $HOME/.asoundrc_backup  # 备份已有的声卡配置（如果有的话）
touch $HOME/.asoundrc
```

之后添加您选择的声卡编号和设备。这里举两种常见的配置。

* 第一种：您使用的是一个自带音响和录音的组合设备（例如会议麦克风喇叭，或者一块连接了麦克风和音响的独立USB声卡），那么只需设置 pcm 为该组合设备的编号即可。示例：

```
pcm.!default {
        type plug slave {
                pcm "hw:1,0"
        }
}

ctl.!default {
        type hw
        card 1
}
```

上面的 `hw:1,0` 表示使用 card 1，设备 0。即 `C-Media USB Headphone Set` 。如果配成 `hw:Set,0` ，效果相同（个人更推荐使用声卡名字）。

默认情况下 arecord 使用 `U8` 作为采样格式（[sample format](https://linux.die.net/man/1/arecord)），使用 8000Hz 作为采样率。有些用户的录音硬件可能会不支持。此时可以通过增加 `sample` 和 `rate` 参数来调整到支持的值，例如（仅供参考，具体请以实际测试为准）：

```
pcm.!default {
        type plug slave {
                pcm "hw:1,0"
                format S16_LE
                rate 16000
        }
}

ctl.!default {
        type hw
        card 1
}
```

* 第二种：您使用的是一个单独的 USB 麦克风，并直接通过树莓派的 AUX 3.5 口外接一个音响。那么可以参考如下配置：

```
pcm.!default {
        type asym
            playback.pcm {
                type plug
                slave.pcm "hw:0,0"
            }
            capture.pcm {
                type plug
                slave.pcm "hw:2,0"
            }        
}

ctl.!default {
        type hw
        card 2
}
```

由于播放设备（playback）和录音设备（capture）是独立的，所以需要各自配置。

完成后可以再次[测试下命令行录音和播放](/run?id=_1-检查声卡配置)，看看是否能正常工作。

如果还有问题，建议求助 google/百度 。不同的硬件和系统环境可能有不同的配置方法，作者很难给出完全通用的方案，也难以对一些特定情况下遇到的问题进行定位。也建议阅读 [Asoundrc](https://www.alsa-project.org/wiki/Asoundrc) 的配置文档，了解如何配置采样格式、采样率等技巧。

## 运行 wukong-robot

``` bash
cd wukong-robot 所在的目录
python3 wukong.py
```

第一次启动时将提示你是否要到用户目录下创建一个配置文件，输入 `y` 即可。

然后通过唤醒词 “snowboy” 唤醒 wukong-robot 进行交互（该唤醒词可自定义，详见[更新唤醒词](/install?id=_6-更新唤醒词（可选，树莓派必须）) 以提升唤醒成功率和准确率）。

启动时如遇到如下问题：

```
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 924
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 924
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 934
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 934
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 934
Cannot connect to server socket err = No such file or directory
Cannot connect to server request channel
jack server is not running or cannot be started
JackShmReadWritePtr::~JackShmReadWritePtr - Init not done for -1, skipping unlock
JackShmReadWritePtr::~JackShmReadWritePtr - Init not done for -1, skipping unlock
Cannot connect to server socket err = No such file or directory
```

**不影响功能，只是pulseaudio的告警，可以忽略。**

如果遇到其他问题，可以移步 [常见问题解答](https://github.com/wzpan/wukong-robot/wiki/troubleshooting) 和 [Github issue](https://github.com/wzpan/wukong-robot/issues) 看看是否有类似问题。例如，如果遇到类似这样的 `-9997` 错误：

```
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 924
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 924
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 934
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 934
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 934
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 924
Expression 'paInvalidSampleRate' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 2048
Expression 'PaAlsaStreamComponent_InitialConfigure( &self->capture, inParams, self->primeBuffers, hwParamsCapture, &realSr )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 2719
Expression 'PaAlsaStream_Configure( stream, inputParameters, outputParameters, sampleRate, framesPerBuffer, &inputLatency, &outputLatency, &hostBufferSizeMode )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 2843
CRITICAL:main:离线唤醒机制初始化失败：[Errno -9997] Invalid sample rate
```

到 [Github issue 里搜 -9997](https://github.com/wzpan/wukong-robot/issues?q=-9997) 即可搜出类似问题。

### 小技巧：

要让 wukong-robot 暂时屏蔽离线监听，可以在配置文件中设置 `hotword_switch` 的 `enable` 配置为 true：

``` yaml
# 勿扰模式，该时间段内自动进入睡眠，避免监听
do_not_bother:
    ...
    hotword_switch: false  # 是否使用唤醒词开关唤醒模式
    ...
```

然后使用唤醒词 “悟空别吵” 屏蔽离线监听。需要时再通过 “悟空醒醒” 恢复监听。

?> 同样的，这两个唤醒词也建议自行训练，并修改配置文件中的 `hotword_switch` 的 `on_hotword` 和 `off_hotword` 两个设置。

## 管理端 ##

wukong-robot 默认在运行期间还会启动一个后台管理端，提供了远程对话、查看修改配置、查看 log 等能力。

- 默认地址：http://localhost:5001
- 默认账户名：wukong
- 默认密码：wukong@2019

建议正式使用时修改用户名和密码，以免泄漏隐私。

## 后台运行 ##

直接在终端中启动 wukong-robot ，等关掉终端后 wukong-robot 的进程可能就没了。

要想在后台保持运行 wukong-robot ，可以在 [tmux](http://blog.jobbole.com/87278/) 或 supervisor 中运行。

## 性能诊断 ##

如果发现 wukong-robot 运行时响应很慢（例如有用户反馈交互一次后要等两分钟才能响应下一次交互），通常和你的网络环境有很大关系。例如某个服务因为防火墙的原因无法触达。可以以如下方式运行 wukong-robot ：

``` bash
python3 wukong.py profiling
```

wukong-robot 将在每一步交互后打印当次交互的性能调优数据。

![性能调优](https://hahack-1253537070.file.myqcloud.com/images/wukong-docs/profiling.jpg)

标红的这一列会累计每一个任务的操作耗时。一般往下找到数字突然变小的那一行的上一行就是最大黑手。

!> 执行 `python3 wukong.py help` 可以了解更多命令行用法。

## 外网可访问 ##

要在外网访问你家中的 wukong-robot ，可以参考 [使用技巧 - 在家访问家中的 wukong-robot](tips?id=_4-在外网访问家中的-wukong-robot)。

## 其他使用技巧 ##

可以参考 [使用技巧](tips) 。

## 遇到问题？ ##

1. 参见 [常见问题解答](https://github.com/wzpan/wukong-robot/wiki/troubleshooting) ，找找有没有解决方案；
2. 搜索 [项目issue](https://github.com/wzpan/wukong-robot/issues) 和 [第三方插件issue](https://github.com/wzpan/wukong-contrib/issues)，看看有没有人问过；
3. 加群（580447290）提问；
4. 给项目 [提issue](https://github.com/wzpan/wukong-robot/issues/new/choose) 。第三方插件的问题请提到 [wukong-contrib](https://github.com/wzpan/wukong-contrib/issues) 。
