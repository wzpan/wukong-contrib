# -*- coding: utf-8 
#author: chenzhuo
#Raspberry Pi or other platform can connect to the mqtt client,publisher and subscriber can access to bidirectional communication by switching their identities.
#Example:you can get temperature of the enviroment collected by Arduino using Raspberry Pi when Raspberry Pi and Arduino communicate with each other.
#The actions' file must be /home/pi/.dingdang/action.json

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
import json
import os
from robot import config, logging
from robot.sdk.AbstractPlugin import AbstractPlugin

logger = logging.getLogger(__name__)

class Plugin(AbstractPlugin):

    SLUG = "mqttPub"

    def get_topic(self, text):
        home_dir = os.path.expandvars('$HOME')
        location = home_dir + '/.dingdang/action.json'
        f = open(location).read()
        fjson = json.loads(f)
        topic = None
        for key in fjson.keys():
            if text in fjson[key]:
                topic = key
        return topic

    def handle(self, text, parsed):

        profile = config.get()

        #get config
        if ( self.SLUG not in profile ) or ( 'host' not in profile[self.SLUG] ) or ( 'port' not in profile[self.SLUG] ) or ( 'topic_s' not in profile[self.SLUG] ):
            self.say("主人，配置有误", cache=True)
            return

        host = profile[self.SLUG]['host']
        port = profile[self.SLUG]['port']
        topic_s = profile[self.SLUG]['topic_s']
        text = text.split("，")[0]   #百度语音识别返回的数据中有个中文，
        topic_p = self.get_topic(text)
        if topic_p == None:
            return
        try:
            self.say("已经接收到指令", cache=True)
            mqtt_contro(host,port,topic_s,topic_p,text,self.con)
        except Exception as e:
            logger.error(e)
            self.say("抱歉出了问题", cache=True)
            return

    def isValid(self, text, parsed):
        home_dir = os.path.expandvars('$HOME')
        location = home_dir + '/.dingdang/action.json'
        words = []
        if os.path.exists(location):
            f = open(location).read()
            try:
                fjson = json.loads(f)
                for value in fjson.values():
                    if isinstance(value,list):
                        words += value
                    else:
                        words += []
            except ValueError:
                words += []
        return any(word in text for word in words)

class mqtt_contro(object):

    def __init__(self,host,port,topic_s,topic_p,message,mic):
        self._logger = logging.getLogger(__name__)
        self.host = host
        self.port = port
        self.topic_s = topic_s
        self.topic_p = topic_p
        self.message = message
        self.mic = mic
        self.mqttc = mqtt.Client()
        self.mqttc.on_message = self.on_message
        self.mqttc.on_connect = self.on_connect
        #mqttc.on_publish = on_publish
        #mqttc.on_subscribe = on_subscribe
        #mqttc.on_log = on_log
        if self.host and self.topic_p:
            publish.single(self.topic_p, payload=self.message, hostname=self.host,port=1883)
            if self.port and self.topic_s and self.host:
                self.mqttc.connect(self.host, self.port, 5)
                self.mqttc.subscribe(topic_s, 0)
            #while True:
            #    self.mqttc.loop(timeout=5)
            self.mqttc.loop_start()

    def on_connect(self,mqttc, obj, flags, rc):
        if rc == 0:
            pass
        else:
            self._logger.critical("error connect")

    def on_message(self,mqttc, obj, msg):
        if msg.payload:
            self.mqttc.loop_stop()
            self.mqttc.disconnect()
            self.mic.say( str(msg.payload))
        else:
            time.sleep(5)
            self.mqttc.loop_stop()
            self.mqttc.disconnect()
            self.mic.say("连接超时", cache=True)

    def on_publish(self,mqttc, obj, mid):
        self._logger.debug("mid: " + str(mid))

    def on_subscribe(self,mqttc, obj, mid, granted_qos):
        self._logger.debug("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_log(self,mqttc, obj, level, string):
        self._logger.debug(string)
