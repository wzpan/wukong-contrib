#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: omi
# @Date:   2014-08-24 21:51:57
'''
网易云音乐 Api
'''
from builtins import chr
from builtins import int
from builtins import map
from builtins import open
from builtins import range
from builtins import str
from builtins import pow

import re
import os
import json
import time
import hashlib
import random
import base64
import binascii
import sys

from Crypto.Cipher import AES
from http.cookiejar import LWPCookieJar
import requests
import requests_cache
from robot import constants, logging
log = logging.getLogger(__name__)

class TooManyTracksException(Exception):
    """The playlist contains more than 1000 tracks."""
    pass

# 歌曲榜单地址
top_list_all = {
    0: ['云音乐新歌榜', '/discover/toplist?id=3779629'],
    1: ['云音乐热歌榜', '/discover/toplist?id=3778678'],
    2: ['网易原创歌曲榜', '/discover/toplist?id=2884035'],
    3: ['云音乐飙升榜', '/discover/toplist?id=19723756'],
    4: ['云音乐电音榜', '/discover/toplist?id=10520166'],
    5: ['UK排行榜周榜', '/discover/toplist?id=180106'],
    6: ['美国Billboard周榜', '/discover/toplist?id=60198'],
    7: ['KTV嗨榜', '/discover/toplist?id=21845217'],
    8: ['iTunes榜', '/discover/toplist?id=11641012'],
    9: ['Hit FM Top榜', '/discover/toplist?id=120001'],
    10: ['日本Oricon周榜', '/discover/toplist?id=60131'],
    11: ['韩国Melon排行榜周榜', '/discover/toplist?id=3733003'],
    12: ['韩国Mnet排行榜周榜', '/discover/toplist?id=60255'],
    13: ['韩国Melon原声周榜', '/discover/toplist?id=46772709'],
    14: ['中国TOP排行榜(港台榜)', '/discover/toplist?id=112504'],
    15: ['中国TOP排行榜(内地榜)', '/discover/toplist?id=64016'],
    16: ['香港电台中文歌曲龙虎榜', '/discover/toplist?id=10169002'],
    17: ['华语金曲榜', '/discover/toplist?id=4395559'],
    18: ['中国嘻哈榜', '/discover/toplist?id=1899724'],
    19: ['法国 NRJ EuroHot 30周榜', '/discover/toplist?id=27135204'],
    20: ['台湾Hito排行榜', '/discover/toplist?id=112463'],
    21: ['Beatport全球电子舞曲榜', '/discover/toplist?id=3812895']
}

default_timeout = 10

modulus = ('00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7'
           'b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280'
           '104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932'
           '575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b'
           '3ece0462db0a22b8e7')
nonce = b'0CoJUm6Qyw8W8jud' ##因为AES加密，需编码为bytes
pubKey = '010001'

