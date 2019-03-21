# -*- coding: utf-8-*-
from robot.sdk import unit
from robot.sdk.AbstractPlugin import AbstractPlugin
from sdk.weibo import WeiBo
import time
import os
import requests

weibo = WeiBo()

class Plugin(AbstractPlugin):

    IS_IMMERSIVE = True

    def __init__(self, con):
        super(Plugin, self).__init__(con)
        self.playList = []
        self.idx = 0

    def handle(self, text, parsed):
        if self.nlu.hasIntent(parsed, "GET_WEIBO"):
            slots = self.nlu.getSlots(parsed, 'GET_WEIBO')
            for slot in slots:
                if slot['name'] == 'user_person':
                    self.person = slot['normalized_word']
                    # 为杨超越定制
                    if self.person == "超越":
                        self.person = "杨超越"
                    self.playList = weibo.getInfo(self.person)
                    self.say("{}最近的一条微博发布于{}。{}".format(slot['normalized_word'], self.playList[0]['time'], self.playList[0]['content']))
        elif self.nlu.hasIntent(parsed, "NEXT_CONTENT"):
            if self.idx + 1 >= len(self.playList):
                self.say("已经是最后一条信息了")
            else:
                self.idx += 1
                self.say("{}发布于{}的一条微博。{}".format(self.person, self.playList[self.idx]['time'], self.playList[self.idx]['content']))
        elif self.nlu.hasIntent(parsed, 'LAST_CONTENT'):
            if self.idx - 1 <= 0:
                self.say("已经是第一条微博了")
            else:
                self.idx -= 1
                self.say("{}发布于{}的一条微博。{}".format(self.person, self.playList[self.idx]['time'], self.playList[self.idx]['content']))
        elif self.nlu.hasIntent(parsed, 'EXIT_WEIBO'):
            self.clearImmersive()
            self.say('已退出微博插件')
        else:
            self.say('没听懂你的意思呢，要退出微博，请说退出微博')

    def restore(self):
        pass

    def isValidImmersive(self, text, parsed):
        return any(self.nlu.hasIntent(parsed, intent) for intent in ['LAST_CONTENT', 'NEXT_CONTENT',
                                                                     'GET_WEIBO', 'EXIT_WEIBO'])

    def isValid(self, text, parsed):
        return unit.hasIntent(parsed, 'GET_WEIBO')

