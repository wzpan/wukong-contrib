# -*- coding: utf-8-*-
# 智米风扇控制插件
import sys
import socket
import subprocess
import re
from robot import config, logging
from robot.sdk.AbstractPlugin import AbstractPlugin

logger = logging.getLogger(__name__)

WORDS = ["FENGSHANG"]
SLUG = "smart_mi_fan"
smart_mi_fan = None

class FanStatus:
    """Container for status reports from the fan."""
    def __init__(self, data):
        #['temp_dec', 'humidity', 'angle', 'speed', 'poweroff_time', 'power', 'ac_power', 'battery', 'angle_enable', 'speed_level', 'natural_level', 'child_lock', 'buzzer', 'led_b']
        #[232, 46, 30, 298, 0, 'on', 'off', 98, 'off', 1, 0, 'off', 'on', 1]
        self.data = data

    @property
    def temp_dec(self):
        return self.data[0]
    @property
    def humidity(self):
        return self.data[1]
    @property
    def angle(self):
        return self.data[2]
    @property
    def speed(self):
        return self.data[3]
    @property
    def poweroff_time(self):
        return self.data[4]
    @property
    def power(self):
        return self.data[5]
    @property
    def ac_power(self):
        return self.data[6]
    @property
    def battery(self):
        return self.data[7]
    @property
    def angle_enable(self):
        return self.data[8]
    @property
    def speed_level(self):
        return self.data[9]
    @property
    def natural_level(self):
        return self.data[10]
    @property
    def child_lock(self):
        return self.data[11]
    @property
    def buzzer(self):
        return self.data[12]
    @property
    def led_b(self):
        return self.data[13]


dictnum ={
    '零':0, '一':1, '二':2, '三':3, '四':4,
    '五':5, '六':6, '七':7, '八':8, '九':9,
    '两':2, '十':10, '百':12}


def getNumicForCNDigit(a):
    count = len(a)-1
    result = 0
    tmp = 0

    while count >= 0:
        tmpChr = a[count:count+1]
        tmpNum = 0
        if tmpChr.isdigit():  # 防止大写数字中夹杂阿拉伯字母
            tmpNum=int(tmpChr)
        elif tmpChr in dictnum:
            tmpNum = dictnum[tmpChr]
        else:
            count += 1
            continue
        if tmpNum >10:  # 获取0的个数
            tmp=tmpNum-10
        # 如果是个位数
        else:
            if tmp == 0:
                result+=tmpNum
            else:
                result+=pow(10,tmp)*tmpNum
            tmp = tmp+1
        count -= 1
    return result



def get_prop(fan):
    prop = fan.send("get_prop", ["temp_dec","humidity","angle","speed","poweroff_time","power","ac_power","battery","angle_enable","speed_level","natural_level","child_lock","buzzer","led_b"])
    return FanStatus(prop)

