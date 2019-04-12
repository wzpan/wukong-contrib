# wukong-robot

wukong-robot 是一个简单、灵活、优雅的中文语音对话机器人/智能音箱项目，目的是让中国的 Maker 和 Hacker 们也能快速打造个性化的智能音箱。

## 特性

![wukong-robot的特性](https://hahack-1253537070.file.myqcloud.com/images/wukong-docs/wukong-robot-mindmap.png)

* 模块化。功能插件、语音识别、语音合成、对话机器人都做到了高度模块化，第三方插件单独维护，方便继承和开发自己的插件。
* 中文支持。集成百度、科大讯飞、阿里、腾讯等多家中文语音识别和语音合成技术，且可以继续扩展。
* 对话机器人支持。支持接入图灵机器人、Emotibot 等对话机器人。
* 全局监听，离线唤醒。支持无接触地离线语音指令唤醒。
* 灵活可配置。支持定制机器人名字，支持选择语音识别和合成的插件。
* 智能家居。支持和 mqtt、HomeAssistant 等智能家居协议联动，支持语音控制智能家电。
* 后台配套支持。提供配套后台，可实现远程操控、修改配置和日志查看等功能。
* 开放API。可利用后端开放的API，实现更丰富的功能。
* 微信接入。配合 [wukong-itchat](http://github.com/wzpan/wukong-itchat) ，可实现通过微信远程操控自己家中的设备。
* 安装简单，支持更多平台。相比 dingdang-robot ，舍弃了 PocketSphinx 的离线唤醒方案，安装变得更加简单，代码量更少，更易于维护并且能在 Mac 以及更多 Linux 系统中运行。

## Demo

* Demo视频1

coming soon

* Demo视频2：ycy-robot 月芽特别定制版
    
<iframe src="//player.bilibili.com/player.html?aid=48873736&cid=85589172&page=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>
    
* 后台管理端Demo 
    - 体验地址：https://bot.hahack.com/  （体验用户名：wukong；体验密码：wukong@2019）

## 环境要求 ##

### Python 版本 ###

wukong-robot 只支持 Python 3.x，不支持 Python 2.x 。

### 设备要求 ###

wukong-robot 支持运行在以下的设备和系统中：

* 64bit Mac OS X
* 64bit Ubuntu（12.04 and 14.04）
* 全系列的树莓派（Raspbian 系统）
* Pine 64 with Debian Jessie 8.5（3.10.102）
* Intel Edison with Ubilinux （Debian Wheezy 7.8）
* 装有 WSL（Windows Subsystem for Linux） 的 Windows

## 免责声明

* wukong-robot 只用作个人学习研究，如因使用 wukong-robot 导致任何损失，本人概不负责。
* 本开源项目与腾讯叮当助手及优必选悟空项目没有任何关系。
