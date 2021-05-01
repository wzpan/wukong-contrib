# 安装 wukong-robot

你可以选择 docker 安装或者手动安装两种方式。

?> 若您想要将 wukong-robot 与 homeassistant 搭配使用，请参照 [智能家庭](/smarthome) 章节进行操作。或您想要使用 wukong-robot 控制您家里的智能家电，甚至改装您的旧家电使其支持智能控制，您可以使用 homeassistant 来达成该目的，您可以在 [智能家庭](/smarthome) 章节找到 homeassistant 的安装方式。

!> 注意：慎用 `sudo` ！初学者很容易犯的问题就是什么命令都加 `sudo` ，这会导致用户配置文件没生效、权限错乱等问题。只有在提示权限不够的情况下（例如要 `apt-get install` 时），才考虑使用 `sudo` 。

* [docker 安装](/install?id=方式一：docker-安装)
* [手动安装](/install?id=方式二：手动安装)
* [其他安装方式](/install?id=其他安装方式)
* [其他非官方教程](/install?id=其他非官方教程)

## 方式一：docker 安装

docker 镜像安装更适用于 Linux 系统。对于 Windows 和 Mac ，由于底层音频驱动方式不同，没办法实现离线唤醒和语音播放的功能，但后台端的文本或录音的交互依然可用。

### X86-64 架构设备

