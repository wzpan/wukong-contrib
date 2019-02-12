# 配置 #

参考[配置文件的注释](https://github.com/wzpan/wukong-robot/blob/master/static/default.yml)进行配置即可。注意不建议直接修改 default.yml 里的内容，否则会给后续通过 `git pull` 更新带来麻烦。你应该拷贝一份放到 `$HOME/.wukong/config.yml` 中，或者在运行的时候按照提示让 wukong-robot 为你完成这件事。

几个 tips：

1. 建议在运行 wukong-robot 的机器上重新训练一下唤醒词，不同设备录制出来的唤醒词模型使用效果会大打折扣。比如，如果你是在电脑上访问snowboy网站训练唤醒词，然后到树莓派上用，那么唤醒成功率和正确率就会很不理想。树莓派的唤醒词录制方法可以参见 [snowboy 教程](http://docs.kitt.ai/snowboy/#my-trained-model-works-well-on-laptops-but-not-on-pi-s) 。
2. 不论使用哪个厂商的API，都建议注册并填上自己注册的应用信息，而不要用默认的配置。这是因为这些API都有使用频率和并发数限制，过多人同时使用会影响服务质量。
3. 如果使用网易邮箱，还需设置允许第三方客户端收发邮件：

  <http://config.mail.163.com/settings/imap/index.jsp?uid=您的邮箱地址>

  注意把链接中 您的邮箱地址 改为您真实的网易邮箱地址（带邮箱后缀）。
