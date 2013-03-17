#!/usr/bin/env python
#coding: utf-8

import os
import gevent
import multi_config

cmd_list = list()

optional_args = ' -d ' + multi_config.music_dir + ' &'

if multi_config.album:
	optional_args = ' -a' + optional_args

for singer in multi_config.singer_list:
	cmd_list.append('python baidu_music_downloader.py -s ' + singer + optional_args)

threads = [gevent.spawn(os.system, task) for task in cmd_list]
gevent.joinall(threads)
