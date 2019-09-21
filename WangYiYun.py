# -*- coding: utf-8-*-
import shutil
import re
import math
import time
from random import shuffle
from robot.sdk.AbstractPlugin import AbstractPlugin
from robot.Player import MusicPlayer
from robot import config, logging, constants
from sdk import NetEaseApi

logger = logging.getLogger(__name__)
CN_NUM = {
    '〇' : 0, '一' : 1, '二' : 2, '三' : 3, '四' : 4, '五' : 5, '六' : 6, '七' : 7, '八' : 8, '九' : 9, '零' : 0,
    '壹' : 1, '贰' : 2, '叁' : 3, '肆' : 4, '伍' : 5, '陆' : 6, '柒' : 7, '捌' : 8, '玖' : 9, '貮' : 2, '两' : 2,
}
CN_UNIT = {
    '十' : 10,
    '拾' : 10,
    '百' : 100,
    '佰' : 100,
    '千' : 1000,
    '仟' : 1000,
    '万' : 10000,
    '萬' : 10000,
    '亿' : 100000000,
    '億' : 100000000,
    '兆' : 1000000000000,
}
class WangYiYunPlayer(MusicPlayer):
    """
    给网易云播放器插件使用的，
    在 MusicPlayer 的基础上支持登陆和外接网易云API，返回相关信息。
    """
    SLUG = 'WangYiYunPlayer'

    def __init__(self, account, md5pass, playlist, plugin, **kwargs):
        super(WangYiYunPlayer, self).__init__(playlist, plugin, **kwargs)
        self.account = account
        self.md5pass = md5pass
        self.userid = None
        self.nickname = None
        self.api = NetEaseApi.NetEase()
        self.playlist = None
        self.multi_playlists = None
        self.list_idx = None

        ## 首次登陆则需发起请求获取cookies，cookies过期则需发起请求
        if len(self.api.session.cookies) == 0:
            self.login()
            self.daily_checkin()
        else:
            self.userid = config.get('/' + self.plugin.SLUG + '/userid')
            self.nickname = config.get('/' + self.plugin.SLUG + '/nickname')
            self.daily_checkin()

    def play(self):
        logger.debug('WangYiYunPlayer play')
        ##### 因为MusicPlayer对象的Play和Next方法是假定self.playlist的时效性是永久，因此重构play方法来检查playlist的时效性
        if time.time() - self.playlist[self.idx]['expires'] - self.playlist[self.idx]['get_time'] >= 0:
            self.refresh_urls()

        path = self.playlist[self.idx]['mp3_url']
        if 'song/media/outer' in path:
            logger.info('{}--{}怀疑未获取到版权, 你可以试试用"play {}"命令试试看~'.format(self.playlist[self.idx]['artist'], self.playlist[self.idx]['song_name'], self.playlist[self.idx]['mp3_url']))
            self.next()
        else:
            logger.info('目前播放的歌曲是{}, 歌手是{}'.format(self.playlist[self.idx]['song_name'], self.playlist[self.idx]['artist']))
            super(MusicPlayer, self).stop()
            super(MusicPlayer, self).play(path, False, self.next)

    def next(self):
        logger.debug('WangYiYunPlayer next')
        super(MusicPlayer, self).stop()
        self.idx = (self.idx+1) % len(self.playlist)
        self.play()

    def login(self):
        resp = self.api.login(self.account, self.md5pass)
        if resp["code"] == 200:
            self.userid = resp["account"]["id"]
            self.nickname = resp["profile"]["nickname"]
            profile = config.get()
            if 'userid' not in profile[self.plugin.SLUG] and 'nickname' not in profile[self.plugin.SLUG]:
                temp = open('add_info', 'w')
                with open(constants.getConfigPath(), 'r') as f:
                    for line in f:
                        if line.startswith('    md5pass'):
                            line = line + "    userid: \'" + str(self.userid) + "\'\n    nickname: \'" + str(self.nickname) + "\'\n"
                        temp.write(line)
                temp.close()
                shutil.move('add_info', constants.getConfigPath())
                self.plugin.say('首次登陆成功，哇哈哈哈!', cache=True, wait=True)
        else:
            self.plugin.say('登陆失败，是不是密码错了呢？', cache=True, wait=True)
            logger.error('状态码:{}'.format(resp['code']))

    def daily_checkin(self):
        res = self.api.daily_task(is_mobile=False)
        if res["code"] == 200:
            self.plugin.say('已帮你悄悄的签到了，哇哈哈!', cache=True, wait=True)

    def get_recommend_songs(self):
        datalist = self.api.dig_info(self.api.recommend_playlist(), 'songs')
        return self.pack_info(datalist, "song_id", "song_name", "mp3_url", "artist", "album_name", "album_id", "expires", "get_time") if datalist else None

    def get_recommend_playlist(self):
        datalist = self.api.dig_info(self.api.recommend_resource(), 'top_playlists')
        self.multi_playlists = self.pack_info(datalist, "playlist_id", "playlist_name", "creator_name")
        playlist_name = [each_list['playlist_name'] for each_list in self.multi_playlists][:5]
        say_info = ''
        for idx, name in enumerate(playlist_name, start=1):
            say_info = say_info + '第{}张叫：{}。'.format(idx, name)
        return say_info

    def get_user_playlist(self):
        datalist = self.api.dig_info(self.api.user_playlist(self.userid), 'top_playlists')
        self.multi_playlists = self.pack_info(datalist, "playlist_id", "playlist_name", "creator_name")
        if len(self.multi_playlists) > 5:
            playlist_name = [each_list['playlist_name'] for each_list in self.multi_playlists][:5]
        else:
            playlist_name = [each_list['playlist_name'] for each_list in self.multi_playlists]
        say_info = ''
        for idx, name in enumerate(playlist_name, start=1):
            say_info = say_info + '第{}张叫：{}。'.format(idx, name)
        return say_info

    def get_playlist_detail(self, list_id):
        datalist = self.api.dig_info(self.api.playlist_detail(list_id), 'songs')
        return self.pack_info(datalist, "song_id", "song_name", "mp3_url", "artist", "album_name", "album_id", "expires", "get_time") if datalist else None

    def get_playlists_portions(self, idx):
        playlist_name = [each_list['playlist_name'] for each_list in self.multi_playlists][(idx-1)*5:(idx)*5]
        say_info = ''
        for idx, name in enumerate(playlist_name, start=(idx-1)*5+1):
            say_info = say_info + '第{}张叫：{}。'.format(idx, name)
        return say_info

    def get_search_result(self, singerName=None, songName=None):
        if songName:
            data = self.api.search(songName + ', ' + singerName) if songName and singerName else self.api.search(songName)
            if not data['songCount']:
                return None
            if singerName and singerName != data['songs'][0]['artists'][0]['name']:
                return None
            datalist = self.api.dig_info([data['songs'][0]], 'songs')
        elif singerName:
            data = self.api.search(singerName, stype=100)
            if not data['artistCount']:
                return None
            datalist = self.api.dig_info(self.api.artists(data['artists'][0]['id']), 'songs')
        return self.pack_info(datalist, "song_id", "song_name", "mp3_url", "artist", "album_name", "album_id", "expires", "get_time")

    def set_playlist(self, listNumber=None, singerName=None, songName=None):
        if singerName and songName:
            self.playlist = self.get_search_result(singerName, songName)
        elif singerName:
            self.playlist = self.get_search_result(singerName)
        elif songName:
            self.playlist = self.get_search_result(songName)
        elif listNumber:
            self.list_idx = listNumber
            self.playlist = self.get_playlist_detail(self.multi_playlists[listNumber]['playlist_id'])
        else:
            self.playlist = self.get_recommend_songs()
            self.shuffle_songs()

    def pack_info(self, datalist, *args):
        if not datalist:
            return []
        result = []
        for data in datalist:
            info = {}
            for item in args:
                if item == 'playlist_name':
                    info.setdefault(item, re.sub("[^\u0020^\u4e00-\u9fa5^a-z^A-Z^0-9]", '', data.get(item)))
                info.setdefault(item, data.get(item))
            result.append(info)
        return result

    def shuffle_songs(self):
        if self.playlist:
            shuffle(self.playlist)

    def refresh_urls(self):
        ids = [eachSong['song_id'] for eachSong in self.playlist]
        songs = self.api.dig_info(ids, "refresh_urls")
        if songs:
            for idx, newSong in enumerate(songs):
                if not newSong['mp3_url']:
                    pass
                for oldSong in self.playlist:
                    if oldSong['song_id'] == newSong['song_id']:
                        oldSong['mp3_url'] = newSong['mp3_url']
                        oldSong['expires'] = newSong['expires']
                        oldSong['get_time'] = newSong['get_time']
                        break

