# -*- coding: utf-8-*-
# 重启系统插件
import time
import subprocess
from robot import logging
from robot.sdk.AbstractPlugin import AbstractPlugin

logger = logging.getLogger(__name__)

class Plugin(AbstractPlugin):

    SLUG = 'reboot'

    def onConfirm(self, input):
        if input is not None and any(word in input for word in [u"确认", u"好", u"是", u"OK"]):
            self.say('授权成功，开始进行相关操作', cache=True)
            time.sleep(3)
            subprocess.Popen("reboot -f", shell=True)
            return
        self.say('授权失败，操作已取消，请重新尝试', cache=True)

    def handle(self, text, parsed):
        try:
            self.say('将要重新启动系统，请在滴一声后进行确认，授权相关操作', cache=True, onCompleted=self.onConfirm(self.activeListen()))
        except Exception as e:
            logger.error(e)
            self.say('抱歉，重新启动系统失败', cache=True)

    def isValid(self, text, parsed):
        return any(word in text for word in [u"重启", u"重新启动"])
