# -*- coding: utf-8-*-
import os
import logging
import json
import requests
from robot import config

SLUG = "roadcondition"

def request(url, params): 
    result = requests.post(url, data=params)
    return json.loads(result.text, encoding='utf-8')

def onAsk(input, mic, app_key, adcode):

    if input is None:
        input = "龙岗大道"
    
    url_transit = "http://restapi.amap.com/v3/traffic/status/road"
    params = {"adcode" : adcode,"name" : input,"key" : app_key}
   
    res = request(url_transit,params)
    logger.debug(res)
    if res:        
        status = res["status"]
        if status == "1":
            logger.debug("status == 1")
            logger.debug(res['trafficinfo'])
            if len(res['trafficinfo']) > 0:
                trafficinfo = res['trafficinfo']['evaluation']['description']
                trafficinfo1 = res['trafficinfo']['description']
                mic.say(trafficinfo, plugin=__name__)
                mic.say(trafficinfo1, plugin=__name__)
            else:
                mic.say(u"无法获取到信息", plugin=__name__)
                return
        else:
            logger.error(u"接口错误:")
            return
    else:
        logger.error(u"接口调用失败")
        return 

def handle(text, mic, parsed=None):
    logger = logging.getLogger(__name__)
    profile = config.get()
    if SLUG not in profile or \
       'app_key' not in profile[SLUG] or \
       'adcode' not in profile[SLUG]:
        mic.say(u"插件配置有误，插件使用失败", plugin=__name__)
        return
        
    app_key = profile[SLUG]['app_key']  
    adcode  = profile[SLUG]['adcode']
    mic.say(u'哪条道路?', plugin=__name__, onCompleted=lambda: onAsk(mic.activeListen(MUSIC=True), mic, app_key, adcode))

    


def isValid(text, parsed=None):
    return any(word in text for word in [u"路况"])
