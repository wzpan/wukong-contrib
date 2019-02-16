# 安装 wukong-robot

你可以选择 docker 安装或者手动安装两种方式。

* [docker 安装](/install?id=方式一：docker-安装)
* [手动安装](/install?id=方式二：手动安装)

## 方式一：docker 安装

docker 镜像安装更适用于 PC 的 Linux 系统。对于 Windows 和 Mac ，由于底层音频驱动方式不同，没办法实现离线唤醒和语音播放的功能，但后台端的文本或录音的交互依然可用。

!> 目前 docker 镜像不支持 ARM 架构，请不要在树莓派等 ARM 板上尝试。

``` bash
docker pull wzpan/wukong-robot:latest
```

对于 Linux 系统，可以将 `/dev/snd` 桥接给 docker，这样可以实现声卡的支持：

``` bash
docker run --rm -it -p 5000:5000 --device /dev/snd wzpan/wukong-robot:latest
```

而对于 Mac 和 Windows 系统，则只能放弃声卡的支持：

``` bash
docker run --rm -it -p 5000:5000 wzpan/wukong-robot:latest
```

因此 Mac 系统更推荐手动安装的方式。而 Windows ，则建议装个 Linux 虚拟机来跑 wukong-robot 。

!> 如果遇到 docker 拉取慢的问题，你或许需要考虑先配置好[docker加速器](https://www.daocloud.io/mirror#accelerator-doc)。

`docker run` 完成后，就可以参考 [运行](/?id=运行) 一节，启动 wukong-robot 了。

## 方式二：手动安装

### 1. 克隆本仓库：

``` bash
git clone https://github.com/wzpan/wukong-robot.git
```

### 2. 安装 sox ，ffmpeg 和 PyAudio：

#### Linux 系统：

``` bash
sudo apt-get install python-pyaudio python3-pyaudio sox libsox-fmt-all ffmpeg
pip3 install pyaudio
```

#### Mac 系统：

``` bash
brew install portaudio sox ffmpeg
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
wget http://hahack-1253537070.file.myqcloud.com/misc/swig-3.0.10.tar.gz
tar xvf swig-3.0.10.tar.gz
cd swig-3.0.10
sudo apt-get -y update
sudo apt-get install -y libpcre3 libpcre3-dev
./configure --prefix=/usr --without-clisp --without-maximum-compile-warnings
make
make install
install -v -m755 -d /usr/share/doc/swig-3.0.10
sudo cp -v -R Doc/* /usr/share/doc/swig-3.0.10
sudo apt-get install -y libatlas-base-dev
```

如果提示找不到 `python3-config` 命令，你还需要安装 `python3-dev`：

``` bash
sudo apt-get install python3-dev  # 注意 Ubuntu 18.04 可能叫 python3-all-dev
```

对于 Mac 系统：

``` bash
brew install swig
```

#### 构建 snowboy

``` bash
git clone https://github.com/wzpan/snowboy.git  # 使用我fork出来的版本以确保接口兼容
cd swig/Python3
make
cp _snowboydetect.so <wukon-robot的根目录/snowboy/>
```

!> 如果 make 阶段遇到问题，尝试在 [snowboy 项目 issue 中找到解决方案](https://github.com/Kitt-AI/snowboy/issues) 。

使用 Mac 、Ubuntu 16.04 、Deepin 和 Raspberry Pi 系统的用户也可以试试预编译好的版本：

* [Mac](http://hahack-1253537070.file.myqcloud.com/misc/snowboy-mac/_snowboydetect.so)
* [Ubuntu](http://hahack-1253537070.file.myqcloud.com/misc/snowboy-ubuntu16.04/_snowboydetect.so)
* [Deepin](http://hahack-1253537070.file.myqcloud.com/misc/snowboy-deepin/_snowboydetect.so)
* [Raspberry Pi](http://hahack-1253537070.file.myqcloud.com/misc/snowboy-pi/_snowboydetect.so)

### 5. 安装第三方技能插件库 dingdang-contrib

``` bash
cd $HOME/.wukong
git clone http://github.com/wzpan/wukong-contrib contrib
pip3 install -r contrib/requirements.txt
```

### 6. 更新唤醒词（可选，树莓派必须）

默认自带的唤醒词是在 Macbook 上录制的，用的是作者的声音模型。但由于不同的人发声不同，所以不保证对于其他人都能很好的适用。

而树莓派上或者其他板子上接的麦克风可能和 PC 上的麦克风的声音畸变差异非常大，所以现有的模型更加不能直接在树莓派上工作，否则效果会非常糟糕。

比较建议到 [snowboy 官网](https://snowboy.kitt.ai/dashboard) 上训练自己的模型，然后把模型放在 `~/.wukong` 中，并修改 `~/.wukong/config.yml` 里的几个 hotword 指向的文件名（如果文件名没改，则不用变）。一共有三个唤醒词需要修改：

1. `hotword`：全局唤醒词。默认为 “孙悟空” （wukong.pmdl）
2. `/do_not_bother/on_hotword`：让 wukong-robot 进入勿扰模式的唤醒词。默认为 “悟空别吵” （悟空别吵.pmdl）
3. `/do_not_bother/off_hotword`：让 wukong-robot 结束勿扰模式的唤醒词。默认为 “悟空醒醒” （悟空醒醒.pmdl）

对于树莓派用户，如果不想自己训练模型，wukong-robot 也提供了几个针对树莓派训练的模型，直接修改配置即可：

``` yaml
# snowboy 离线唤醒
# https://snowboy.kitt.ai/dashboard
# 建议到 https://snowboy.kitt.ai/hotword/32768
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

但是同样建议到 [snowboy 官网](https://snowboy.kitt.ai/dashboard) 自己训练。snowboy 官方建议在树莓派上先用 `rec t.wav` 这样的命令录制唤醒词，然后在训练的时候通过上传按钮上传到服务器中进行训练：

![](http://docs.kitt.ai/snowboy/_images/upload.png)
