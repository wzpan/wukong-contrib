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

1. 由于音乐技能可能会有多个（比如有用户贡献了 [BaiduFM](contrib?id=BaiduFm)），为了便于区分不同技能，所以可以直接判断是否包含关键词 `'本地音乐'`  ，以避免被误当做其他意图。
2. 可以把音乐路径作为一个配置项 `path` ，例如：

    ``` yaml
    ## 本地音乐插件

    LocalPlayer:
        path: "/home/pi/musics"
    ```

3. 扫描该目录下的所有 `.mp3` 格式的音乐，得到一个音乐列表，然后从第一个开始播放音乐。
4. 在音乐播放模式下，还能支持响应诸如 “上一首”、“下一首”、“停止播放”、“大声一点”、“小声一点”等控制指令。
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
    def isValid(self, text, parsed):
        return '本地音乐' in text
```

### `handle()` 实现 ###

`handle()` 方法主要就是做两件事：

1. 扫描配置文件中指定的本地音乐目录，得到一个播放列表；
2. 循环列表，播放歌曲。

我们先写一个方法，扫描音乐目录，并返回播放列表：

``` python
# -*- coding: utf-8-*-
import os
from robot import config, logging
from robot.sdk.AbstractPlugin import AbstractPlugin

logger = logging.getLogger(__name__)

class Plugin(AbstractPlugin):

    IS_IMMERSIVE = True  # 这是个沉浸式技能

    def __init__(self, con):
        super(Plugin, self).__init__(con)
        self.player = None

    def get_song_list(self, path):
        if not os.path.exists(path) or \
           not os.path.isdir(path):
            return []
        flist = list(filter(lambda d: d.endswith('.mp3'), os.listdir(path)))
        return flist

```

* 在第 2~3 行中，我们又引入了几个必要的模块。
* 因为这个插件比较复杂，我们在第 6 行声明了一个 `logger` 方便后面打 log 调试；
* 我们写了个 `get_song_list()` 方法用于扫描指定目录下的后缀名为 `.mp3` 的文件列表；

然后我们在 `handle()` 方法中扫描配置文件中指定的目录，并调用 `get_song_list()` 方法得到音乐列表：

``` python

    def handle(self, text, parsed):
        music_list = self.get_song_list(config.get('/LocalPlayer/path'))
        if music_list == None:
            logger.error('{} 插件配置有误'.format(self.SLUG))
        logger.info(music_list)

```

如果这时候我们运行 wukong-robot ，并使用这个技能，如果存在音乐文件，将会打印类似这样的日志：

``` bash
INFO:LocalPlayer:['perfume.mp3', '可惜没如果.mp3']
```

接下来我们写个播放器，去处理这个播放列表，并支持上一首、下一首、停止播放等操作：

``` python
class MusicPlayer(object):

    def __init__(self, playlist, plugin):
        super(MusicPlayer, self).__init__()
        self.playlist = playlist
        self.plugin = plugin
        self.idx = 0
        self.volume = 0.6
        
    def play(self):
        logger.debug('MusicPlayer play')
        path = self.playlist[self.idx]
        if os.path.exists(path):
            self.plugin.play(path, False, self.next, self.volume)
        else:
            logger.error('文件不存在: {}'.format(path))    

    def next(self):
        logger.debug('MusicPlayer next')
        self.idx = (self.idx+1) % len(self.playlist)
        self.play()

    def prev(self):
        logger.debug('MusicPlayer prev')
        self.idx = (self.idx-1) % len(self.playlist)
        self.play()

    def stop(self):
        logger.debug('MusicPlayer stop')
        self.plugin.clearImmersive()  # 去掉沉浸式

    def turnUp(self):
        if self.volume < 0.2:
            self.volume += 0.2
        self.play()

    def turnDown(self):
        if self.volume > 0:
            self.volume -= 0.2
        self.play()
