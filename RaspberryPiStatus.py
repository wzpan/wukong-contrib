# -*- coding: utf-8-*-
# 树莓派状态插件
import os
from robot import logging
from robot.sdk.AbstractPlugin import AbstractPlugin

logger = logging.getLogger(__name__)

class Plugin(AbstractPlugin):

    SLUG = "pi_status"

    def getCPUtemperature(self):
        result = 0.0
        try:
            tempFile = open("/sys/class/thermal/thermal_zone0/temp")
            res = tempFile.read()
            result = float(res) / 1000
        except:
            self.say(u'抱歉，无法获取处理器温度', cache=True)
        return result

    def getRAMinfo(self):
        p = os.popen('free')
        i = 0
        while 1:
            i = i + 1
            line = p.readline()
            if i == 2:
                return (line.split()[1:4])

    def getDiskSpace(self):
        p = os.popen("df -h /")
        i = 0
        while 1:
            i = i +1
            line = p.readline()
            if i == 2:
                return (line.split()[1:5])

    def getPiStatus(self):
        result = {'cpu_tmp': 0.0,
                  'ram_total': 0, 'ram_used': 0, 'ram_percentage': 0,
                  'disk_total': '0.0', 'disk_used': '0.0','disk_percentage': 0}

        result['cpu_tmp'] = self.getCPUtemperature()
        ram_stats = self.getRAMinfo()
        result['ram_total'] = int(ram_stats[0]) / 1024
        result['ram_used'] = int(ram_stats[1]) / 1024
        result['ram_percentage'] = int(result['ram_used'] * 100 / result['ram_total'])
        disk_stats = self.getDiskSpace()
        result['disk_total'] = disk_stats[0]
        result['disk_used'] = disk_stats[1]
        result['disk_percentage'] = disk_stats[3].split('%')[0]
        return result

    def handle(self, text, parsed):
        try:
            status = self.getPiStatus()
            self.say(u'处理器温度' + str(status['cpu_tmp']) + u'度,内存使用百分之' + str(status['ram_percentage']) + u',存储使用百分之' + str(status['disk_percentage']))
        except Exception as e:
            logger.error(e)
            self.say(u'抱歉，我没有获取到树莓派状态', cache=True)

    def isValid(self, text, parsed):
        return any(word in text for word in [u"树莓派状态", u"状态", u"运行状态"])
