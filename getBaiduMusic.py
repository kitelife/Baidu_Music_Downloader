#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os
import platform
import requests
import re
from BeautifulSoup import BeautifulSoup

GLOBAL_VARIABLE = dict()
HAVEDOWNLOADED = list()

def downloadMusic(musicName, musicId):
	url = 'http://music.baidu.com/song/' + musicId + '/download'
	print url
	musicObject = requests.get(url)
	if musicObject.status_code == 200:
		musicSoup = BeautifulSoup(musicObject.content)
		downloadItem = musicSoup.find('div', attrs={'class': 'operation clearfix'}).find('a')
		if downloadItem['href']:
			downloadUrl = downloadItem['href'].replace('/data/music/file?link=', '')
			if platform.system() == 'Linux':
				downloadCmd = 'wget ' + downloadUrl + ' -O ' + GLOBAL_VARIABLE['savePath'] + \
					'/' + musicName + '.mp3'
				downloadCmd = downloadCmd.encode('utf-8')
				os.system(downloadCmd)
				HAVEDOWNLOADED.append(musicName)
			else:
				import urllib2
				print downloadUrl
				try:
					req = urllib2.Request(downloadUrl)
					response = urllib2.urlopen(req)
					with open(GLOBAL_VARIABLE['savePath'] + '/' + musicName +'.mp3', 'w') \
					as musicHandler:
						musicHandler.write(response.read())
					HAVEDOWNLOADED.append(musicName)
				except Exception, e:
					print e.message


def getSearchResultNum(searchFirstPageResult):
	soup = BeautifulSoup(searchFirstPageResult)
	return soup.find('span', attrs={'class': 'number'}).text


def parseMusicList(musicListPageContent):
	soup = BeautifulSoup(musicListPageContent)
	musicItemList = soup.findAll('div', attrs={'class': 'song-item clearfix'})
	for musicItem in musicItemList:
		author_list = musicItem.find('span', attrs={'class' : 'author_list'})['title'].split(',')
		if GLOBAL_VARIABLE['singerName'] in author_list:
			music = musicItem.find('span', attrs={'class' : 'song-title'}).find('a')
			musicTitle = music.text.strip().replace(' ', '_')
			if not musicTitle in HAVEDOWNLOADED:
				downloadMusic(musicTitle, music['href'].split('/')[-1])


def parseAlbumList(albumPageContent):

	def downloadAlbum(albumUrl):
		albumObject = requests.get(albumUrl)
		if albumObject.status_code == 200:
			albumSoup = BeautifulSoup(albumObject.content)
			albumItems = albumSoup.findAll('div', attrs={'class': 'song-item'})
			for albumItem in albumItems:
				music = albumItem.find('span', attrs={'class': 'song-title'}).find('a')
				if music:
					musicName = music.text.strip().replace(' ', '_')
					musicId = music['href'].replace('/song/', '')
					downloadMusic(musicName, musicId)

	soup = BeautifulSoup(albumPageContent)
	albumList = soup.findAll('div', attrs={'class': 'title clearfix'})
	for albumItem in albumList:
		album = albumItem.find('a', attrs={'href': re.compile('/album/\d+$')})
		albumName = album.text.replace('《'.decode('utf-8'), '').replace('》'.decode('utf-8'), '')
		albumName = albumName.strip().replace(' ', '_')
		albumUrl = 'http://music.baidu.com/' + album['href']
		basePath = GLOBAL_VARIABLE['savePath']
		GLOBAL_VARIABLE['savePath'] += '/' + albumName
		if not os.path.exists(GLOBAL_VARIABLE['savePath']):
			os.mkdir(GLOBAL_VARIABLE['savePath'])
		downloadAlbum(albumUrl)
		GLOBAL_VARIABLE['savePath'] = basePath


def searchSingerMusic(singerName, album=False):
	url = 'http://music.baidu.com/search?key=' + singerName
	if album:
		url = 'http://music.baidu.com/search/album?key=' + singerName

	pageObject = requests.get(url)
	if pageObject.status_code == 200:
		if album:
			totalNum = getSearchResultNum(pageObject.content)
			parseAlbumList(pageObject.content)
			start, size = 10, 10
			while start < totalNum:
				url = 'http://music.baidu.com/search/album?key=' + singerName + '&start=' + \
					str(start) + '&size=' + str(size)
				pageObject = requests.get(url)
				parseAlbumList(pageObject.content)
				start += size
		else:
			totalNum = getSearchResultNum(pageObject.content)
			parseMusicList(pageObject.content)
			start, size = 20, 20
			while start < totalNum:
				url = 'http://music.baidu.com/search/song?key=' + singerName + '&start=' + \
					str(start) + '&size=' + str(size)
				pageObject = requests.get(url)
				parseMusicList(pageObject.content)
				start += size


def main():
	album = False
	dirname = ''
	if '-a' in sys.argv:
		album = True
	if '-d' in sys.argv:
		dirname = sys.argv[sys.argv.index('-d') + 1]
		if not dirname.endswith('/'):
			dirname += '/'
	singerName = sys.argv[1]
	savePath = dirname + singerName.replace(' ', '_')
	if not os.path.exists(savePath):
		os.mkdir(savePath)
	GLOBAL_VARIABLE['savePath'] = unicode(savePath, "utf-8")
	GLOBAL_VARIABLE['singerName'] = unicode(singerName, 'utf-8')

	searchSingerMusic(singerName, album = album)


if __name__ == '__main__':
	main()