```

`MusicPlayer` 是我们封装的一个列表音乐播放器类，它在普通播放器 [`SoxPlayer`](https://www.hahack.com/wukong-robot/robot.html#robot.Player.SoxPlayer) 的基础上提供了诸如播放 `play()`、下一首 `next()`、上一首 `prev()`、停止播放 `stop()`、调大声 `turnUp()`、调小声 `turnDown()` 的功能。为了方便调用 `Plugin` 自带的方法，我们把 `Plugin` 的实例作为参数 `plugin` 传给 MusicPlayer 类。

之后，我们就可以很方便地利用这个 `MusicPlayer` 类实现我们要的播放功能。将 `handle()` 方法改写如下：

``` python
    def handle(self, text, parsed):
        if not self.player:
            self.player = self.init_music_player()
        if self.nlu.hasIntent(parsed, 'MUSICRANK'):
            self.player.play()
        elif self.nlu.hasIntent(parsed, 'CHANGE_TO_NEXT'):
            self.say('下一首歌')
            self.player.next()
        elif self.nlu.hasIntent(parsed, 'CHANGE_TO_LAST'):
            self.say('上一首歌')
            self.player.prev()
        elif self.nlu.hasIntent(parsed, 'CHANGE_VOL'):
            word = self.nlu.getSlotWords(parsed, 'CHANGE_VOL', 'user_vd')[0]
            if word == '--LOUDER--':
                self.say('大声一点')
                self.player.turnUp()
            else:
                self.say('小声一点')
                self.player.turnDown()
        elif self.nlu.hasIntent(parsed, 'CLOSE_MUSIC') or self.nlu.hasIntent(parsed, 'PAUSE'):
            self.player.stop()
            self.clearImmersive()  # 去掉沉浸式
            self.say('退出播放')
        else:
            self.say('没听懂你的意思呢，要停止播放，请说停止播放')
            self.player.play()
```

在做意图判断时，我们充分利用了百度 UNIT 预置的[音乐技能](https://ai.baidu.com/unit/v2#/preskilldetail/34889/%E9%9F%B3%E4%B9%90)：


<center>
<img src="https://hahack-1253537070.file.myqcloud.com/images/unit-music.png" alt="UNIT 预置的音乐技能"/>
</center>

特别要注意，对于音乐这种长时间处于沉浸模式的场景，你应该设计一个能调用退出沉浸模式 `clearImmersive()` 的指令，比如第 20~23 行中的实现：当用户说出的指令命中 `CLOSE_MUSIC` 或者 `PAUSE` 的意图时，停止播放并结束当前的沉浸模式。

### `isValidImmersive()` 方法实现 ###

某些意图在进入这个技能前，其实并不能以此作为是否适用于这个技能处理的条件。比如，在你唤醒 wukong-robot 让它 “播放本地音乐” 之前，如果你先说 “上一首歌” ，此时并不应该交给 `LocalPlayer` 这个技能来处理。因为可能有非常多音乐插件都希望能在自己的模式下处理这个指令。如果你在 `isValid()` 方法里头通过判断这个意图就强制要求 `LocalPlayer` 处理，这就会导致其他音乐插件再也响应不了 “下一首歌” 这个指令。

正确的做法应该是只在进入本地音乐的模式下才决定是否响应这些意图，这就要用到 `isValidImmersive()` 方法。它用于告诉 wukong-robot 在这个技能的服务期间，它还应该能额外响应其他哪些指令。我们来实现这个方法：

``` python
    def isValidImmersive(self, text, parsed):
        return any(self.nlu.hasIntent(parsed, intent) for intent in ['CHANGE_TO_LAST', 'CHANGE_TO_NEXT', 'CHANGE_VOL', 'CLOSE_MUSIC', 'PAUSE'])