首先确保已经 [安装 docker](https://docs.docker.com/install/)。

如果你的设备是普通的 X86-64 架构设备（例如 PC 或 Mac） ，可以使用 wzpan/wukong-robot 镜像：

``` bash
docker pull wzpan/wukong-robot:latest
```

!> 如果遇到 docker 拉取慢的问题，你或许需要考虑先配置好[docker加速器](https://www.daocloud.io/mirror#accelerator-doc)。

对于 Linux 系统，可以将 `/dev/snd` 桥接给 docker，这样可以实现声卡的支持：

``` bash
docker run -it -p 5000:5000 --device /dev/snd wzpan/wukong-robot:latest
```

而对于 Mac 和 Windows 系统，则只能放弃声卡的支持：

``` bash
docker run -it -p 5000:5000 wzpan/wukong-robot:latest
```

因此 Mac 系统更推荐手动安装的方式。而 Windows ，则可以参考 [其他安装方式](#其他安装方式) 中的一键自动安装脚本。

`docker run` 完成后，就可以参考 [运行](/run?id=运行) 一节，启动 wukong-robot 了。

!> 注意：每次重启 Docker 后镜像内的数据会被重置。如果不希望每次 Docker 每次重启导致数据丢失，可以使用 Docker commit 命令保存镜像的改动。详见 [Docker保存修改后的镜像](https://www.jianshu.com/p/2885eaa5d36d) 。

### ARM 架构设备

如果你的设备是 ARM 架构设备（例如树莓派 3B），可以使用 wzpan/wukong-robot-arm 镜像（注意 Pi Zero 是 armv6l 架构，因此不支持 docker 安装，请使用手动安装）：

``` bash
git clone https://github.com/wzpan/wukong-robot-pi-installer.git
cd wukong-robot-pi-installer
sudo ./pi_installer
```

!> 如果遇到 docker 拉取慢的问题，你或许需要考虑先配置好[docker加速器](https://www.daocloud.io/mirror#accelerator-doc)。

然后使用如下命令启动 docker 镜像即可：

``` bash
docker run -it -p 5000:5000 --device /dev/snd -e LANG=C.UTF-8 wzpan/wukong-robot-arm:latest
```

如果运行时提示

```
docker: unknown server OS: .
```

则可以在上面的命令前带上 `sudo` 再试。

`docker run` 完成后，就可以参考 [运行](/?id=运行) 一节，启动 wukong-robot 了。

!> 注意：每次重启 Docker 后镜像内的数据会被重置。如果不希望每次 Docker 每次重启导致数据丢失，可以使用 Docker commit 命令保存镜像的改动。详见 [Docker保存修改后的镜像](https://www.jianshu.com/p/2885eaa5d36d) 。

## 方式二：手动安装

### 1. 克隆本仓库：

``` bash
git clone https://github.com/wzpan/wukong-robot.git
```

### 2. 安装 sox ，ffmpeg 和 PyAudio：

#### Linux 系统：

``` bash
sudo apt-get install portaudio19-dev python-pyaudio python3-pyaudio sox pulseaudio libsox-fmt-all ffmpeg
pip3 install pyaudio
```

?> 如果遇到 pip3 安装慢的问题，可以考虑使用 Pypi 镜像。例如 [清华大学 Pypi 镜像](https://mirror.tuna.tsinghua.edu.cn/help/pypi/) 。

#### Mac 系统：

``` bash
brew install portaudio --HEAD  # 安装 Git 最新版本，确保 Big Sur 系统可用
brew install sox ffmpeg
pip3 install pyaudio
```

!> 如果你没有 Homebrew ，参考[本文](http://brew.sh/)安装

### 3. 安装依赖的库：

``` bash
cd wukong-robot
pip3 install -r requirements.txt
```

### 4. 编译 _snowboydetect.so

[手动编译 snowboy](https://github.com/wzpan/snowboy) ，得到 _snowboydetect.so ，以支持更多的平台。

#### 安装 swig

首先确保你的系统已经装有 swig 。

对于 Linux 系统：

``` bash
wget https://wzpan-1253537070.cos.ap-guangzhou.myqcloud.com/misc/swig-3.0.10.tar.gz
tar xvf swig-3.0.10.tar.gz
cd swig-3.0.10
sudo apt-get -y update
sudo apt-get install -y libpcre3 libpcre3-dev
./configure --prefix=/usr --without-clisp --without-maximum-compile-warnings
make
sudo make install
sudo install -v -m755 -d /usr/share/doc/swig-3.0.10
sudo cp -v -R Doc/* /usr/share/doc/swig-3.0.10
sudo apt-get install -y libatlas-base-dev
```

如果提示找不到 `python3-config` 命令，你还需要安装 `python3-dev`：

``` bash
sudo apt-get install python3-dev  # 注意 Ubuntu 18.04 可能叫 python3-all-dev
```

对于 Mac 系统：

``` bash
brew install swig wget
```

#### 构建 snowboy

``` bash
wget https://wzpan-1253537070.cos.ap-guangzhou.myqcloud.com/misc/snowboy.tar.bz2 # 使用我fork出来的版本以确保接口兼容
tar -xvjf snowboy.tar.bz2
cd snowboy/swig/Python3
make
cp _snowboydetect.so <wukon-robot的根目录/snowboy/>
```

!> 如果 make 阶段遇到问题，尝试在 [snowboy 项目 issue 中找到解决方案](https://github.com/Kitt-AI/snowboy/issues) 。

使用 Mac 、Ubuntu 16.04 、Deepin 和 Raspberry Pi 系统的用户也可以试试预编译好的版本：

* [Mac](http://hahack-1253537070.file.myqcloud.com/misc/snowboy-mac/_snowboydetect.so)
* [Ubuntu](http://hahack-1253537070.file.myqcloud.com/misc/snowboy-ubuntu16.04/_snowboydetect.so)
* [Deepin](http://hahack-1253537070.file.myqcloud.com/misc/snowboy-deepin/_snowboydetect.so)
* [Raspberry Pi](http://hahack-1253537070.file.myqcloud.com/misc/snowboy-pi/_snowboydetect.so)

### 5. 安装第三方技能插件库 wukong-contrib

``` bash
mkdir $HOME/.wukong
cd $HOME/.wukong
git clone http://github.com/wzpan/wukong-contrib.git contrib
pip3 install -r contrib/requirements.txt
```

### 6. 更新唤醒词（可选，树莓派必须）

默认自带的唤醒词是在 Macbook 上录制的，用的是作者的声音模型。但由于不同的人发声不同，所以不保证对于其他人都能很好的适用。

而树莓派上或者其他板子上接的麦克风可能和 PC 上的麦克风的声音畸变差异非常大，所以现有的模型更加不能直接在树莓派上工作，否则效果会非常糟糕。

如果你是第一次使用，需要先创建一个配置文件方便配置唤醒词。这个工作可以交给 wukong-robot 帮你完成。在 wukong-robot 的根目录下执行：

``` bash
python3 wukong.py
```

第一次启动将提示你是否要到用户目录下创建一个配置文件，输入 `y` 即可。配置文件将会保存在 `~/.wukong/config.yml` 。

接下来我们来训练和更新唤醒词。比较建议[自行训练自己的模型](/tips?id=_2-%e4%bf%ae%e6%94%b9%e5%94%a4%e9%86%92%e8%af%8d)，然后把模型放在 `~/.wukong` 中，并修改 `~/.wukong/config.yml` 里的几个 hotword 指向的文件名（如果文件名没改，则不用变）。一共有三个唤醒词需要修改：

1. `hotword`：全局唤醒词。默认为 “孙悟空” （wukong.pmdl）
2. `/do_not_bother/on_hotword`：让 wukong-robot 进入勿扰模式的唤醒词。默认为 “悟空别吵” （悟空别吵.pmdl）
3. `/do_not_bother/off_hotword`：让 wukong-robot 结束勿扰模式的唤醒词。默认为 “悟空醒醒” （悟空醒醒.pmdl）

对于树莓派用户，如果不想自己训练模型，wukong-robot 也提供了几个针对树莓派训练的模型，直接修改配置即可：

``` yaml
# snowboy 离线唤醒
# 建议使用 snowboy-seasalt (https://snowboy.hahack.com)
# 使用相同环境录入你的语音，以提升唤醒成功率和准确率
hotword: 'wukong_pi.pmdl'  # 唤醒词模型，如要自定义请放到 $HOME/.wukong 目录中
sensitivity: 0.4  # 灵敏度

# 勿扰模式，该时间段内自动进入睡眠，避免监听
do_not_bother:
    enable: false # 开启勿扰模式
    since: 23    # 开始时间
    till: 9      # 结束时间，如果比 since 小表示第二天
    on_hotword: '悟空别吵_pi.pmdl'  # 通过这个唤醒词可切换勿扰模式。默认是“悟空别吵”
    off_hotword: '悟空醒醒_pi.pmdl'  # 通过这个唤醒词可切换勿扰模式。默认是“悟空醒醒”
```

但是建议[自己训练](/tips?id=_2-%e4%bf%ae%e6%94%b9%e5%94%a4%e9%86%92%e8%af%8d)。snowboy 官方建议在树莓派上先用 `rec t.wav` 这样的命令录制唤醒词，然后在训练的时候通过上传按钮上传到服务器中进行训练：

![](https://github.com/rhasspy/snowboy-seasalt/raw/master/screenshot.png)

- 完成后修改下 config.yml 把唤醒词改成刚刚训练的唤醒词即可。

#### CentOS 没声音问题解决

有用户在 CentOS 系统中遇到播放没声音的问题。解决方法是：

``` sh
mknod /dev/dsp c 14 3
chmod 666 /dev/dsp
```

## 其他安装方式 ##

除了官方提供的安装方法外，还有一些热心用户提供了其他可选的安装方案。

!> 使用第三方安装方式可能会无法正常获取更新，请慎重考虑。

1. 小白同学 @musistudio 提供了一个[一键自动安装脚本](https://github.com/musistudio/wukong-robot-install-script)，适用于 MacOS/Ubuntu/WSL（Windows Subsystem for Linux） 系统。
2. 用户QQ群（580447290）上还有一些用户提供了树莓派的安装镜像，可以入群索取。

## 其他非官方教程 ##

这里收录一些非官方课程。如果你也录制了课程，欢迎[给这个文档仓库](https://github.com/wzpan/wukong-contrib)提PR。

1. [树莓派语音机器人接入homeassistant控制nodemcu开发板教程](https://www.bilibili.com/video/av46877916?from=search&seid=7428641102072962094)
2. [人工智能开发实战：悟空智能音箱](https://www.boxuegu.com/live/detail-1319)

## AnyQ 安装（可选） ##

如果希望使用 [AnyQ](https://github.com/baidu/AnyQ) 作为聊天机器人，需要先安装 AnyQ 。

### X86-64 架构设备 ###

对于 X86-64 架构（例如 PC 或 Mac），推荐使用 docker 安装：

``` bash
docker pull keejo/anyq:1.0
```

然后使用如下命令启动 AnyQ 服务和 solr 引擎：

``` bash
docker run -it -p 8999:8999 -p 8900:8900 keejo/anyq:1.0 ./run.sh
```

然后可以在当前机器上访问 <http://localhost:8999/anyq?question=账号> 确认是否正常返回。

### ARM 架构设备 ###

ARM 架构设备（例如树莓派）需要则手动编译安装。安装前请确保满足以下依赖：

* cmake 3.0以上(推荐3.2.2版本)
* g++ >=4.8.2
* bison >=3.0

安装命令：

``` bash
mkdir build && cd build && cmake .. && make
```

完成后执行如下命令启动 AnyQ 服务和 solr 引擎：

``` bash
# 进入目录
cd /home/AnyQ/build
# 启动solr
sh solr_script/anyq_solr.sh solr_script/sample_docs
# 启动AnyQ
./run_server
```

然后可以在当前机器上访问 <http://localhost:8999/anyq?question=账号> 确认是否正常返回。

## HanTTS 安装（可选） ##

如果要使用 HanTTS 以实现本地 TTS 服务，则需要先从 SourceForge 下载语音库 [syllables.zip](https://sourceforge.net/projects/hantts/files/?source=navbar) 。完成后解压到 ~/.wukong 目录下。

相关配置：

``` yaml
# 语音合成服务配置
# 可选值：
# han-tts       - HanTTS
# baidu-tts     - 百度语音合成（推荐）
# xunfei-tts    - 讯飞语音合成
# ali-tts       - 阿里语音合成（推荐）
# tencent-tts   - 腾讯云语音合成（推荐）
tts_engine: han-tts

# HanTTS 服务
han-tts:
    # 所使用的语音库目录
    # 需放在 ~/.wukong/ 目录下
    # 也支持自行录制，详见：
    # https://github.com/junzew/HanTTS
    voice: 'syllables'
```

如果希望自己录制语音，可以参见 [HanTTS 提供的官方教程](https://github.com/junzew/HanTTS/blob/master/README.zh.md#%E5%BD%95%E5%88%B6%E6%96%B0%E7%9A%84%E8%AF%AD%E9%9F%B3%E5%BA%93)。

