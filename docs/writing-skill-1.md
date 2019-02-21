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

![创建新技能](http://hahack-1253537070.file.myqcloud.com/images/wukong-docs/hello-world-1.png)

!> 在阅读下面的内容前，请先查阅百度UNIT的[官方教程](https://ai.baidu.com/docs#/UNIT-v2-download/top)。本文将略过对 UNIT 中各种术语的介绍。

接下来我们来创建一个对话意图。进入这个技能后，点击 【新建对话意图】 按钮，新建一个叫做 `HELLO_WORLD` 的意图，并填好信息：

![新建对话意图](http://hahack-1253537070.file.myqcloud.com/images/wukong-docs/hello-world-6.png)

在上面中我们定义了一个叫做 `user_person` 的可选词槽，用于确定要向谁问好。在创建的时候，可以复用 UNIT 自带的 `sys_per(人物，包含虚拟人物在内的各类人名)` 系统词槽，你还可以根据需要再添加多一些自定义词典。

接下来我们在左侧面板点击 【训练数据】 -> 【对话样本集】，在对话样本集面板中点击 【新建对话样本集】 ，创建一个样本集。在样本集中尽可能丰富对话语料，并确保正确标定。

![增加语料](http://hahack-1253537070.file.myqcloud.com/images/wukong-docs/hello-world-4.png)

完成后就可以对该技能进行训练和测试，确保模型正常工作，并且不会被误判为其他技能。如果意图判断不理想，可以继续补充语料，直到结果比较理想为止。

![测试训练结果](http://hahack-1253537070.file.myqcloud.com/images/wukong-docs/hello-world-res.png)

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
<img src="http://hahack-1253537070.file.myqcloud.com/images/wukong-docs/service-id.png" alt="service_id"/>
</center>

* 在 `isValid()` 的实现中，我们使用 `unit.hasIntent()` 方法从百度 UNIT 解析的结果中判断是否包含 `HELLO_WORLD` 意图，如果是，则命中这个技能。
* 在 `handle()` 的实现中，我们先通过 `unit.getSlots()` 方法取出所有词槽，再利用词槽的 `name` 属性和 `normalized_word` 属性遍历词槽找出名为 `user_person` 的词槽对应的人名。如果能找到，就语音反馈 “你好，`<人名>`”；如果找不到，则说“hello world”。
* 特别注意的是，在开发阶段我们对传进来的 parsed 进行了修改，改成了我们进一步调我们的 UNIT 服务解析出来的结果（第13行、第24行）。在正式提交发布时，需要将这个改写删除。并在 Pull Request 中提供你的技能分享码，由 wukong-robot 的维护者将你的技能加进 wukong-robot 的 UNIT 账号中。

!> 虽然插件中调 UNIT 可以让插件正常工作，但你不该在最终的代码中这么做。试想想后面如果有几十上百个技能插件，每个都各自执行发一次 UNIT 请求，这该有多高的延时？所以，最好的做法是在提交插件时顺便提供你的 UNIT 技能的分享码，让 wukong-robot 的 UNIT 账户也共享你的插件。在轮询插件前，由 wukong-robot 主动解析一次指令再把解析结果通过 `parsed` 传给各个插件，就可以避免对 UNIT 的滥用。

## 发布技能 ##

技能开发完后，如果希望别人也能用上这个技能，那就可以申请发布你的技能。见[实战篇5：发布技能](writing-skill-publish)。