```

这个方法告诉 wukong-robot 当处于 LocalPlayer 的沉浸模式下时，还能额外处理 `CHANGE_TO_LAST`、`CHANGE_TO_NEXT`、`CHANGE_VOL`、`CLOSE_MUSIC`、`PAUSE` 几种意图。

### `restore()` 方法实现 ###

还有一个问题：当用户打断音乐播放时，wukong-robot 处理完用户打断的指令后，理想情况下应该是继续播放音乐。所以我们还可以再实现一个 `restore()` 方法，这个方法将在 wukong-robot 被打断后，恢复技能的处理。

?> 当然，这个方法是可选的，如果你并不希望恢复技能，可以不实现这个方法。

``` python
    def restore(self):
        if self.player:
            self.player.play()
```

### 完整实现 ###

``` python
# -*- coding: utf-8-*-
import os
from robot import config, logging
from robot.sdk.AbstractPlugin import AbstractPlugin

logger = logging.getLogger(__name__)

class MusicPlayer(object):

    def __init__(self, playlist, plugin):
        super(MusicPlayer, self).__init__()
        self.playlist = playlist
        self.plugin = plugin
        self.idx = 0
        self.volume = 0.6
        
    def play(self):
        logger.debug('MusicPlayer play')
        path = self.playlist[self.idx]
        if os.path.exists(path):
            self.plugin.play(path, False, self.next, self.volume)
        else:
            logger.error('文件不存在: {}'.format(path))    

    def next(self):
        logger.debug('MusicPlayer next')
        self.idx = (self.idx+1) % len(self.playlist)
        self.play()

    def prev(self):
        logger.debug('MusicPlayer prev')
        self.idx = (self.idx-1) % len(self.playlist)
        self.play()

    def stop(self):
        logger.debug('MusicPlayer stop')

    def turnUp(self):
        if self.volume < 0.2:
            self.volume += 0.2
        self.play()

    def turnDown(self):
        if self.volume > 0:
            self.volume -= 0.2
        self.play()


class Plugin(AbstractPlugin):

    IS_IMMERSIVE = True  # 这是个沉浸式技能

    def __init__(self, con):
        super(Plugin, self).__init__(con)
        self.player = None

    def get_song_list(self, path):
        if not os.path.exists(path) or \
           not os.path.isdir(path):
            return []
        song_list = list(filter(lambda d: d.endswith('.mp3'), os.listdir(path)))        
        return [os.path.join(path, song) for song in song_list]

    def init_music_player(self):
        song_list = self.get_song_list(config.get('/LocalPlayer/path'))
        if song_list == None:
            logger.error('{} 插件配置有误'.format(self.SLUG))
        logger.info(song_list)
        return MusicPlayer(song_list, self)

    def handle(self, text, parsed):
        if not self.player:
            self.player = self.init_music_player()
        if self.nlu.hasIntent(parsed, 'MUSICRANK'):
            self.player.play()
        elif self.nlu.hasIntent(parsed, 'CHANGE_TO_NEXT'):
            self.say('下一首歌')
            self.player.next()
        elif self.nlu.hasIntent(parsed, 'CHANGE_TO_LAST'):
            self.say('上一首歌')
            self.player.prev()
        elif self.nlu.hasIntent(parsed, 'CHANGE_VOL'):
            word = self.nlu.getSlotWords(parsed, 'CHANGE_VOL', 'user_vd')[0]
            if word == '--LOUDER--':
                self.say('大声一点')
                self.player.turnUp()
            else:
                self.say('小声一点')
                self.player.turnDown()
        elif self.nlu.hasIntent(parsed, 'CLOSE_MUSIC') or self.nlu.hasIntent(parsed, 'PAUSE'):
            self.player.stop()
            self.clearImmersive()  # 去掉沉浸式
            self.say('退出播放')
        else:
            self.say('没听懂你的意思呢，要停止播放，请说停止播放')
            self.player.play()

    def restore(self):
        if self.player:
            self.player.play()

    def isValidImmersive(self, text, parsed):
        return any(self.nlu.hasIntent(parsed, intent) for intent in ['CHANGE_TO_LAST', 'CHANGE_TO_NEXT', 'CHANGE_VOL', 'CLOSE_MUSIC', 'PAUSE'])

    def isValid(self, text, parsed):
        return "本地音乐" in text
```
