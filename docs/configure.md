# 配置 #

参考[配置文件的注释](https://github.com/wzpan/wukong-robot/blob/master/static/default.yml)进行配置即可。

几个 tips：

1. 不建议直接修改 default.yml 里的内容，否则会给后续通过 `git pull` 更新带来麻烦。你应该拷贝一份放到 `$HOME/.wukong/config.yml` 中，或者在运行的时候按照提示让 wukong-robot 为你完成这件事。

   ?> 配置文件的读取优先级：`$HOME/.wukong/config.yml` > `static/default.yml` 。如果存在 `$HOME/.wukong/config.yml` 文件，则只读取该文件的配置，而不读取 default.yml ；如果不存在，则读取 default.yml 作为兜底配置。

2. 建议在运行 wukong-robot 的机器上重新训练一下唤醒词，不同设备录制出来的唤醒词模型使用效果会大打折扣。详见 [安装教程-更新唤醒词](/install?id=_6-%e6%9b%b4%e6%96%b0%e5%94%a4%e9%86%92%e8%af%8d%ef%bc%88%e5%8f%af%e9%80%89%ef%bc%8c%e6%a0%91%e8%8e%93%e6%b4%be%e5%bf%85%e9%a1%bb%ef%bc%89) 。
3. 不论使用哪个厂商的API，都建议注册并填上自己注册的应用信息，而不要用默认的配置。这是因为这些API都有使用频率和并发数限制，过多人同时使用会影响服务质量。
4. 如果使用网易邮箱，还需设置允许第三方客户端收发邮件：

  ?> <http://config.mail.163.com/settings/imap/index.jsp?uid=您的邮箱地址>

  注意把链接中 您的邮箱地址 改为您真实的网易邮箱地址（带邮箱后缀）。

5. 任一技能插件都允许关闭，方法是在配置文件中为该插件添加一个 `enable: false` 的设置。例如，如果你想关闭新闻头条插件，而该插件的 SLUG 是 `headline_news` ，那么可以如下设置：

    ``` yaml
	# 新闻头条
	# 聚合数据新闻头条API
	# https://www.juhe.cn/docs/api/id/235
    headline_news:
	    enable: false
		key: 'AppKey'  # 其他配置
    ```
