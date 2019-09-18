# -*- coding: utf-8-*-
import shutil
import re
import cn2an
import math
from random import shuffle
from robot.sdk.AbstractPlugin import AbstractPlugin
from robot.Player import MusicPlayer
from robot import config, logging, constants
from sdk import NetEaseApi

logger = logging.getLogger(__name__)

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
        self.playlist_info = None
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
 
    def replay(self):
        logger.debug('WangYiYunPlayer replay')
        path = self.playlist[self.idx]
        super().stop()
        super(MusicPlayer, self).play(path, False, self.replay)

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
        return self.pack_info(datalist, "song_id", "song_name", "artist", "album_name", "mp3_url", "quality")

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
        return self.pack_info(datalist, "song_id", "song_name", "artist", "album_name", "mp3_url", "quality")

    def get_playlists_portions(self, idx):
        playlist_name = [each_list['playlist_name'] for each_list in self.multi_playlists][(idx-1)*5:(idx)*5]
        say_info = ''
        for idx, name in enumerate(playlist_name, start=(idx-1)*5+1):
            say_info = say_info + '第{}张叫：{}。'.format(idx, name)
        return say_info

    def pack_info(self, datalist, *args):
        result = []
        for data in datalist:
            info = {}
            for item in args:
                info.setdefault(item, data.get(item))
            result.append(info)
        return result

    def shuffle_songs(self):
        if self.playlist:
            shuffle(self.playlist)

