# -*- coding: utf-8-*-
# author: wzpan
# 天气插件 v 2.0
import requests
import json
from robot import config, logging
from robot.sdk import unit
from robot.sdk.AbstractPlugin import AbstractPlugin

logger = logging.getLogger(__name__)

class Plugin(AbstractPlugin):

    SLUG = "weather"

    def analyze_today(self, weather_code, suggestion):
        """ analyze today's weather """
        weather_code = int(weather_code)
        if weather_code <= 8:
            if u'适宜' in suggestion:
                return u'今天天气不错，空气清新，适合出门运动哦'
            else:
                return u'空气质量比较一般，建议减少出行'
        elif weather_code in range(10, 16):
            return u'主人，出门记得带伞哦'
        elif weather_code in range(16, 19) or \
        weather_code in range(25, 30) or \
        weather_code in range(34, 37):
            return u'极端天气来临，尽量待屋里陪我玩吧'
        elif weather_code == 38:
            return u'天气炎热，记得多补充水分哦'
        elif weather_code == 37:
            return u'好冷的天，记得穿厚一点哦'
        else:
            return u''


    def fetch_weather(self, api, key, location):
        body = {
            'key': key,
            'location': location
        }
        result = requests.get(api, params=body, timeout=3)
        res = json.loads(result.text, encoding='utf-8')
        return res


    def get_location(self, parsed):
        """ 获取位置 """
        slots = unit.getSlots(parsed, 'USER_WEATHER')
        # 如果 query 里包含了地点，用该地名作为location
        for slot in slots:
            if slot['name'] == 'user_loc':
                return slot['normalized_word']
        # 如果不包含地点，但配置文件指定了 location，则用 location
        else:
            return config.get('location', '深圳')


    def handle(self, text, parsed):
        # get config
        key = config.get('/{}/key'.format(self.SLUG), '')
        location = self.get_location(parsed)
        WEATHER_API = 'https://api.seniverse.com/v3/weather/daily.json'
        SUGGESTION_API = 'https://api.seniverse.com/v3/life/suggestion.json'
        try:
            weather = self.fetch_weather(WEATHER_API, key, location)
            logger.debug("Weather report: ", weather)
            if 'results' in weather:
                daily = weather['results'][0]['daily']
                days = set([])
                day_text = [u'今天', u'明天', u'后天']
                for word in day_text:
                    if word in text:
                        days.add(day_text.index(word))
                if not any(word in text for word in day_text):
                    days = set([0, 1, 2])
                responds = u'%s天气：' % location
                analyze_res = ''
                for day in days:
                    responds += u'%s：%s，%s到%s摄氏度。' % (day_text[day], daily[day]['text_day'], daily[day]['low'], daily[day]['high'])
                    if day == 0:
                        suggestion = self.fetch_weather(SUGGESTION_API, key, location)
                        if 'results' in suggestion:
                            suggestion_text = suggestion['results'][0]['suggestion']['sport']['brief']
                            analyze_res = self.analyze_today(daily[day]['code_day'], suggestion_text)
                responds += analyze_res
                self.say(responds, cache=True)
            else:
                self.say('抱歉，我获取不到天气数据，请稍后再试', cache=True)
        except Exception as e:
            logger.error(e)
            self.say('抱歉，我获取不到天气数据，请稍后再试', cache=True)


    def isValid(self, text, parsed):
        return unit.hasIntent(parsed, 'USER_WEATHER')


