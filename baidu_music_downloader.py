#!/usr/bin/env python
#-*- coding: utf-8 -*-

import argparse
import os
import requests
import urllib2
import re
import platform
from BeautifulSoup import BeautifulSoup
from system_encoding import get_platform_encoding

platform_encoding = get_platform_encoding()

GLOBAL_VARIABLE = dict()
HAVEDOWNLOADED = list()


def download_music(music_name, music_id):
    url = 'http://music.baidu.com/song/' + music_id + '/download'
    print url
    music_object = None
    try:
        music_object = requests.get(url)
    except Exception:
        print 'music_object: requests.get Error'
    if music_object and music_object.status_code == 200:
        download_item = None
        music_soup = BeautifulSoup(music_object.content)
        div_for_download = music_soup.find('div', attrs={'class': 'operation clearfix'})
        if div_for_download:
            download_item = div_for_download.find('a')
        if download_item:
            download_href = download_item.get('href', None)
        if download_item and download_href:
            download_url = download_href.replace('/data/music/file?link=', '')
            if platform.system() == 'Linux':
                download_cmd = 'wget ' + download_url + ' -O ' + GLOBAL_VARIABLE['save_path'] + \
                    os.sep + music_name + '.mp3'
                download_cmd = download_cmd.encode(platform_encoding)
                print download_cmd
                os.system(download_cmd)
                HAVEDOWNLOADED.append(music_name)
            else:
                print music_name, download_url
                try:
                    req = urllib2.Request(download_url)
                    response = urllib2.urlopen(req)
                    with open(GLOBAL_VARIABLE['save_path'] + os.sep + music_name +'.mp3', 'wb') \
                    as music_handler:
                        music_handler.write(response.read())
                    HAVEDOWNLOADED.append(music_name)
                except Exception, e:
                    print e.message


def download_lrc(music_name, music_id):
    url = 'http://music.baidu.com/song/' + music_id + '/lyric'
    lrc_object = None
    try:
        lrc_object = requests.get(url)
    except Exception:
        print 'lrc_object: requests.get Error'
    if lrc_object and lrc_object.status_code == 200:
        lrc_soup = BeautifulSoup(lrc_object.content)
        download_url = None
        download_item = lrc_soup.find('a', attrs={'class': 'down-lrc-btn'})
        if download_item:
            download_url = download_item.get('href', None)
        if download_item and download_url:
            print 'LRC: ', download_url
            if platform.system() == 'Linux':
                cmd = 'wget ' + download_url + ' -O ' + GLOBAL_VARIABLE['save_path'] + \
                    os.sep + music_name + '.lrc'
                cmd = cmd.encode(platform_encoding)
                os.system(cmd)
            else:
                try:
                    req = urllib2.Request(download_url)
                    response = urllib2.urlopen(req)
                    with open(GLOBAL_VARIABLE['save_path'] + os.sep + music_name + '.lrc', 'w') \
                    as lrc_handler:
                        lrc_handler.write(response.read())
                except Exception, e:
                    print e.message


def get_searchresult_num(search_firstpage_result):
    soup = BeautifulSoup(search_firstpage_result)
    result_num_ele = soup.find('span', attrs={'class': 'number'})
    if result_num_ele:
        print result_num_ele.text
        return result_num_ele.text
    else:
        return 0


def parse_music_list(musiclistpage_content):
    soup = BeautifulSoup(musiclistpage_content)
    musicitem_list = soup.findAll('div', attrs={'class': 'song-item clearfix'})
    for music_item in musicitem_list:
        author_list = []
        author_list_ele = music_item.find('span', attrs={'class': 'author_list'})
        if author_list_ele:
            author_list = author_list_ele.get('title', '').split(',')
        if GLOBAL_VARIABLE['singer_name'] in author_list:
            music = music_item.find('span', attrs={'class' : 'song-title'}).find('a')
            music_title = music.text.strip().replace("#", "").replace(' ', '_')
            for punc in ['《', '》', '(', ')', '（', '）', '/']:
                music_title = music_title.replace(punc.decode('utf-8'), '')
            if not music_title in HAVEDOWNLOADED:
                music_id = music['href'].split('/')[-1]
                print music_title
                download_music(music_title, music_id)
                download_lrc(music_title, music_id)


def parse_album_list(albumpage_content):
    
    def download_album(album_url):
        album_object = None
        try:
            album_object = requests.get(album_url)
        except Exception:
            print 'album_object: requests.get Error'
        if album_object and album_object.status_code == 200:
            album_soup = BeautifulSoup(album_object.content)
            album_items = album_soup.findAll('div', attrs={'class': 'song-item'})
            for album_item in album_items:
                music = album_item.find('span', attrs={'class': 'song-title '}).find('a')
                music_href = music.get('href', None)
                if music and music_href:
                    music_name = music.text.strip().replace(' ', '_')
                    music_id = music_href.replace('/song/', '')
                    download_music(music_name, music_id)
                    download_lrc(music_name, music_id)

    soup = BeautifulSoup(albumpage_content)
    album_list = soup.findAll('div', attrs={'class': 'title clearfix'})
    for album_item in album_list:
        album = album_item.find('a', attrs={'href': re.compile('/album/\d+$')})
        album_name = album.text.strip().replace(' ', '_')
        for punc in ['《', '》', '(', ')', '（', '）', '/']:
            album_name = album_name.replace(punc.decode('utf-8'), '')
        album_url = 'http://music.baidu.com/' + album['href']
        base_path = GLOBAL_VARIABLE['save_path']
        GLOBAL_VARIABLE['save_path'] += os.sep + album_name
        if not os.path.exists(GLOBAL_VARIABLE['save_path']):
            os.mkdir(GLOBAL_VARIABLE['save_path'].encode(platform_encoding))
        download_album(album_url)
        GLOBAL_VARIABLE['save_path'] = base_path


