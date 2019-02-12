# 安装 wukong-robot

你可以选择 docker 安装或者手动安装两种方式。

* [docker 安装](#方式一docker-安装)
* [手动安装](#方式二手动安装)

## 方式一、docker 安装

docker 镜像安装更适用于 PC 的 Linux 系统。对于 Windows 和 Mac ，由于底层音频驱动方式不同，没办法实现离线唤醒和语音播放的功能，但后台端的文本或录音的交互依然可用。

!> 目前 docker 镜像不支持 ARM 架构，请不要在树莓派等 ARM 架构上尝试。

``` sh
docker pull wzpan/wukong-robot:latest
```

对于 Linux 系统，可以将 `/dev/snd` 桥接给 docker，这样可以实现声卡的支持：

``` sh
docker run --rm -it -p 5000:5000 --device /dev/snd wzpan/wukong-robot:latest
```

而对于 Mac 和 Windows 系统，则只能放弃声卡的支持：

``` sh
docker run --rm -it -p 5000:5000 wzpan/wukong-robot:latest
```

因此 Mac 系统更推荐手动安装的方式。而 Windows ，则建议装个 Linux 虚拟机来跑 wukong-robot 。

!> 如果遇到 docker 拉取慢的问题，你或许需要考虑先配置好[docker加速器](https://www.daocloud.io/mirror#accelerator-doc)。

`docker run` 完成后，就可以参考 [运行](/?id=运行) 一节，启动 wukong-robot 了。

## 方式二、手动安装

### 1. 克隆本仓库：

``` bash
git clone https://github.com/wzpan/wukong-robot.git
```

### 2. 安装 sox 和 PyAudio：

#### Linux 系统：

``` bash
sudo apt-get install python-pyaudio python3-pyaudio sox libsox-fmt-all
pip3 install pyaudio
```

#### Mac 系统：

``` bash
brew install portaudio sox
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

使用 Mac 、Ubuntu 和 Deepin 系统的用户也可以试试预编译好的版本：

* [Mac](http://hahack-1253537070.file.myqcloud.com/misc/snowboy-mac/_snowboydetect.so)
* [Ubuntu](http://hahack-1253537070.file.myqcloud.com/misc/snowboy-ubuntu16.04/_snowboydetect.so)
* [Deepin](http://hahack-1253537070.file.myqcloud.com/misc/snowboy-deepin/_snowboydetect.so)

### 5. 安装第三方技能插件库 dingdang-contrib

``` bash
cd $HOME/.wukong
git clone http://github.com/wzpan/wukong-contrib contrib
pip3 install -r contrib/requirements.txt
```
