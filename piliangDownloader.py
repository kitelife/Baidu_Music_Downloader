#!/usr/bin/env python
#coding: utf-8

import os
import gevent

#singerList = ["任贤齐", "罗大佑", "朴树", "陈奕迅", "方大同", "周杰伦", "曲婉婷", "莫文蔚", "孙燕姿"]
singerList = ["曹格", "张震岳"]
cmdList = list()

# 如果想下载歌手的所有专辑，而不是单曲，则设为True
album = True

optionalArgs = ' -d ~/Music &'
if album:
	optionalArgs = ' -a' + optionalArgs

for singer in singerList:
	cmdList.append('./getBaiduMusic.py ' + singer + optionalArgs)

threads = [gevent.spawn(os.system, task) for task in cmdList]
print len(threads)
gevent.joinall(threads)