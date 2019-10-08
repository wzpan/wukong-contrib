# 在您的系统上部署homeassistant以及wukong-robot

关于homeassistant部署的其他问题，组件使用方式或了解更多请进入[官网](https://www.home-assistant.io)寻找答案

您可以在本文档找到这些指引

* [安装homeassistant](/install?id=方式二：手动安装)
* [在您的homeassistant系统（hass.io）上通过安装插件以快速安装wukong-robot](/install?id=方式二：手动安装)
* [在hass.io上配置并运行您的wukong-robot插件](/install?id=其他安装方式)
* [进行简单的homeassistant配置](/install?id=其他安装方式)
* [制作一个简单的兼容homeassistant的传感器或一个wifi开关](/install?id=其他安装方式)
* [配置wukong-robot的homeassistant技能插件](/install?id=其他安装方式)
* [trouble shooting  问题与解决方案](/install?id=其他安装方式)

## 安装homeassistant

本章节中产生的问题您可以前往homeassistant[官网](https://www.home-assistant.io/hassio/installation/)或[论坛](https://community.home-assistant.io/)尝试寻找答案

所有的homeassistant前端ui都可以在```http://ipaddress:8123/```访问，**ipadress**是您安装homeassistant的机器的局域网ip地址，一般您可以在

路由器的管理页面中找到

### 方法1：部署含有hass.io的系统（强烈推荐）

hass.io是一个为homeassistant开发的**插件**，您可以将其理解成一个系统管理器。他可以帮助你用最简单的方式安装大量有用的插件，且保护您的系

不受不良插件影响。hass.io采用应用商店的设计，通过添加不同存储库，您可以免费安装世界各地开发者的优秀插件，包括本文中的wukong-robot插件

#### 使用已封装的镜像进行快速安装（强烈推荐）

兼容以下设备：

Raspberry Pi Zero （不推荐）

Raspberry Pi Zero W （不推荐）

Raspberry Pi 1 Model B（不推荐）

Raspberry Pi 2 Model B

Raspberry Pi 3 Model B and B+  (推荐)

Raspberry Pi 4 Model B  (推荐)

Tinkerboard

Odroid-C2

Odroid-XU4

OrangePi-Prime

Intel-Nuc

或使用虚拟机：

官方提供VHDX、VMDK、VDI的虚拟磁盘镜像，覆盖大多数需求

点击[此处](https://www.home-assistant.io/hassio/installation/)前往官网下载官方对应您设备的的hassbian

使用 balenaEtcher将下载好的系统镜像压缩包解压后写入一张大于等于16GB的TF卡

!> 强烈建议使用高品质sd卡来保障流畅的使用体验，低速或低容量的TF卡可导致极为糟糕的使用体验

本方法安装后您可以在```http://hassio.local```和```http://ipaddress:8123/```连接到您的homeassistant前端ui

#### 从您已有的homeassistant迁移全部配置到最新版本的hass.io版本

得益于homeassistant的集中化配置存储设计，您只需要拷贝整个```/config```目录下内容并将其覆盖到您最新安装的hass.io的```/config```目录下

并停止您旧的homeassistant服务，即可完全无损迁移安装。

#### 若您已通过别的办法进行了homeassistant的安装，或您的设备不在镜像支持列表内，您可以使用下列方法手动部署安装hass.io组件，而无需从头安装整个homeassistant。

第一步：安装依赖，使你的系统可以安装hass.io
```
sudo -i
apt-get install software-properties-common
add-apt-repository universe
apt-get update
apt-get install -y apparmor-utils apt-transport-https avahi-daemon ca-certificates curl dbus jq network-manager socat
curl -fsSL get.docker.com | sh
```

第二步：安装hass.io

在多数通用linux系统上您通过这条命令即可安装(arch linux/debian/ubuntu)

```
curl -sL "https://raw.githubusercontent.com/home-assistant/hassio-installer/master/hassio_install.sh" | bash -s
```

在部分系统上您需要输入额外的```arguement```（额外选项）来选择机器型号例如：您使用树莓派3，命令则是

```
curl -sL "https://raw.githubusercontent.com/home-assistant/hassio-installer/master/hassio_install.sh" | bash -s -- -m raspberrypi3
```
规律是：```-m 机器型号```

机器型号有下列选择：（若您的设备不在列表中，请使用第一条命令进行通用安装）
```
intel-nuc
raspberrypi
raspberrypi2
raspberrypi3
raspberrypi3-64
odroid-c2
odroid-cu2
odroid-xu
orangepi-prime
```

备注：若出现依赖错误，请尝试自行百度解决


### 只安装homeassistant，不安装hass.io

!>使用此方法您将无法使用wukong-robot插件，若您依旧想使用wukong-robot，请参照文档**安装**章节进行安装，然后回到本章节的**配置wukong-robot的homeassistant技能插件** 段落进行配置

依次运行这些命令来进行安装

如果出现权限错误，尝试命令前加上**sudo**

```
python3 -m venv homeassistant
cd homeassistant
source bin/activate
python3 -m pip install homeassistant
```
运行：

```
hass --open-ui
```

升级：

首先停止homeassistant

```
cd homeassistant
source bin/activate
python3 -m pip install --upgrade homeassistant
```

本方法安装后您可以在```http://ipaddress:8123/```连接到您的homeassistant前端ui界面


## 在您的homeassistant系统（hass.io）上通过安装插件以快速安装wukong-robot
