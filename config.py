#coding: utf-8

from system_encoding import DEFAULT_ENCODING

# 歌手姓名列表
singerList = ['蔡琴', '刘若英']

for index, singer in enumerate(singerList):
	singerList[index] = singer.decode('utf-8').encode(DEFAULT_ENCODING)

# 音乐存储目录
musicDir = '~/Music'

# 是否按照专辑下载
album = True
