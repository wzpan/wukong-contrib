# -*- coding: utf-8-*-
import re
import os
import math
import time
import json
from random import shuffle
from robot.sdk.AbstractPlugin import AbstractPlugin
from robot.Player import MusicPlayer
from robot import config, logging
from sdk import NetEaseApi

logger = logging.getLogger(__name__)
CONF_PATH = os.path.expanduser("~/.neteasemusic")
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

def chinese_to_arabic(cn:str):
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

def hasNumbers(inputString):
    return any(char.isnumeric() for char in inputString if '什' != char)

def whichNumber(text):
    number = re.compile(r"(\d+\.?\d*|[一二三四五六七八九零十百千万亿]+|[0-9]+[,]*[0-9]+.[0-9]+)")
    listNumber = number.findall(text)[0]
    return int(listNumber) if listNumber.isdigit() else chinese_to_arabic(listNumber)



"""
将NeteaseMusic用户的个人信息保存于Json文件, Learned by Catofes
"""
class Storage(object):
    def __init__(self):
        self.database = {
            "user_info": {"user_id": "", "nickname": ""},
            "preference_info": {
                "user_playlists": [],
                "user_music_types": []
            },
        }
        if not os.path.exists(CONF_PATH):
            try:
                os.mkdir(CONF_PATH)
            except OSError as e:
                logger.error('创建{}目录失败，原因是{}'.format(CONF_PATH, e))

        self.storage_path = os.path.join(CONF_PATH, 'database.json')

    def user_info(self, userid, nickname):
        self.database["user_info"] = dict(user_id=userid, nickname=nickname)
        self.save()

    def user_playlist(self, lists):
        self.database["preference_info"]['user_playlists'] = lists
        self.save()

    def utf8_data_to_file(self, f, data):
        if hasattr(data, "decode"):
            f.write(data.decode("utf-8"))
        else:
            f.write(data)

    def load(self):
        try:
            with open(self.storage_path, 'r') as f:
                for k, v in json.load(f).items():
                    if isinstance(self.database[k], dict):
                        self.database[k].update(v)
                    else:
                        self.database[k] = v
        except (OSError, KeyError, ValueError) as e:
            logger.error('加载database.json文件失败，请检查！原因是{}'.format(e))
        self.save()

    def save(self):
        with open(self.storage_path, "w") as f:
            data = json.dumps(self.database, ensure_ascii=False)
            self.utf8_data_to_file(f, data)

