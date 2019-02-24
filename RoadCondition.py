# -*- coding: utf-8-*-
import json
import requests
from robot import config, logging
from robot.sdk.AbstractPlugin import AbstractPlugin

logger = logging.getLogger(__name__)

class Plugin(AbstractPlugin):

    SLUG = "roadcondition"

    def request(self, url, params): 
        result = requests.post(url, data=params)
        return json.loads(result.text, encoding='utf-8')

    def onAsk(self, input, app_key, adcode):

        if input is None:
            input = "龙岗大道"

        url_transit = "http://restapi.amap.com/v3/traffic/status/road"
        params = {"adcode" : adcode,"name" : input,"key" : app_key}

        res = self.request(url_transit,params)
        logger.debug(res)
        if res:        
            status = res["status"]
            if status == "1":
                logger.debug("status == 1")
                logger.debug(res['trafficinfo'])
                if len(res['trafficinfo']) > 0:
                    trafficinfo = res['trafficinfo']['evaluation']['description']
                    trafficinfo1 = res['trafficinfo']['description']
                    self.say(trafficinfo)
                    self.say(trafficinfo1)
                else:
                    self.say(u"无法获取到信息")
                    return
            else:
                logger.error(u"接口错误:")
                return
        else:
            logger.error(u"接口调用失败")
            return 

    def handle(self, text, parsed):
        profile = config.get()
        if self.SLUG not in profile or \
           'app_key' not in profile[self.SLUG] or \
           'adcode' not in profile[self.SLUG]:
            self.say(u"插件配置有误，插件使用失败")
            return

        app_key = profile[self.SLUG]['app_key']  
        adcode  = profile[self.SLUG]['adcode']
        self.say(u'哪条道路?', onCompleted=lambda: self.onAsk(self.activeListen(), app_key, adcode))

    def isValid(self, text, parsed):
        return any(word in text for word in [u"路况"])
