# wukong-robot 使用技巧

## 1. 提升唤醒成功率和准确度

snowboy 的唤醒准确率和录制时的设备环境有很大的关系。建议到 [snowboy 官网](https://snowboy.kitt.ai/dashboard)，在运行 wukong-robot 的机器上训练一下唤醒词，不同设备录制出来的唤醒词模型使用效果会大打折扣。详见 [安装教程-更新唤醒词](/install?id=_6-%e6%9b%b4%e6%96%b0%e5%94%a4%e9%86%92%e8%af%8d%ef%bc%88%e5%8f%af%e9%80%89%ef%bc%8c%e6%a0%91%e8%8e%93%e6%b4%be%e5%bf%85%e9%a1%bb%ef%bc%89) 。

另外，如果出现经常误唤醒 wukong-robot ，可以尝试在配置文件中将 `sensitivity` 调低。

## 2. 修改唤醒词

1. 到 https://snowboy.kitt.ai/ ，训练你自己的模型；
2. 下载 pmdl 模型并放到 ~/.wukong 中；
3. 修改 config.yml 的 `model` 配置，改为你训练好的模型的文件名。

## 3. 提升语音识别准确率

不同的厂商都提供了录入自己的词库以提升识别率的方案。以百度的ASR为例，可以将常用的指令、姓名等术语写成一个 command.txt 文件，然后登录您的百度语音应用管理页面，在 【自定义设置】 的 【语音识别词库设置】 项目中，点击 【进行设置】 按钮，上传该指令文件即可。文件内容示例：

```
音乐
下一首歌
下首歌
切歌
上一首歌
上首歌
停止
停止播放
暂停
暂停播放
重新播放
随机播放
单曲循环
大声
小声
大点声
小点声
大声点
小声点
歌单
榜单
几点
时间
邮件
邮箱
绕口令
笑话
搜索
别听我的
听我的
```

## 4. 在外网访问家中的 wukong-robot

有多种方案可以实现内网穿透，例如：

1. [frp](https://diannaobos.com/frp/)
2. [ngrok](https://ngrok.com/)
3. [花生棒](https://hsk.oray.com/device)

可以详细参考如下几篇文章：

* [可以实现内网穿透的几款工具](https://my.oschina.net/ZL520/blog/2086061)
* [内网穿透哪家好？端口映射/DDNS/花生壳/Ngrok/Frp 逐一介绍分析](https://www.zhihu.in/archives/237)
* [内网穿透的一点经验](https://sst.st/p/213)
