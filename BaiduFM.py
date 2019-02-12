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
import random
import time
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
        self.mic = mic
        self.song_info = {}

    def play(self):
        logger.debug('MusicPlayer play')
        song_url = "http://music.baidu.com/data/music/fmlink?" +\
            "type=mp3&rate=320&songIds={}".format(self.playlist[self.idx]['id'])
        info =\
            self.get_song_info(song_url)
        if info['song_link']:
            path = self.download_mp3_by_link(info)
            self.play_mp3_by_link(path, info)
        else:
            self.mic.say('获取音频URL失败，请稍后再试', plugin=__name__, cache=True)

    def next(self):        
        self.idx = (self.idx+1) % len(self.playlist)
        self.play()

    def prev(self):
        self.idx = (self.idx-1) % len(self.playlist)
        self.play()

    def stop(self):
        self.mic.setImmersiveMode(None)  # 去掉沉浸式
        
    def download_mp3_by_link(self, song_info):
        logger.debug("begin DownLoad {}" % (song_info))
        mp3 = requests.get(song_info['song_link']).content
        tmpfile = utils.write_temp_file(mp3, '.mp3')
        return tmpfile

    def play_mp3_by_link(self, path, song_info):
        if os.path.exists(path):
            self.song_info = song_info
            self.mic.play(path, True, self.next)
            self.mic.setImmersiveMode(SLUG)  # 沉浸式
        else:
            logger.error('文件不存在: {}'.format(path))

    def get_song_info(self, song_url):
        try:
            htmldoc = requests.get(song_url).text
            content = json.loads(htmldoc)

            song_link = content['data']['songList'][0]['songLink']
            song_name = content['data']['songList'][0]['songName']            
            song_size = int(content['data']['songList'][0]['size'])
            song_time = int(content['data']['songList'][0]['time'])
            artist_name = content['data']['songList'][0]['artistName']

            return {
                'song_name': song_name,
                'artist_name': artist_name,
                'song_link': song_link,
                'song_size': song_size,
                'song_time': song_time
                }
        except:
            logger.error('get real link failed')
            return(None, None, 0, 0)        

    def get_current_song_info(self):
        return self.song_info


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


def init_music_player(mic, channel):
    global music_player    
    page_url = 'http://fm.baidu.com/dev/api/?tn=channellist'
    channel_list = get_channel_list(page_url)    
    channel_id = channel_list[channel]['channel_id']
    channel_name = channel_list[channel]['channel_name']
    mic.say(u"播放列表" + channel_name, plugin=__name__, cache=True)
    time.sleep(3)
    channel_url = 'http://fm.baidu.com/dev/api/' +\
                  '?tn=playlist&format=json&id=%s' % channel_id
    song_id_list = get_song_list(channel_url)
    music_player = MusicPlayer(song_id_list, mic)


def handle(text, mic, parsed=None):
    global music_player
    if not music_player:
        init_music_player(mic, config.get('/{}/channel'.format(SLUG, DEFAULT_CHANNEL)))
    if unit.hasIntent(parsed, 'MUSICRANK') or any(word in text for word in [u"百度音乐", u"百度电台"]):
        music_player.play()
    elif unit.hasIntent(parsed, 'CHANGE_MUSIC'):
        mic.say('换歌', plugin=__name__, cache=True)
        init_music_player(mic, random.choice(range(0, 40)))        
        music_player.play()
    elif unit.hasIntent(parsed, 'CHANGE_TO_NEXT'):
        mic.say('下一首歌', plugin=__name__, cache=True)
        music_player.next()
    elif unit.hasIntent(parsed, 'CHANGE_TO_LAST'):
        mic.say('上一首歌', plugin=__name__, cache=True)
        music_player.prev()
    elif unit.hasIntent(parsed, 'CLOSE_MUSIC') or unit.hasIntent(parsed, 'PAUSE'):        
        music_player.stop()
        mic.say('退出播放', plugin=__name__, cache=True)
    elif '什么歌' in text:
        info = music_player.get_current_song_info()
        if info is not None and info != {}:
            if info['artist_name']:
                mic.say('正在播放的是：{} 的 {}'.format(info['artist_name'], info['song_name']), plugin=__name__, cache=True)
            else:
                mic.say('正在播放的是：{}'.format(info['song_name']), plugin=__name__, cache=True)
            time.sleep(3)
            music_player.play()
    else:
        mic.say('没听懂你的意思呢，要退出播放，请说退出播放', plugin=__name__, cache=True)
        music_player.play()
        

def restore():
    global music_player
    if music_player:
        music_player.play()

def isControlCommand(text, parsed, immersiveMode):
    """ 判断是否当前音乐模式下的控制指令 """
    return immersiveMode == SLUG and any(unit.hasIntent(parsed, intent) for intent in ['CHANGE_MUSIC', 'CHANGE_TO_LAST', 'CHANGE_TO_NEXT', 'CHANGE_VOL', 'CLOSE_MUSIC', 'PAUSE']) or '什么歌' in text


def isValid(text, parsed=None, immersiveMode=None):
    return any(word in text for word in [u"百度音乐", u"百度电台"]) or isControlCommand(text, parsed, immersiveMode)
