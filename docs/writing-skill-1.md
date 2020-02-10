# 实战篇1：hello world 

我们进入正题，开始写一个最简单的 “hello world” 插件。

在编写插件前，我们需要先考虑以下几个问题：

* 如何判断用户的指令是否适合用这个插件处理？
* 需要暴露哪些配置项？
* 如何处理用户的指令并得到需要的信息？

## 最简单的版本 ##

我们可以先设计一个最简单的版本：

* 通过关键词 "打个招呼" 来触发这个插件响应；
* 无需任何配置项；
* 无需处理用户的指令，直接回复“hello world”。

这个最简单的版本实现如下：

``` python
# -*- coding: utf-8-*-
from robot.sdk.AbstractPlugin import AbstractPlugin

class Plugin(AbstractPlugin):

    def handle(self, text, parsed):
        self.say('hello world!', cache=True)

    def isValid(self, text, parsed):
        return "打个招呼" in text
```

没错，就是这么简单！下面解释下这个插件做了什么事情：

* 第2行：我们将插件的基类 [`robot.sdk.AbstractPlugin`](https://www.hahack.com/wukong-robot/robot.sdk.html#module-robot.sdk.AbstractPlugin) 引入；
* 第4行：我们编写一个名为 Plugin 的类，这个类集成了 `AbstractPlugin` 基类；
* 第6行和9行：我们分别实现了 `AbstractPlugin` 的两个接口 [`handle()`](https://www.hahack.com/wukong-robot/robot.sdk.html#robot.sdk.AbstractPlugin.AbstractPlugin.handle) 和 [`isValid()`](https://www.hahack.com/wukong-robot/robot.sdk.html#robot.sdk.AbstractPlugin.AbstractPlugin.isValid) 。其中，`isValid()` 用于判断用户的指令是否适合交给这个插件处理；`handle()` 用于执行处理；
* 第10行，我们设置让用户的指令中包含了 “打个招呼” 关键词就执行响应。
* 第7行，插件的处理过程就是说一句“hello world”，可以利用 `AbstractPlugin` 基类中提供的 [`say()`](https://www.hahack.com/wukong-robot/robot.sdk.html#robot.sdk.AbstractPlugin.AbstractPlugin.say) 方法来实现这个目的。而 `cache` 参数为 `True` 则告诉 wukong-robot 应该将这句话缓存下来，以后要说这句话就无需再请求 TTS 合成，而是直接播放缓存语音。一些相对固定的回复话术适合加上缓存功能，而一些实时变化的话术（例如当前时间）就不应该加上缓存，因为很可能再也不会有播放的机会。

我们将它保存到 `$HOME/.wukong/custom` 目录下（如果不存在该目录，可以创建一个），并取名为 `HelloWorld.py` 。然后试试唤醒后如下交互：

* 用户：打个招呼
* 悟空：hello world!

?> tips：`$HOME/.wukong/custom` 目录是为插件开发者设计的一个目录。当你在开发插件时，应该先考虑将插件写在这，这样不会影响 `contrib` 目录的日常更新。等你开发完成，希望发布分享给其他用户时，再挪至 contrib 目录给 wukong-contrib 项目发 Pull Request。

### 解惑：为什么我的插件没有被触发？ ###

有几种可能：

1. 你的插件有 bug ，所以加载失败了；
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

## 更智能的版本：结合 NLU ##

接下来我们试试把这个插件做得更智能。

我们可以让用户在指令中包含人名，并支持对这个人问好。例如：

* “跟王力宏打个招呼”
* “向周杰伦打个招呼”
* “给林俊杰打个招呼”

这样，当 wukong-robot 接收到这个指令时，首先判断是否适合交给这个插件执行。如果是，再进一步提取出人名，并说“您好, `<人名>`”。

为了达到这个目的，我们可以利用传入的 `parsed` 参数。在轮询插件之前，wukong-robot 会先对用户的指令交给[百度UNIT](https://ai.baidu.com/unit/v2)解析，并将解析得到的结构化信息作为 `parsed` 参数传给插件。

### 1. 训练 UNIT 技能 ###

我们先在百度UNIT中训练这个技能。注册登录百度UNIT后，在 【[我的技能](https://ai.baidu.com/unit/v2#/sceneliblist)】 面板中点击 【新建技能】 按钮，在弹出的窗口中填好信息，完成创建。

![创建新技能](https://hahack-1253537070.file.myqcloud.com/images/wukong-docs/hello-world-1.png)

!> 在阅读下面的内容前，请先查阅百度UNIT的[官方教程](https://ai.baidu.com/docs#/UNIT-v2-download/top)。本文将略过对 UNIT 中各种术语的介绍。

接下来我们来创建一个对话意图。进入这个技能后，点击 【新建对话意图】 按钮，新建一个叫做 `HELLO_WORLD` 的意图，并填好信息：

![新建对话意图](https://hahack-1253537070.file.myqcloud.com/images/wukong-docs/hello-world-6.png)

在上面中我们定义了一个叫做 `user_person` 的可选词槽，用于确定要向谁问好。在创建的时候，可以复用 UNIT 自带的 `sys_per(人物，包含虚拟人物在内的各类人名)` 系统词槽，你还可以根据需要再添加多一些自定义词典。

接下来我们在左侧面板点击 【训练数据】 -> 【对话样本集】，在对话样本集面板中点击 【新建对话样本集】 ，创建一个样本集。在样本集中尽可能丰富对话语料，并确保正确标定。

![增加语料](https://hahack-1253537070.file.myqcloud.com/images/wukong-docs/hello-world-4.png)

完成后就可以对该技能进行训练和测试，确保模型正常工作，并且不会被误判为其他技能。如果意图判断不理想，可以继续补充语料，直到结果比较理想为止。

![测试训练结果](https://hahack-1253537070.file.myqcloud.com/images/wukong-docs/hello-world-res.png)

### 2. 使用 UNIT 技能 ###

在 UNIT 上训练好技能后，我们就可以在 wukong-robot 中利用这个技能来对普通文本进行解析，判断是否是 `HELLO_WORLD` 意图，并提取出 `user_person` 这个词槽里的值。

但在开发阶段，你训练的 UNIT 技能还不属于 wukong-robot 的 UNIT 账户。为了方便调试，你可以在插件中手动调用 UNIT 的 API，得到解析的结果；等插件开发完成，准备提交发布时，再删除 UNIT 的调用，并在 Pull Request 中告知 wukong-robot 的维护者在 wukong-robot 的 UNIT 账户中导入你分享的技能。

我们改写一下上面的插件代码：

``` python
# -*- coding: utf-8-*-
from robot.sdk import unit
from robot.sdk.AbstractPlugin import AbstractPlugin

# 调试用，发布时删除
SERVICE_ID='你的技能service_id'
API_KEY='你的技能api_key'
SECRET_KEY='你的技能secret_key'

class Plugin(AbstractPlugin):

    def handle(self, text, parsed):
        import time  # 调试用，用于避免频繁调用UNIT导致QPS超限，发布时删除
        time.sleep(1)  # 调试用，用于避免频繁调用UNIT导致QPS超限，发布时删除
        parsed = unit.getUnit(text, SERVICE_ID, API_KEY, SECRET_KEY) # 调试用，发布时删除
        slots = unit.getSlots(parsed, 'HELLO_WORLD')  # 取出所有词槽
        # 遍历词槽，找出 user_person 对应的值
        for slot in slots:
            if slot['name'] == 'user_person':
                self.say('您好，{}！'.format(slot['normalized_word']))
                return
        # 如果没命中词槽，说 hello world
        self.say('hello world!', cache=True)

    def isValid(self, text, parsed):
        parsed = unit.getUnit(text, SERVICE_ID, API_KEY, SECRET_KEY) # 调试用，发布时删除
        # 判断是否包含 HELLO_WORLD 意图
        return unit.hasIntent(parsed, 'HELLO_WORLD')
```

* 在第2行中，我们引入了 [`robot.sdk.unit`](writing-skill-basic?id=unit-%e6%a8%a1%e5%9d%97) 百度UNIT模块；
* 在第4～7行中，我们将自己创建的技能的 `service_id`、`api_key`、`secret_key` 写成几个全局变量（正式发布的时候无需用到，可以删除）。其中 `service_id` 是你的机器人 ID （例如我的值就是 `S13442`）：

<center>
<img src="https://hahack-1253537070.file.myqcloud.com/images/wukong-docs/service-id.png" alt="service_id"/>
</center>

* 在 `isValid()` 的实现中，我们使用 `unit.hasIntent()` 方法从百度 UNIT 解析的结果中判断是否包含 `HELLO_WORLD` 意图，如果是，则命中这个技能。
* 在 `handle()` 的实现中，我们先通过 `unit.getSlots()` 方法取出所有词槽，再利用词槽的 `name` 属性和 `normalized_word` 属性遍历词槽找出名为 `user_person` 的词槽对应的人名。如果能找到，就语音反馈 “你好，`<人名>`”；如果找不到，则说“hello world”。
* 特别注意的是，在开发阶段我们对传进来的 parsed 进行了修改，改成了我们进一步调我们的 UNIT 服务解析出来的结果（第13行、第24行）。在正式提交发布时，需要将这个改写删除。并在 Pull Request 中提供你的技能分享码，由 wukong-robot 的维护者将你的技能加进 wukong-robot 的 UNIT 账号中。

!> 虽然插件中调 UNIT 可以让插件正常工作，但你不该在最终的代码中这么做。试想想后面如果有几十上百个技能插件，每个都各自执行发一次 UNIT 请求，这该有多高的延时？所以，最好的做法是在提交插件时顺便提供你的 UNIT 技能的分享码，让 wukong-robot 的 UNIT 账户也共享你的插件。在轮询插件前，由 wukong-robot 主动解析一次指令再把解析结果通过 `parsed` 传给各个插件，就可以避免对 UNIT 的滥用。

## 发布技能 ##

技能开发完后，如果希望别人也能用上这个技能，那就可以申请发布你的技能。见[实战篇5：发布技能](writing-skill-publish)。

