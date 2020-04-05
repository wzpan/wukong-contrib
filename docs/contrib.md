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

* 用于控制接入 HomeAssistant 的设备，支持读取和设置 HomeAssistant 的实体状态（states），以及诸如调用 HomeAssistant 的脚本（script）等多种服务（service）。
* 源码：https://github.com/wzpan/wukong-contrib/blob/HEAD/Hass.py

### 示例

- 用户：打开灯
- 悟空：设备执行成功
- 用户：空调温度
- 悟空：空调温度状态是17℃
- 用户：当前水质
- 悟空：水质状态是1TDS

### 配置

下面介绍如何配置 Hass 插件。为了关联两个平台，HomeAssistant 和 wukong-robot 都需要做一些配置工作。

#### 1. HomeAssistant 设置

在 HomeAssistant 中，需要做以下几件事：

1. 获取 token ；
2. 开启高级模式（Advanced Mode）；
3. 自定义实体的触发命令。

##### 获取 token

登陆 HomeAssistant 网页，在侧拉菜单中点击 HomeAssistant 字样旁自己的头像，进入用户资料页：

![用户资料页入口](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/wukong-docs/hass-1.png)

然后将页面拉至最底下找到“长期访问令牌”点击创建令牌，随意取一个名字如： wukong ，点击确认。

![创建长期访问令牌](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/wukong-docs/hass-2.png)

在随后弹出的窗口中复制并想办法记录自己的密钥。

##### 开启高级模式

