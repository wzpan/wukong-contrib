# -*- coding: utf-8-*-
import json
import logging
import os
import hashlib
import socket
import subprocess
import tempfile
import urllib
import requests
from robot import config, logging, utils
from robot.sdk import unit

SLUG = "baidufm"

logger = logging.getLogger(__name__)

music_player = None

DEFAULT_CHANNEL = 14

class MusicPlayer():

    def __init__(self, playlist, mic):
        super(MusicPlayer, self).__init__()
        self.playlist = playlist
        self.idx = 0
        self.song_file = "dummy"
        self.mic = mic

    def play(self):
        logger.debug('MusicPlayer play')
        song_url = "http://music.baidu.com/data/music/fmlink?" +\
            "type=mp3&rate=320&songIds={}".format(self.playlist[self.idx]['id'])
        song_name, song_link, song_size, song_time =\
            self.get_song_real_url(song_url)
        if song_link:
            self.download_mp3_by_link(song_link, song_name, song_size)
            self.play_mp3_by_link(song_link, song_name, song_size, song_time)
        else:
            self.mic.say('获取音频URL失败，请稍后再试')

    def next(self):        
        self.idx = (self.idx+1) % len(self.playlist)
        self.play()

    def prev(self):
        self.idx = (self.idx-1) % len(self.playlist)
        self.play()

    def stop(self):
        self.mic.setImmersiveMode(None)  # 去掉沉浸式
        
    def play_mp3_by_link(self, song_link, song_name, song_size, song_time):
        if os.path.exists(self.song_file):
            self.mic.play(self.song_file, True, self.next)
            self.mic.setImmersiveMode(SLUG)  # 沉浸式
        else:
            logger.error('文件不存在: {}'.format(self.song_file))

    def download_mp3_by_link(self, song_link, song_name, song_size):
        logger.debug("begin DownLoad %s size %d" % (song_name, song_size))
        mp3 = requests.get(song_link).content
        self.song_file = utils.write_temp_file(mp3, '.mp3')

    def get_song_real_url(self, song_url):
        try:
            htmldoc = requests.get(song_url).text
            content = json.loads(htmldoc)

            song_link = content['data']['songList'][0]['songLink']
            song_name = content['data']['songList'][0]['songName']
            song_size = int(content['data']['songList'][0]['size'])
            song_time = int(content['data']['songList'][0]['time'])

            return song_name, song_link, song_size, song_time
        except:
            logger.error('get real link failed')
            return(None, None, 0, 0)        


def get_channel_list(page_url):
    try:
        htmldoc = requests.get(page_url).text
    except:
        return {}

    content = json.loads(htmldoc)
    channel_list = content['channel_list']    
    return channel_list


def get_song_list(channel_url):
    try:
        htmldoc = requests.get(channel_url).text
    except:
        return{}

    content = json.loads(htmldoc)
    song_id_list = content['list']

    return song_id_list


def init_music_player(mic):
    global music_player    
    page_url = 'http://fm.baidu.com/dev/api/?tn=channellist'
    channel_list = get_channel_list(page_url)
    channel = config.get('/{}/channel'.format(SLUG, DEFAULT_CHANNEL))
    channel_id = channel_list[channel]['channel_id']
    channel_name = channel_list[channel]['channel_name']
    mic.say(u"播放列表" + channel_name, plugin=__name__, cache=True)
    channel_url = 'http://fm.baidu.com/dev/api/' +\
                  '?tn=playlist&format=json&id=%s' % channel_id
    song_id_list = get_song_list(channel_url)
    music_player = MusicPlayer(song_id_list, mic)


def handle(text, mic, parsed=None):
    global music_player
    if not music_player:
        init_music_player(mic)
    if unit.hasIntent(parsed, 'MUSICRANK') or any(word in text for word in [u"百度音乐", u"百度电台"]):
        music_player.play()
    elif unit.hasIntent(parsed, 'CHANGE_MUSIC') or unit.hasIntent(parsed, 'CHANGE_TO_NEXT'):
        mic.say('下一首歌')
        music_player.next()
    elif unit.hasIntent(parsed, 'CHANGE_TO_LAST'):
        mic.say('上一首歌')
        music_player.prev()
    elif unit.hasIntent(parsed, 'CLOSE_MUSIC') or unit.hasIntent(parsed, 'PAUSE'):        
        music_player.stop()
        mic.say('退出播放')
    else:
        mic.say('没听懂你的意思呢，要退出播放，请说退出播放')

def restore():
    global music_player
    if music_player:
        music_player.play()

def isControlCommand(parsed, immersiveMode):
    """ 判断是否当前音乐模式下的控制指令 """
    return immersiveMode == SLUG and any(unit.hasIntent(parsed, intent) for intent in ['CHANGE_MUSIC', 'CHANGE_TO_LAST', 'CHANGE_TO_NEXT', 'CHANGE_VOL', 'CLOSE_MUSIC', 'PAUSE'])


def isValid(text, parsed=None, immersiveMode=None):
    return any(word in text for word in [u"百度音乐", u"百度电台"]) or isControlCommand(parsed, immersiveMode)
