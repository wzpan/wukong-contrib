# -*- coding: utf-8-*-
# 重启系统插件
import logging
import time
import subprocess


SLUG = "reboot"

def handle(text, mic, parsed=None):
    logger = logging.getLogger(__name__)
    try:
        mic.say('将要重新启动系统，请在滴一声后进行确认，授权相关操作', cache=True, plugin=__name__)
        input = mic.activeListen()
        if input is not None and any(word in input for word in [u"确认", u"好", u"是", u"OK"]):
            mic.say('授权成功，开始进行相关操作', cache=True, plugin=__name__)
            time.sleep(3)
            subprocess.Popen("reboot -f", shell=True)
            return
        mic.say('授权失败，操作已取消，请重新尝试', cache=True, plugin=__name__)
    except Exception as e:
        logger.error(e)
        mic.say('抱歉，重新启动系统失败', cache=True, plugin=__name__)

def isValid(text, parsed=None, immersiveMode=None):
    return any(word in text for word in [u"重启", u"重新启动"])
