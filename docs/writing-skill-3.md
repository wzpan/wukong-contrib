# 实战篇3：开发一个天气查询技能

本节我们来写一个稍微复杂的普通技能插件——天气插件，这个插件包含了自定义配置项、网络请求和百度UNIT解析。

## 了解天气 API ##

要实现天气预报功能，少不了要搜下现有的一些开放的天气 API 。不难可以找到一款免费的天气 API —— [心知天气](https://www.seniverse.com/) 。心知天气提供了天气、空气质量、生活指数等多种数据信息。其中[逐日天气预报](https://www.seniverse.com/doc#daily)是免费的，可以利用来实现我们要的天气预报查询技能。

选择心知天气的另一个理由是他们的 API 文档非常详细，还提供了多种语言的 [demo](https://github.com/seniverse/seniverse-api-demos) 。下面是官方提供的一个 Python 版的示例：

``` python
import requests
from utils.const_value import API, KEY, UNIT, LANGUAGE
from utils.helper import getLocation

def fetchWeather(location):
    result = requests.get(API, params={
        'key': KEY,
        'location': location,
        'language': LANGUAGE,
        'unit': UNIT
    }, timeout=1)
    return result.text

if __name__ == '__main__':
    location = getLocation()
    result = fetchWeather(location)
    print(result)
```

其中，`API` 是 API 的地址，逐日天气预报的 API 地址是 https://api.seniverse.com/v3/weather/daily.json ；`KEY` 则是心知天气的 API 密钥，每个注册账户都可以得到一个密钥；`location` 是城市名，例如深圳就是 `深圳` 或者 `shenzhen`；而 `language` 和 `unit` 分别表示语言和单位，由于是可选参数，这里不做详细介绍。有兴趣的朋友请阅读[官方文档](https://www.seniverse.com/doc)。

整段代码也没有什么特别好说的：先是定义了一个 `fetchWeather()` 函数，该函数使用 requests 模块发起 API 请求，请求超时设置为 1 秒。之后调用这个函数并打印返回的结果。

## 开发天气查询技能 ##

同样地，在编写插件前，我们需要先考虑以下几个问题：

* 如何判断用户的指令是否适合用这个插件处理？
* 需要暴露哪些配置项？
* 如何处理用户的指令并得到需要的信息？

围绕这几个问题，我们可以将这个插件设计成如下的形式：

* 只要百度UNIT判断为天气查询意图，即认为适合交给本插件进行处理；
* 从心知天气的 API 接口可以知道，查询参数至少需要提供心知天气的 API key 和城市名称。其中，API key 可以作为这个插件的一个配置项，而城市名称则可以在使用时从用户的指令中提取出城市词槽。如果取不到，再从配置文件的 `location` 选项中读取；
* 首先尝试从指令中提取出城市信息，如果有提取到，那么将其作为 `fetchWeather()` 的 `location` 参数；如果没提取到，就将配置文件中的 `location` 配置作为 `fetchWeather()` 的 `location` 参数，调用心知天气的 API ，取出天气信息并读给用户。

我们一步步来将实现这样的的插件。

### 1. 拷贝模板 ###

同样可以先将简单版 Hello World 技能插件代码拷贝过来，保存为 `$HOME/.wukong/custom/Weather.py`：

``` python
# -*- coding: utf-8-*-
from robot.sdk.AbstractPlugin import AbstractPlugin

class Plugin(AbstractPlugin):

    def handle(self, text, parsed):
        self.say('hello world!', cache=True)

    def isValid(self, text, parsed):
        return "打个招呼" in text
```

### 2. `isValid()` 实现 ###

我们先修改 `isValid()` 实现，将这个判断规则改为判断是否属于天气意图。

一种简单的思路是直接通过诸如“天气”之类的关键词来判断，不过这样可能会误判。例如，如果用户说的是“如果明天天气好，我就出去跑步”，此时突然回复天气就显得不太合适。所以，更智能的方案是使用百度 UNIT 来帮我们判断意图。在写 [智能版 Hello World](writing-skill-1?id=%e6%9b%b4%e6%99%ba%e8%83%bd%e7%9a%84%e7%89%88%e6%9c%ac%ef%bc%9a%e7%bb%93%e5%90%88-nlu) 技能时我们已经了解到了 UNIT 技能的训练方法。不过，百度 UNIT 其实也自带了一些预置技能，其中就包括[天气技能](https://ai.baidu.com/unit/v2#/preskilldetail/34838)：

![百度UNIT预置的天气技能](http://hahack-1253537070.file.myqcloud.com/images/wukong-docs/unit-weather.png)

查看[这个技能的说明页](https://ai.baidu.com/unit/v2#/preskilldetail/34838)，可以看到它提供了非常多的意图。其中有一个查天气的意图 `USER_WEATHER` ，看起来就是我们需要的：

![`USER_WEATHER` 意图](http://hahack-1253537070.file.myqcloud.com/images/wukong-docs/USER_WEATHER.png)

!> 如果你要实现的技能已经有现成的相应 UNIT 预置技能，那么你应该毫不犹豫地使用它，而不要自己训练。因为 UNIT 提供的预置技能往往有更强的泛化能力。这是因为训练这些预置技能时所选用的语料样本集比你自己能找到的要大得多。

于是，我们可以直接利用这个技能来实现我们的天气查询功能。将该技能添加到你的 UNIT 机器人中，然后和[前面的文章](writing-skill-1?id=%e6%9b%b4%e6%99%ba%e8%83%bd%e7%9a%84%e7%89%88%e6%9c%ac%ef%bc%9a%e7%bb%93%e5%90%88-nlu)类似，实现如下的 `isValid()` 方法：

``` python
# -*- coding: utf-8-*-
from robot.sdk import unit
from robot.sdk.AbstractPlugin import AbstractPlugin

# 调试用，发布时删除
SERVICE_ID='你的技能service_id'
API_KEY='你的技能api_key'
SECRET_KEY='你的技能secret_key'

class Plugin(AbstractPlugin):

    SLUG = "weather"

    def handle(self, text, parsed):
	    self.say('hello world!', cache=True)

    def isValid(self, text, parsed):
        parsed = unit.getUnit(text, SERVICE_ID, API_KEY, SECRET_KEY) # 调试用，发布时删除
        # 判断是否包含 USER_WEATHER 意图
        return unit.hasIntent(parsed, 'USER_WEATHER')
```

注意在上面的第 12 行中我们修改了插件的 SLUG 为 `weather` 。它用于标识这个插件，如果不指定的话，插件默认的 SLUG 则会以插件的文件名命名，即 `Weather` 。

?> 这里只是为了演示插件编写的灵活性，一般情况下你并不需要指定 SLUG 。直接把文件名当 SLUG 反而更能避免配置的人出错。

### 3. `handle()` 实现 ###

接下来我们来实现 `handle()` 方法。在这个方法中，我们需要解决以上两个任务：

1. 将心知天气的 API key 作为这个插件的一个配置项，而城市名称则可以在使用时从用户的指令中提取出城市词槽。如果取不到，再从配置文件的 `location` 选项中读取；
2. 首先尝试从指令中提取出城市信息，如果有提取到，那么将其作为 `fetchWeather()` 的 `location` 参数；如果没提取到，就将配置文件中的 `location` 配置作为 `fetchWeather()` 的 `location` 参数，调用心知天气的 API ，取出天气信息并读给用户。

首先我们先把 API Key 放进配置项。我们可以设计如下的配置。将其加进 `$HOME/.wukong/config.yml` 中。

``` yaml
...

# 天气
# 使用心知天气的接口
# https://www.seniverse.com/
weather:
    key: 'etxzx9abupxplhic' # 心知天气 API Key
```

其中，`weather` 是我们刚刚给这个技能定义的 SLUG 。如果没有显式定义，那这里就应该写 `Weather` （因为插件文件名是 `Weather.py`）；`key` 是心知天气的 API Key 。

接下来我们在 `handle()` 方法中取出这个 `key` ，我们可以利用 [`robot.config`](writing-skill-basic?id=config-%e6%a8%a1%e5%9d%97) 模块提供的 `get()` 方法。

``` python
...

from robot import config

...

    def handle(self, text, parsed):
        parsed = unit.getUnit(text, SERVICE_ID, API_KEY, SECRET_KEY) # 调试用，发布时删除
        # get config
        key = config.get('/{}/key'.format(self.SLUG), '')
...
```

接下来我们需要解析出要查询的城市。`USER_WEATHER` 意图包含了地点 `user_loc` 的词槽，所以我们可以写一个 `get_location()` 方法尝试提取这个词槽：

``` python
...

    def get_location(self, parsed):
        """ 获取位置 """
        slots = unit.getSlots(parsed, 'USER_WEATHER')
        # 如果 query 里包含了地点，用该地名作为location
        for slot in slots:
            if slot['name'] == 'user_loc':
                return slot['normalized_word']
        # 如果不包含地点，但配置文件指定了 location，则用 location
        else:
            return config.get('location', '深圳')
...
```

有了这些参数后，我们可以开始写心知天气的 API 请求。我们先把心知的 Demo 给出的 `fetchWeather` 函数做一点调整，放进代码中方便复用：

``` python
...

    def fetch_weather(self, api, key, location):
        result = requests.get(api, params={
	                'key': key,
                    'location': location
                 }, timeout=3)
        res = json.loads(result.text, encoding='utf-8')
        return res

...
```

接下来就可以完成我们的 `handle()` 函数，把整个天气查询逻辑串起来：

```
...

from robot import config, logging
logger = logging.getLogger(__name__)

...
 
    def handle(self, text, mic, parsed):
        parsed = unit.getUnit(text, SERVICE_ID, API_KEY, SECRET_KEY) # 调试用，发布时删除
        key = config.get('/{}/key'.format(self.SLUG), '')
        location = self.get_location(parsed)
        WEATHER_API = 'https://api.seniverse.com/v3/weather/daily.json'
        try:
            weather = self.fetch_weather(WEATHER_API, key, location)
            logger.debug("Weather report: ", weather)
            if 'results' in weather:
                daily = weather['results'][0]['daily']
                day_text = ['今天', '明天', '后天']
                responds = '%s天气：' % location
                for day in range(len(day_text)):
                    responds += '%s：%s，%s到%s摄氏度。' % (day_text[day], daily[day]['text_day'], daily[day]['low'], daily[day]['high'])
                self.say(responds)
            else:
                self.say('抱歉，我获取不到天气数据，请稍后再试')
        except Exception, e:
            logger.error(e)
            self.say('抱歉，我获取不到天气数据，请稍后再试')
...

```

我们来解释一下上面的代码：

* 由于这个插件比较复杂，又涉及到网络调用，为了方便调试和定位问题，所以我们在第 3~4 行中，又引入了 [`robot.logging`](writing-skill-basic?id=logging-%e6%a8%a1%e5%9d%97) 模块帮助我们打 log 。
* 第 14 行我们调用了前面编写的 `fetch_weather()` 成员方法来获取天气数据，这个接口会直接返回未来三天的天气，所以我们在第 20~21 行将三天的结果拼成三句话并朗读给用户。（当然，更好的做法是还要判断用户的指令有没有特别问到是哪一天，这里为了不把问题复杂化所以只实现了简单的拼接。一个更好的版本可以参见 wukong-contrib 的 [Weather 插件](https://github.com/wzpan/wukong-contrib/blob/HEAD/Weather.py)）

### 完整实现 ###

``` python
# -*- coding: utf-8-*-
# author: wzpan
# 天气插件 v 1.0
import requests
import json
from robot import config, logging
from robot.sdk import unit
from robot.sdk.AbstractPlugin import AbstractPlugin

logger = logging.getLogger(__name__)

# 调试用，发布时删除
SERVICE_ID='你的技能service_id'
API_KEY='你的技能api_key'
SECRET_KEY='你的技能secret_key'

class Plugin(AbstractPlugin):

    SLUG = "weather"

    def fetch_weather(self, api, key, location):
        result = requests.get(api, params={
	                'key': key,
                    'location': location
                 }, timeout=3)
        res = json.loads(result.text, encoding='utf-8')
        return res

    def get_location(self, parsed):
        """ 获取位置 """
        slots = unit.getSlots(parsed, 'USER_WEATHER')
        # 如果 query 里包含了地点，用该地名作为location
        for slot in slots:
            if slot['name'] == 'user_loc':
                return slot['normalized_word']
        # 如果不包含地点，但配置文件指定了 location，则用 location
        else:
            return config.get('location', '深圳')

    def handle(self, text, mic, parsed):
        parsed = unit.getUnit(text, SERVICE_ID, API_KEY, SECRET_KEY) # 调试用，发布时删除
        key = config.get('/{}/key'.format(self.SLUG), '')
        location = self.get_location(parsed)
        WEATHER_API = 'https://api.seniverse.com/v3/weather/daily.json'
        try:
            weather = self.fetch_weather(WEATHER_API, key, location)
            logger.debug("Weather report: ", weather)
            if 'results' in weather:
                daily = weather['results'][0]['daily']
                day_text = ['今天', '明天', '后天']
                responds = '%s天气：' % location
                for day in range(len(day_text)):
                    responds += '%s：%s，%s到%s摄氏度。' % (day_text[day], daily[day]['text_day'], daily[day]['low'], daily[day]['high'])
                self.say(responds)
            else:
                self.say('抱歉，我获取不到天气数据，请稍后再试')
        except Exception, e:
            logger.error(e)
            self.say('抱歉，我获取不到天气数据，请稍后再试')

    def isValid(self, text, parsed):
        parsed = unit.getUnit(text, SERVICE_ID, API_KEY, SECRET_KEY) # 调试用，发布时删除
        # 判断是否包含 USER_WEATHER 意图
        return unit.hasIntent(parsed, 'USER_WEATHER')
```
