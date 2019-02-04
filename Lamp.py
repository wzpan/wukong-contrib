# -*- coding: utf-8-*-
# 台灯控制
import os
import logging

SLUG="Lamp"

def handle(text, mic, profile, wxbot=None):

    logger = logging.getLogger(__name__)
    # get config
    pin=profile[SLUG]['pin']
    wiringpi.wiringPiSetupPhys()
    wiringpi.pinMode(pin,1)

    if any(word in text for word in [u"打开",u"开启"]):
        wiringpi.digitalWrite(pin,0)
        mic.say("好的，已经打开台灯")
    elif any(word in text for word in [u"关闭",u"关掉",u"熄灭"]):
        wiringpi.digitalWrite(pin,1)
        mic.say("好的，已经关闭台灯")
    return True


def isValid(text):
    try:
        import wiringpi
        return u"台灯" in text
    except Exception:
        return False
