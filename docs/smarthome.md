# 在您的系统上部署homeassistant以及wukong-robot


您可以在这里找到这些知识

* [安装homeassistant](/install?id=方式二：手动安装)
* [在您的homeassistant系统（hass.io）上通过安装插件以快速安装wukong-robot](/install?id=方式二：手动安装)
* [在hass.io上配置并运行您的wukong-robot插件](/install?id=其他安装方式)
* [进行简单的homeassistant配置](/install?id=其他安装方式)
* [制作一个简单的兼容homeassistant的传感器或一个wifi开关](/install?id=其他安装方式)
* [配置wukong-robot的homeassistant技能插件](/install?id=其他安装方式)
* [trouble shooting  问题与解决方案](/install?id=其他安装方式)

## 安装homeassistant

### 方法1：部署含有hass.io的系统（强烈推荐）

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


#### 从您已有的homeassistant迁移全部配置到最新版本的hass.io版本

得益于homeassistant的集中化配置存储设计，您只需要拷贝整个```/config```目录下内容并将其覆盖到您最新安装的hass.io的```/config```目录下

并停止您旧的homeassistant服务，即可完全无损迁移安装。

#### 若您已通过别的办法进行了homeassistant的安装，或您的设备不在镜像支持列表内，您可以使用下列方法单独手动部署安装hass.io，而无需从头安装。