这一步是为了开启实体的[自定义功能](https://www.home-assistant.io/docs/configuration/customizing-devices/)，方便为你接入的每一个实体定制 wukong-robot 的 Hass 插件的触发命令。

在用户资料页里，滚到上面一点的位置，能找到一个高级模式（Advanced Mode），点击开启。

![开启高级模式](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/wukong-docs/hass-3.png)

完成后，还需要在 configuration.yaml 相同目录下创建一个 customize.yaml 文件（初始为空即可）。然后在 configurations.yaml 中 include 这个文件：

``` yaml
homeassistant:
  customize: !include customize.yaml
```

完成了这些操作后，我们可以强制让 HomeAssistant 重新读取下配置文件。进入 HomeAssistant 的开发者工具页，点击服务选项卡，在里头找到 `homeassistant.reload_core_config` ，选中后点击 “调用服务” ，等待片刻即可生效。

##### 定制实体触发命令

完成上面 HomeAssistant 的两步操作后，我们还需要解决一个问题：如何让 wukong-robot 理解用户的指令并转成对 HomeAssistant 的控制指令？在这一步中，我们在 customize.yaml 配置文件中，给希望能让 wukong-robot 控制的实体加点 “说明” ，将这些 HomeAssistant 的设备暴露给 wukong-robot 。

下面我举几个实际例子。我家有：

- 三个电灯泡（提供了 `light` 类型实体）。我希望通过类似 “打开灯”、“把灯关了” 的语音指令，让 wukong-robot 能给 HomeAssistant 下发开关这三个实体的控制指令：

  ![`light` 实体](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/wukong-docs/hass-4.png)
  
- 一个净水器（提供了 `sensor` 类型实体）。我希望通过类似 “当前水质” 的语音指令，让 wukong-robot 帮我查询净水器的水质状态：

  ![`sensor` 类型实体](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/wukong-docs/hass-5.png)
  
- 一个电风扇（我为其编写了 `script.zhimi_turn_on` 脚本和 `script.zhimi_turn_off` 脚本两个 `script` 类型服务）。我希望通过类似 “打开风扇”、“关了风扇” 的语音指令，让 wukong-robot 能给 HomeAssistant 下发执行这两个脚本的控制指令：

  ![`script` 类型服务](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/wukong-docs/hass-6.png)

对于三个 `light` 类型实体，我们希望通过设置这几个实体的状态，例如调用 `turn_on`，`turn_off` 的开关命令来控制开关状态，因此可以在 customize.yaml 中配置如下：

``` yaml
light.zhi_rui_deng_pao_1:
  wukong:
    ".*开.*灯": turn_on
    ".*灯.*开": turn_on
    ".*关.*灯": turn_off
    ".*灯.*关": turn_off
light.zhi_rui_deng_pao_2:
  wukong:
    ".*开.*灯": turn_on
    ".*灯.*开": turn_on
    ".*关.*灯": turn_off
    ".*灯.*关": turn_off
light.zhi_rui_deng_pao_3:
  wukong:
    ".*开.*灯": turn_on
    ".*灯.*开": turn_on
    ".*关.*灯": turn_off
    ".*灯.*关": turn_off
```

其中，每个实体都有一个 `wukong` 的配置，且此时值为字典形式，表示需使用该值的信息设置状态。其中，键为语音指令的正则表达式，值为相应控制指令。例如，当用户的指令与 `.*开.*灯` （比如 `打开电灯`，`开灯`）的正则表达式匹配时，即执行对应的控制指令 `turn_on` 。

对于 `sensor` 实体，我们希望读取诸如水质、温度之类的状态值，不需要设置状态，因此可以在 customize.yaml 中追加配置如下：

``` yaml
sensor.filtered_water:
  wukong:
    - ".*水质.*"
```

此时 `wukong` 的配置值变成了一个数组 `[".*水质.*"]` ，表示只需读取状态值无需设置值。当用户的指令与 `.*水质.*` （比如 `当前水质`，`水质怎么样`）的正则表达式匹配时，即读取并播报净水器的水质状态值。

对于 `script` 类型服务，我们需要直接执行它，因此可以在 customize.yaml 中追加配置如下：

``` yaml
script.zhimi_turn_on:
  wukong:
    - ".*开.*风扇"
script.zhimi_turn_off:
  wukong:
    - ".*关.*风扇"
```

和 `sensor` 实体类似，脚本等服务无需传值，所以 `wukong` 的配置值是一个数组。当用户的指令与 `.*开.*风扇` （比如 `打开电风扇`，`开启风扇`）的正则表达式匹配时，及打开电风扇。

#### 2. 配置 wukong-robot 的 Hass 插件

打开 wukong 的 config.yml 配置文件（或在 wukong-robot 的后台管理端配置页面），先添加：

``` yaml
hass:
    url: "http://127.0.0.1"   #切记加上http://，ip或者域名为你的HomeAssistant的主机
    port: "8123"             # 端口为你的HomeAssistant的端口和网页端口一样
    key: "Bearer XXXXXXXXXX" # 密钥，注意 Bearer 不可少
    patterns:
        - ".*开.*灯"
        - ".*关.*灯"
        - ".*灯.*开"
        - ".*灯.*关"
        - ".*水质.*"
        - ".*开.*风扇"
        - ".*关.*风扇"
        - ".*风扇.*开"
        - ".*风扇.*关"
```

用上面获取到的 token 替换 `XXXXXXXXXX` (保留 Bearer 和 `XXXXXXXXXX` 之间的空格)，将其整体填入双引号中。

而 `patterns` 则是在上一步中 `customize.yaml` 里所有 `wukong` 包含的正则表达式。

当用户跟 wukong-robot 说完控制指令时，这个控制指令会先尝试与 Hass 插件的 `patterns` 里的每一个正则式进行匹配，如果匹配成功，则触发 Hass 插件，再由 Hass 插件尝试与 HomeAssistant 暴露的所有控制指令进行进一步匹配。如果匹配成功，则由 HomeAssistant 执行对应指令。

![Hass 插件执行效果](https://hahack-1253537070.cos.ap-chengdu.myqcloud.com/images/wukong-docs/hass-7.png)

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
### NodeMCU 参考代码 ###

下面是NodeMCU硬件端参考代码，使用Arduino IDE进行开发。

```C
/* wukong-robot control the NodeMCU by MQTT
   Compile with Arduino IDE
   Author: IAMLIUBO
   Github: github.com/imliubo
*/
#include "EspMQTTClient.h"

#define RELAY_PIN D1   //GPIO5
#define LED_PIN   D6   //GPIO12

void onConnectionEstablished();

EspMQTTClient client(
  "XXXXXXXXX",                 // Wifi ssid
  "XXXXXXXXX",                 // Wifi password
  onConnectionEstablished,     // MQTT connection established callback
  "XXX.XXX.XXX.XXX"            // MQTT broker ip
  1883,                        // MQTT broker port
  "mqttusr",                   // MQTT username
  "mqttpass",                  // MQTT password
  "test",                      // Client name
  true,                        // Enable web updater
  true                         // Enable debug messages
);

long lastTime = 0;
uint8_t pin_status = 0;

void LED_Control_Callback(const String & payload) {
  const char* p = payload.c_str();
  //  Serial.println(p);
  if (strstr(p, "开灯")) {
    digitalWrite(RELAY_PIN, LOW);
    client.publish("/wukong/mqtt", "主人，灯已打开！");// "wukong/mqtt" 是在config.yml中定义的 topic_s 字段，用来回复wukong_robot的自定义消息。
  }
  if (strstr(p, "关灯")) {
    digitalWrite(RELAY_PIN, HIGH);
    client.publish("/wukong/mqtt", "主人，灯已关闭！");
  }
}

void onConnectionEstablished()
{
  client.subscribe("开发板一", LED_Control_Callback);// "开发板一" 是在action.json文件中定义的，用来接收wukong-robot下发的命令。
}

void setup()
{
  Serial.begin(115200);
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH);
}

void loop()
{
  client.loop();

  long now = millis();
  if (now - lastTime > 1000) {
    lastTime = now;
    digitalWrite(LED_PIN, !pin_status);
    pin_status = !pin_status;
  }
}
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


## SmartMiFan ##

[智米电风扇](https://www.xiaomiyoupin.com/detail?gid=102194)插件，可以使用叮当机器人声控智米电风扇。功能包括：

* 电源开关
* 风量调节
* 预约关机
* 自然风开关
* 摇头开关

### Demo

[Demo](http://t.cn/RK05OV8)

### 依赖安装

依赖 python-miio 库：

``` bash
pip install python-miio
```

另外，为了方便获取智米风扇的端口号和token，需要安装一个 `miio` 工具：

``` bash
npm install -g miio
```

### 配置

先确保你的智米电风扇已开机并和 wukong-robot 所在的机器处于同一个局域网下。然后执行以下命令获取风扇的 `host` 和  `token`:

``` sh
miio discover
```

然后在 config.yml 中添加如下配置：

``` yml
# 智米风扇
SmartMiFan:
    host: "192.168.1.106"
    token: "32e9af2050bc9d6f599c061733effee0"
    angle: 60  # 摇头的角度范围。可选值为 30/60/90/120
```

完成后重启叮当即可使用本插件。

### 指令列表

| 指令 | 相同指令  |  用途 |
| ---- | -------- | ----- |
| 打开风扇 | 启动风扇 | 打开风扇 |
| 关闭风扇 | - | 关闭风扇 |
| 开启自然风 | 启动自然风    | 切换到自然风模式 |
| 关闭自然风 | 关闭自然风    | 切换到普通模式 |
| 开始摇头 | 开启摇头    | 开始摇头 |
| 停止摇头 | 结束摇头，关闭摇头    | 结束摇头 |
| 加大风速 | 加快风速，加大风量，加大风力    | 加大风扇转速 |
| 减少风速 | 减慢风速，减少风量，减小风力    | 降低风扇转速 |
| $num $unit 后关闭风扇 | $num 是数字，$unit 可以是秒/分钟/小时  | 预约关机 |


## NeteaseMusic ##

* 根据Github上的[musicbox](https://github.com/darknessomi/musicbox)所提供的api文件进行抽离和修改，配合wukong项目达到语音交互型的NeteaseMusic插件。
* 目前功能：
  1. **个性化推荐歌单**
  2. **每日推荐歌曲**
  3. **个人账号下的“我的歌单”**
  4. **搜索歌手/歌名/歌手+歌名**
  5. **自动签到**
  6. **收藏当前播放的歌单到个人账号**
  7. **收藏当前播放的歌曲到红心歌单（我喜欢的音乐歌单）**
  8. **当播放红心歌单，开启心动模式（红心歌单的歌曲+推荐相似的新歌）**
  9. **询问当前播放歌曲信息**
  10. **基本的播放器操作**
  11. **往后还会有更多功能，请敬请期待一下...**
* 代码比较啰嗦，希望多多学习，欢迎大家多出建议和问题来改良。
* 源码：[https://github.com/wzpan/wukong-contrib/blob/HEAD/BaiduMap.py](https://github.com/wzpan/wukong-contrib/blob/HEAD/WangYiYun.py)

### 配置
1. 首先请将账号信息配置在用户目录~/.wukong/config.yml，在文件最尾处添加类似下方的方式配置。
``` yml
# 网易云音乐插件
NeteaseMusic:
    account: 'XXXXXXXX'  # 网易云音乐账号
    #密码的 md5，可以用 python3 wukong.py md5 "密码" 获得
    md5pass: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx' 
```
2. 将~/.wukong/contrib主库更新一下以获取WangYiYun.py插件，还有调用pip3下载一些额外的依赖库requests_cache。
``` sh
cd $HOME/.wukong/contrib
git pull
cd ../
pip3 install -r contrib/requirements.txt
``` 

### 关于首次登陆的那些事
* 首次登陆会通过账号信息account和md5pass尝试获取两周有效期的Cookies并保存于本地~/.neteasemusic/cookies，同时会定期检查有效期。
* 在~/.neteasemusic/目录有一个名为reqcache文件，用于requests的缓存。
* 还有~/.neteasemusic/目录有一个名为database.json文件，用于保存用户的个人信息以便于往后的查询请求，例如userid和个人歌单。

### 交互示例
为了简化交互和满足不同的问句，一次的播报信息中只会包含五个歌单名称，可以对悟空喊：“我想听下去”来了解更多歌单名称。

> 每日推荐歌单 / 我的歌单

- 用户：播放网易云的推荐歌单 / 打开我的网易云歌单
- 悟空：共找到X张歌单，第1张叫XXX，第2张叫XXX...想听哪一张，或者要不要继续听下去呢？
- 用户：我想听下去 / 我要继续听更多
- 悟空：共找到X张歌单，第6张叫XXX，第7张叫XXX...想听哪一张，或者要不要继续听下去呢？
- 用户：（中途可打断悟空）悟空悟空，我要听第8张。（然后播放歌曲）
- 用户：刚刚第4张歌单叫什么来的？
- 悟空：第四张歌单叫XXXX
- 用户：那我要听第4张
- 悟空：选了第4张

> 每日推荐歌曲

- 用户：播放网易云的推荐歌曲 / 今天网易云有什么推荐的歌曲
- 悟空：今天共有X首推荐歌曲噢！（然后播放歌曲）

> 打开红心歌单和开启心动模式 (我喜欢的音乐歌单)

- 用户：播放网易云的红心歌单
- 悟空：红心歌单共有X首歌曲噢！
- 用户：开启/打开心动模式
- 悟空：已成功开启心动模式，目前有X首歌曲！

> 搜索歌手/歌名（模板抓取，""双引号的字必须说, |表示or）

- 用户：赶紧"播放|搜索|找"李荣浩的“歌|歌曲”
- 悟空：你要听你荣号，对吗？不对的话，请重新说一次！
- 用户：不对，我要“听”李荣浩的“歌曲”
- 悟空：你要听李荣浩，对吗？不对的话，请重新说一次！
- 用户：对的|是的|确认
- 悟空：找到了李荣浩的XX。（然后播放歌曲）

or 

- 用户：我想“听”陈奕迅“的”红玫瑰
- 悟空：你要听陈奕迅的红玫瑰，对吗？不对的话，请重新说一次！
- 用户：算了，不用了。
- 悟空：退出搜索

> 播放歌曲时的语句

- 用户：这首歌叫什么
- 悟空：这首歌叫XXX，是XXX唱的
- 用户：这张歌单叫什么名字
- 悟空：目前播放的歌单叫XXX
- 用户：我想要收藏这首歌  / 我要收藏这个歌单
- 悟空：这首歌已帮你收藏成功 / 目前的歌单已收藏成功！
- 用户：再放一遍吧
- 悟空：重新播放当前的歌曲
