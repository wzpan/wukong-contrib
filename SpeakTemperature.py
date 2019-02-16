# -*- coding: utf-8-*-
# 获取室温插件
import time
import socket
import subprocess
from robot import config, logging
from robot.sdk.AbstractPlugin import AbstractPlugin

logger = logging.getLogger(__name__)

class Plugin(AbstractPlugin):

    SLUG = "speak_temperature"

    def getTempperature(self, temp):
        import RPi.GPIO as GPIO
        data = []
        j = 0
        channel =0 #输入GPIO号
        channel = int(temp)
        GPIO.setmode(GPIO.BCM)
        time.sleep(1)
        GPIO.setup(channel, GPIO.OUT)
        GPIO.output(channel, GPIO.LOW)
        time.sleep(0.02)
        GPIO.output(channel, GPIO.HIGH)
        GPIO.setup(channel, GPIO.IN)

        while GPIO.input(channel) == GPIO.LOW:
          continue
        while GPIO.input(channel) == GPIO.HIGH:
          continue

        while j < 40:
          k = 0
          while GPIO.input(channel) == GPIO.LOW:
            continue
          while GPIO.input(channel) == GPIO.HIGH:
            k += 1
            if k > 100:
              break
          if k < 8:
            data.append(0)
          else:
            data.append(1)
          j += 1
        logger.info("sensor is working.")
        logger.debug(data)
        humidity_bit = data[0:8]
        humidity_point_bit = data[8:16]
        temperature_bit = data[16:24]
        temperature_point_bit = data[24:32]
        check_bit = data[32:40]
        humidity = 0
        humidity_point = 0
        temperature = 0
        temperature_point = 0
        check = 0

        for i in range(8):
          humidity += humidity_bit[i] * 2 ** (7-i)
          humidity_point += humidity_point_bit[i] * 2 ** (7-i)
          temperature += temperature_bit[i] * 2 ** (7-i)
          temperature_point += temperature_point_bit[i] * 2 ** (7-i)
          check += check_bit[i] * 2 ** (7-i)

        tmp = humidity + humidity_point + temperature + temperature_point

        if check == tmp:
           logger.info("temperature :", temperature, "*C, humidity :", humidity, "%")
           return "主人，当前家中温度"+str(temperature)+"摄氏度，湿度:百分之"+str(humidity)
        else:
          #return "抱歉主人，传感器犯了点小错"
          getTempperature(channel)
        GPIO.cleanup()

    def handle(self, text, parsed):
        profile = config.get()
        if self.SLUG not in profile or \
           'gpio' not in profile[self.SLUG]:
            self.say('DHT11配置有误，插件使用失败', cache=True)
            return
        if 'gpio' in profile[self.SLUG]:
            temp = profile[self.SLUG]['gpio']
        else:
            temp = profile['gpio']
        try:
            temper = getTempperature(temp)
            logger.debug('getTempperature: ', temper)
            self.say(temper)
        except Exception as e:
            logger.critical("配置异常 {}".format(e))
            self.say('抱歉，我没有获取到湿度', cache=True)

    def isValid(self, text, parsed):
        try:
            import RPi.GPIO as GPIO
            return any(word in text for word in [u"室温", u"家中温度"])
        except Exception:
            return False
