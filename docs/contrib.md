## Weather

* 用于查询天气情况。数据来自 [心知天气API](https://www.seniverse.com/doc)。
* 源码：https://github.com/wzpan/wukong-contrib/blob/HEAD/Weather.py

### 交互示例

- 用户：天气
- 悟空：深圳天气。今天：晴。最高气温：25～30摄氏度；明天：晴。26～31摄氏度；后天：小雨。最高气温：23～29摄氏度。

### 配置

``` yaml
# 天气
# 使用心知天气的接口
# https://www.seniverse.com/
weather:
    key: '心知天气 API Key'
```

## HeadlineNews

* 用于播报5条新闻。数据来自 [聚合数据新闻头条API](https://www.juhe.cn/docs/api/id/235)。新闻更新周期5-30分钟，免费用户每天100次API调用。申请数据接口需要注册实名认证，并创建一个应用审核通过，申请审核速度都很快。
* 源码：https://github.com/wzpan/wukong-contrib/blob/HEAD/HeadlineNews.py

### 交互示例

- 用户：体育新闻（可选值：头条, 社会, 国内, 国际，娱乐, 体育 ,军事, 科技，财经,  时尚）
- 悟空：2017马术世界杯总决赛第二日 骑手惊艳赛场。郭艾伦受伤？辽宁队的目标，只有CBA总冠军。中国女排又一女神横空出世！颜值不输惠若琪，或成下一个袁心玥。WWE最佳选手奖又是“他”简直可笑。甘肃敦煌办双遗马拉松 引万人竞逐古丝路景观

### 配置

``` yaml
# 新闻头条
# 聚合数据新闻头条API
# https://www.juhe.cn/docs/api/id/235
headline_news:
    key: 'AppKey'
```

## Direction

* 通过和悟空进行交互，用户说出一个地名，可以获取一条推荐公交线路。插件利用[百度LBS的Web服务API](http://lbsyun.baidu.com/index.php?title=webapi)，使用了[Place suggestion](http://lbsyun.baidu.com/index.php?title=webapi/place-suggestion-api)和[Direction API v2.0](http://lbsyun.baidu.com/index.php?title=webapi/direction-api-v2)两个接口，用户需要在[百度地图开放平台](http://lbsyun.baidu.com/apiconsole/key)注册创建应用以获取app key。为了简化交互，目前只支持查询本市内的地点，而且只给出一条公交(地铁)线路规划。
* 源码：https://github.com/wzpan/wukong-contrib/blob/HEAD/Direction.py

### 交互示例

- 用户：线路
- 悟空：去哪里
- 用户：世纪大道
- 悟空：世纪大道-地铁站参考路线:步行169米.锦绣路站(4口)乘地铁7号线(花木路方向)经过2站到龙阳路站.站内换乘 步行170米.龙阳路站乘地铁2号线(徐泾东方向)经过3站到世纪大道站.

### 配置

``` yaml
# 出行线路规划插件
# 百度LBS Web服务API
# http://lbsyun.baidu.com/index.php?title=webapi
direction:
    app_key: 你申请到的app key
    origin: 出发起始地坐标，可在此http://api.map.baidu.com/lbsapi/getpoint/获取，如:"39.91405,116.404269",纬度在前，经度在后
```

## RoadCondition

* 通过和悟空进行交互，询问道路，可以返回当前道路的路况，计划出行。插件利用高德地图API。用户需要在高德地图开放平台注册创建应用以获取app key。
* 源码：https://github.com/wzpan/wukong-contrib/blob/HEAD/ReadCondition.py

### 交互示例

* 用户：路况
* 悟空：哪条道路
* 用户：龙岗大道
* 悟空：双向畅通

### 配置

``` yaml
roadcondition:
    app_key: "高德app key"  # http://lbs.amap.com/api/
    adcode: "城市码"  # http://lbs.amap.com/api/javascript-api/example/amap-ui-districtexplorer/group/
```

## BaiduFM

* 百度 FM 插件。用户通过配置文件选择一个频道，随机播放音乐。
* 源码：https://github.com/wzpan/wukong-contrib/blob/HEAD/BaiduFM.py

!> 目前不能暂停，只能停止，歌曲是下载一首播放一首，没有做缓存，视网络状况，一首歌曲下载需要几秒到几十秒。

### 常用指令

| 指令 | 相同指令  |  用途 |
| ---- | -------- | ----- |
| 播放百度音乐 | -    | 开始播放指定的电台列表。 |
| 下一首 | 切歌, 下一首歌, 下首歌 | 切换到下一首歌。如果没有下一首歌，就回到列表中第一首歌 |
| 上一首 | 上一首歌，上首歌 | 切换到上一首歌。如果没有上一首歌，就跳到列表中最后一首歌 |
| 停止播放 | 结束播放/退出播放 | 停止播放音乐的播放 |
| 换歌 | - | 随机换另一个列表 |
| 什么歌 | - | 正在播放的是什么歌 |

### 交互示例

- 用户：百度音乐
- 悟空：开始播放90后频道

音乐播放过程中唤醒 wukong-robot ，会停止播放。如果说出“停止播放/退出播放/结束播放”，则插件退出，否则会继续从头播放。

### 配置

``` yaml
baidufm:
    channel: 13  # 默认频道，如果没有配置，默认选择90后频道，更多频道见下表

0-漫步春天
1-秋日私语
2-温暖冬日
3-热歌
4-KTV金曲
5-Billboard
6-成名曲
7-网络歌曲
8-开车
9-影视
10-随便听听
11-经典老歌
12-70后
13-80后
14-90后
15-火爆新歌
16-儿歌
17-旅行
18-夜店
19-流行
20-摇滚
21-民谣
22-轻音乐
23-小清新
24-中国风
25-DJ舞曲
26-电影
27-轻松假日
28-欢快旋律
29-甜蜜感受
30-寂寞
31-单身情歌
32-舒缓节奏
33-慵懒午后
34-伤感
35-华语
36-欧美
37-日语
38-韩语
39-粤语
```

## SpeakIP

* 语音播报树莓派IP地址，可用于获取悟空机器人的内网IP。
* 源码：https://github.com/wzpan/wukong-contrib/blob/HEAD/SpeakIP.py

?> 参考项目：https://github.com/ma6174/speak_raspi_ip  感谢 [ma6174](https://github.com/ma6174) 。

### 交互示例

- 用户：IP地址
- 悟空：192.168.1.7 完毕

## Reboot ##

* 重新启动树莓派（需root权限），可用于开机启动悟空机器人后，强制重启树莓派。
* 源码：https://github.com/wzpan/wukong-contrib/blob/HEAD/Reboot.py

### 交互示例

- 用户：重新启动
- 悟空：将要重新启动系统，请在滴一声后进行确认，授权相关操作
- 用户：确认
- 悟空：授权成功，开始操作

!> 执行命令后需进行确认。

## WebServer ##

* 启动HTTP服务器，浏览悟空临时目录（temp/）。
* 源码：https://github.com/wzpan/wukong-contrib/blob/HEAD/WebServer.py

### 交互示例

- 用户：启动服务器
- 悟空：正在启动服务器
- 悟空：后台服务器启动成功，服务端口 8080

通过浏览器打开  http://[树莓派IP]:8080/ ，可以查看到悟空临时目录的文件列表。

### 配置

可自定义服务器端口，端口号小于1024需root用户执行。

``` yaml
# WEB服务器
webserver:
    webport: 8080
```

## Halt ##

* 关闭树莓派（需root权限），可用于开机启动悟空机器人后，强制关闭树莓派。
* 源码：https://github.com/wzpan/wukong-contrib/blob/HEAD/Halt.py

### 交互示例

* 用户：关闭系统（关机）
* 悟空：将要关闭操作系统，请在滴一声后进行确认，授权相关操作
* 用户：确认
* 悟空：授权成功，开始操作

!> 执行命令后需进行确认。

## WOL ##

* 通过WOL(Wake On Lan)启动电脑，实现语音开机
* 电脑需事先设置WOL，具体流程可参照[这里](http://www.iplaysoft.com/wol.html)

?> 参考项目：[Python WOL/WakeOnLan/网络唤醒数据包发送工具](http://iplayit.blog.51cto.com/7753603/1576048)

### 交互示例

- 用户：打开电脑
- 悟空：启动成功

### 配置

需自定义广播IP及电脑MAC地址

``` yaml
# WOL启动
wol:
    ip: '局域网广播地址或指定电脑IP地址'
    mac: '电脑MAC地址'
```

### 说明

- 设置为局域网广播地址与电脑IP地址有什么区别？
  - 使用广播地址可向当前局域网广播Magic Packet，无需指定电脑IP，适用于动态IP(DHCP)环境，故推荐使用
- 如何查看局域网广播地址？
  - 若网段为192.168.1.1-192.168.1.255，则广播地址为192.168.1.255(即当前子网的最后一个IP地址)
- 如何查看电脑IP&MAC地址？
  - 参照[这里](http://www.iplaysoft.com/wol.html)，MAC地址应使用 `XX:XX:XX:XX:XX:XX` 或 `XX-XX-XX-XX-XX-XX` 格式
- 为什么提示启动成功却并未启动？
  - 电脑需支持网络唤醒并进行[设置](http://www.iplaysoft.com/wol.html)，若确认支持且已设置，请尝试重新安装网卡驱动

## YoudaoFanYi ##

* 用于中英互译的插件，基于有道翻译的API。
* 源码：https://github.com/wzpan/wukong-contrib/blob/HEAD/YoudaoFanYi.py

### 交互示例

- 用户：翻译你好（你好的翻译）
- 悟空：你好的翻译是 hello
- 用户：翻译hello(hello的翻译） 
- 悟空：hello的翻译是 你好

### 配置

使用前需要先到 [有道智云](http://ai.youdao.com/) 分别注册一个应用和有道文本翻译实例，并关联到一起。然后在[我的应用](http://ai.youdao.com/appmgr.s) 中，记下你关联了有道文本翻译实例的应用的应用ID，点击进入该应用，记下该应用的应用密钥。然后如下配置：

``` yaml
youdao:
    appId: 应用ID
    appSecret: 应用密钥
```

## Hass ##

* 用于控制接入 HomeAssistant 的设备
* 源码：https://github.com/wzpan/wukong-contrib/blob/HEAD/Hass.py

最新版本插件基于baidu NLU进行了改良，可实现一轮对话完成交互，也可使用后台web界面进行交互

由于目前没有百度没有提供智能家庭相关NLU字典库的支持，因此作者正努力完善自建词典库来实现更准确的命中和更多的语法

如果遇到配置正常，命中插件，wukong却不回应的情况，说明遇到了词典库的缺失，请尽可能简化您的语法，并将词典库的缺失内容反馈到电子邮箱**cyk0317@sina.com**，或qq群内@杭州-PatrickChen。作者将尽快更新，本插件的完善将离不开大家的支持。

当前词典数据点击[这里](https://github.com/PatrickChina/wukonghass/blob/master/wukong/user_user_smarthome_%E8%87%AA%E5%AE%9A%E4%B9%89%E8%AF%8D%E5%85%B8%E5%80%BC.txt)查看，您可以使用记事本或浏览器的搜索功能搜索您需要的指令是否在词典中，若不在您则可选择使用存在的近义词，谢谢理解。

### 示例
- 用户：“智能家庭当前温度”
- 悟空：“温度状态是22.6摄氏度”

### 配置

官方api页面：https://home-assistant.io/developers/rest_api/

第一步：

在 homeassistant 的 configuration.yaml 里添加：

``` yaml
api：
  api_password: 
```

修改后 api 插件就启动了

注意:在`api_password: `后设置 api 接口密码，建议设置，但是这个密码在与 wukong 之间通信时用不到，以后自行开发 homeassistant 时可能用到这里的 api 密码，此密码的修改不影响 wukong 工作。（冒号之后有空格！在空格之后直接输入密码无需引号）

第二步：

登陆 homeassistant 网页，在侧拉菜单中点击 homeassistant 字样旁自己的头像，然后将页面拉至最底下找到“长期访问令牌”点击创建令牌，随意取一个名字如： wukong 点击确认

在随后弹出的窗口中复制并想办法记录自己的密钥

第三步：

打开 wukong 的配置文件（网页后台或直接修改都一样），添加：

``` yaml
homeassistant:
    url: "http://127.0.0.1"   #切记加上http://，ip或者域名为你的homeassistant的主机
    port: "8123"             # 端口为你的homeassistant的端口和网页端口一样
    key: "" # 密钥
```

key 处填写的内容如下：

Bearer ABCDE

用第二步获取到的密钥替换 ABCDE (保留 Bearer 和 ABCDE 之间的空格)，将其整体填入双引号中
 

### HomeAssistant 配置

configuration.yaml 相同目录下添加 customize.yaml 并 include 进配置文件。

查看状态类的设备(传感器等)将命令写成 list；控制类的设备命令写成 dict，控制命令为 key ，动作为 value。

现阶段配置时使用的命令建议点击[这里](https://github.com/PatrickChina/wukonghass/blob/master/wukong/user_user_smarthome_%E8%87%AA%E5%AE%9A%E4%B9%89%E8%AF%8D%E5%85%B8%E5%80%BC.txt)参照词典写(使用您的文本编辑器的搜索功能模糊搜索您需要的指令)，避免词典缺失影响使用

如下是示例的部分配置：

``` yaml
sensor.tempareture:
  friendly_name: "环境温度"
  wukong: ["查看环境温度", "当前环境温度", "环境温度"]
sensor.humidity:
  friendly_name: "环境湿度"
  wukong: ["查看环境湿度度", "当前环境湿度", "环境湿度"]
switch.light:
  friendly_name: "补光"
  wukong: {"开始补光":"turn_on", "补光":"turn_on", "停止补光":"turn_off", "结束补光":"turn_off"}
switch.pump:
  friendly_name: "浇水"
  wukong: {"开始浇水":"turn_on", "浇水":"turn_on", "停止浇水":"turn_off", "结束浇水":"turn_off"}  
``` 

## ControlMqtt ##

* 通过 Mqtt 协议与其他开发板通讯传递数据。
* 源码：https://github.com/wzpan/wukong-contrib/blob/master/ControMqtt.py

注：

1. 目前处于开发阶段，难免会有一些BUG，以后功能还会慢慢加。
2. 需要 paho-mqtt 的支持
3. 原来action.txt应该为action.json，格式为json格式，如下所示

``` json
{
    "开发板一": ["浇水","补光"],
    "开发板二": ["环境温度","环境湿度"],
    "开发板三": ["土壤湿度"]
}
```

4. 悟空回答的信息需要在下位机生成，也就是说悟空say的内容为其他开发板返回的内容，本程序不会对此内容封装，因为回答有很多很多种类，按照每个人喜欢的形式，比如有人喜欢傲娇的、有人喜欢女王范、有人喜欢抖M的……

### 交互示例 1 ###

- 用户：环境温度
- 悟空：已经接收到指令
- 悟空：当前环境温度26℃

### 交互示例2（RaspberryPi & Arduino） ###

- 用户：补光
- 悟空：已经接收到指令

然后此时 Arduino 控制灯光等补光，为了防止补光时长过量或不足，补光时长和光强量为开发者在 Arduino 中设定的根据当前环境确定的范围。

### 交互示例3（RaspberryPi & Arduino & Nodemcu & ......） ###

- 用户：浇水
- 悟空：开发板X1已经接收到指令
(可以看到浇水开始)
- 用户：土壤湿度
- 悟空：当前开发板X2土壤湿度为xxx

!> 注：所执行的动作都有阈值，比如浇水，为了防止浇水过量或不足，浇水量为开发者在开发板X1中设定的根据当前土壤湿度确定的浇水范围。这里的开发板Xn是所希望动作的实际施行者(也就是对应的下位机)。每个命令都建立一个进程，不同的命令理论上不会因为前一个出现堵塞而后一个不能执行。

### 配置 ###

``` yaml
# 使用mqtt与其他设备连接，作为Publisher
mqttPub:
    host: 'mqtt代理器的地址'
    port: 'mqtt代理器的端口'
    topic_s: '订阅的主题'

```

## RaspberryPiStatus ##

* 语音播报树莓派的CPU温度、内存使用率、存储使用率。
* 源码：https://github.com/wzpan/wukong-contrib/blob/master/RaspberryPiStatus.py

### 交互示例

- 用户：树莓派状态
- 悟空：处理器温度50度,内存使用百分之75，存储使用百分之30

## Lamp ##

通过树莓派的 GPIO 7 口控制台灯

### 常用指令

* 打开台灯： 控制GPIO 7口输出电平，通过继电器打开被控制端电源
* 关闭台灯： 控制GPIO 7口输出电平，通过继电器关闭被控制端电源

### 配置

``` yaml
Lamp:
    pin: 7  # 实际控制电平的管脚
```

### 需求技能

* 需要安装 wiringpi python 支持扩展包，可以通过 pip 命令从官方获取。

  ``` bash
  pip install wiringpi
  ```

* 继电器建议采购高低可选，带光耦的继电器。自己做电子开关。