class Plugin(AbstractPlugin):
    IS_IMMERSIVE = True  # 这是个沉浸式技能
    SLUG = "WangYiYun"

    def __init__(self, con):
        super(Plugin, self).__init__(con)
        self.player = None
        self.isSearch = None
        self.playlist_number_cut = 1

    def chinese_to_arabic(self, cn:str):
        unit = 0   # current
        ldig = []  # digest
        for cndig in reversed(cn):
            if cndig in CN_UNIT:
                unit = CN_UNIT.get(cndig)
                if unit == 10000 or unit == 100000000:
                    ldig.append(unit)
                    unit = 1
            else:
                dig = CN_NUM.get(cndig)
                if unit:
                    dig *= unit
                    unit = 0
                ldig.append(dig)
        if unit == 10:
            ldig.append(10)
        val, tmp = 0, 0
        for x in reversed(ldig):
            if x == 10000 or x == 100000000:
                val += tmp * x
                tmp = 0
            else:
                tmp += x
        val += tmp
        return val

    def hasNumbers(self, inputString):
        return any(char.isnumeric() for char in inputString if '什' != char)

    def whichNumber(self, text):
        number = re.compile(r"(\d+\.?\d*|[一二三四五六七八九零十百千万亿]+|[0-9]+[,]*[0-9]+.[0-9]+)")
        listNumber = number.findall(text)[0]
        return int(listNumber) if listNumber.isdigit() else self.chinese_to_arabic(listNumber)

    def handle_playlists(self, text):
        ### 多轮询问用户想选择的歌单，一直循环直到得到答案或喊出’不用‘
        ###################################询问具体某一张歌单名###########################################
        if any(word in text for word in [u'啥', u'什么', u'叫']) and self.hasNumbers(text):
            listNumber = self.whichNumber(text) - 1
            if listNumber <= len(self.player.multi_playlists):
                self.say('第{}歌单叫{}！'.format(listNumber+1, self.player.multi_playlists[listNumber]['playlist_name']), onCompleted=lambda: self.handle_playlists(self.activeListen()))
            else:
                self.say('都说了只有{}张歌单啦，哼！'.format(len(self.player.multi_playlists)), onCompleted=lambda: self.handle_playlists(self.activeListen()))
        ###################################表示想继续听下一轮###########################################
        elif u'继续' in text and len(self.player.multi_playlists) > 5:
            playlists_info = self.player.get_playlists_portions(self.playlist_number_cut)
            self.playlist_number_cut += 1
            logger.info(playlists_info)
            if self.playlist_number_cut  > math.ceil(len(self.player.multi_playlists)/5):
                self.say(playlists_info + '你想听哪一张呢，就这么多歌单了，要我重新报一次吗？', onCompleted=lambda: self.handle_playlists(self.activeListen()))
            else:
                self.say(playlists_info + '你想听哪一张呢，还是要不要听下去呢', onCompleted=lambda: self.handle_playlists(self.activeListen()))
        ###################################表示重新播报歌单###########################################
        elif any(word in text for word in [u"重新", u"报"]):
            self.playlist_number_cut = 1
            playlists_info = self.player.get_playlists_portions(self.playlist_number_cut)
            self.say('这么纠结呀，好的吧。' + playlists_info + '你想听哪一张呢', onCompleted=lambda: self.handle_playlists(self.activeListen()))
        ###################################选择某一张歌单###########################################
        elif u'第' in text and self.hasNumbers(text):
            listNumber = self.whichNumber(text) - 1
            if listNumber <= len(self.player.multi_playlists):
                self.player.set_playlist(listNumber=listNumber)
                if self.player.playlist:
                    self.say('选择了第{}张'.format(listNumber+1), wait=True)
                    self.player.play()
                else:
                    self.say('哎！获取不到相关的歌单！不好意思。', wait=True)
            else:
                self.say('都说了只有{}张歌单啦，哼！'.format(len(self.player.multi_playlists)), onCompleted=lambda: self.handle_playlists(self.activeListen()))
        ###################################选择退出此循环###########################################
        elif any(word in text for word in [u"不要", u"算了", u"不用"]):
            self.say('哼！白浪费帮你找来了这么多歌单。', cache=True)
        ###################################当说了别的话语###########################################
        else:
            self.say('别岔开话题，到底想听哪张歌单呀~混蛋！', cache=True, onCompleted=lambda: self.handle_playlists(self.activeListen()))

    def handle_search(self, input):
        ### 多轮询问用户是否要搜索此歌名/歌手，一直循环直到得到答案‘
        ###################################询问刚刚识别到的歌名或歌手，是否正确###########################################
        if any(word in input for word in [u"是的", u"对的"]):
            resDict = self.isSearch.groupdict()
            if resDict['artist'] and resDict['artist_song']:
                self.player.set_playlist(singerName=resDict['artist'], songName=resDict['artist_song'])
            elif resDict['singer']:
                self.player.set_playlist(singerName=resDict['singer'])
            elif resDict['song']:
                self.player.set_playlist(songName=resDict['song'])

            if self.player.playlist:
                self.say('找到了{}的{}！'.format(self.player.playlist[self.player.idx]['artist'], self.player.playlist[self.player.idx]['song_name']), wait=True)
                self.player.play()
            else:
                self.say('哎！在网易云找不到你要的那首歌或歌手，对不起。', wait=True)
        ###################################选择退出此循环###########################################
        elif any(word in input for word in [u"不要", u"算了", u"不用"]):
            self.say('哼！搞得我这么认真听你说话！', cache=True)
        ###################################提取歌手或歌名，提取不了则再次询问###########################################
        else:
            tempSearch = re.match(r'.*[搜索|找|播放|听](?P<singer>.*)的[咯|歌.?]|.*[搜索|找|播放|听](?P<artist>.*)的(?P<artist_song>.*)|.*[搜索|找|播放|听](?P<song>.*)这首歌', input)
            if tempSearch:
                self.isSearch = tempSearch
                if self.isSearch.groups()[1]:
                    self.say('你要听{}的{}，对吗？不对的话，请重新说一次！'.format(self.isSearch.groups()[1], self.isSearch.groups()[2]), onCompleted=lambda: self.handle_search(self.activeListen()))
                else:
                    singerOrsong = self.isSearch.groups()[0] if self.isSearch.groups()[0] else self.isSearch.groups()[3]
                    self.say('你要听{}，对吗？不对的话，请重新说一次！'.format(singerOrsong), onCompleted=lambda: self.handle_search(self.activeListen()))
            else:
                self.say('你想怎样，到底想听谁的歌或什么歌曲', onCompleted=lambda: self.handle_search(self.activeListen()))

    def handle(self, text, parsed):
        #需要给网易云插件配置相关的信息
        profile = config.get()
        if self.SLUG not in profile or \
           'account' not in profile[self.SLUG] or \
           'md5pass' not in profile[self.SLUG]:
            self.say(u"你得在配置文件调整一下呀，哼！", cache=True)
            return
        if not self.player:
            self.player = WangYiYunPlayer(profile[self.SLUG]['account'], profile[self.SLUG]['md5pass'], None, self)

        try:
            # 插件核心处理逻辑
            ###################################尚未播放歌曲，如遇到OPEN_MUSIC意图则分析想做什么###########################################
            if any(word in text for word in ['推荐歌曲', '推荐的歌曲', '歌推荐', '每日推荐']):
                self.player.set_playlist()
                if self.player.playlist:
                    self.say('一共有{}首推荐歌曲噢！'.format(len(self.player.playlist)), wait=True)
                    self.player.play()
                else:
                    self.say('哎！获取不到相关的歌单！不好意思。', wait=True)

            ###################################获取每日推荐歌单####################################
            elif any(word in text for word in ['歌单推荐', '推荐歌单']):
                playlists_info = self.player.get_recommend_playlist()
                self.playlist_number_cut += 1
                logger.info(playlists_info)
                self.say('共找到了{}张歌单哦！'.format(len(self.player.multi_playlists)) + playlists_info + '想听哪一张，或者要不要继续听下去呢', onCompleted=lambda: self.handle_playlists(self.activeListen()))

            ###################################获取我的歌单####################################
            elif any(word in text for word in ['我的歌单', '网易云歌单']):
                playlists_info = self.player.get_user_playlist()
                logger.info(playlists_info)
                if len(self.player.multi_playlists) > 5:
                    self.playlist_number_cut += 1
                    self.say('你一共有{}张歌单哦！'.format(len(self.player.multi_playlists)) + playlists_info + '想听哪一张，或者要不要继续听下去呢', onCompleted=lambda: self.handle_playlists(self.activeListen()))
                else:
                    self.say('你一共有{}张歌单哦！'.format(len(self.player.multi_playlists)) + playlists_info + '你想听哪一张呢，或者需要我重新报一次吗', onCompleted=lambda: self.handle_playlists(self.activeListen()))

            ###################################如用户想搜索歌手/歌名/歌名带歌手，则会有此意图####################################
            elif self.isSearch:
                self.handle_search(text)

            ###################################询问某张歌单名字或者当前歌名####################################
            elif self.player.playlist and any(word in text for word in ['啥', '什么']):
                ## 当还没播放歌曲时，突然打掉播报歌单信息，询问第某张的歌单名
                if self.player.multi_playlists and u"歌单" in text:
                    if self.player.list_idx:
                        #logger.info('目前播放的歌单叫{}！'.format(self.player.multi_playlists[self.player.list_idx]['playlist_name']))
                        self.say('目前播放的歌单叫{}！'.format(self.player.multi_playlists[self.player.list_idx]['playlist_name']), wait=True)
                        self.player.resume()
                    else:
                        self.say('你选的推荐歌曲，怎么会有歌单名呢，哼！', cache=True)
                else:
                    #logger.info('这首歌叫{}, 是{}唱的！'.format(self.player.playlist[self.player.idx]['song_name']))
                    self.say('这首歌叫{}, 是{}唱的！'.format(self.player.playlist[self.player.idx]['song_name'], self.player.playlist[self.player.idx]['artist']), wait=True)
                    self.player.resume()

            ###################################播报歌单信息时被打断，选择某张歌单###########################################
            elif u"第" in text and self.hasNumbers(text):
                self.handle_playlists(text)

            ###################################播放歌曲时，收藏当前播放的歌曲或歌单###########################################
            elif self.nlu.hasIntent(parsed, 'SAVE') and self.player.playlist:
                if u"歌单" in text:
                    if self.player.list_idx:
                        if self.player.api.subscribe_playlist(self.player.multi_playlists[self.player.list_idx]['playlist_id']):
                            self.say('目前的歌单已收藏成功！', cache=True, wait=True)
                        else:
                            self.say('这歌单收藏失败，估计之前就收藏了吧', cache=True, wait=True)
                    else:
                        self.say('目前播放的不是歌单啦！怎么收藏呢~哼。', cache=True, wait=True)
                elif u"歌" in text:
                    if self.player.api.like_song(self.player.playlist[self.player.idx]['song_id']):
                        self.say('这歌已收藏成功啦！', cache=True, wait=True)
                    else:
                        self.say('这歌收藏失败了，估计之前就收藏了吧', cache=True, wait=True)
                else:
                    self.say('你得告诉是要收藏歌单还是歌呀！哼！', cache=True, wait=True)
                self.player.resume()

            ###########################################播放器的基本操作#####################################################
            elif self.nlu.hasIntent(parsed, 'CHANGE_TO_NEXT'):
                if self.player.playlist:
                    self.say('下一首歌', cache=True, wait=True)
                    self.player.next()
                else:
                    self.say('你都还没有播放歌曲，哼~', cache=True)
            elif self.nlu.hasIntent(parsed, 'CHANGE_TO_LAST'):
                if self.player.playlist:
                    self.say('上一首歌', cache=True, wait=True)
                    self.player.prev()
                else:
                    self.say('你都还没有播放歌曲，哼~', cache=True)
            elif self.nlu.hasIntent(parsed, 'CHANGE_VOL'):   ### 尚未修改
                slots = self.nlu.getSlots(parsed, 'CHANGE_VOL')
                for slot in slots:
                    if slot['name'] == 'user_d':
                        word = self.nlu.getSlotWords(parsed, 'CHANGE_VOL', 'user_d')[0]
                        if word == '--HIGHER--':
                            self.player.turnUp()
                        else:
                            self.player.turnDown()
                        return
                    elif slot['name'] == 'user_vd':
                        word = self.nlu.getSlotWords(parsed, 'CHANGE_VOL', 'user_vd')[0]
                        if word == '--LOUDER--':
                            self.player.turnUp()
                        else:
                            self.player.turnDown()
            elif self.nlu.hasIntent(parsed, 'PAUSE'):
                if self.player.playlist:
                    self.say('那就不吵你咯~', cache=True, wait=True)
                    self.player.pause()
            elif self.nlu.hasIntent(parsed, 'CONTINUE'):
                if self.player.playlist:
                    self.player.resume()
            elif self.nlu.hasIntent(parsed, 'RESTART_MUSIC'):
                if self.player.playlist:
                    self.player.play()
            elif self.nlu.hasIntent(parsed, 'CLOSE_MUSIC'):
                self.player.stop()
                self.clearImmersive()  # 去掉沉浸式
                self.say('退出网易云', cache=True)

            ###################################尚未澄清词槽关键信息，例如用户说: 打开网易云(未抓取关键信息)####################################
            else:
                self.say('你想播放什么？我能帮你要到推荐歌曲，推荐歌单或是你的歌单，甚至搜索某歌手或歌名噢？', cache=True)

        except Exception as e:
            logger.error(e)
            self.say('哎呀！处理语句出错~赶紧检查一下吧！', cache=True)

    def pause(self):
        if self.player:
            self.player.stop()

    def restore(self):
        if self.player and not self.player.is_pausing():
            self.player.resume()

    def isValidImmersive(self, text, parsed):
        return any(self.nlu.hasIntent(parsed, intent) for intent in ['CHANGE_TO_LAST', 'CHANGE_TO_NEXT', 'CHANGE_VOL', 'CLOSE_MUSIC', 'PAUSE', 'CONTINUE', 'RESTART_MUSIC', 'SAVE']) or \
        any(word in text for word in [u"什么", u"啥", u"退出", u"歌单", u"推荐", u"第"])

    def isValid(self, text, parsed):
        self.isSearch = re.match(r'.*[搜索|找|播放|听](?P<singer>.*)的[咯|歌.?]|.*[搜索|找|播放|听](?P<artist>.*)的(?P<artist_song>.*)|.*[搜索|找|播放|听](?P<song>.*)这首歌', text)
        return u"网易云" in text or \
        (u"网易云" in text and any(word in text for word in [u"歌单", u"推荐"])) or self.isSearch

