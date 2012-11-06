#!/usr/bin/env python
#coding: utf-8

import os
import gevent
import config

cmdList = list()

optionalArgs = ' -d ' + config.musicDir + ' &'

if config.album:
	optionalArgs = ' -a' + optionalArgs

for singer in config.singerList:
	cmdList.append('python getBaiduMusic.py ' + singer + optionalArgs)

threads = [gevent.spawn(os.system, task) for task in cmdList]
gevent.joinall(threads)