class Plugin(AbstractPlugin):
    IS_IMMERSIVE = True  # 这是个沉浸式技能
    SLUG = "WangYiYun"

    def __init__(self, con):
        super(Plugin, self).__init__(con)
        self.player = None
        self.playlist_number_cut = 1

    def hasNumbers(self, inputString):
        return any(char.isnumeric() for char in inputString if '什' != char)

    def whichNumber(self, text):
        number = re.compile(r"(\d+\.?\d*|[一二三四五六七八九零十百千万亿]+|[0-9]+[,]*[0-9]+.[0-9]+)")
        listNumber = number.findall(text)[0]
        return int(listNumber) if listNumber.isdigit() else cn2an.cn2an(listNumber, "normal")

    def handle_playlists(self, input):
        if any(word in input for word in [u"我要", u"好", u"继续", u"听"]) and len(self.player.multi_playlists) > 5:
            playlists_info = self.player.get_playlists_portions(self.playlist_number_cut)
            self.playlist_number_cut += 1
            logger.info(playlists_info)
            if self.playlist_number_cut  > math.ceil(len(self.player.multi_playlists)/5):
                self.say(playlists_info + '你想听哪一张呢，就这么多歌单了，要我重新报一次吗？', onCompleted=lambda: self.handle_playlists(self.activeListen()))
            else:
                self.say(playlists_info + '你想听哪一张呢，还是要不要听下去呢', onCompleted=lambda: self.handle_playlists(self.activeListen()))
        
        elif any(word in input for word in [u"重新", u"报"]):
            self.playlist_number_cut = 1
            playlists_info = self.player.get_playlists_portions(self.playlist_number_cut)
            self.say('这么纠结呀，好的吧。' + playlists_info + '你想听哪一张呢', onCompleted=lambda: self.handle_playlists(self.activeListen()))

        elif any(word in input for word in ['啥', '什么', '叫']) and self.hasNumbers(input):
            listNumber = self.whichNumber(input) - 1
            if listNumber < len(self.player.multi_playlists):
                self.say('第{}歌单叫{}！'.format(listNumber+1, self.player.multi_playlists[listNumber]['playlist_name']), onCompleted=lambda: self.handle_playlists(self.activeListen()))
            else:
                self.say('都说了只有{}张歌单啦，哼！'.format(len(self.player.multi_playlists)), onCompleted=lambda: self.handle_playlists(self.activeListen()))

        elif u"第" in input and self.hasNumbers(input):
            listNumber = self.whichNumber(input) - 1
            if listNumber < len(self.player.multi_playlists):
                self.player.list_idx = listNumber
                self.player.playlist_info = self.player.get_playlist_detail(self.player.multi_playlists[listNumber]['playlist_id'])
                self.player.playlist = [each_song['mp3_url'] for each_song in self.player.playlist_info]
                self.player.shuffle_songs()
                #logger.debug([each_song['song_name'] for each_song in self.player.playlist_info])
                self.say('选择了第{}张'.format(listNumber+1), wait=True)
                self.player.play()
            else:
                self.say('都说了只有{}张歌单啦，哼！'.format(len(self.player.multi_playlists)), onCompleted=lambda: self.handle_playlists(self.activeListen()))
        
        elif any(word in input for word in [u"不要", u"算了", u"不用"]):
            self.say('哼！白浪费帮你找来了这么多歌单。', cache=True)

        else:
            self.say('别岔开话题，到底想听哪张歌单~混蛋', cache=True, onCompleted=lambda: self.handle_playlists(self.activeListen()))

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
            ##################################获取每日推荐歌曲####################################
            if any(word in text for word in ['推荐歌曲', '推荐的歌曲', '歌推荐', '每日推荐']):
                self.player.playlist_info = self.player.get_recommend_songs()
                self.player.playlist = [each_song['mp3_url'] for each_song in self.player.playlist_info]
                self.say('一共有{}首推荐歌曲噢！'.format(len(self.player.playlist)), wait=True)
                self.player.play()

            ###################################获取每日推荐歌单####################################
            elif u"歌单推荐" in text or u"推荐歌单" in text:
                playlists_info = self.player.get_recommend_playlist()
                self.playlist_number_cut += 1
                logger.info(playlists_info)
                self.say('共找到了{}张歌单哦！'.format(len(self.player.multi_playlists)) + playlists_info + '想听哪一张，或者要不要继续听下去呢', onCompleted=lambda: self.handle_playlists(self.activeListen()))

            ###################################获取我的歌单####################################
            elif u"我的歌单" in text or u"网易云歌单" in text:
                playlists_info = self.player.get_user_playlist()
                logger.info(playlists_info)
                if len(self.player.multi_playlists) > 5:
                    self.playlist_number_cut += 1
                    self.say('你一共有{}张歌单哦！'.format(len(self.player.multi_playlists)) + playlists_info + '想听哪一张，或者要不要继续听下去呢', onCompleted=lambda: self.handle_playlists(self.activeListen()))
                else:
                    self.say('你一共有{}张歌单哦！'.format(len(self.player.multi_playlists)) + playlists_info + '你想听哪一张呢，或者需要我重新报一次吗', onCompleted=lambda: self.handle_playlists(self.activeListen()))

            ###################################询问歌单名字或者当前歌名####################################
            elif self.player.playlist and any(word in text for word in ['啥', '什么', '叫']):
                if self.player.multi_playlists and u"歌单" in text:
                    if self.player.list_idx:
                        logger.info(self.player.multi_playlists[self.player.list_idx]['playlist_name'])
                        self.say('目前播放的歌单叫{}！'.format(self.player.multi_playlists[self.player.list_idx]['playlist_name']), wait=True)
                        self.player.resume()
                    else:
                        self.say('你选的推荐歌曲，怎么会有歌单名呢，哼！', cache=True)
                else:
                    logger.info(self.player.playlist_info[self.player.idx])
                    self.say('这首歌叫{}, 是{}唱的！'.format(self.player.playlist_info[self.player.idx]['song_name'], self.player.playlist_info[self.player.idx]['artist']), wait=True)
                    self.player.resume()

            ###################################收藏当前播放的歌曲或歌单###########################################
            elif self.player.playlist and self.nlu.hasIntent(parsed, 'SAVE'):
                if u"歌单" in text and self.player.list_idx:
                    if self.player.api.subscribe_playlist(self.player.multi_playlists[self.player.list_idx]['playlist_id']):
                        self.say('目前的歌单已收藏成功！', cache=True, wait=True)
                    else:
                        self.say('这歌单收藏失败，估计之前就收藏了吧', cache=True, wait=True)
                    self.player.resume()
                elif u"歌" in text:
                    if self.player.api.like_song(self.player.playlist_info[self.player.idx]['song_id']):
                        self.say('这歌已收藏成功啦！', cache=True, wait=True)
                    else:
                        self.say('这歌收藏失败了，估计之前就收藏了吧', cache=True, wait=True)
                    self.player.resume()
                else:
                    self.say('你得告诉是要收藏歌单还是歌呀！哼！', cache=True, wait=True)
                    self.player.resume()

            ###################################播放器的基本操作####################################
            elif self.nlu.hasIntent(parsed, 'CHANGE_TO_NEXT'):
                self.say('下一首歌', cache=True, wait=True)
                self.player.next()
            elif self.nlu.hasIntent(parsed, 'CHANGE_TO_LAST'):
                self.say('上一首歌', cache=True, wait=True)
                self.player.prev()
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
                self.player.pause()
            elif self.nlu.hasIntent(parsed, 'CONTINUE'):
                self.player.resume()
            elif self.nlu.hasIntent(parsed, 'RESTART_MUSIC'):
                self.player.play()
            elif self.nlu.hasIntent(parsed, 'CLOSE_MUSIC') or u"退出" in text:
                self.player.stop()
                self.clearImmersive()  # 去掉沉浸式
                self.say('退出网易云', cache=True)
            else:
                self.say('你想播放什么呢？推荐歌曲，推荐歌单还是你的歌单？', cache=True)
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
        any(word in text for word in [u"什么", u"啥", u"退出", u"歌单", u"推荐"])

    def isValid(self, text, parsed):
        return u"网易云" in text or \
        (u"网易云" in text and any(word in text for word in [u"歌单", u"推荐"]))
