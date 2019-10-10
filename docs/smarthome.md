# 在您的系统上部署 homeassistant 以及 wukong-robot

homeassistant 是一个开源项目，其 logo 与源代码版权由原作者所有，与本项目作者没有任何关系

关于 homeassistant 部署的其他问题，组件使用方式或了解更多请进入[官网](https://www.home-assistant.io)寻找答案

您可以在本文档找到这些指引

* [安装 homeassistant](/smarthome?id=安装homeassistant)
* [在您的 homeassistant 系统（hass.io）上通过安装插件以快速安装 wukong-robot](/smarthome?id=在您的homeassistant系统（hass.io）上通过安装插件以快速安装wukong-robot)
* [在 hass.io 上配置并运行您的 wukong-robot 插件](/smarthome?id=在 hass.io上配置并运行您的wukong-robot插件)
* [进行简单的 homeassistant 配置](/install?id=进行简单的homeassistant配置)
* [制作一个简单的兼容 homeassistant 的传感器或一个 wifi 开关（comming soon）](/install?id=配置wukong-robot的homeassistant 技能插件)
* [配置 wukong-robot 的 homeassistant 技能插件](/install?id=配置wukong-robot的homeassistant 技能插件)
* [trouble shooting  问题与解决方案](/install?id=无)

## 安装 homeassistant

本章节中产生的问题您可以前往 homeassistant [官网](https://www.home-assistant.io/hassio/installation/)或[论坛](https://community.home-assistant.io/)尝试寻找答案

所有的 homeassistant 前端 ui 都可以在```http://ipaddress:8123/```访问，**ipadress**是您安装homeassistant的机器的局域网ip地址，一般您可以在路由器的管理页面中找到

### 方法1：部署含有 hass.io 的系统（强烈推荐）

hass.io 是一个为 homeassistant 开发的**插件**，您可以将其理解成一个系统管理器。他可以帮助你用最简单的方式安装大量有用的插件，且保护您的系统不受不良插件影响。hass.io 采用应用商店的设计，通过添加不同存储库，您可以免费安装世界各地开发者的优秀插件，包括本文中的 wukong-robot 插件

#### 使用已封装的镜像进行快速安装（强烈推荐）

兼容以下设备：

- Raspberry Pi Zero （不推荐）
- Raspberry Pi Zero W （不推荐）
- Raspberry Pi 1 Model B（不推荐）
- Raspberry Pi 2 Model B
- Raspberry Pi 3 Model B and B+  (推荐)
- Raspberry Pi 4 Model B  (推荐)
- Tinkerboard
- Odroid-C2
- Odroid-XU4
- OrangePi-Prime
- Intel-Nuc

或使用虚拟机：

官方提供 VHDX、VMDK、VDI 的虚拟磁盘镜像，覆盖大多数需求

点击[此处](https://www.home-assistant.io/hassio/installation/)前往官网下载官方对应您设备的的 hassbian

使用 balenaEtcher 将下载好的系统镜像压缩包解压后写入一张大于等于 16GB 的 TF 卡

!> 强烈建议使用高品质 sd 卡来保障流畅的使用体验，低速或低容量的 TF 卡可导致极为糟糕的使用体验

本方法安装后您可以在```http://hassio.local:8123```和```http://ipaddress:8123/```连接到您的homeassistant前端ui

#### 从您已有的 homeassistant 迁移全部配置到最新版本的 hass.io 版本

得益于 homeassistant 的集中化配置存储设计，您只需要拷贝整个```/config```目录下内容并将其覆盖到您最新安装的 hass.io 的```/config```目录下

并停止您旧的 homeassistant 服务，即可完全无损迁移安装。

#### 若您已通过别的办法进行了 homeassistant 的安装，或您的设备不在镜像支持列表内，您可以使用下列方法手动部署安装 hass.io 组件，而无需从头安装整个 homeassistant。

!>若您是所谓的**小白**，不具备基本的linux系统知识或者问题解决能力，或者您只求简单稳妥，作者不推荐您进行手动安装，失败率会相对高。作者建议您使用第一段落的镜像安装方式进行安装，然后迁移您的配置。

第一步：安装依赖，使你的系统可以安装 hass.io
```
sudo -i
apt-get install software-properties-common
add-apt-repository universe
apt-get update
apt-get install -y apparmor-utils apt-transport-https avahi-daemon ca-certificates curl dbus jq network-manager socat
curl -fsSL get.docker.com | sh
```

第二步：安装 hass.io

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

安装完毕后请打开 homeassistant 的配置文件**configuration.yaml**

在其中添加独立的两行（均顶格）：
```
discovery:

hassio：
```

### 方法2：只安装 homeassistant，不安装 hass.io

!>使用此方法您将无法使用 wukong-robot hass.io addon 插件，若您依旧想使用 wukong-robot，请参照文档**安装**章节进行安装，然后回到本章节的**配置wukong-robot的homeassistant技能插件** 段落进行配置，您的 homeassistant 和 wukong-robot 将是完全独立的。由于手动安装 wukong-robot 相对麻烦，作者推荐若您有将 wukong-robot 与 homeassistant 配套使用的需求，请尽可能使用 hass.io 插件进行安装

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
 
第一次运行需要以 root 权限运行 Homeassistant，即```sudo hass --open-ui```

升级：

首先停止 homeassistant

```
cd homeassistant
source bin/activate
python3 -m pip install --upgrade homeassistant
```

本方法安装后您可以在```http://ipaddress:8123/```连接到您的homeassistant前端ui界面


## 在您的 homeassistant 系统（hass.io）上通过安装插件以快速安装 wukong-robot

第一步：打开您的 homeassistant 页面!

[主界面](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/hass/smp1.png)

第二步：点击 hass.io 图标，切换到 ADD-ON STORE 选项卡

第三步：复制本链接```https://github.com/PatrickChina/wukonghass```并粘贴到**add newrepository by URL**处，点击add

![addon](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/hass/smp2.png)

第四步：点击右上角刷新图标，在页面中寻找**wukong-robot**插件，并点击进入

![addon1](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/hass/smp10.png)

第五步：点击 INSTALL，等待 hass.io 完成安装，由于要下载大量文件进行自动构建，因此会消耗较多时间，请耐心等待。（视网络环境而定）

![addon2](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/hass/smp9.png)

第六步：安装过程将自动完成，完成后如图所示，请不要急于**START**，请耐心读完本文档，完成配置过程后启动

![addon3](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/hass/smp8.png)

若安装成功，请向下阅读，若失败请考虑从第四步开始重试

## 在 hass.io 上配置并运行您的 wukong-robot 插件

在上一步您完成了 wukong-robot 的安装，此时您其实已经可以启动 wukong-robot 并按照 wukong-robot 文档其余部分进行配置但是您将遇到以下问题：

**每次重启 homeassistant 后 wukong-robot 的配置丢失**此问题是由 hass.io 将插件构建为 docker 容器运行所导致的，但是经过作者的通宵努力我们带来了解决方案，此解决方案可能会在未来被更换为更可靠的方案

**无法使用语音与 wukong-robot 交互**此问题同样由docker的特性导致，所幸我们已经有了可靠的解决方案，请继续阅读

**点击 START 后 wukong-robot 没有正常启动**这是由第一条问题采用的自动备份逻辑解决方案所导致的，在完成本章节的配置后您的 wukong-robot 将正常启动，若您不想配置自动备份，请切换到 trouble shooting 寻找替代方案。

### 配置自动备份

第一步：参考上一段，再次进入 ADD-ON STORE

第二步：ADD-on store 内寻找插件**FTP**

![addon4](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/hass/smp7.png)

第三步：点击 INSTALL，等待hass.io完成安装

第四步：切换到 DASH BOARD 选项卡，点击插件 FTP，进入页面后不要 START！请保持**Start on boot**开关处于激活状态。向下滚页面，直至显示**config**配置框

![addon5](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/hass/smp5.png)

![addon6](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/hass/smp4.png)

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
**由于配置文件暂时不能设置为自己的用户名密码，因此请勿将 homeassistant 所在设备 ip 地址上的21端口映射到外网！！！**

**若您需要直接浏览或编辑 homeassistant 内的文件，请安装 Samba share 插件，尽可能避免使用 ftp，且 ftp 是无法直接编辑文件的，也推荐使用 Samba 代替，关于 Samba share 相关配置教程请在 Samba share 插件页面内寻找**

第六步：点击 Start，启动 FTP 插件。

第七步：使用您电脑上的 windows 资源管理器或访达连接到 homeassistant 的 FTP 服务器地址是：```ftp://yourhassip```将**yourhassip**替换成您homeassistant的局域网ip地址(用户名**hassio**,密码**wukong2019hassio**)

第八步：进入后您应该看到一个名叫**share**的文件夹，打开这个文件夹，在**share**下新建一个文件夹，命名为**wukongdata**

第九步：右键点击[这里](https://github.com/PatrickChina/wukonghass/raw/master/wukong/config.yml)，选择**链接另存为（windows chrome）**或**从链接另存文件为（ubuntu firefox）**或您系统的同义选项来下载wukong-robot的默认配置文件，下载后将其复制到您新建的**wukongdata**文件夹目录下，请不要重命名！

剩下关于自动备份的操作已经被作者集成在插件中，wukong 将在启动时自动为您搞定

### 至此您已经顺利完成了自动备份的配置，下面开始进行语音交互的配置

为本插件配置音频极为简单，您只需执行这些步骤：

第一步：插入您的usb麦克风，请注意**respeaker**暂不被支持，作者个人推荐使用**ps3eye**，在3.5mm接口插入您的扬声器，或您也可以选择使用usb声卡来同时解决麦克风和扬声器

第二步：进入 homeassistant 的配置页面，点击服务控制，点击重启服务，等待5分钟左右

第三步：重新进入 hass.io 选项卡并点击 wukong-robot ，此时由于系统进行了重启，因此 wukong-robot 已经自动开始运行，请点击**STOP**使其停止运行后再进行后续操作

第四步：向下拉动页面找到**Audio**配置框，在**input**处设定您的输入设备，在**output**处选择您的输出设备（bcm2835_alsa-bcm.2835 ALSA:0是树莓派的板载3.5mm接口输出），配置后点击**SAVE**保存您的配置

![addon7](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/hass/smp6.png)

第五步：向上滑动页面点击**START**来启动您的wukong-robot服务。

至此，对于 wukong-robot 插件的配置已经完全完成，基本保留所有功能不受影响。我后续将会发布一个 homeassitant 插件，让您在 lovelce 中可以直接和 wukong 对话。

![addon8](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/hass/smp3.png)

#### 进行简单的 homeassistant 配置

由于作者依旧在努力完善百度 NLU 数据库，暂时没有时间亲自写入门教程，后续将会补上含有作者经验的入门及进阶教程

先为大家推荐两个论坛地址和两篇教程

- 论坛1.hassbian 网址 https://bbs.hassbian.com
- 论坛2.HAchina  网址https://www.hachina.io/
- 教程1：https://bbs.hassbian.com/thread-370-1-1.html
- 教程2：https://bbs.hassbian.com/thread-31-1-1.html

!>仅是作者个人推荐，选择了主观上质量相对优秀的论坛和教程进行推荐。论坛与作者和wzpan无关，内容不由我们可控，因此我们不对推荐链接中的内容负任何责任，也不保证内容质量

## 配置 wukong-robot 的 homeassistant 技能插件

最新版本插件基于 baidu NLU 进行了改良，可实现一轮对话完成交互，也可使用后台 web 界面进行交互

由于目前没有百度没有提供智能家庭相关 NLU 字典库的支持，因此作者正努力完善自建词典库来实现更准确的命中和更多的语法

如果遇到配置正常，命中插件，wukong 却不回应的情况，说明遇到了词典库的缺失，请尽可能简化您的语法，并将词典库的缺失内容反馈到电子邮箱**cyk0317@sina.com**，或qq群内 @杭州-PatrickChen。作者将尽快更新，本插件的完善将离不开大家的支持。

当前词典数据点击[这里](https://github.com/PatrickChina/wukonghass/blob/master/wukong/user_user_smarthome_%E8%87%AA%E5%AE%9A%E4%B9%89%E8%AF%8D%E5%85%B8%E5%80%BC.txt)查看，您可以使用记事本或浏览器的搜索功能搜索您需要的指令是否在词典中，若不在您则可选择使用存在的近义词，谢谢理解。

### 示例

- 用户：“智能家庭当前温度”
- 悟空：“温度状态是22.6摄氏度”

### 配置

官方api页面：https://home-assistant.io/developers/rest_api/

第一步：

在 homeassistant 的 configuration.yaml 里添加：

``` yaml
api：
  api_password: 
```

修改后 api 插件就启动了

注意:在`api_password: `后设置 api 接口密码，建议设置，但是这个密码在与 wukong 之间通信时用不到，以后自行开发 homeassistant 时可能用到这里的 api 密码，此密码的修改不影响 wukong 工作。（冒号之后有空格！在空格之后直接输入密码无需引号）

第二步：

登陆 homeassistant 网页，在侧拉菜单中点击 homeassistant 字样旁自己的头像，然后将页面拉至最底下找到“长期访问令牌”点击创建令牌，随意取一个名字如： wukong 点击确认

在随后弹出的窗口中复制并想办法记录自己的密钥

第三步：

打开 wukong 的配置文件（网页后台或直接修改都一样），添加：

``` yaml
homeassistant:
    url: "http://127.0.0.1"   #切记加上http://，ip或者域名为你的homeassistant的主机
    port: "8123"             # 端口为你的homeassistant的端口和网页端口一样
    key: "" # 密钥
```

key 处填写的内容如下：

Bearer ABCDE

用第二步获取到的密钥替换 ABCDE (保留 Bearer 和 ABCDE 之间的空格)，将其整体填入双引号中
 

### HomeAssistant 配置

configuration.yaml 相同目录下添加 customize.yaml 并 include 进配置文件。

查看状态类的设备(传感器等)将命令写成 list；控制类的设备命令写成 dict，控制命令为 key ，动作为 value。

现阶段配置时使用的命令建议点击[这里](https://github.com/PatrickChina/wukonghass/blob/master/wukong/user_user_smarthome_%E8%87%AA%E5%AE%9A%E4%B9%89%E8%AF%8D%E5%85%B8%E5%80%BC.txt)参照词典写(使用您的文本编辑器的搜索功能模糊搜索您需要的指令)，避免词典缺失影响使用

如下是示例的部分配置：

``` yaml
sensor.tempareture:
  friendly_name: "环境温度"
  wukong: ["查看环境温度", "当前环境温度", "环境温度"]
sensor.humidity:
  friendly_name: "环境湿度"
  wukong: ["查看环境湿度度", "当前环境湿度", "环境湿度"]
switch.light:
  friendly_name: "补光"
  wukong: {"开始补光":"turn_on", "补光":"turn_on", "停止补光":"turn_off", "结束补光":"turn_off"}
switch.pump:
  friendly_name: "浇水"
  wukong: {"开始浇水":"turn_on", "浇水":"turn_on", "停止浇水":"turn_off", "结束浇水":"turn_off"}  
``` 


