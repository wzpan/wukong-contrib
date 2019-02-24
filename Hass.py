# -*- coding:utf-8 -*-
import requests
import json
from robot import logging
from robot import config
from robot.sdk.AbstractPlugin import AbstractPlugin

logger = logging.getLogger(__name__)

class Plugin(AbstractPlugin):

    SLUG = "homeassistant"

    def handle(self, text, parsed):
        def onAsk(input):
            if not input:
                self.say("指令有误，请重新尝试", cache=True)
                return
            input = input.split(",")[0].split("，")[0]
            self.hass(input)
        if "帮我" in text:
            input = text.replace("帮我", "")
            onAsk(input)
        else:
            self.say("开始家庭助手控制，请在滴一声后说明内容", cache=True, onCompleted=lambda: onAsk(self.activeListen()))


    def hass(self, text):
        if isinstance(text, bytes):
            text = text.decode('utf8')
        profile = config.get()
        if self.SLUG not in profile or 'url' not in profile[self.SLUG] or \
           'port' not in profile[self.SLUG] or \
           'password' not in profile[self.SLUG]:
            self.say("HomeAssistant 插件配置有误", cache=True)
            return
        url = profile[self.SLUG]['url']
        port = profile[self.SLUG]['port']
        password = profile[self.SLUG]['password']
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
                            logger.error(e)
                        if 'measurement' in locals().keys():
                            text = text + "状态是" + state + measurement
                            self.say(text, cache=True)
                        else:
                            text = text + "状态是" + state
                            self.say(text, cache=True)
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
                                self.say("执行成功", cache=True)
                            else:
                                self.say("对不起,执行失败", cache=True)
                                print(format(request.status_code))
                        except Exception as e:
                            logger.error(e)
                        break
        else:
            self.say("对不起,指令不存在", cache=True)


    def isValid(self, text, parsed):
        return any(word in text for word in ["开启家庭助手",
                                             "开启助手", "打开家庭助手", "打开助手",
                                             "家庭助手", "帮我"])
