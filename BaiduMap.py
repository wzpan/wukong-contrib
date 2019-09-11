# -*- coding: utf-8-*-
import json, jsonpath, re
import requests
from robot import config, logging
from robot.sdk.AbstractPlugin import AbstractPlugin

logger = logging.getLogger(__name__)
CHINESE_NUMNERS={'一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}

class Plugin(AbstractPlugin):

    IS_IMMERSIVE = True  # 这是个沉浸式技能
    SLUG = "BaiduMap"

    def __init__(self, con):
        super(Plugin, self).__init__(con)
        self.parsed = None
        self.routes = None

    def hasNumbers(self, inputString):
        return any(char.isnumeric() for char in inputString)

    def request(self, url, params):
        r = requests.get(url, params=params)
        content = r.text
        return json.loads(content)

    def getLatLng(self, app_key, checkPlace):
        #调出配置文件中的城市, 并找到出发点和目的地的经纬度
        city = config.get('location', '深圳')
        url_place = "http://api.map.baidu.com/place/v2/suggestion"
        params_place = {
            "query" : checkPlace,
            "region" : city,
            "city_limit" : "true",
            "output" : "json",
            "ak" : app_key,
        }
        res = self.request(url_place, params_place)
        if res:
            status = res["status"]
            if status == 0:
                if len(res['result']):
                    self.place = res['result'][0]["name"]
                    if not 'location' in res['result'][0]:
                        return "%f,%f" % (res['result'][1]["location"]['lat'], res['result'][1]["location"]['lng'])
                    else:
                        return "%f,%f" % (res['result'][0]["location"]['lat'], res['result'][0]["location"]['lng'])
                else:
                    self.say(u"找不到{}的经纬度，对不起！".format(checkPlace))
                    return
            else:
                logger.error(u"位置接口:" + res['message'])
                return
        else:
            logger.error(u"位置接口调用失败")
            return

    def getRoutes(self, app_key, origin, destination):
        url_direction = "http://api.map.baidu.com/direction/v2/transit"
        params_direction = {
            "origin" : origin,
            "destination" : destination,
            "ak" : app_key
        }
        res = self.request(url_direction, params_direction)
        if res:
            if res["status"] == 0:
                if len(res['result']['routes']) > 0:
                    taxiDuration = jsonpath.jsonpath(res, "$.[taxi].duration")[0]
                    taxiFee = jsonpath.jsonpath(res, "$.[taxi].detail.[total_price]")
                    result = jsonpath.jsonpath(res, "$..routes.*.duration")
                    busroutes = jsonpath.jsonpath(res, '$..routes..steps')
                    for route in range(len(busroutes)):
                        instruc = ''
                        for direction in range(len(busroutes[route])):
                            if busroutes[route][direction][0]['vehicle_info']['type'] == 3 and instruc == '':
                                instruc = re.sub(r'\([^)]*\)','',busroutes[route][direction][0]['instructions'])
                            elif busroutes[route][direction][0]['vehicle_info']['type'] == 3:
                                instruc = '{},接着{}'.format(instruc,re.sub(r'\([^)]*\)','',busroutes[route][direction][0]['instructions']))
                        result[route] = '{},这条路线约耗时{}分钟'.format(instruc, round(result[route]/60))
                    result.append('坐出租车的话需要{}分钟,白天大概要{}块，黑夜就要{}块'.format(round(taxiDuration/60), taxiFee[0], taxiFee[1]))
                    return result
                else:
                    self.say(u"找不到导航路线，对不起！", cache=True)
                    return
            else:
                logger.error(u"导航接口:" + res['message'])
                return
        else:
            logger.error(u"导航接口调用失败")
            return

    def handle(self, text, parsed):
        ##需在配置文件给百度地图的API
        profile = config.get()
        if self.SLUG not in profile or \
           'app_key' not in profile[self.SLUG] or \
           'origin' not in profile[self.SLUG]:
            self.say(u"你得在配置文件调整一下呀，哼！", cache=True)
            return

        if any(word in text for word in ['退出', '结束', '可以不用了', '不用','谢谢','谢啦']):
            self.clearImmersive()  # 去掉沉浸式
            if not self.routes:
                self.say('好的吧！不用就算了', cache=True)
            else:
                self.say('路上要小心哦！', cache=True)
        elif self.hasNumbers(text) and any(word in text for word in ['第', '条']) and self.routes:
            number = re.compile(r"(\d+\.?\d*|[一二三四五六七八九零十百千万亿]+|[0-9]+[,]*[0-9]+.[0-9]+)")
            routeNumber = number.findall(text)[0]
            routeNumber = CHINESE_NUMNERS[routeNumber]
            if routeNumber < len(self.routes):
                logger.info('{} 选了{}条'.format(text, routeNumber))
                self.say('这是第{}条:{}, 还想要听别的路线吗？'.format(routeNumber, self.routes[routeNumber-1]))
            else:
                self.say('都说了只有{}条路线啦，哼！'.format(len(self.routes)-1), cache=True, onCompleted=lambda: self.con.doResponse(self.activeListen()))
        elif any(word in text for word in ['打车', '出租车', '计程车']) and self.routes:
            self.say('{}, 超贵的，对不对？还想听别的路线吗？'.format(self.routes[-1]))
        else:
            slots = self.nlu.getSlots(self.parsed, 'FIND_DIRECTION')  # 取出所有词槽
            # 使用if and all来检查slots字典里是否有出发和目的地，多轮询问直到得到出发点和目的地
            if not all(key in [item['name'] for item in slots] for key in {'user_start', 'user_to'}):
                self.say("{}".format(self.nlu.getSay(self.parsed,'FIND_DIRECTION')), cache=True, onCompleted=lambda: self.con.doResponse(self.activeListen()))
            else:
                start_Point = self.nlu.getSlotWords(self.parsed, 'FIND_DIRECTION', 'user_start')
                to_Point = self.nlu.getSlotWords(self.parsed, 'FIND_DIRECTION', 'user_to')

                # 如果出发点是家里则调出配置文件的经纬度
                app_key = profile[self.SLUG]['app_key']
                destination = self.getLatLng(app_key, to_Point)
                if any(word in start_Point for word in [u"我的家", u"家里", u"我家", u"俺家", u"家"]):
                    origin = profile[self.SLUG]['origin']
                else:
                    origin = self.getLatLng(app_key, start_Point)
                self.routes = self.getRoutes(app_key, origin, destination)

                # 播放第一条较方便的路线
                self.say('共找到了{}条路线，这是第一条:{}, 想听别的路线还是打车信息？'.format(len(self.routes)-1, self.routes[0]))

    def isValidImmersive(self, text, parsed):
        return self.nlu.hasIntent(self.parsed, 'FIND_DIRECTION') or \
            any(word in text for word in ['退出', '结束', '可以不用了', '不用','谢谢','谢啦']) or \
            (self.hasNumbers(text) and any(word in text for word in ['第', '条'])) or \
            any(word in text for word in ['打车', '出租车', '计程车'])

    def isValid(self, text, parsed):
        return self.nlu.hasIntent(self.parsed, 'FIND_DIRECTION')