class Plugin(AbstractPlugin):

    def response(self, fan, angle, prop, text):
        """ Response to smart mi fan command """
        text_utf8 = text
        # 启动自然风正则式
        pattern_start_nature_wind = re.compile(r'[\u4e00-\u9fa5]*(开|启)*[\u4e00-\u9fa5]*自然风')
        # 关闭自然风正则式
        pattern_end_nature_wind = re.compile(r'[\u4e00-\u9fa5]*(退|关|结束)[\u4e00-\u9fa5]*自然风')
        # 开始摇头
        pattern_start_shake_head = re.compile(r'[\u4e00-\u9fa5]*(开|启)*[\u4e00-\u9fa5]*摇头')
        # 结束摇头正则式
        pattern_end_shake_head = re.compile(r'[\u4e00-\u9fa5]*(退|关|结束|停)[\u4e00-\u9fa5]*摇头')
        # 定时关闭正则式
        pattern_poweroff_time = re.compile(r'^([\d]*)([\u4e00-\u9fa5]*)([个]?)(小时|分钟|秒)([\u4e00-\u9fa5]?后[\u4e00-\u9fa5]*关[\u4e00-\u9fa5]*)')
        # 加大风量正则式
        pattern_speed_up = re.compile(r'[\u4e00-\u9fa5]*[大|高|快|多]+[\u4e00-\u9fa5]*风')
        # 减小风量正则式
        pattern_speed_down = re.compile(r'[\u4e00-\u9fa5]*[小|低|慢|少]+[\u4e00-\u9fa5]*风')
        is_on = prop.power == 'on'
        oscillating = prop.natural_level != 0
        if oscillating:
            level = prop.natural_level
        else:
            level = prop.speed_level
        if pattern_end_nature_wind.match(text_utf8):
            if not is_on:
                self.say('请先打开风扇')
                return
            if oscillating:
                fan.send('set_speed_level', [level])
                self.say('关闭自然风')            
                oscillating = False
            else:
                self.say('自然风未开启')
        elif pattern_start_nature_wind.match(text_utf8):
            if not is_on:
                self.say('请先打开风扇')
                return
            if not oscillating:
                fan.send('set_natural_level', [level])
                self.say('启动自然风')            
                oscillating = True
            else:
                self.say('自然风已开启')
        elif pattern_end_shake_head.match(text_utf8):
            if not is_on:
                self.say('请先打开风扇')
                return
            fan.send('set_angle_enable', ['off'])
            self.say('关闭摇头')        
        elif pattern_start_shake_head.match(text_utf8):
            if not is_on:
                self.say('请先打开风扇')
                return
            fan.send('set_angle', [angle])
            self.say('开始摇头')        
        elif pattern_speed_up.match(text_utf8):
            if not is_on:
                self.say('请先打开风扇')
                return
            if level >= 4:
                self.say('风量已开到最大')
                return
            if oscillating:
                fan.send('set_natural_level', [level+1])
            else:
                fan.send('set_speed_level', [level+1])
            self.say('风扇风量已加大')
        elif pattern_speed_down.match(text_utf8):
            if not is_on:
                self.say('请先打开风扇')
                return
            if oscillating:
                fan.send('set_natural_level', [level-1])
            else:
                fan.send('set_speed_level', [level-1])
            self.say('风扇风量已减小')
        elif pattern_poweroff_time.match(text_utf8):
            if not is_on:
                self.say('请先打开风扇')
                return
            m = pattern_poweroff_time.search(text_utf8)
            t = m.group(1)
            t_cn = m.group(2)
            if t == '' and t_cn == '':
                self.say('抱歉，我听不清预约时间信息，请再试试')
                return
            if t != '':
                try:
                    time = int(t)
                except:
                    self.say('抱歉，我听不清预约时间信息，请再试试')
                    return
            else:
                t_cn = t_cn.replace('个', '').strip()
                time = getNumicForCNDigit(t_cn)
            original_time = time
            unit = '秒'
            if '小时' in text:
                time = time * 3600
                unit = '小时'
            elif '分钟' in text:
                time = time * 60
                unit = '分钟'
            fan.send('set_poweroff_time', [time])
            self.say('收到，%d%s后为您关闭风扇' % (original_time, unit))
        elif any(ext in text for ext in [u"开", u"启动"]):
            if not is_on:
                fan.send('set_power', ['on'])
            self.say('风扇已开启')
        elif '关闭' in text:
            if not is_on:
                self.say('请先打开风扇')
                return
            fan.send('set_power', ['off'])
            self.say('风扇已关闭')        
        else:
            self.say("没听懂您的风扇指令呢，再说一次好吗？")


    def handle(self, text, parsed):
        global smart_mi_fan
        # get config
        angle = 60
        profile = config.get()
        if self.SLUG not in profile or \
           'host' not in profile[self.SLUG] or \
           'token' not in profile[self.SLUG]:
            self.say('智米风扇插件配置有误，插件使用失败')
            return
        host = profile[self.SLUG]['host']
        token = profile[self.SLUG]['token']
        if 'angle' in profile[self.SLUG]:
            angle = profile[self.SLUG]['angle']
        if smart_mi_fan is None:
            try:
                import miio # import again
                smart_mi_fan = miio.device.Device(host, token)
            except Exception as e:
                logger.error(e)
                self.say('智米风扇连接失败')
                return
        prop = get_prop(smart_mi_fan)
        self.response(smart_mi_fan, angle, prop, text)

    def isValid(self, text, parsed):
        try:
            import miio
            return any(word in text for word in [u"风扇", u"自然风", u"风量", u"风力", u"风速", u"摇头"])
        except:
            return False
