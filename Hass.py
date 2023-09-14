# -*- coding:utf-8 -*-
import requests
import json
import re
from robot import logging
from robot import config
from robot.sdk.AbstractPlugin import AbstractPlugin


logger = logging.getLogger(__name__)

class Plugin(AbstractPlugin):

    SLUG = "hass"
    DEVICES = None

    def match(self, text, patterns):
        for pattern in patterns:
            if re.match(pattern, text):
                return pattern
        return ''

    def get_devices(self, profile):
        if self.DEVICES is None:
            self.refresh_devices(profile)
        return self.DEVICES

    def refresh_devices(self, profile, report=False):
        logger.info('刷新设备')
        url = profile[self.SLUG]['url']
        port = profile[self.SLUG]['port']
        key = profile[self.SLUG]['key']
        headers = {'Authorization': key, 'content-type': 'application/json'}
        r = requests.get(url + ":" + port + "/api/states", headers=headers)
        r_jsons = r.json()
        devices = []
        for r_json in r_jsons:
            entity_id = r_json['entity_id']
            domain = entity_id.split(".")[0]
            if domain not in ["group", "automation"]:
                url_entity = url + ":" + port + "/api/states/" + entity_id
                entity = requests.get(url_entity, headers=headers).json()
                devices.append(entity)
        self.DEVICES = devices
        if report:
            self.say('HomeAssistant 刷新设备缓存成功，共获取到 {} 个设备信息'.format(len(self.DEVICES)), cache=True)
                

    def handle(self, text, parsed):
        if isinstance(text, bytes):
            text = text.decode('utf8')
        profile = config.get()
        if self.SLUG not in profile or 'url' not in profile[self.SLUG] or \
           'port' not in profile[self.SLUG] or \
           'key' not in profile[self.SLUG]:
            self.say("HomeAssistant 插件配置有误", cache=True)
            return
        if '刷新设备' in text:
            self.refresh_devices(profile, True)
            return
        url = profile[self.SLUG]['url']
        port = profile[self.SLUG]['port']
        key = profile[self.SLUG]['key']
        services = profile[self.SLUG]['services']
        headers = {'Authorization': key, 'content-type': 'application/json'}
        devices = self.get_devices(profile)
        has_execute = False
        if len(devices) == 0:
            self.say("HomeAssistant 获取不到设备信息", cache=True)
            return
        # logger.info("device信息: ", devices, len(devices))
        for device in devices:
            state = device["state"]
            attributes = device["attributes"]
            domain = device["entity_id"].split(".")[0]
            entity_id = device["entity_id"]
            if entity_id == "fan.feng_shan":
                # logger.info("my 风扇: ", entity_id, url, port, headers)
                if self.execute_script(entity_id, url, port, headers, services, text):
                    if not has_execute:
                        self.say("设备执行成功", cache=True)
                        has_execute = True
                else:
                    if not has_execute:
                        self.say("对不起，设备执行失败", cache=True)
                        has_execute = True
            if 'wukong' in attributes.keys():
                wukong = attributes["wukong"]
                if isinstance(wukong, list):
                    if self.match(text, wukong) != '':
                        if domain == 'script':
                            entity_id = device['entity_id']
                            if self.execute_script(entity_id, url, port, headers):
                                if not has_execute:
                                    self.say("设备执行成功", cache=True)
                                    has_execute = True
                            else:
                                if not has_execute:
                                    self.say("对不起，设备执行失败", cache=True)                                
                                    has_execute = True
                        else:
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
                            has_execute = True
                        break
                elif isinstance(wukong, dict):
                    pattern = self.match(text, wukong.keys())
                    if pattern != '':
                        if isinstance(text, bytes):
                            text = text.decode('utf8')
                        try:
                            act = wukong[pattern]
                            entity_id = device['entity_id']
                            if self.execute_service(entity_id, url, port, headers, act):
                                if not has_execute:
                                    self.say("设备执行成功", cache=True)
                                    has_execute = True
                            else:
                                if not has_execute:
                                    self.say("对不起，设备执行失败", cache=True)                                
                                    has_execute = True
                        except Exception as e:
                            logger.error(e)
                            #return
        if not has_execute:
            self.say("对不起，指令不存在2", cache=True)

    def execute_script(self, entity_id, url, port, headers, services, text):
        # logger.info('设备执行：', services, text)
        for service in services:
            # logger.info("请求参数", service)
            if service["value"] in text:
                s = "/api/services/" + service["service"]
                url_s = url + ":" + port + s
                p = json.dumps(service["data"])
                request = requests.post(url_s, headers=headers, data=p)
                # logger.info("请求参数", url_s, headers, p)
                if format(request.status_code) == "200" or \
                format(request.status_code) == "201": 
                    return True
                else:
                    logger.error(format(request.status_code))
                    return False


    def execute_service(self, entity_id, url, port, headers, act):
        p = json.dumps({"entity_id": entity_id})
        domain = entity_id.split(".")[0]
        s = "/api/services/" + domain + "/"
        url_s = url + ":" + port + s + act        
        request = requests.post(url_s, headers=headers, data=p)
        if format(request.status_code) == "200" or \
           format(request.status_code) == "201": 
            return True
        else:
            logger.error(format(request.status_code))
            return False


    def isValid(self, text, parsed):
        # 根据配置中的正则式来匹配
        return '刷新设备缓存' in text
