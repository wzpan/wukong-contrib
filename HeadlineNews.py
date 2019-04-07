# -*- coding: utf-8 -*-
# 新闻插件
import requests
from robot import config, logging
from robot.sdk.AbstractPlugin import AbstractPlugin
logger = logging.getLogger(__name__)

class Plugin(AbstractPlugin):

    SLUG = "headline_news"

    def request(self, appkey, type, m="GET"):
        url = "http://v.juhe.cn/toutiao/index"
        params = {
            "key" : appkey,
            "type" : type[1]
        }
        req = requests.get(url,params=params)
        res = req.json()
        if res:
            error_code = res["error_code"]
            if error_code == 0:
                self.say(type[0] + u"新闻", cache=True)
                limit = 5;
                news = res["result"]["data"][0:limit]
                news_for_tts = ""
                for new in news:
                    news_for_tts = news_for_tts + new["title"] + "."
                self.say(news_for_tts, cache=True)
            else:
                logger.error(str(error_code) + ':' + res["reason"])
                self.say(res["reason"], cache=True)
        else:
            self.say(u"新闻接口调用错误", cache=True)

    def getNewsType(self, text):
        newsTypes = {"头条":"top", "社会":"shehui","国内":"guonei", "国际":"guoji", "娱乐":"yule",
                     "体育":"tiyu", "军事":"junshi", "科技":"keji","财经":"caijing","时尚":"shishang"}
        newsType = ["头条","top"]
        for type in newsTypes:
            if type  in text:
                newsType = [type,newsTypes[type]]
        return  newsType

    def handle(self, text, parsed):
        profile = config.get()
        if self.SLUG not in profile or \
           'key' not in profile[self.SLUG]:
            self.say(u"新闻插件配置有误，插件使用失败", cache=True)
            return
        key = profile[self.SLUG]['key']
        type = self.getNewsType(text)
        self.request(key, type)

    def isValid(self, text, parsed):
        return u"新闻" in text