class Parse(object):
    @classmethod
    def _song_url_by_id(cls, sid):
        # 128k
        url = "http://music.163.com/song/media/outer/url?id={}.mp3".format(sid)
        quality = "LD 128k"
        return url, quality

    @classmethod
    def song_url(cls, song):
        if "url" in song:
            # songs_url resp
            url = song["url"]
            if url is None:
                return Parse._song_url_by_id(song["id"])
            br = song["br"]
            if br >= 320000:
                quality = "HD"
            elif br >= 192000:
                quality = "MD"
            else:
                quality = "LD"
            return url, "{} {}k".format(quality, br // 1000)
        else:
            # songs_detail resp
            return Parse._song_url_by_id(song["id"])

    @classmethod
    def song_album(cls, song):
        # 对新老接口进行处理
        if "al" in song:
            if song["al"] is not None:
                album_name = song["al"]["name"]
                album_id = song["al"]["id"]
            else:
                album_name = "未知专辑"
                album_id = ""
        elif "album" in song:
            if song["album"] is not None:
                album_name = song["album"]["name"]
                album_id = song["album"]["id"]
            else:
                album_name = "未知专辑"
                album_id = ""
        else:
            raise ValueError
        return album_name, album_id

    @classmethod
    def song_artist(cls, song):
        artist = ""
        # 对新老接口进行处理
        if "ar" in song:
            artist = ", ".join([a["name"] for a in song["ar"] if a["name"] is not None])
            # 某些云盘的音乐会出现 'ar' 的 'name' 为 None 的情况
            # 不过会多个 ’pc' 的字段
            # {'name': '简单爱', 'id': 31393663, 'pst': 0, 't': 1, 'ar': [{'id': 0, 'name': None, 'tns': [], 'alias': []}],
            #  'alia': [], 'pop': 0.0, 'st': 0, 'rt': None, 'fee': 0, 'v': 5, 'crbt': None, 'cf': None,
            #  'al': {'id': 0, 'name': None, 'picUrl': None, 'tns': [], 'pic': 0}, 'dt': 273000, 'h': None, 'm': None,
            #  'l': {'br': 193000, 'fid': 0, 'size': 6559659, 'vd': 0.0}, 'a': None, 'cd': None, 'no': 0, 'rtUrl': None,
            #  'ftype': 0, 'rtUrls': [], 'djId': 0, 'copyright': 0, 's_id': 0, 'rtype': 0, 'rurl': None, 'mst': 9,
            #  'cp': 0, 'mv': 0, 'publishTime': 0,
            #  'pc': {'nickname': '', 'br': 192, 'fn': '简单爱.mp3', 'cid': '', 'uid': 41533322, 'alb': 'The One 演唱会',
            #         'sn': '简单爱', 'version': 2, 'ar': '周杰伦'}, 'url': None, 'br': 0}
            if artist == "" and "pc" in song:
                artist = "未知艺术家" if song["pc"]["ar"] is None else song["pc"]["ar"]
        elif "artists" in song:
            artist = ", ".join([a["name"] for a in song["artists"]])
        else:
            artist = "未知艺术家"

        return artist

    @classmethod
    def songs(cls, songs):
        song_info_list = []
        for song in songs:
            url, quality = Parse.song_url(song)
            if not url:
                continue

            album_name, album_id = Parse.song_album(song)
            song_info = {
                "song_id": song["id"],
                "artist": Parse.song_artist(song),
                "song_name": song["name"],
                "album_name": album_name,
                "album_id": album_id,
                "mp3_url": url,
                "quality": quality,
                "expires": song["expires"],
                "get_time": song["get_time"],
            }
            song_info_list.append(song_info)
        return song_info_list

    @classmethod
    def artists(cls, artists):
        return [
            {
                "artist_id": artist["id"],
                "artists_name": artist["name"],
                "alias": "".join(artist["alias"]),
            }
            for artist in artists
        ]

    @classmethod
    def albums(cls, albums):
        return [
            {
                "album_id": album["id"],
                "albums_name": album["name"],
                "artists_name": album["artist"]["name"],
            }
            for album in albums
        ]

    @classmethod
    def playlists(cls, playlists):
        return [
            {
                "playlist_id": pl["id"],
                "playlist_name": pl["name"],
                "creator_name": pl["creator"]["nickname"],
            }
            for pl in playlists
        ]

# 歌曲加密算法, 基于https://github.com/yanunon/NeteaseCloudMusic脚本实现
def encrypted_id(id):
    magic = bytearray('3go8&$8*3*3h0k(2)2', 'u8')
    song_id = bytearray(id, 'u8')
    magic_len = len(magic)
    for i, sid in enumerate(song_id):
        song_id[i] = sid ^ magic[i % magic_len]
    m = hashlib.md5(song_id)
    result = m.digest()
    result = base64.b64encode(result)
    result = result.replace(b'/', b'_')
    result = result.replace(b'+', b'-')
    return result.decode('utf-8')


# 登录加密算法, 基于https://github.com/stkevintan/nw_musicbox脚本实现
def encrypted_request(text):
    text = json.dumps(text).encode('utf-8') ##因为pycryto很久没更新，所以需要编码成utf-8才行
    log.debug(text)
    secKey = createSecretKey(16)
    encText = aesEncrypt(aesEncrypt(text, nonce), secKey)
    encSecKey = rsaEncrypt(secKey, pubKey, modulus)
    data = {'params': encText, 'encSecKey': encSecKey}
    return data


def aesEncrypt(text, secKey):
    pad = 16 - len(text) % 16
    text = text + bytearray([pad] * pad)
    encryptor = AES.new(secKey, 2, b'0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext


def rsaEncrypt(text, pubKey, modulus):
    text = text[::-1]
    rs = pow(int(binascii.hexlify(text), 16), int(pubKey, 16), int(modulus, 16))
    return format(rs, 'x').zfill(256)

def createSecretKey(size):
    return binascii.hexlify(os.urandom(size))[:16]

# list去重
def uniq(arr):
    arr2 = list(set(arr))
    arr2.sort(key=arr.index)
    return arr2

def geturl_new_api(song):
    br_to_quality = {128000: 'MD 128k', 320000: 'HD 320k'}
    alter = NetEase().songs_detail_new_api([song['id']])[0]
    url = alter['url']
    quality = br_to_quality.get(alter['br'], '')
    return url, quality

def geturls_new_api(song_ids):
    """ 批量获取音乐的地址 """
    alters = NetEase().songs_detail_new_api(song_ids)
    return alters


class NetEase(object):

    def __init__(self):
        self.header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/search/',
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'  # NOQA
        }
        self.cookies = {'appver': '1.5.2'}
        self.playlist_class_dict = {}
        self.session = requests.Session()
        self.create_file(constants.getConfigData('cookies'))
        self.create_file(constants.getConfigData('reqcache'))
        requests_cache.install_cache(constants.getConfigData('reqcache'), expire_after=3600)
        self.session.cookies = LWPCookieJar(constants.getConfigData('cookies'))
        self.session.cookies.load()
        for cookie in self.session.cookies:
            if cookie.is_expired():
                cookie_jar.clear()

    def create_file(self, path, default="#LWP-Cookies-2.0\n"):
        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write(default)

    def return_toplists(self):
        return [l[0] for l in top_list_all.values()]

    def httpRequest(self,
                    method,
                    action,
                    query=None,
                    urlencoded=None,
                    callback=None,
                    timeout=None):
        connection = json.loads(
            self.rawHttpRequest(method, action, query, urlencoded, callback, timeout)
        )
        return connection

    def rawHttpRequest(self,
                       method,
                       action,
                       query=None,
                       urlencoded=None,
                       callback=None,
                       timeout=None):
        if method == 'GET':
            url = action if query is None else action + '?' + query
            connection = self.session.get(url,
                                          headers=self.header,
                                          timeout=default_timeout)

        elif method == 'POST':
            connection = self.session.post(action,
                                           data=query,
                                           headers=self.header,
                                           timeout=default_timeout)

        elif method == 'Login_POST':
            connection = self.session.post(action,
                                           data=query,
                                           headers=self.header,
                                           timeout=default_timeout)
            self.session.cookies.save()

        connection.encoding = 'UTF-8'
        return connection.text

    def logout(self):
            self.session.cookies.clear()
            self.session.cookies.save()
    # 登录
    def login(self, username, password):
        pattern = re.compile(r'^0\d{2,3}\d{7,8}$|^1[34578]\d{9}$')
        if pattern.match(username):
            return self.phone_login(username, password)
        action = 'https://music.163.com/weapi/login?csrf_token='
        text = {
            'username': username,
            'password': password,
            'rememberLogin': 'true'
        }
        data = encrypted_request(text)
        try:
            return self.httpRequest('Login_POST', action, data)
        except requests.exceptions.RequestException as e:
            log.error(e)
            return {'code': 501}

    # 手机登录
    def phone_login(self, username, password):
        action = 'https://music.163.com/weapi/login/cellphone'
        text = {
            'phone': username,
            'password': password,
            'rememberLogin': 'true'
        }
        data = encrypted_request(text)
        try:
            return self.httpRequest('Login_POST', action, data)
        except requests.exceptions.RequestException as e:
            log.error(e)
            return {'code': 501}

    # 每日签到  --- 已修改 
    def daily_signin(self, is_mobile):
        action = 'http://music.163.com/weapi/point/dailyTask'
        text = dict(type=0 if is_mobile else 1)
        data = encrypted_request(text)
        try:
            return self.httpRequest('POST', action, data)
        except requests.exceptions.RequestException as e:
            log.error(e)
            return -1

    # 用户歌单
    def user_playlist(self, uid, offset=0, limit=100):
        action = 'http://music.163.com/api/user/playlist/?offset={}&limit={}&uid={}'.format(  # NOQA
            offset, limit, uid)
        try:
            data = self.httpRequest('GET', action)
            return data['playlist']
        except (requests.exceptions.RequestException, KeyError) as e:
            log.error(e)
            return -1

    # like
    def like_song(self, songid, like=True, time=25, alg='itembased'):
        action = 'http://music.163.com/api/radio/like?alg={}&trackId={}&like={}&time={}'.format(  # NOQA
            alg, songid, 'true' if like else 'false', time)

        try:
            data = self.httpRequest('GET', action)
            return data["code"] == 200
        except requests.exceptions.RequestException as e:
            log.error(e)
            return -1

   # 收藏歌单
    def subscribe_playlist(self, playlist_id):
        try:
            action = 'http://music.163.com/weapi/playlist/subscribe'
            data = dict(id=playlist_id, t=1)
            self.session.cookies.load()
            csrf = ''
            for cookie in self.session.cookies:
                if cookie.name == '__csrf':
                    csrf = cookie.value
            if csrf == '':
                return False
            data.update({"csrf_token": csrf})
            page = self.session.post(action,
                         data=encrypted_request(data),
                         headers=self.header,
                         timeout=default_timeout)
            return json.loads(page.text)['code'] == 200
        except requests.exceptions.RequestException as e:
            log.error(e)
            return -1

    # 每日推荐歌单 --- 和musicbox保持了一致
    def recommend_resource(self):
        try:
            action = 'http://music.163.com/weapi/v1/discovery/recommend/resource?csrf_token='
            self.session.cookies.load()
            csrf = ''
            for cookie in self.session.cookies:
                if cookie.name == '__csrf':
                    csrf = cookie.value
            if csrf == '':
                return False
            action += csrf
            req = {'csrf_token': csrf}
            page = self.session.post(action,
                         data=encrypted_request(req),
                         headers=self.header,
                         timeout=default_timeout)
            return json.loads(page.text)['recommend']
        except requests.exceptions.RequestException as e:
            log.error(e)
            return -1

    # 每日推荐歌单   --- 和musicbox保持了一致
    def recommend_playlist(self):
        try:
            action = 'http://music.163.com/weapi/v1/discovery/recommend/songs?csrf_token='  # NOQA
            self.session.cookies.load()
            csrf = ''
            for cookie in self.session.cookies:
                if cookie.name == '__csrf':
                    csrf = cookie.value
            if csrf == '':
                return False
            action += csrf
            req = {'offset': 0, 'total': True, 'limit': 20, 'csrf_token': csrf}
            page = self.session.post(action,
                                     data=encrypted_request(req),
                                     headers=self.header,
                                     timeout=default_timeout)
            return json.loads(page.text)['recommend']
        except (requests.exceptions.RequestException, ValueError) as e:
            log.error(e)
            return False

    # 歌单详情
    def playlist_detail(self, playlist_id):
        try:
            action = 'http://music.163.com/weapi/v3/playlist/detail'
            data = dict(id=playlist_id, total="true", limit=1000, n=1000, offest=0)
            self.session.cookies.load()
            csrf = ''
            for cookie in self.session.cookies:
                if cookie.name == '__csrf':
                    csrf = cookie.value
            if csrf == '':
                return False
            data.update({"csrf_token": csrf})
            page = self.session.post(action,
                         data=encrypted_request(data),
                         headers=self.header,
                         timeout=default_timeout)
            return json.loads(page.text)['playlist'].get("tracks", [])
        except requests.exceptions.RequestException as e:
            log.error(e)
            return -1

    # 私人FM
    def personal_fm(self):
        action = 'http://music.163.com/api/radio/get'
        try:
            data = self.httpRequest('GET', action)
            return data['data']
        except requests.exceptions.RequestException as e:
            log.error(e)
            return -1

    # like
    def fm_like(self, songid, like=True, time=25, alg='itembased'):
        action = 'http://music.163.com/api/radio/like?alg={}&trackId={}&like={}&time={}'.format(  # NOQA
            alg, songid, 'true' if like else 'false', time)

        try:
            data = self.httpRequest('GET', action)
            if data['code'] == 200:
                return data
            else:
                return -1
        except requests.exceptions.RequestException as e:
            log.error(e)
            return -1

    # FM trash
    def fm_trash(self, songid, time=25, alg='RT'):
        action = 'http://music.163.com/api/radio/trash/add?alg={}&songId={}&time={}'.format(  # NOQA
            alg, songid, time)
        try:
            data = self.httpRequest('GET', action)
            if data['code'] == 200:
                return data
            else:
                return -1
        except requests.exceptions.RequestException as e:
            log.error(e)
            return -1

    # 搜索单曲(1)，歌手(100)，专辑(10)，歌单(1000)，用户(1002) *(type)*
    def search(self, keywords, stype=1, offset=0, total='true', limit=60):
        action = 'http://music.163.com/api/search/get'
        data = dict(s=keywords, type=stype, offset=offset, total=total, limit=limit)
        return self.httpRequest('POST', action, data).get("result", [])

    # 歌手单曲
    def artists(self, artist_id):
        action = 'http://music.163.com/api/artist/{}'.format(artist_id)
        try:
            data = self.httpRequest('GET', action)
            return data['hotSongs']
        except requests.exceptions.RequestException as e:
            log.error(e)
            return []

    def get_artist_album(self, artist_id, offset=0, limit=50):
        action = 'http://music.163.com/api/artist/albums/{}?offset={}&limit={}'.format(
            artist_id, offset, limit)
        try:
            data = self.httpRequest('GET', action)
            return data['hotAlbums']
        except requests.exceptions.RequestException as e:
            log.error(e)
            return []

    # album id --> song id set
    def album(self, album_id):
        action = 'http://music.163.com/api/album/{}'.format(album_id)
        try:
            data = self.httpRequest('GET', action)
            return data['album']['songs']
        except requests.exceptions.RequestException as e:
            log.error(e)
            return []

    def songs_detail_new_api(self, music_ids, bit_rate=320000):
        action = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='  # NOQA
        self.session.cookies.load()
        csrf = ''
        for cookie in self.session.cookies:
            if cookie.name == '__csrf':
                csrf = cookie.value
        if csrf == '':
            notify('You Need Login', 1)
        action += csrf
        data = {'ids': music_ids, 'br': bit_rate, 'csrf_token': csrf}
        connection = self.session.post(action,
                                       data=encrypted_request(data),
                                       headers=self.header, )
        result = json.loads(connection.text)
        return result['data']
    
    def dig_info(self, data, dig_type):
        temp = []
        if not data:
            return []
        if dig_type == 'songs' or dig_type == 'fmsongs':
            urls = geturls_new_api([s["id"] for s in data])
            timestamp = time.time()
            # api 返回的 urls 的 id 顺序和 data 的 id 顺序不一致
            # 为了获取到对应 id 的 url，对返回的 urls 做一个 id2index 的缓存
            # 同时保证 data 的 id 顺序不变
            url_id_index = {}
            for index, url in enumerate(urls):
                url_id_index[url["id"]] = index
            for s in data:
                url_index = url_id_index.get(s["id"])
                if url_index is None:
                    log.error("can't get song url, id: %s", s["id"])
                    continue
                s["url"] = urls[url_index]["url"]
                s["br"] = urls[url_index]["br"]
                s["expires"] = urls[url_index]["expi"]
                s["get_time"] = timestamp
            temp = Parse.songs(data)

        elif dig_type == 'artists':
            artists = []
            for i in range(0, len(data)):
                artists_info = {
                    'artist_id': data[i]['id'],
                    'artists_name': data[i]['name'],
                    'alias': ''.join(data[i]['alias'])
                }
                artists.append(artists_info)
            return artists

        elif dig_type == 'albums':
            for i in range(0, len(data)):
                albums_info = {
                    'album_id': data[i]['id'],
                    'albums_name': data[i]['name'],
                    'artists_name': data[i]['artist']['name']
                }
                temp.append(albums_info)

        elif dig_type == 'top_playlists':
            temp = Parse.playlists(data)

        elif dig_type == 'playlist_class_detail':
            log.debug(data)
            temp = self.playlist_class_dict[data]
        return temp
