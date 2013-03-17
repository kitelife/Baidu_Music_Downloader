#coding: utf-8

from system_encoding import get_platform_encoding

platform_encoding = get_platform_encoding()

# 歌手姓名列表
singer_list = ['王菲', '阿桑']

for index, singer in enumerate(singer_list):
	singer_list[index] = singer.decode('utf-8').encode(platform_encoding)

# 音乐存储目录
music_dir = '~/Music'

# 是否按照专辑下载
album = True
