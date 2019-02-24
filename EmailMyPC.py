# -*- coding: utf-8-*-
from robot import config, logging
from robot.utils import sendEmail
from robot.sdk.AbstractPlugin import AbstractPlugin

logger = logging.getLogger(__name__)

class Plugin(AbstractPlugin):

    SLUG = "emailmypc"

    def shutdown(self, input):
        if input is not None and any(word in input for word in [u"确认", u"好", u"是", u"OK"]):
            sendEmail("#shutdown", "", "", self.pc_email, self.address, self.address, self.password, self.smtp_server,  self.smtp_port)
            self.say('已发送关机指令', cache=True)
        else:
            self.say('已取消', cache=True)

    def sendHotKey(self, input):
        if input is not None and any(word in input for word in [u"确认", u"好", u"是", u"OK"]):
            sendEmail("#button", self.button, "", self.pc_email, self.address, self.address, self.password, self.smtp_server,  self.smtp_port)
            self.say('已发送快捷键', cache=True)
        else:
            self.say('已取消', cache=True)

    def command(self, input):
        if input is not None and any(word in input for word in [u"确认", u"好", u"是", u"OK"]):
            sendEmail("#cmd", self.cmd, "", self.pc_email, self.address, self.address, self.password, self.smtp_server,  self.smtp_port)
            self.say('已发送指令', cache=True)
        else:
            self.say('已取消', cache=True)

    def handle(self, text):
        profile = config.get()
        if 'email' not in profile or ('enable' in profile['email']
                                      and not profile['email']):
            self.say(u'请先配置好邮箱功能', cache=True)
            return
        self.address = profile['email']['address']
        self.password = profile['email']['password']
        self.smtp_server = profile['email']['smtp_server']
        self.smtp_port = profile['email']['smtp_port']
        if self.SLUG not in profile or \
            'pc_email' not in profile[self.SLUG]:
            self.say('远控插件配置有误，插件使用失败', cache=True)
            return
        self.pc_email = profile[self.SLUG]['pc_email']
        try:
            if any(word in text for word in [u"关机", u"关电脑", u"关闭电脑"]):
                self.say('即将关闭电脑，请在滴一声后进行确认', cache=True, onCompleted=lambda: self.shutdown(self.activeListen()))
            elif any(word in text for word in [u"屏幕", u"截图"]):
                sendEmail("#screen", "", "", self.pc_email, self.address, self.address, self.password, self.smtp_server,  self.smtp_port)
                self.say('已发送截图指令，请查看您的邮箱', cache=True)
            elif any(word in text for word in [u"摄像头"]):
                sendEmail("#cam", "", "", self.pc_email, self.address, self.address, self.password, self.smtp_server,  self.smtp_port)
                self.say('已发送拍照指令，请查看您的邮箱', cache=True)
            elif any(word in text for word in [u"快捷键"]):
                if self.SLUG not in profile or \
                    'button' not in profile[self.SLUG]:
                    self.say('您还未设置快捷键', cache=True)
                    return
                self.button = profile[self.SLUG]['button']
                self.say('即将发送快捷键%s，请在滴一声后进行确认' % self.button, cache=True, onCompleted=lambda: self.sendHotKey(self.activeListen()))
            elif any(word in text for word in [u"命令", u"指令"]):
                if self.SLUG not in profile or \
                    'cmd' not in profile[self.SLUG]:
                    self.say('您还未设置指令', cache=True)
                    return
                self.cmd = profile[self.SLUG]['cmd']
                self.say('即将发送指令%s，请在滴一声后进行确认' % self.cmd, cache=True, onCompleted=lambda: self.command(self.activeListen()))            
        except Exception as e:
            logger.error(e)
            self.say('抱歉，指令发送失败', cache=True)

    def isValid(self, text, parsed=None):
        return any(word in text for word in [u"关电脑", u"关闭电脑", u"屏幕", u"截图", u"摄像头", u"快捷键", u"命令", u"指令"])
