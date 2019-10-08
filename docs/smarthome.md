# 在您的系统上部署homeassistant以及wukong-robot

homeassistant是一个开源项目，其logo与源代码版权由原作者所有，与本项目作者没有任何关系

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

所有的homeassistant前端ui都可以在```http://ipaddress:8123/```访问，**ipadress**是您安装homeassistant的机器的局域网ip地址，一般您可以在路由器的管理页面中找到

### 方法1：部署含有hass.io的系统（强烈推荐）

hass.io是一个为homeassistant开发的**插件**，您可以将其理解成一个系统管理器。他可以帮助你用最简单的方式安装大量有用的插件，且保护您的系统不受不良插件影响。hass.io采用应用商店的设计，通过添加不同存储库，您可以免费安装世界各地开发者的优秀插件，包括本文中的wukong-robot插件

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

第一步：打开您的homeassistant页面

第二步：点击hass.io图标，切换到ADD-ON STORE选项卡

第三步：复制本链接```https://github.com/PatrickChina/wukonghass```并粘贴到**add newrepository by URL**处，点击add

第四步：点击右上角刷新图标，在页面中寻找**wukong-robot**插件，并点击进入

第五步：点击INSTALL，等待hass.io完成安装，由于要下载大量文件进行自动构建，因此会消耗较多时间，请耐心等待。（视网络环境而定）

第六步：安装过程将自动完成，完成后如图所示，请不要急于**START**，请耐心读完本文档，完成配置过程后启动

若安装成功，请向下阅读，若失败请考虑从第四步开始重试

## 在hass.io上配置并运行您的wukong-robot插件

在上一步您完成了wukong-robot的安装，此时您其实已经可以启动wukong-robot并按照wukong-robot文档其余部分进行配置但是您将遇到以下问题：

**每次重启homeassistant后wukong-robot的配置丢失**此问题是由hass.io将插件构建为docker容器运行所导致的，但是经过开发人员的通宵努我们带来了解决方案，此解决方案可能会在未来被更换为更可靠的方案

**无法使用语音与wukong-robot交互**此问题同样由docker的特性导致，所幸我们已经有了可靠的解决方案，请继续阅读

**点击START 后 wukong-robot没有正常启动**这是由第一条问题采用的自动备份逻辑解决方案所导致的，在完成本章节的配置后您的wukong-robot将正常启动，若您不想配置自动备份，请切换到trouble shooting寻找替代方案。

### 配置自动备份

第一步：参考上一段，再次进入ADD-ON STORE

第二步：ADD-on store 内寻找插件**FTP**

第三步：点击INSTALL，等待hass.io完成安装

第四步：切换到DASH BOARD选项卡，点击插件FTP，进入页面后不要START！请保持**Start on boot**开关处于激活状态。向下滚页面，直至显示**config**配置框

第五步：使用以下内容**覆盖**默认配置，请**不要**修改任何配置内容**包括**用户名密码！
```
{
  "port": 21,
  "data_port": 20,
  "banner": "Welcome to the Hass.io FTP service.",
  "pasv": true,
  "pasv_min_port": 30000,
  "pasv_max_port": 30010,
  "pasv_address": "",
  "ssl": false,
  "certfile": "fullchain.pem",
  "keyfile": "privkey.pem",
  "implicit_ssl": false,
  "max_clients": 5,
  "users": [
    {
      "username": "hassio",
      "password": "wukong2019hassio",
      "allow_chmod": true,
      "allow_download": true,
      "allow_upload": true,
      "allow_dirlist": true,
      "addons": false,
      "backup": false,
      "config": false,
      "share": true,
      "ssl": false
    }
  ]
}
```
**由于配置文件暂时不能设置为自己的用户名密码，因此请勿将homeassistant所在设备ip地址上的21端口到外网！！！**

**若您需要直接浏览或编辑homeassistant内的文件，请安装Samba share插件，尽可能避免使用ftp，且ftp是无法直接编辑文件的，也推荐使用Samba代替，关于Samba share相关配置教程请在Samba share插件页面内寻找**

第六步：点击Start，启动FTP插件。

第七步：使用您电脑上的windows资源管理器或访达连接到homeassistant的FTP服务器地址是：```ftp://yourhassip```将**yourhassip**替换成您homeassistant的局域网ip地址

第八步：进入后您应该看到一个名叫**share**的文件夹，打开这个文件夹，在**share**下新建一个文件夹，命名为**wukongdata**

第九步：点击[这里](https://github.com/PatrickChina/wukonghass/raw/master/wukong/config.yml)下载wukong-robot的默认配置文件，下载后将其复制到您新建的**wukongdata**文件夹目录下，请不要重命名！


