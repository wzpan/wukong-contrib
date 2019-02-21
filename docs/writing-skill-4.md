# 实战篇4：开发一个沉浸式音乐播放技能

在这一节中，我们来写一个沉浸式技能插件。有别于普通技能插件，沉浸式技能插件的特点在于能在这个技能服务期间内，响应更多类型的指令，且具备唤醒后自动恢复技能的能力。

沉浸式技能最典型的应用场景是音乐播放器。通常的交互模式是唤醒 wukong-robot 后，说出指令并触发该技能插件，由其进入该技能的沉浸式场景中。在该技能的沉浸式场景下，用户唤醒 wukong-robot 后，允许响应更多指令以完成更丰富的操作（例如“下一首歌”、“这是什么歌”等指令）。如果唤醒后只是简单的聊天，而不是进入其他技能，那么还允许 wukong-robot 在回答后恢复该技能的沉浸式场景（例如，用户在音乐场景中唤醒 wukong-robot 并问完时间后，wukong-robot 可以自动恢复音乐播放）。

编写一个沉浸式技能插件和普通技能插件大同小异，仅仅只需要设置 `IS_IMMERSIVE` 成员属性为 `True` ，并根据需求实现多两个方法： [`isValidImmersive()`](https://www.hahack.com/wukong-robot/robot.sdk.html#robot.sdk.AbstractPlugin.AbstractPlugin.isValidImmersive) 方法和 [`restore()`](https://www.hahack.com/wukong-robot/robot.sdk.html#robot.sdk.AbstractPlugin.AbstractPlugin.restore) 方法即可，这两个方法分别用来支持沉浸模式下更多指令的响应以及恢复技能。

我们可以试着实现一个本地音乐播放器插件 LocalPlayer 。

## 设计技能 ##

依然是这老生常谈的三个问题：

1. 如何判断用户的指令是否适合用这个插件处理？
2. 需要暴露哪些配置项？
3. 如何处理用户的指令并得到需要的信息？

看了这么久教程你应该熟悉了套路：其实这三个问题分别决定了 `isValid()` 的实现、`config.yml` 中的配置以及 `handle()` 的实现。

不过，沉浸式插件还有额外的两个问题：

4. 在该技能工作的过程中，还可以唤醒响应后哪些其他指令？
5. 如果在该技能工作的过程中打断了这个技能，怎么恢复这个技能？

显然这两个则是对应了 `isValidImmersive()` 和 `restore()` 方法的实现。

我们可以这么设计：

1. 由于音乐技能可能会有多个（比如有用户贡献了 [BaiduFM](contrib?id=BaiduFm)），为了便于区分不同技能，所以可以直接判断是否包含 `['本地音乐', '本机音乐']` 中的一个关键词，以避免被误当做其他意图。
2. 所以可以把音乐路径作为一个配置项 `path` ，例如：

    ``` yaml
    ## 本地音乐插件

    LocalPlayer:
        path: "/home/pi/musics"
    ```

3. 扫描该目录下的所有 `.mp3` 格式的音乐，得到一个音乐列表，然后从第一个开始播放音乐。
4. 在音乐播放模式下，还能支持响应诸如 “上一首”、“下一首”、“停止播放”、“随机播放”、“大声一点”、“小声一点”等控制指令。
5. 如果播放过程中唤醒打断了技能，可以恢复播放。

## 沉浸式插件的模板 ##

按照国际惯例，先把 Hello World 模板拷贝过来：

``` python
# -*- coding: utf-8-*-
from robot.sdk.AbstractPlugin import AbstractPlugin

class Plugin(AbstractPlugin):

    def handle(self, text, parsed):
        self.say('hello world!', cache=True)

    def isValid(self, text, parsed):
        return "打个招呼" in text
```

如上所述，沉浸式插件不外乎多设了个 `IS_IMMERSIVE` 属性和两个新方法，接下来我们先把它改造成沉浸式插件的模板：

``` python
# -*- coding: utf-8-*-
from robot.sdk.AbstractPlugin import AbstractPlugin

class Plugin(AbstractPlugin):

    IS_IMMERSIVE = True  # 这是个沉浸式技能

    def handle(self, text, parsed):
        self.say('hello world!', cache=True)

    def restore(self):
        pass

    def isValidImmersive(self, text, parsed):
        return False

    def isValid(self, text, parsed):
        return "打个招呼" in text
```

* 第 6 行我们设置了一个 `IS_IMMERSIVE` 成员变量，并将值改为 True 。用于告知 wukong-robot 这是一个沉浸式插件，它需要在适当时机执行额外的 `restore()` 方法和 `isValidImmersive()` 方法。
* 第 11~15 行我们将两个新方法 `restore()` 方法和 `isValidImmersive()` 方法添加进来，并暂时提供一个空实现。我们将在后面完成这两个方法的实现。

### `isValid()` 实现 ###

前面提到，由于音乐技能可能会有多个，为了便于区分不同技能，所以可以直接判断是否包含 “本地音乐”关键词即可，以避免被误当做其他意图。

``` python
...
    def isValid(self, text, parsed):
        return '本地音乐' in text
`````

### `handle()` 实现 ###

（未完待续）