def search_singer_music(singer_name, album=False):
    url = 'http://music.baidu.com/search?key=' + singer_name
    if album:
        url = 'http://music.baidu.com/search/album?key=' + singer_name
    page_object = None
    try:
        print url
        page_object = requests.get(url)
    except Exception:
        print 'page_object: requests.get Error'
    if page_object and page_object.status_code == 200:
        if album:
            total_num = int(get_searchresult_num(page_object.content))
            parse_album_list(page_object.content)
            start, size = 10, 10
            while start < total_num:
                url = 'http://music.baidu.com/search/album?key=' + singer_name + '&start=' + \
                    str(start) + '&size=' + str(size)
                page_object = None
                try:
                    page_object = requests.get(url)
                except Exception:
                    print 'page_object: requests.get Error'
                if page_object and page_object.status_code == 200:
                    parse_album_list(page_object.content)
                start += size
        else:
            total_num = int(get_searchresult_num(page_object.content))
            parse_music_list(page_object.content)
            start, size = 20, 20
            while start < total_num:
                url = 'http://music.baidu.com/search/song?key=' + singer_name + '&start=' + \
                    str(start) + '&size=' + str(size)
                page_object = None
                try:
                    page_object = requests.get(url)
                except Exception:
                    print 'page_object: requests.get Error'
                if page_object and page_object.status_code == 200:
                    parse_music_list(page_object.content)
                start += size


def get_topten_list(music_name):
    topten_list = []
    album_name = ''
    url = 'http://music.baidu.com/search?key=' + music_name
    response = None
    try:
        response = requests.get(url)
    except Exception:
        print 'get_topten_list requests.get Error'
    if response and response.status_code == 200:
        responseSoup = BeautifulSoup(response.content)
        songitem_list = responseSoup.findAll('div', attrs={'class': 'song-item clearfix'})
        singer_list = []
        if songitem_list:
            for song_item in songitem_list:
                title_item = song_item.find('span', attrs={'class': 'song-title'})
                a = title_item.find('a')
                if title_item and a:
                    song_id = a['href'].split('/')[-1]
                    song_title = a.text
                singer_item = song_item.find('span', attrs={'class': 'author_list'})
                if singer_item and singer_item.get('title', None):
                    singer_list = singer_item['title'].split(',')

                album_item = song_item.find('span', attrs={'class': 'album-title'})
                if album_item and album_item.find('a'):
                    album_name = album_item.find('a').text
                topten_list.append([song_id, song_title, singer_list, album_name])
    return topten_list


def select_entry(music_list):
    for index, music in enumerate(music_list):
        print index,'\t', music[1], '\t',
        for singer in music[2]:
            print singer,
        print '\t',
        print music[3]
    select = input('Please input a number to select music: ')
    return int(select)


def get_parser():
    arg_parser = argparse.ArgumentParser(description='Tool to download music from http://music.baidu.com')
    arg_parser.add_argument('-s', '--singer', help='singer name whose music will be downloaded', type=str)
    arg_parser.add_argument('-m', '--music', help='name of music you want to download', type=str)
    arg_parser.add_argument('-a', '--album', help='if you download musics as album?', action='store_true')
    arg_parser.add_argument('-d', '--directory', help='name of target directory to store music', default='./', type=str)
    
    return  arg_parser


def main():
    arg_parser = get_parser()
    args = vars(arg_parser.parse_args())
    if not (args['singer'] or args['music']):
        arg_parser.print_usage()
        return

    dirname = args['directory']
    
    if args['music']:
        music_name = args['music'].decode(platform_encoding).encode('utf-8')
        top_ten = get_topten_list(music_name)
        user_select = select_entry(top_ten)
        if user_select in range(0, len(top_ten)):
            save_path = dirname
            if not os.path.exists(save_path):
                os.mkdir(save_path)
            GLOBAL_VARIABLE['save_path'] = unicode(save_path, platform_encoding)
            selected_item = top_ten[user_select]
            singer_str = '.'.join(selected_item[2])
            song_title = selected_item[1].replace(' ', '_').replace('\'', '\\\'')
            download_music(song_title+'-'+singer_str, selected_item[0])
            download_lrc(song_title+'-'+singer_str, selected_item[0])
    else:
        singer_name = args['singer']
        if not dirname.endswith(os.sep):
            dirname += os.sep
        save_path = dirname + singer_name.replace(' ', '_')
        if not os.path.exists(save_path):
            os.mkdir(save_path)

        GLOBAL_VARIABLE['save_path'] = save_path.decode(platform_encoding)
        GLOBAL_VARIABLE['singer_name'] = singer_name.decode(platform_encoding)

        singer_name = singer_name.decode(platform_encoding).encode('utf-8')
        search_singer_music(singer_name, album = args['album'])


if __name__ == '__main__':
    main()
