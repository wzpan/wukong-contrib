# 在您的系统上部署 homeassistant 以及 wukong-robot

homeassistant 是一个开源项目，其 logo 与源代码版权由原作者所有，与本项目作者没有任何关系。

智能家庭支持由PatrickChen（github：PatrickChina, QQ：@杭州-PatrickChen）提供，特别感谢wzpan的大力支持。

关于 homeassistant 部署的其他问题，组件使用方式或了解更多请进入[官网](https://www.home-assistant.io)寻找答案。

您可以在本文档找到这些指引：

* [安装 homeassistant](/smarthome?id=安装-homeassistant)
* [在您的 homeassistant 系统（hass.io）上通过安装插件以快速安装 wukong-robot](/smarthome?id=在您的-homeassistant-系统（hassio）上通过安装插件以快速安装-wukong-robot)
* [在 hass.io 上配置并运行您的 wukong-robot 插件](/smarthome?id=在-hassio-上配置并运行您的-wukong-robot-插件)
* [进行简单的 homeassistant 配置](/smarthome?id=进行简单的-homeassistant-配置)
* [配置 wukong-robot 的 homeassistant 技能插件](/smarthome?id=配置-wukong-robot-的-homeassistant-技能插件)
* [trouble shooting/FAQ/常见问题与解决方案](/smarthome?id=trouble-shooting/FAQ/常见问题与解决方案)

## 安装 homeassistant

本章节中产生的问题您可以前往 homeassistant [官网](https://www.home-assistant.io/hassio/installation/)或[论坛](https://community.home-assistant.io/)尝试寻找答案。

所有的 homeassistant 前端 ui 都可以在 <http://ipaddress:8123/> 访问，**ipadress**是您安装homeassistant的机器的局域网ip地址，一般您可以在路由器的管理页面中找到。

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

本方法安装后您可以在<http://hassio.local:8123>和<http://ipaddress:8123/>连接到您的homeassistant前端ui

#### 从您已有的 homeassistant 迁移全部配置到最新版本的 hass.io 版本

得益于 homeassistant 的集中化配置存储设计，您只需要拷贝整个`/config`目录下内容并将其覆盖到您最新安装的 hass.io 的`/config`目录下

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

在部分系统上您需要输入额外的`arguement`（额外选项）来选择机器型号例如：您使用树莓派3，命令则是

```
curl -sL "https://raw.githubusercontent.com/home-assistant/hassio-installer/master/hassio_install.sh" | bash -s -- -m raspberrypi3
```
规律是：`-m 机器型号`

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

备注：若出现依赖错误，请尝试自行百度解决。

安装完毕后请打开 homeassistant 的配置文件**configuration.yaml**

在其中添加独立的两行（均顶格）：
```
discovery:

hassio：
```

### 方法2：只安装 homeassistant，不安装 hass.io

!>使用此方法您将无法使用 wukong-robot hass.io addon 插件，若您依旧想使用 wukong-robot，请参照文档**安装**章节进行安装，然后回到本章节的**配置wukong-robot的homeassistant技能插件** 段落进行配置，您的 homeassistant 和 wukong-robot 将是完全独立的。由于手动安装 wukong-robot 相对麻烦，作者推荐若您有将 wukong-robot 与 homeassistant 配套使用的需求，请尽可能使用 hass.io 插件进行安装。

依次运行这些命令来进行安装。

如果出现权限错误，尝试命令前加上**sudo**。

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
 
第一次运行需要以 root 权限运行 Homeassistant，即`sudo hass --open-ui`

升级：

首先停止 homeassistant

```
cd homeassistant
source bin/activate
python3 -m pip install --upgrade homeassistant
```

本方法安装后您可以在<http://ipaddress:8123/>连接到您的homeassistant前端ui界面


## 在您的 homeassistant 系统（hass.io）上通过安装插件以快速安装 wukong-robot

第一步：打开您的 homeassistant 页面

![主界面](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/hass/smp1.png)

第二步：点击 hass.io 图标，切换到 ADD-ON STORE 选项卡

第三步：复制本链接<https://github.com/PatrickChina/wukonghass>并粘贴到**add newrepository by URL**处，点击add

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

第七步：使用您电脑上的 windows 资源管理器或访达连接到 homeassistant 的 FTP 服务器地址是：`ftp://yourhassip`将**yourhassip**替换成您homeassistant的局域网ip地址(用户名**hassio**,密码**wukong2019hassio**)

第八步：进入后您应该看到一个名叫**share**的文件夹，打开这个文件夹，在**share**下新建一个文件夹，命名为**wukongdata**

第九步：右键点击[这里](https://github.com/PatrickChina/wukonghass/raw/master/wukong/config.yml)，选择**链接另存为（windows chrome）**或**从链接另存文件为（ubuntu firefox）**或您系统的同义选项来下载wukong-robot的默认配置文件，下载后将其复制到您新建的**wukongdata**文件夹目录下，请不要重命名！

右键点击[这里](https://github.com/PatrickChina/wukonghass/raw/master/wukong/wukong.pmdl)，选择**链接另存为（windows chrome）**或**从链接另存文件为（ubuntu firefox）**或您系统的同义选项来下载wukong-robot的默认唤醒词，下载后将其复制到您新建的**wukongdata**文件夹目录下，请不要重命名！

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

 接下来关于wukong-robot的配置请访问本文档的**配置**部分了解更多,本插件的配置方式与其他方式安装的wukong-robot完全相同，您可以在hass.io插件页面顶部点击
**OPEN WEB UI**或者访问<http://youripaddress:5000>来访问wukong-robot的后台管理页面，`youripaddres`替换为您homeassistant所处设备的局域网ip地址。

## 进行简单的 homeassistant 配置

先为大家推荐两个论坛地址和两篇教程

- 论坛1.hassbian 网址 https://bbs.hassbian.com
- 论坛2.HAchina  网址https://www.hachina.io/
- 教程1：https://bbs.hassbian.com/thread-370-1-1.html
- 教程2：https://bbs.hassbian.com/thread-31-1-1.html

!>仅是作者个人推荐，选择了主观上质量相对优秀的论坛和教程进行推荐。论坛与作者和wzpan无关，内容不由我们可控，因此我们不对推荐链接中的内容负任何责任，也不保证内容质量

### 入门站：访问您的homeassistant配置文件夹目录

第一步：访问hass.io addon store选项卡，点击**install**安装Samba Share的hass.io插件

![ss1](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/hass/ss3.png)
![ss2](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/hass/ss2.png)

第二步：安装过程应该在5分钟内完成，完成后从**DASHBOARD**进入插件，应该能看到UNINSTALL REBUILD START的选项。此时请不要急着START，此时由于未进行配置也无法正常启动。

第三步：向下滑动页面直至看到`config`选项卡如图所示：

![ss3](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/hass/ss1.png)

第四步：复制下面的配置**覆盖**粘贴到`config`选项卡内，并将**hassio**替换成您的用户名，将**password**替换成您的密码，此处的密码请您务必更换并牢记。**不要忘记点击SAVE保存配置**
```
{
  "workgroup": "WORKGROUP",
  "username": "hassio",
  "password": "password",
  "interface": "",
  "allow_hosts": [
    "10.0.0.0/8",
    "172.16.0.0/12",
    "192.168.0.0/16"
  ]
}
```
第五步：滑动页面到顶部点击**START**来启动Samba share

第六步：连接并访问您的homeassistant配置文件夹。

Windows：

确保您的电脑与homeassistant在同一局域网下在图中标注处输入`\\youripaddress\config`替换youripaddress为您homeassistant的局域网ip地址（一般情况下请访问您路由器的管理页面获得ip地址），由于作者的ip地址是192.168.1.28,因此如图所示。在弹出的窗口中输入您上一步设置的用户名与密码。

![ss4](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/hass/w1.png)

您应该看如下图所示页面，此时您已经访问到homeassistant的配置文件目录。您对homeassistant进行的大部分配置都需要通过修改本目录下的某个文件来实现。

![ss5](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/hass/w2.png)

MAC OS：

确保您的电脑与homeassistant在同一局域网下,打开访达，切换到网络选项卡，将鼠标移动到顶部选项栏的**前往**菜单栏，选择**前往服务器**

![ss6](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/hass/m4.JPG)

在如图标记处，输入`smb://youripaddress/config`替换youripaddress为您homeassistant的局域网ip地址（一般情况下请访问您路由器的管理页面获得ip地址），由于作者的ip地址是192.168.1.28,因此如下图所示。

![ss7](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/hass/m5.JPG)

点击连接

![ss8](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/hass/m6.JPG)

在弹出的窗口中输入您上一步设置的用户名与密码。

![ss9](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/hass/m2.JPG)

您应该看如下图所示页面，此时您已经访问到homeassistant的配置文件目录。您对homeassistant进行的大部分配置都需要通过修改本目录下的某个文件来实现。

![ss10](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/hass/m1.JPG)

LINUX（UBUNTU)：

确保您的电脑与homeassistant在同一局域网下在图中标注处输入`smb://youripaddress/config`替换youripaddress为您homeassistant的局域网ip地址（一般情况下请访问您路由器的管理页面获得ip地址），由于作者的ip地址是192.168.1.28,因此如图所示。在弹出的窗口中输入您上一步设置的用户名与密码。

![ss11](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/hass/u3.png)

在弹出的窗口中输入你在前面设置的samba密码

![ss12](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/hass/u2.png)

您应该看如下图所示页面，此时您已经访问到homeassistant的配置文件目录。您对homeassistant进行的大部分配置都需要通过修改本目录下的某个文件来实现。

![ss13](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/hass/u3.png)

## 配置 wukong-robot 的 homeassistant 技能插件

详见 [Hass 插件配置](/contrib?id=hass) 。

## trouble shooting/FAQ/常见问题与解决方案

- 问1 :我不想配置wukong-robot hass.io插件的自动备份
- 答1:若您是担心备份配置文件导致隐私泄露，您无需有这个担忧，因为数据存储在本地，不会以任何形式上传到任何外部服务器。若您坚持不配置自动备份，在添加插件存储库URL时请添加这个地址<https://github.com/PatrickChina/wukonghass-avoidbackup>,来替代原本应使用的wukonghass存储库

!>由于两个库的结构，版本，hass.io插件部署文件一样，因此严禁作者的两个插件库同时存在，请明确您的目的后选择正确的存储库添加

- 问2:文档内提到将`customize.yaml`include到`configuration.yaml`中，这该如何操作？
- 答2:您只需要在`configuration.yaml`同目录下创建`customize.yaml`若已存在则无需再创建。然后将这段代码复制到`configuration.yaml`中即可
```
homeassistant:
  customize: !include customize.yaml
```

- 问3: 我遇到了配置正确wukong却回应指令不存在的情况
- 答3:这个问题作者开发时已经发现，且尝试解决，若问题依旧发生，作者深表遗憾。该问题主要由于您使用插件`configurator`来配置您的`wukong:`部分导致。`configurator`是一款很好的插件来帮助您使用web页面配置您的homeassistant，不幸的是作者已经证实使用该插件配置`wukong:`部分会导致wukong-robot无法识别配置，该问题还可能由于您在非官方站点下载hassbian或者您家ip地址非国内ip地址导致的的编码识别错误。解决这个问题请先检查您的配置是否**真的不存在问题**再尝试接下来的解决方案。请尝试安装Samba Share插件并使用Samba访问hass的配置`config`目录，并将`customize.yaml`复制到本地，使用您的本地文本编辑器尝试重写`wukong：`部分，同时在另存为时选择`UTF-8`编码方式，然后删除您服务器内的`customize.yaml`,并将您本地另存为后的文件上传到服务器配置文件夹内。此时您的问题应当被解决。

- 问4:我想要访问来自wukong-robot的log信息
- 答4:请进入hass.io插件界面，滚动到页面底部，点击refresh即可获得来自wukong-robot的全部log信息。

- 问5:wukong-robot没有正常启动，我无法访问其后台管理界面
- 答5:插件安装不应出现任何依赖或文件缺失问题，请确认您按步骤进行了配置，重试后若依旧存在问题请联系作者。

- 问6:如何在插件环境内更新wukong-robot的唤醒词
- 答6:使用您的电脑访问**wukongdata**文件夹（参照配置自动备份中的第七、八、九 步骤），将您的新唤醒词重命名为**wukong.pmdl** (必须)，并覆盖**wukongdata**中的**wukong.pmdl**文件。（为避免ftp导致的覆盖错误，建议先删除**wukongdata**中的**wukong.pmdl**再上传您新的重命名完毕的唤醒词），重启**插件**，即可正常使用新唤醒词唤醒。
