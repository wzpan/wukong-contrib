# -*- coding: utf-8-*-
# 获取IP插件
import time
import socket
import subprocess
from robot import logging
from robot.sdk.AbstractPlugin import AbstractPlugin

logger = logging.getLogger(__name__)

class Plugin(AbstractPlugin):

    SLUG = "speak_ip"

    def getLocalIP(self):
        ip = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('114.114.114.114', 0))
            ip = s.getsockname()[0]
        except:
            name = socket.gethostname()
            ip = socket.gethostbyname(name)
        if ip.startswith("127."):
            cmd = '''/sbin/ifconfig | grep "inet " | cut -d: -f2 | awk '{print $1}' | grep -v "^127."'''
            a = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            a.wait()
            out = a.communicate()
            ip = out[0].strip().split("\n")  # 所有的列表
            if len(ip) == 1 and ip[0] == "" or len(ip) == 0:
                return False
            ip = '完毕'.join(ip)
        return ip

    def handle(self, text, parsed):
        try:
            count = 0
            while True:
                ip = self.getLocalIP()
                logger.debug('getLocalIP: ', ip)
                if ip == False:
                    self.say('正在获取中', cache=True)
                else:
                    count += 1
                    ip += '完毕'
                    self.say(ip, cache=True)
                if count == 1:
                    break
                time.sleep(1)
        except Exception as e:
            logger.error(e)
            self.say('抱歉，我没有获取到地址', cache=True)

    def isValid(self, text, parsed):
        return any(word in text for word in [u"IP", u"网络地址"])
