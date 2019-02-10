# -*- coding:utf-8 -*-
import requests
import json
import logging
from robot import config

SLUG = "homeassistant"

def handle(text, mic, parsed=None):
    def onAsk(input):
        while not input:
            mic.say("请重新说", cache=True, plugin=__name__, onCompleted=lambda: onAsk(mic.activeListen(MUSIC=True)))
        input = input.split(",")[0].split("，")[0]
        hass(input, mic)
    if "帮我" in text:
        input = text.replace("帮我", "")
        onAsk(input)
    else:
        mic.say("开始家庭助手控制，请在滴一声后说明内容", cache=True, plugin=__name__, onCompleted=lambda: onAsk(mic.activeListen(MUSIC=True)))


def hass(text, mic):
    if isinstance(text, bytes):
        text = text.decode('utf8')
    logger = logging.getLogger(__name__)
    profile = config.get()
    if SLUG not in profile or 'url' not in profile[SLUG] or \
       'port' not in profile[SLUG] or \
       'password' not in profile[SLUG]:
        mic.say("HomeAssistant 插件配置有误", cache=True, plugin=__name__)
        return
    url = profile[SLUG]['url']
    port = profile[SLUG]['port']
    password = profile[SLUG]['password']
    headers = {'x-ha-access': password, 'content-type': 'application/json'}
    r = requests.get(url + ":" + port + "/api/states", headers=headers)
    r_jsons = r.json()
    devices = []
    for r_json in r_jsons:
        entity_id = r_json['entity_id']
        domain = entity_id.split(".")[0]
        if domain not in ["group", "automation", "script"]:
            url_entity = url + ":" + port + "/api/states/" + entity_id
            entity = requests.get(url_entity, headers=headers).json()
            devices.append(entity)
    for device in devices:
        state = device["state"]
        attributes = device["attributes"]
        domain = device["entity_id"].split(".")[0]
        if 'wukong' in attributes.keys():
            wukong = attributes["wukong"]
            if isinstance(wukong, list):
                if text in wukong:
                    try:
                        measurement = attributes["unit_of_measurement"]
                    except Exception as e:
                        pass
                    if 'measurement' in locals().keys():
                        text = text + "状态是" + state + measurement
                        mic.say(text, cache=True, plugin=__name__)
                    else:
                        text = text + "状态是" + state
                        mic.say(text, cache=True, plugin=__name__)
                    break
            elif isinstance(wukong, dict):
                if text in wukong.keys():
                    if isinstance(text, bytes):
                        text = text.decode('utf8')
                    try:
                        act = wukong[text]
                        p = json.dumps({"entity_id": device["entity_id"]})
                        s = "/api/services/" + domain + "/"
                        url_s = url + ":" + port + s + act
                        request = requests.post(url_s, headers=headers, data=p)
                        if format(request.status_code) == "200" or \
                           format(request.status_code) == "201":
                            mic.say("执行成功", cache=True, plugin=__name__)
                        else:
                            mic.say("对不起,执行失败", cache=True, plugin=__name__)
                            print(format(request.status_code))
                    except Exception as e:
                        pass
                    break
    else:
        mic.say("对不起,指令不存在", cache=True, plugin=__name__)


def isValid(text, parsed=None):
    return any(word in text for word in ["开启家庭助手",
                                         "开启助手", "打开家庭助手", "打开助手",
                                         "家庭助手", "帮我"])
