# -*- coding: utf-8-*-
import sys
import logging
from robot import config
from robot.utils import sendEmail

SLUG = "emailmypc"

def shutdown(input, mic):
    if input is not None and any(word in input for word in [u"确认", u"好", u"是", u"OK"]):
        sendEmail("#shutdown", "", "", pc_email, address, address, password, smtp_server, smtp_port)
        mic.say('已发送关机指令', cache=True, plugin=__name__)
    else:
        mic.say('已取消', cache=True, plugin=__name__)

def sendHotKey(input, mic):
    if input is not None and any(word in input for word in [u"确认", u"好", u"是", u"OK"]):
        sendEmail("#button", button, "", pc_email, address, address, password, smtp_server, smtp_port)
        mic.say('已发送快捷键', cache=True, plugin=__name__)
    else:
        mic.say('已取消', cache=True, plugin=__name__)

def command(input, mic):
    if input is not None and any(word in input for word in [u"确认", u"好", u"是", u"OK"]):
        sendEmail("#cmd", cmd, "", pc_email, address, address, password, smtp_server, smtp_port)
        mic.say('已发送指令', cache=True, plugin=__name__)
    else:
        mic.say('已取消', cache=True, plugin=__name__)

def handle(text, mic):
    logger = logging.getLogger(__name__)
    profile = config.get()
    if 'email' not in profile or ('enable' in profile['email']
                                  and not profile['email']):
        mic.say(u'请先配置好邮箱功能', cache=True, plugin=__name__)
        return
    address = profile['email']['address']
    password = profile['email']['password']
    smtp_server = profile['email']['smtp_server']
    smtp_port = profile['email']['smtp_port']
    if SLUG not in profile or \
        'pc_email' not in profile[SLUG]:
        mic.say('远控插件配置有误，插件使用失败', cache=True, plugin=__name__)
        return
    pc_email = profile[SLUG]['pc_email']
    try:
        if any(word in text for word in [u"关机", u"关电脑", u"关闭电脑"]):
            mic.say('即将关闭电脑，请在滴一声后进行确认', cache=True, plugin=__name__, onCompleted=lambda: shutdown(mic.activeListen(), mic))                        
        elif any(word in text for word in [u"屏幕", u"截图"]):
            sendEmail("#screen", "", "", pc_email, address, address, password, smtp_server, smtp_port)
            mic.say('已发送截图指令，请查看您的邮箱', cache=True, plugin=__name__)
        elif any(word in text for word in [u"摄像头"]):
            sendEmail("#cam", "", "", pc_email, address, address, password, smtp_server, smtp_port)
            mic.say('已发送拍照指令，请查看您的邮箱', cache=True, plugin=__name__)
        elif any(word in text for word in [u"快捷键"]):
            if SLUG not in profile or \
                'button' not in profile[SLUG]:
                mic.say('您还未设置快捷键', cache=True, plugin=__name__)
                return
            button = profile[SLUG]['button']
            mic.say('即将发送快捷键%s，请在滴一声后进行确认' % button, cache=True, plugin=__name__, onCompleted=lambda: sendHotKey(mic.activeListen(), mic))
        elif any(word in text for word in [u"命令", u"指令"]):
            if SLUG not in profile or \
                'cmd' not in profile[SLUG]:
                mic.say('您还未设置指令', cache=True, plugin=__name__)
                return
            cmd = profile[SLUG]['cmd']
            mic.say('即将发送指令%s，请在滴一声后进行确认' % cmd, cache=True, plugin=__name__, onCompleted=lambda: command(mic.activeListen(), mic))            
    except Exception as e:
        logger.error(e)
        mic.say('抱歉，指令发送失败', cache=True, plugin=__name__)

def isValid(text, parsed=None, immersiveMode=None):
    return any(word in text for word in [u"关电脑", u"关闭电脑", u"屏幕", u"截图", u"摄像头", u"快捷键", u"命令", u"指令"])