"""
给网易云播放器插件使用的，
在 MusicPlayer 的基础上支持登陆和外接网易云API，返回相关信息。
"""
class NeteaseMusicPlayer(MusicPlayer):
    SLUG = 'NeteaseMusicPlayer'

    def __init__(self, playlist, plugin, **kwargs):
        super(NeteaseMusicPlayer, self).__init__(playlist, plugin, **kwargs)
        self.storage = Storage()
        self.storage.load()
        self.api = NetEaseApi.NetEase()
        self.isLogin = False
        self.playlist = None
        self.multi_listChoices = None
        self.list_idx = None

        ## 首次登陆则需发起请求获取cookies，cookies过期或找不到用户id则需发起请求
        if len(self.api.session.cookies) == 0 or not self.userid:
            if self.login():
                self.isLogin = True
                self.daily_checkin()
                self.update_user_playlist()
        else:
            self.isLogin = True
            self.daily_checkin()
            self.update_user_playlist()

    @property
    def user(self):
        return self.storage.database["user_info"]

    @property
    def preference(self):
        return self.storage.database["preference_info"]

    @property
    def userid(self):
        return self.user["user_id"]

    @property
    def nickname(self):
        return self.user["nickname"]

    @property
    def likelist_id(self):
        return self.preference["user_playlists"][0]['playlist_id'] if self.preference["user_playlists"] else None

    @property
    def account(self):
        return config.get('/' + self.plugin.SLUG + '/account')

    @property
    def md5pass(self):
        return config.get('/' + self.plugin.SLUG + '/md5pass')

    def login(self):
        resp = self.api.login(self.account, self.md5pass)
        if resp["code"] == 200:
            userid = resp["account"]["id"]
            nickname = resp["profile"]["nickname"]
            self.storage.user_info(userid, nickname)
            self.plugin.say('首次登陆成功，恭喜恭喜!', cache=True)
            return True
        else:
            self.plugin.say('登陆失败，请检查账号和密码是否正确。', cache=True, wait=True)
            logger.error('状态码:{}'.format(resp['code']))

    def daily_checkin(self):
        res = self.api.daily_task(is_mobile=False)
        if res["code"] == 200:
            self.plugin.say('已帮你悄悄的签到了，哇哈哈!', cache=True, wait=True)

    def update_user_playlist(self):
        datalist = self.api.dig_info(self.api.user_playlist(self.userid), 'top_playlists')
        self.storage.user_playlist(self.pack_info(datalist, "playlist_id", "playlist_name"))

    def play(self):
        logger.debug('NeteaseMusicPlayer play')
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
        logger.debug('NeteaseMusicPlayer next')
        super(MusicPlayer, self).stop()
        self.idx = (self.idx+1) % len(self.playlist)
        self.play()

    def resume(self):
        super().resume()
        self.onCompleteds = [self.next]

    def get_playlist(self, fromUser=False):
        if not fromUser:
            datalist = self.api.dig_info(self.api.personalized_playlist(), 'personalized_playlists')
            self.multi_listChoices = self.pack_info(datalist, "playlist_id", "playlist_name")
        else:
            self.multi_listChoices = self.preference['user_playlists']

        say_info = ''
        if not self.multi_listChoices:
            return say_info
        elif self.multi_listChoices and len(self.multi_listChoices) > 5:
            playlist_name = [each_list['playlist_name'] for each_list in self.multi_listChoices][:5]
        else:
            playlist_name = [each_list['playlist_name'] for each_list in self.multi_listChoices]
        for idx, name in enumerate(playlist_name, start=1):
            say_info = say_info + '第{}张叫：{}。'.format(idx, name)
        return say_info

    def get_playlists_portions(self, idx):
        playlist_name = [each_list['playlist_name'] for each_list in self.multi_listChoices][(idx-1)*5:(idx)*5]
        say_info = ''
        for idx, name in enumerate(playlist_name, start=(idx-1)*5+1):
            say_info = say_info + '第{}张叫：{}。'.format(idx, name)
        return say_info

    def get_playlist_detail(self, list_id):
        datalist = self.api.dig_info(self.api.playlist_detail(list_id), 'songs')
        return self.pack_info(datalist, "song_id", "song_name", "mp3_url", "artist", "album_name", "album_id", "expires", "get_time") if datalist else None

    def get_recommend_songs(self):
        datalist = self.api.dig_info(self.api.recommend_songs(), 'songs')
        return self.pack_info(datalist, "song_id", "song_name", "mp3_url", "artist", "album_name", "album_id", "expires", "get_time") if datalist else None

    def get_likelist_songs(self):
        datalist = self.api.dig_info(self.api.like_playlist(self.userid), 'likesongs')
        return self.pack_info(datalist, "song_id", "song_name", "mp3_url", "artist", "album_name", "album_id", "expires", "get_time") if datalist else None

    def get_search_result(self, singerName=None, songName=None):
        if songName:
            data = self.api.search(songName + ', ' + singerName) if songName and singerName else self.api.search(songName)
            if not data['songCount']:
                return None
            # 优化判断逻辑（由于不能很好的拆分歌手名和歌曲名）
            # 例：播放许飞的父亲写的散文诗
            #       singerName: 许飞的父亲写
            #       songName: 散文诗
            if singerName:
                datalist = None
                # 若存在歌手名，则精确获取当前歌手的歌曲
                for song in data['songs']:
                    if singerName == song['artists'][0]['name']:
                        datalist = self.api.dig_info([song], 'songs')
                        break
                # 若不能精确匹配歌手名，则获取第一首歌
                if not datalist:
                    datalist = self.api.dig_info([data['songs'][0]], 'songs')
            else:
                datalist = self.api.dig_info([data['songs'][0]], 'songs')
        elif singerName:
            data = self.api.search(singerName, stype=100)
            if not data['artistCount']:
                return None
            datalist = self.api.dig_info(self.api.artists(data['artists'][0]['id']), 'songs')
        return self.pack_info(datalist, "song_id", "song_name", "mp3_url", "artist", "album_name", "album_id", "expires", "get_time")

    def set_playlist(self, listNumber=None, singerName=None, songName=None, isLikeList=False):
        ### 当获取到歌手名和歌名时
        if singerName and songName:
            self.playlist = self.get_search_result(singerName, songName)
        ### 当获取到歌手时
        elif singerName:
            self.playlist = self.get_search_result(singerName)
        ### 当获取到歌名时
        elif songName:
            self.playlist = self.get_search_result(None, songName)
        ### 当获取到多张歌单，选了某张歌单时
        elif listNumber:
            self.playlist = self.get_playlist_detail(self.multi_listChoices[listNumber]['playlist_id'])
            self.shuffle_songs()
        ### 当获取到红心歌单/我喜欢的音乐歌单时
        elif isLikeList:
            self.playlist = self.get_likelist_songs()
            self.shuffle_songs()
        ### 当获取到每日推荐歌曲时
        else:
            self.playlist = self.get_recommend_songs()

    def change_playmode_intelligence(self, current_songId):
        datalist = self.api.dig_info(self.api.playmode_intelligence(current_songId, self.likelist_id), 'songs')
        self.playlist =  self.pack_info(datalist, "song_id", "song_name", "mp3_url", "artist", "album_name", "album_id", "expires", "get_time") if datalist else None

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

