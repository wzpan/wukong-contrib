# -*- coding: utf-8 
# 有道翻译插件

import json
import urllib
import time
import re
import requests
import hashlib
import random
import sys
from robot import config, logging
from robot.sdk.AbstractPlugin import AbstractPlugin

class Plugin(AbstractPlugin):

    SLUG = "youdao"

    def translate(self, appId, appSecret, sentence):
        logger = logging.getLogger(__name__)             
        url = 'https://openapi.youdao.com/api'
        salt = random.randint(1, 65536)
        sign = appId+sentence+str(salt)+appSecret
        m1 = hashlib.md5(sign.encode('utf-8'))
        sign = m1.hexdigest()
        params = {
                 'q': sentence,
                 'from': 'auto',
                 'to': 'auto',
                 'appKey': appId,
                 'salt': salt,
                 'sign': sign
        }
        result = requests.get(url, params=params)
        res = json.loads(result.text, encoding='utf-8')
        s = res['translation'][0]
        return s


    def getSentence(self, text):
        pattern1 = re.compile("翻译.*?")
        pattern2 = re.compile(".*?的翻译")

        if re.match(pattern1, text) != None:
            sentence = text.replace("翻译", "")
        elif re.match(pattern2, text) != None:
            sentence = text.replace("的翻译", "")
        else:
            sentence = ""
        sentence = sentence.replace(",","")
        sentence = sentence.replace("，","")
        return sentence


    def handle(self, text, parsed):
        logger = logging.getLogger(__name__)
        profile = config.get()
        if SLUG not in profile or \
           'appId' not in profile[SLUG] or\
           'appSecret' not in profile[SLUG]:
            self.say('有道翻译插件配置有误，插件使用失败', cache=True)
            return
        appId = profile[SLUG]['appId']
        appSecret = profile[SLUG]['appSecret']
        sentence = self.getSentence(text)
        logger.info('sentence: ' + sentence)
        if sentence:
            try:
                s = self.translate(appId, appSecret, sentence)
                if s:
                    self.say(sentence+"的翻译是" + s, cache=False)
                else:
                    self.say("翻译" + sentence +"失败，请稍后再试", cache=False)
            except Exception as e:
                logger.error(e)
                self.say('抱歉, 我不知道怎么翻译' + sentence, cache=False)
        else:
            self.say(u"没有听清楚 请重试", cache=True)


    def isValid(self, text, parsed):
        return u"翻译" in text
