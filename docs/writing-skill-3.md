# 实战篇3：开发一个天气查询技能

本节我们来写一个带网络请求和百度UNIT解析的普通技能插件 —— 天气插件。

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

（未完待续）