"""
此类主要处理用户的文字输入请求，
剥离请求中的参数并交给NeteaseMusicPlayer去处理。
"""
class Plugin(AbstractPlugin):
    IS_IMMERSIVE = True  # 这是个沉浸式技能
    SLUG = "NeteaseMusic"

    def __init__(self, con):
        super(Plugin, self).__init__(con)
        self.player = None
        self.isSearch = None
        self.isContinueAsking = False
        self.playlist_number_cut = 1

    def handle_multilists(self, text):
        ### 多轮询问用户想选择的歌单，一直循环直到得到答案或喊出’不用‘
        ###################################询问具体某一张歌单名###########################################
        if any(word in text for word in [u'啥', u'什么', u'叫']) and hasNumbers(text):
            listNumber = whichNumber(text) - 1
            if listNumber <= len(self.player.multi_listChoices):
                self.say('第{}张叫{}！'.format(listNumber+1, self.player.multi_listChoices[listNumber]['playlist_name']), onCompleted=lambda: self.handle_multilists(self.activeListen()))
            else:
                self.say('都说了只有{}张啦，哼！'.format(len(self.player.multi_listChoices)), onCompleted=lambda: self.handle_multilists(self.activeListen()))
        ###################################表示想继续听下一轮###########################################
        elif u'继续' in text and len(self.player.multi_listChoices) > 5:
            playlists_info = self.player.get_playlists_portions(self.playlist_number_cut)
            self.playlist_number_cut += 1
            logger.info(playlists_info)
            if self.playlist_number_cut  > math.ceil(len(self.player.multi_listChoices)/5):
                self.say(playlists_info + '你想听哪一张呢，就这么多了，要我重新报一次吗？', onCompleted=lambda: self.handle_multilists(self.activeListen()))
            else:
                self.say(playlists_info + '你想听哪一张呢，还是要不要听下去呢', onCompleted=lambda: self.handle_multilists(self.activeListen()))
        ###################################表示重新播报歌单###########################################
        elif any(word in text for word in [u"重新", u"报"]):
            self.playlist_number_cut = 1
            playlists_info = self.player.get_playlists_portions(self.playlist_number_cut)
            self.say('这么纠结呀，好的吧。' + playlists_info + '你想听哪一张呢', onCompleted=lambda: self.handle_multilists(self.activeListen()))
        ###################################选择某一张歌单###########################################
        elif u'第' in text and hasNumbers(text):
            listNumber = whichNumber(text) - 1
            if listNumber >= len(self.player.multi_listChoices):
                self.say('都说了只有{}张啦，哼！'.format(len(self.player.multi_listChoices)), onCompleted=lambda: self.handle_multilists(self.activeListen()))
            else:
                self.player.list_idx = listNumber
                self.isContinueAsking = False
                self.playlist_number_cut = 1
                self.isOpenLikelist = True if self.player.list_idx == 0 else False

                self.player.set_playlist(listNumber=self.player.list_idx)
                if self.player.playlist:
                    self.say('选择了第{}张'.format(self.player.list_idx+1), wait=True)
                    self.player.play()
                else:
                    self.say('哎！获取不到相关的信息！不好意思。', wait=True)
        ###################################选择退出此循环###########################################
        elif any(word in text for word in [u"不要", u"算了", u"不用"]):
            self.playlist_number_cut = 1
            self.isContinueAsking = False
            self.say('哼！白浪费帮你找来了这么多的资源！。', cache=True)
        ###################################当说了别的话语###########################################
        else:
            self.say('别岔开话题，到底想听哪张的呀~混蛋！', cache=True, onCompleted=lambda: self.handle_multilists(self.activeListen()))

    def handle_search(self, input):
        ### 多轮询问用户是否要搜索此歌名/歌手，一直循环直到得到答案‘
        ###################################询问刚刚识别到的歌名或歌手，是否正确###########################################
        if any(word in input for word in [u"是的", u"对", u"确认"]):
            resDict = self.isSearch.groupdict()
            if resDict['artist'] and resDict['artist_song']:
                self.player.set_playlist(singerName=resDict['artist'], songName=resDict['artist_song'])
            elif resDict['singer']:
                self.player.set_playlist(singerName=resDict['singer'])
            elif resDict['song']:
                self.player.set_playlist(songName=resDict['song'])

            if self.player.playlist:
                self.isOpenLikelist = False
                self.say('找到了{}的{}！'.format(self.player.playlist[self.player.idx]['artist'], self.player.playlist[self.player.idx]['song_name']), wait=True)
                self.player.play()
            else:
                self.say('是搜索不到歌手或歌曲吗，目前歌单里没歌哦。', cache=True, wait=True)
        ###################################选择退出此循环###########################################
        elif any(word in input for word in [u"不要", u"算了", u"不用"]):
            self.say('哼！搞得我这么认真听你说话！', cache=True, wait=True)
        ###################################提取歌手或歌名，提取不了则再次询问###########################################
        else:
            tempSearch = re.match(r'.*[搜索|找|播放|听](?P<singer>.*)的.?[歌|咯|歌曲]|.*[搜索|找|播放|听](?P<artist>.*)的(?P<artist_song>.*)|.*[搜索|找|播放|听](?P<song>.*)这首歌', input)
            if tempSearch:
                self.isSearch = tempSearch
                singerOrSong = self.isSearch.groups()[0] if self.isSearch.groups()[0] else self.isSearch.groups()[3]
                if self.isSearch.groups()[1]:
                    self.say('你要听{}的{}歌曲，对吗？不对的话，请重新说一次！'.format(self.isSearch.groups()[1], self.isSearch.groups()[2]), onCompleted=lambda: self.handle_search(self.activeListen()), wait=True)
                elif self.isSearch.groups()[0]:
                    self.say('你要听{}这位歌手，对吗？不对的话，请重新说一次！'.format(singerOrSong), onCompleted=lambda: self.handle_search(self.activeListen()), wait=True)
                else:
                    self.say('你要听{}这首歌，对吗？不对的话，请重新说一次！'.format(singerOrSong), onCompleted=lambda: self.handle_search(self.activeListen()), wait=True)
            else:
                self.say('没听懂你的意思哦', cache=True, wait=True)

    def handle(self, text, parsed):
        #需要给网易云插件配置相关的信息
        profile = config.get()
        if self.SLUG not in profile or \
           'account' not in profile[self.SLUG] or \
           'md5pass' not in profile[self.SLUG]:
            self.say(u"你得在配置文件调整一下呀，哼！", cache=True)
            return

        if not self.player:
            self.player = NeteaseMusicPlayer(None, self)
            if not self.player.isLogin:
                self.player = None
                return

        try:
            # 插件核心处理逻辑
            ###################################如用户想搜索歌手/歌名/歌名带歌手，则会有此意图####################################
            if self.isSearch:
                self.handle_search(text)
            ###################################播报歌单信息时被打断，直接进入多轮询问###########################################
            elif self.isContinueAsking:
                self.handle_multilists(text)

            ###################################尚未播放歌曲，获取用户的每日推荐歌曲###########################################
            elif any(word in text for word in ['推荐歌曲', '推荐的歌曲', '歌推荐', '每日推荐']):
                self.player.set_playlist()
                self.isOpenLikelist = False
                if self.player.playlist:
                    self.say('今天共有{}首推荐歌曲噢！'.format(len(self.player.playlist)), wait=True)
                    self.player.play()
                else:
                    self.say('哎！获取不到相关的每日推荐歌曲！不好意思。', cache=True, wait=True)

            ###################################获取每日推荐歌单##############################################################
            elif any(word in text for word in ['歌单推荐', '推荐歌单']):
                playlists_info = self.player.get_playlist(fromUser=False)
                if not self.player.multi_listChoices:
                    self.say('很抱歉，找不到任何推荐歌单！你是不是很少用网易云~', cache=True, wait=True)
                else:
                    logger.info(playlists_info)
                    self.playlist_number_cut += 1
                    self.isContinueAsking = True
                    self.say('共找到了{}张歌单噢！'.format(len(self.player.multi_listChoices)) + playlists_info + '想听哪一张，或者要不要继续听下去呢', onCompleted=lambda: self.handle_multilists(self.activeListen()))

            ###################################获取用户的红心歌单（用户喜欢的音乐）###########################################
            elif any(word in text for word in ['红心歌单', '红星歌单', '喜欢的音乐']):
                self.player.set_playlist(isLikeList=True)
                if self.player.playlist:
                    self.isOpenLikelist = True
                    self.say('红心歌单共有{}首歌曲噢！'.format(len(self.player.playlist)), wait=True)
                    self.player.play()
                else:
                    self.say('哎！获取不到你的红心歌单！不好意思。', cache=True, wait=True)

            ###################################获取我的歌单####################################
            elif any(word in text for word in ['我的歌单', '我的网易云歌单']):
                playlists_info = self.player.get_playlist(fromUser=True)
                logger.info(playlists_info)

                if not self.player.multi_listChoices:
                    self.say('很抱歉，找不到任何你的歌单！你是不是很少用网易云~', cache=True, wait=True)
                elif len(self.player.multi_listChoices) > 5:
                    self.playlist_number_cut += 1
                    self.isContinueAsking = True
                    self.say('你一共有{}张歌单噢！'.format(len(self.player.multi_listChoices)) + playlists_info + '想听哪一张，或者要不要继续听下去呢', onCompleted=lambda: self.handle_multilists(self.activeListen()))
                else:
                    self.isContinueAsking = True
                    self.say('你一共有{}张歌单噢！'.format(len(self.player.multi_listChoices)) + playlists_info + '你想听哪一张呢，或者需要我重新报一次吗', onCompleted=lambda: self.handle_multilists(self.activeListen()))

            ###################################播放我的红心歌单时，开启心动模式（将你自己的红心曲目与系统推荐的新歌交替进行播放）###########################################
            elif u'心动模式' in text  and self.player.playlist:
                if not self.isOpenLikelist:
                    self.say('真抱歉，你得选择红心歌单才能开启心动模式噢~', cache=True, wait=True)
                else:
                    self.player.change_playmode_intelligence(self.player.playlist[self.player.idx]['song_id'])
                    if self.player.playlist:
                        self.say('已成功开启心动模式，目前有{}首歌曲！'.format(len(self.player.playlist)), wait=True)
                        self.player.play()
                    else:
                        self.say('哎！开启心动模式失败，获取不到歌曲！不好意思。', cache=True, wait=True)

            ###################################询问某张歌单名字或者当前歌名####################################
            elif any(word in text for word in ['啥', '什么']) and self.player.playlist:
                if u"歌单" in text and self.player.list_idx:
                        self.say('目前播放的歌单叫{}！'.format(self.player.multi_listChoices[self.player.list_idx]['playlist_name']), wait=True)
                elif u"歌单" in text:
                        self.say('你选择的都不是歌单，怎么会有歌单名呢，哼！', cache=True)
                else:
                    #logger.info('这首歌叫{}, 是{}唱的！'.format(self.player.playlist[self.player.idx]['song_name']))
                    self.say('这首歌叫{}, 是{}唱的！'.format(self.player.playlist[self.player.idx]['song_name'], self.player.playlist[self.player.idx]['artist']), wait=True)
                self.player.resume()

            ###################################播放歌曲时，收藏当前播放的歌曲或歌单###########################################
            elif self.nlu.hasIntent(parsed, 'SAVE') and self.player.playlist:
                if u"歌单" in text and self.player.list_idx:
                    if self.player.api.subscribe_playlist(self.player.multi_listChoices[self.player.list_idx]['playlist_id']):
                        self.say('目前的歌单已收藏成功！', cache=True, wait=True)
                    else:
                        self.say('这歌单收藏失败，估计之前就收藏了吧', cache=True, wait=True)
                elif u"歌单" in text:
                        self.say('目前播放的不是歌单啦！怎么收藏呢~哼!', cache=True, wait=True)
                else:
                    if self.player.api.like_song(self.player.playlist[self.player.idx]['song_id']):
                        self.say('这首歌已收藏成功啦！', cache=True, wait=True)
                    else:
                        self.say('这首歌收藏失败了，估计之前就收藏了吧', cache=True, wait=True)
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
            elif self.nlu.hasIntent(parsed, 'CHANGE_VOL'):
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
                    self.player.pause()
            elif self.nlu.hasIntent(parsed, 'CONTINUE'):
                if self.player.playlist:
                    self.player.resume()
            elif self.nlu.hasIntent(parsed, 'RESTART_MUSIC'):
                if self.player.playlist:
                    self.player.play()
            elif self.nlu.hasIntent(parsed, 'CLOSE_MUSIC') or u'退出' in text:
                self.player.stop()
                self.player = None
                self.clearImmersive()  # 去掉沉浸式
                self.say('退出网易云', cache=True)

            ###################################不清楚用户的意图时就再次询问，例如用户说: 打开网易云(未抓取关键信息)####################################
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
        any(word in text for word in [u"什么", u"啥", u"退出", u"歌单", u"推荐", u"红心", u"红星", u"第", u"心动模式", u"不用", u"算了", u"喜欢的"])

    def isValid(self, text, parsed):
        self.isSearch = re.match(r'.*[搜索|找|播放|听](?P<singer>.*)的.?[歌|咯|歌曲]|.*[搜索|找|播放|听](?P<artist>.*)的(?P<artist_song>.*)|.*[搜索|找|播放|听](?P<song>.*)这首歌', text)
        return u"网易云" in text or \
        (u"网易云" in text and any(word in text for word in [u"歌单", u"推荐", u"红心", u"红星"])) or self.isSearch

