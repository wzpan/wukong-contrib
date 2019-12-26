# 技能插件通用使用技巧

## 禁用任意技能插件 ###

默认情况下，wukong-robot 会试图加载自带的和 `~/.wukong/contrib` 目录下的所有技能。任一技能插件都允许关闭，方法是在配置文件中为该插件添加一个 `enable: false` 的设置。例如，如果你想关闭新闻头条插件，而该插件的 `SLUG` 是 `headline_news` ，那么可以如下设置：

    ``` yaml
	# 新闻头条
	# 聚合数据新闻头条API
	# https://www.juhe.cn/docs/api/id/235
    headline_news:
	    enable: false
		key: 'AppKey'  # 其他配置
    ```

## 自定义技能命中规则 ###

从 [2.1.0](https://github.com/wzpan/wukong-robot/wiki/update-notes#210%E4%BB%A3%E5%8F%B7%E6%95%96%E4%B8%99) 版本开始，wukong-robot 的任一插件的命中规则，均可在配置文件中以正则表达式的形式自行扩充。

例如，如果用户希望使用 “芝麻开门” 指令来唤醒电脑（[WOL 插件](https://wukong.hahack.com/#/contrib?id=wol)），可以在 `config.yml` 中，为 WOL 插件的配置增加一个 `patterns` 配置：

``` yaml
# WOL启动
wol:
    ip: '局域网广播地址或指定电脑IP地址'
    mac: '电脑MAC地址'
    patterns: ['芝麻开门']  # 必须为数组形式
```

之后即可在唤醒wukong-robot后，实现类似这样的交互：

* 用户：芝麻开门
* 悟空：启动成功 

`patterns` 里面的值允许为正则表达式，以实现更灵活的命中规则。例如，若给 [Hass 插件](https://wukong.hahack.com/#/contrib?id=hass) 添加如下的正则表达式：

``` yaml
hass:
    url: "http://ip地址"   #切记加上http://，ip或者域名为你的homeassistant的主机
    port: "8123"             # 端口为你的homeassistant的端口和网页端口一样
    key: "Bearer XXXXXXX" # 密钥
    patterns:
        - ".*开.*灯"
        - ".*关.*灯"
        - ".*灯.*开"
        - ".*灯.*关"
```

那么以下的命令都会触发 Hass 插件的技能：

* 帮我打开灯
* 开灯
* 开下灯
* 把灯开了
* 帮我关灯
* 关灯
* 把灯关了

![](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/wukong-docs/hass-7.png)

## 解惑：为什么有的插件没有被触发？ ###

有几种可能：

1. 插件有 bug ，所以加载失败了；
2. ASR 没有准确识别出你的插件的触发词；
3. 你的插件的 `isValid()` 方法与其他插件冲突，导致其他插件先被触发了。

对于第一种情况，最方便的做法是直接查看后台管理端的日志界面，不难看到有类似下面这样的日志：

```
2019-10-03 13:17:41,189 - robot.ASR - INFO - 使用 baidu-asr ASR 引擎
2019-10-03 13:17:41,190 - robot.AI - INFO - 使用 anyq 对话机器人
2019-10-03 13:17:41,190 - robot.TTS - INFO - 使用 baidu-tts TTS 引擎
2019-10-03 13:17:41,190 - robot.NLU - INFO - 使用 unit NLU 引擎
2019-10-03 13:17:41,191 - robot.plugin_loader - INFO - 插件 Camera 已被禁用
2019-10-03 13:17:41,192 - robot.plugin_loader - INFO - 插件 CleanCache 加载成功 
2019-10-03 13:17:41,193 - robot.plugin_loader - INFO - 插件 Echo 加载成功 
2019-10-03 13:17:41,196 - robot.plugin_loader - INFO - 插件 Email 加载成功 
2019-10-03 13:17:41,197 - robot.plugin_loader - INFO - 插件 Geek 加载成功 
2019-10-03 13:17:41,198 - robot.plugin_loader - INFO - 插件 LocalPlayer 加载成功 
2019-10-03 13:17:41,198 - robot.plugin_loader - INFO - 插件 Poem 加载成功 
2019-10-03 13:17:41,199 - robot.plugin_loader - INFO - 插件 BaiduFM 加载成功 
2019-10-03 13:17:41,201 - robot.plugin_loader - INFO - 插件 BaiduMap 加载成功 
2019-10-03 13:17:41,214 - robot.plugin_loader - INFO - 插件 ControMqtt 加载成功 
2019-10-03 13:17:41,215 - robot.plugin_loader - INFO - 插件 Direction 加载成功 
2019-10-03 13:17:41,217 - robot.plugin_loader - INFO - 插件 EmailMyPC 加载成功 
2019-10-03 13:17:41,217 - robot.plugin_loader - INFO - 插件 Halt 加载成功 
2019-10-03 13:17:41,218 - robot.plugin_loader - INFO - 插件 Hass 加载成功 
2019-10-03 13:17:41,219 - robot.plugin_loader - INFO - 插件 HeadlineNews 加载成功 
2019-10-03 13:17:41,220 - robot.plugin_loader - INFO - 插件 Lamp 加载成功 
2019-10-03 13:17:41,249 - robot.plugin_loader - INFO - 插件 NeteaseMusic 加载成功 
2019-10-03 13:17:41,250 - robot.plugin_loader - INFO - 插件 RaspberryPiStatus 加载成功 
2019-10-03 13:17:41,251 - robot.plugin_loader - INFO - 插件 Reboot 加载成功 
2019-10-03 13:17:41,253 - robot.plugin_loader - INFO - 插件 RoadCondition 加载成功 
2019-10-03 13:17:41,254 - robot.plugin_loader - INFO - 插件 SmartMiFan 加载成功 
2019-10-03 13:17:41,254 - robot.plugin_loader - INFO - 插件 SpeakIP 加载成功 
2019-10-03 13:17:41,255 - robot.plugin_loader - INFO - 插件 SpeakTemperature 加载成功 
2019-10-03 13:17:41,257 - robot.plugin_loader - INFO - 插件 WOL 加载成功 
2019-10-03 13:17:41,258 - robot.plugin_loader - INFO - 插件 Weather 已被禁用
2019-10-03 13:17:41,260 - robot.plugin_loader - INFO - 插件 WeiBo 加载成功 
2019-10-03 13:17:41,261 - robot.plugin_loader - INFO - 插件 YouDaoFanYi 加载成功 
2019-10-03 13:17:41,264 - robot.plugin_loader - INFO - 插件 photos 加载成功 
2019-10-03 13:17:41,264 - robot.Brain - INFO - 已激活插件：['cleancache', 'Echo', 'email', 'Geek', 'LocalPlayer', 'poem', 'baidufm', 'BaiduMap', 'mqttPub', 'direction', 'emailmypc', 'halt', 'homeassistant', 'headline_news', 'Lamp', 'NeteaseMusic', 'pi_status', 'reboot', 'roadcondition', 'SmartMiFan', 'speak_ip', 'speak_temperature', 'wol', 'WeiBo', 'youdao', 'photos']
```

如果你能在已激活插件中找到你的插件，说明插件加载成功。反之，如果看到类似这样的日志：

```
2019-10-03 13:35:11,159 - robot.plugin_loader - WARNING - 插件 BaiduFM 加载出错，跳过
Traceback (most recent call last):
  File "/Users/panweizhou/Documents/projects/wukong-robot/robot/plugin_loader.py", line 36, in init_plugins
    mod = loader.load_module(name)
  File "<frozen importlib._bootstrap_external>", line 407, in _check_name_wrapper
  File "<frozen importlib._bootstrap_external>", line 907, in load_module
  File "<frozen importlib._bootstrap_external>", line 732, in load_module
  File "<frozen importlib._bootstrap>", line 265, in _load_module_shim
  File "<frozen importlib._bootstrap>", line 696, in _load
  File "<frozen importlib._bootstrap>", line 677, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 728, in exec_module
  File "<frozen importlib._bootstrap>", line 219, in _call_with_frames_removed
  File "/Users/panweizhou/.wukong/contrib/BaiduFM.py", line 10, in <module>
    a = thth
NameError: name 'thth' is not defined
```

说明你的插件存在 bug ，请自行定位修复。

对于第二种情况，也可以查看日志，确认下 ASR 识别出的词是否你设置的唤醒词。你可以在日志中看到类似这样的信息：

``` bash
INFO:robot.ASR:baidu-asr 语音识别到了：['天启怎么样，']
```

像上面的例子，本来要问“天气怎么样”，但却被识别成了“天启怎么样”，当然没办法触发对应的技能。你可以在所使用的 ASR 里提高下自定义热词的识别权重。参见 [技巧-提升语音识别准确率](/tips?id=_4-提升语音识别准确率)。

对于第三种情况，你可以看看当前是哪个插件处理了你的指令，得重新换一个不会与这个插件冲突的触发词。举个例子，假如我开发出一个使用百度引擎搜索音乐的技能，我的触发词设置成 “百度音乐” ，那么这就跟 BaiduFM 插件发生了冲突。此时可以在 `isValid()` 中把触发词改为 “搜索音乐” ，就可以避免冲突的发生。


