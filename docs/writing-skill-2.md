# 实战篇2：开发一个清除缓存技能

本节我们开始写一个有真正用途的普通技能插件。

为了节省 TTS 消耗的时间，wukong-robot 支持将语音文件缓存到 `temp` 目录，但是如果时间久了，整个目录里的文件数量就会越来越多，大量占用设备的存储空间；此外，如果修改了 TTS 配置改了发音人的音色，如果没有清理已有的缓存语音，也会出现 wukong-robot 使用过程中混杂着多种音色的奇怪体验。所以，我们可以开发一个插件，来帮助清除缓存。

?> “缓存 LRU 自清理”是后面计划要做一件事：自动淘汰删除久未使用的缓存，就可以将缓存目录控制在一定的体积以内，避免造成过多的空间浪费。在这个功能完成之前，你可以[关注项目的进展](https://github.com/users/wzpan/projects/1)查看这个功能的实现进度，或者[帮助我实现它](https://github.com/wzpan/wukong-robot#%E8%B4%A1%E7%8C%AE)。

同样地，在编写插件前，我们需要先考虑以下几个问题：

* 如何判断用户的指令是否适合用这个插件处理？
* 需要暴露哪些配置项？
* 如何处理用户的指令并得到需要的信息？

围绕这几个问题，我们可以将这个插件设计成如下的形式：

* 只要指令中包含关键词 “清除缓存”、“清空缓存”或者 “清缓存”就触发这个插件响应；
* 无需任何配置项。
* 无需处理用户的指令，直接清除缓存。并告知用户“缓存目录已清空”；

我们可以把上一篇教程简单版 Hello World 技能插件代码拷贝过来，看看有哪些地方可以复用，哪些地方则要修改：

``` python
# -*- coding: utf-8-*-
from robot.sdk.AbstractPlugin import AbstractPlugin

class Plugin(AbstractPlugin):

    def handle(self, text, parsed):
        self.say('hello world!', cache=True)

    def isValid(self, text, parsed):
        return "打个招呼" in text
```

很容易可以看出，首先我们需要修改 `isValid()` 中的实现，将这个判断规则改为判断指令文本中是否包含 `["清除缓存", u"清空缓存", u"清缓存"]` 中的任意一个。我们可以改成这样：

``` python
    def isValid(self, text, parsed):
        return any(word in text for word in ["清除缓存", u"清空缓存", u"清缓存"])
```

接下来我们再看看 `handle()` 方法，原来的交互仅仅只是说一句“hello world”，现在我们需要修改为删除缓存再说一句“缓存已清空”。

[`constants`](writing-skill-basic?id=constants-%e6%a8%a1%e5%9d%97) 模块的 `TEMP_PATH` 变量提供了 `temp` 目录的绝对路径，而 [`utils`](/writing-skill-basic?id=unit-%e6%a8%a1%e5%9d%97) 模块则提供了检查并删除文件/文件夹的方法 `check_and_delete()`，我们可以利用这两个帮手实现一个删除缓存目录的功能。

``` python
# 引入必要的模块
import os
from robot import constants, utils
...

    def handle(self, text, parsed):
        temp = constants.TEMP_PATH
        for f in os.listdir(temp):
            if f != 'DIR':
                utils.check_and_delete(os.path.join(temp, f))
        self.say(u'缓存目录已清空', cache=True)
```

在上面的代码中，我们首先引入一些必要的模块，然后在 `handle()` 方法中，遍历 `temp` 目录下的所有文件，并将文件名不是 `DIR` 的文件和文件夹都删除。

?> `DIR` 文件只是一个空文件，Git 并不允许只提交一个空的目录。所以在 wukong-robot 中保留了这个空文件，用以确保所有用户拉取 wukong-robot 下来后本地都能有一个 `temp` 目录。

完整的代码如下：

``` python
# -*- coding: utf-8-*-

import os
from robot import constants, utils
from robot.sdk.AbstractPlugin import AbstractPlugin

class Plugin(AbstractPlugin):

    SLUG = 'cleancache'

    def handle(self, text, parsed):
        temp = constants.TEMP_PATH
        for f in os.listdir(temp):
            if f != 'DIR':
                utils.check_and_delete(os.path.join(temp, f))
        self.say(u'缓存目录已清空', cache=True)

    def isValid(self, text, parsed):
        return any(word in text.lower() for word in ["清除缓存", u"清空缓存", u"清缓存"])
```
