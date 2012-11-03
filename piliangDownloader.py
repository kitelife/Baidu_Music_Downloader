#!/usr/bin/env python
#coding: utf-8

import os
import gevent

singerList = ["任贤齐", "罗大佑", "朴树", "陈奕迅", "方大同", "周杰伦", "曲婉婷", "莫文蔚", "孙燕姿"]
cmdList = list()

for singer in singerList:
	cmdList.append('./getBaiduMusic.py ' + singer + ' -d Music &')

threads = [gevent.spawn(os.system, task) for task in cmdList]
print len(threads)
gevent.joinall(threads)