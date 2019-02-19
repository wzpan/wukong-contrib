# 技能开发教程 - 准备篇

## wukong-robot 工作机制 ##

![wukong-robot 的工作机制](http://hahack-1253537070.file.myqcloud.com/images/wukong-docs/wukong-robot.png)

wukong-robot 的工作机制如下：

1. wukong-robot 被唤醒后，用户的语音指令先经过 ASR 引擎进行 ASR 识别成文本；
2. 之后，wukong-robot 会对识别到的文本进行语义理解（NLU），得到解析结果；
3. 轮询每个可用插件，进行技能匹配，交给适合处理该指令的技能插件去处理。
4. 插件处理过程中，还可以根据需要使用 TTS 引擎合成成语音，播放给用户。

在第 3 步中，插件的轮询机制如下：

1. 在初始化阶段，依次扫描 `plugins` 目录、`$HOME/.wukong/contrib` 目录和 `$HOME/.wukong/custom` 目录下的可用插件。可用插件的判定标准为：
  - 包含一个继承了 `AbstractPlugin` 基类的 `Plugin` 类；
  - 在配置文件中没有将这个插件的 `enable` 设为 `false`。
2. 在扫描过程中，如果存在插件设置了 `PRIORITY` 属性，则对其优先级进行重排。默认都为 0，`PRIORITY` 值设得越大，则优先级越高。
3. 在轮询过程中，wukong-robot 会根据优先级逐个执行插件的 `isValid()` 方法，如果值为 `True`，则调用该插件的 `handle()` 方法进入处理。

## 技能插件类型 ##

wukong-robot 支持两类技能插件：

1. **普通技能插件**，适用于普通的查询、助手类技能。通常的交互模式是唤醒 wukong-robot 后，说出指令并触发该技能插件，由其完成处理并汇报结果。如果需要询问用户问题，则可以利用 `self.activeListen()` 方法进入主动聆听，从而实现多轮对话。
2. **沉浸式技能插件**，适用于音乐、电台等技能。通常的交互模式是唤醒 wukong-robot 后，说出指令并触发该技能插件，由其进入该技能的沉浸式场景中。在该技能的沉浸式场景下，用户唤醒 wukong-robot 后，允许响应更多指令以完成更丰富的操作（例如“下一首歌”、“这是什么歌”等指令）。如果唤醒后只是简单的聊天，还允许 wukong-robot 在回答后恢复该技能的沉浸式场景（例如，用户在音乐场景中唤醒 wukong-robot 并问完时间后，wukong-robot 可以自动恢复音乐播放）。

不论是哪种类型的插件，都只需继承同一个基类 [`robot.sdk.AbstractPlugin`](https://www.hahack.com/wukong-robot/_modules/robot/sdk/AbstractPlugin.html#AbstractPlugin) ，并实现相应相关接口即可。其中：

* 普通技能插件只需实现 `isValid()` 和 `handle()` 两个接口，分别用来判断用户指令是否适合交给该技能插件处理，以及如何处理；
* 沉浸式技能插件在普通技能插件的基础上，还需要设置 `IS_IMMERSIVE` 成员属性为 `True` ，此外还可以根据需求实现 `isValidImmersive()` 和 `restore()` 两个方法，分别用来支持沉浸模式下更多指令的响应以及恢复技能。

## 辅助模块 ##

wukong-robot 提供了多个便利模块，可以用于完成读取用户配置、相关目录和文件位置、打日志、发送邮件、文件读写、音频格式转换等任务。在动手开发 wukong-robot 的技能前，先了解这些模块，有助于更灵活地实现自己要的功能，避免重复造轮子。

* [`robot.config`](https://www.hahack.com/wukong-robot/robot.html#module-robot.config)：配置模块，用于获取 wukong-robot 的配置信息。
* [`robot.constants`](https://www.hahack.com/wukong-robot/robot.html#module-robot.constants): 用于获取 wukong-robot 相关的目录和文件的位置信息。
* [`robot.logging`](https://www.hahack.com/wukong-robot/robot.html#module-robot.logging)：日志模块，用于打印日志。
* [`robot.utils`](https://www.hahack.com/wukong-robot/robot.html#module-robot.utils)：其他辅助脚本的集合，包含了邮件发送、文件读写、wav/mp3 音频格式互转、缓存管理等方法。
* [`robot.sdk.unit`](https://www.hahack.com/wukong-robot/robot.html#module-robot.sdk.utils.unit)：百度 UNIT 模块，可用于将用户指令解析成结构化数据，并支持提取意图、词槽和回复文本。

### config 模块 ###

配置模块，用于获取 wukong-robot 的配置信息。

最常用的是 [`get()`](https://www.hahack.com/wukong-robot/robot.html#robot.config.get) 方法，可以用于获取指定配置的值，并允许提供一个默认值。使用示例：

``` python
from robot import config

# 得到一个包含全部配置信息的 dict 并打印
print(config.get())

# 打印 robot_name_cn 的配置值
# 如果不存在该配置，则取默认值“孙悟空”
print(config.get('robot_name_cn', '孙悟空'))

# 打印后端服务器的 host 配置
# 如果不存在该配置，则取默认值 0.0.0.0
print(config.get('/server/host', '0.0.0.0'))
```

### constants 模块 ###

维护了 wukong-robot 相关的目录和文件的位置信息。示例：

``` python
from robot import constants

# 打印 wukong-robot 的根路径
print(constants.APP_PATH)

# 打印 wukong-robot/static 的路径
print(constants.DATA_PATH)

# 打印 wukong-robot/temp 的路径
print(constants.TEMP_PATH)

# 打印配置文件的路径
print(constants.getConfigPath())

# 打印某个资源文件的路径
print(constants.getData('beep_lo.wav))
```

### logging 模块 ###

在标准库 `logging` 模块的基础上封装的一个模块，最大的好处是同时支持输出到 stdout 和分片日志文件中，并统一了日志的输出格式。

* 对于`stdout`，level 为 `INFO` 级别及以上的日志才会被打印，以节省性能开销；
* 对于文件输出，level 为 `DEBUG` 级别及以上的日志才被打印，以方便获取更丰富的调试信息。

`robot.logging` 模块使用上和标准的 `logging` 模块并无二致，区别仅仅在于引用方式上：

``` python
from robot import logging

logger = logging.getLogger(__name__)

logger.debug('this is a debug message')
logger.info('this is an info message')
logger.error('this is an error message')
logger.critical('this is a critical message')
```

!> 注意：你无须再为 logging 模块设置 Formatter 。

### utils 模块 ###

若干辅助脚本的集合，包含了邮件发送、文件读写、wav/mp3 音频格式互转、缓存管理等方法。以下只列举部分插件开发中可能会用到的方法。其他方法可以通过阅读 [utils的文档](https://www.hahack.com/wukong-robot/robot.html#module-robot.utils) 了解。

#### 邮件发送 ####

##### 发给自己 #####

``` python
from robot import utils

attach_files = ['/home/pi/test1.png', '/home/pi/test2.png']
utils.emailUser('这是邮件的标题', '这是邮件的正文', attach_files)
```

##### 发给指定用户 #####

``` python
from robot import utils, config

recipient = config.get('/email/address', '')
robot_name = config.get('robot_name_cn', 'wukong-robot')
recipient = robot_name + " <%s>" % recipient
user = config.get('/email/address', '')
password = config.get('/email/password', '')
server = config.get('/email/smtp_server', '')
port = config.get('/email/smtp_port', '')

attach_files = ['/home/pi/test1.png', '/home/pi/test2.png']

# 给 zhangsan@test.com 发邮件
sendEmail('这是邮件的标题', '这是邮件的正文', attach_files, 'zhangsan@test.com', user, recipient, password, server, port)
```

#### 文件操作 ####

##### 读取文件 #####

[`get_file_content()`](https://www.hahack.com/wukong-robot/robot.html#robot.utils.get_file_content) 方法用于读取一个文件的内容并返回。示例：

``` python
from robot import utils

# 打印 /home/pi/test.txt 的文件内容
print(utils.get_file_content('/home/pi/test.txt'))
```

##### 删除文件 #####

[`check_and_delete()`](https://www.hahack.com/wukong-robot/robot.html#robot.utils.check_and_delete) 方法用于检查并删除文件。示例：

``` python
from robot import utils

# 删除 /home/pi/test.txt 
utils.check_and_delete('/home/pi/test.txt')
```

##### 写入临时文件 #####

[`write_temp_file()`](https://www.hahack.com/wukong-robot/robot.html#robot.utils.write_temp_file) 方法用于写入临时文件。示例：

``` python
from robot import utils

# 假定 data 是某段 wav 音频的二进制数据
utils.write_temp_file(data, '.wav')
```

### unit 模块 ###

用于对用户指令进行　NLU 解析，得到结构化的数据，并支持提取意图、词槽和回复文本。常用的是 [`getUnit()`](https://www.hahack.com/wukong-robot/robot.sdk.robot.sdk.unit.getUnit)、[`hasIntent()`](https://www.hahack.com/wukong-robot/robot.sdk.html#robot.sdk.unit.hasIntent)、[`getSlots()`](https://www.hahack.com/wukong-robot/robot.sdk.html#robot.sdk.unit.getSlots) 、[`getSay()`](https://www.hahack.com/wukong-robot/robot.sdk.html#robot.sdk.unit.getSay) 等方法。示例：

``` python
from robot.sdk import unit

query = '今天深圳的天气'
# 获取解析结果
parsed = unit.getUnit(query, "S13442", 'w5v7gUV3iPGsGntcM84PtOOM', 'KffXwW6E1alcGplcabcNs63Li6GvvnfL')
# 判断是否包含 `USER_WEATHER` 意图
if unit.hasIntent(parsed, 'USER_WEATHER'):
    # 得到词槽
    slots = unit.getSlots(parsed, 'USER_WEATHER')
    # 获取 user_loc 词槽的内容
    for slot in slots:
        if slot['name'] == 'user_loc':
           print(slot['normalized_word'])  # 深圳
```


