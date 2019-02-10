# -*- coding: utf-8-*-
# 关闭系统插件
import logging
import sys
import time
import subprocess

SLUG = "halt"

def onAsk(input, mic):
    try:
        if input is not None and any(word in input for word in [u"确认", u"好", u"是", u"OK"]):
            mic.say('授权成功，开始进行相关操作', cache=True, plugin=__name__)
            time.sleep(3)
            subprocess.Popen("shutdown -h now", shell=True, plugin=__name__)
            return
        mic.say('授权失败，操作已取消，请重新尝试', cache=True, plugin=__name__)
    except Exception as e:
        logger.error(e)
        mic.say('抱歉，关闭系统失败', cache=True, plugin=__name__)

def handle(text, mic, parsed=None):
    logger = logging.getLogger(__name__)   
    mic.say('将要关闭系统，请在滴一声后进行确认，授权相关操作', cache=True, plugin=__name__, onCompleted=lambda: onAsk(mic.activeListen(MUSIC=True), mic))
    

def isValid(text, parsed=None):
    return any(word in text for word in [u"关机", u"关闭系统"])
