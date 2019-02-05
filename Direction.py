# -*- coding: utf-8-*-
import sys
import os
import logging
import json
import urllib
from urllib.parse import urlencode
from robot import config

SLUG = "direction"

def request(url, params):
    params = urlencode(params)

    f = urllib.request.urlopen("%s?%s" % (url, params))

    content = f.read()
    return json.loads(content)

def handle(text, mic):
    logger = logging.getLogger(__name__)

    def onAsk(input):
        if input is None:
            mic.say(u'已取消', plugin=__name__)
            return

        profile = config.get()
        if SLUG not in profile or \
           'app_key' not in profile[SLUG] or \
           'city' not in profile[SLUG] or \
           'origin' not in profile[SLUG] or \
           'method' not in profile[SLUG]:
            mic.say(u"插件配置有误，插件使用失败", plugin=__name__)
            return

        app_key = profile[SLUG]['app_key']
        city = profile[SLUG]['city']

        url_place = "http://api.map.baidu.com/place/v2/suggestion"
        params_place = {
            "query" : input,
            "region" : city,
            "city_limit" : "true",
            "output" : "json",
            "ak" : app_key,
        }

        res = request(url_place, params_place)

        if res:
            status = res["status"]
            if status == 0:
                if len(res['result']) > 0:
                    place_name = res['result'][0]["name"]
                    destination = "%f,%f" % (res['result'][0]["location"]['lat'], res['result'][0]["location"]['lng'])
                else:
                    mic.say(u"错误的位置", plugin=__name__)
                    return
            else:
                logger.error(u"位置接口:" + res['message'])
                return
        else:
            logger.error(u"位置接口调用失败")
            return

        origin = profile[SLUG]['origin']

        url_direction = "http://api.map.baidu.com/direction/v2/transit"
        params_direction = {
            "origin" : origin,
            "destination" : destination,
            "page_size" : 1,
            "ak" : app_key,
        }

        res = request(url_direction, params_direction)
        if res:
            status = res["status"]
            if status == 0:
                if len(res['result']['routes']) > 0:
                    direction = ""
                    for step in res['result']['routes'][0]['steps']:
                        direction = direction + step[0]["instructions"] + "."
                        result = place_name + u"参考路线:" + direction
                    mic.say(result, plugin=__name__)
                else:
                    mic.say(u"导航错误", plugin=__name__)
                    return
            else:
                logger.error(u"导航接口:" + res['message'])
                return
        else:
            logger.error(u"导航接口调用失败")
            return

    mic.say("去哪里", cache=True, plugin=__name__, onCompleted=lambda: onAsk(mic.activeListen(MUSIC=True)))
    

def isValid(text):
    return any(word in text for word in [u"怎么去", u"线路", u"路线"])
