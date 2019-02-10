# -*- coding: utf-8-*-
# 树莓派状态插件
import os
import logging

SLUG = "pi_status"

def getCPUtemperature(logger, mic):
    result = 0.0
    try:
        tempFile = open("/sys/class/thermal/thermal_zone0/temp")
        res = tempFile.read()
        result = float(res) / 1000
    except:
        logger.error(e)
        mic.say(u'抱歉，无法获取处理器温度', cache=True, plugin=__name__)
    return result

def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i == 2:
            return (line.split()[1:4])

def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i == 2:
            return (line.split()[1:5])

def getPiStatus(logger, mic):
    result = {'cpu_tmp': 0.0,
              'ram_total': 0, 'ram_used': 0, 'ram_percentage': 0,
              'disk_total': '0.0', 'disk_used': '0.0','disk_percentage': 0}

    result['cpu_tmp'] = getCPUtemperature(logger, mic)
    ram_stats = getRAMinfo()
    result['ram_total'] = int(ram_stats[0]) / 1024
    result['ram_used'] = int(ram_stats[1]) / 1024
    result['ram_percentage'] = int(result['ram_used'] * 100 / result['ram_total'])
    disk_stats = getDiskSpace()
    result['disk_total'] = disk_stats[0]
    result['disk_used'] = disk_stats[1]
    result['disk_percentage'] = disk_stats[3].split('%')[0]
    return result

def handle(text, mic, parsed=None):
    logger = logging.getLogger(__name__)
    try:
        status = getPiStatus(logger, mic)
        mic.say(u'处理器温度' + str(status['cpu_tmp']) + u'度,内存使用百分之' + str(status['ram_percentage']) + u',存储使用百分之' + str(status['disk_percentage']), plugin=__name__)
    except Exception as e:
        logger.error(e)
        mic.say(u'抱歉，我没有获取到树莓派状态', cache=True, plugin=__name__)

def isValid(text, parsed=None):
    return any(word in text for word in [u"树莓派状态", u"状态", u"运行状态"])
