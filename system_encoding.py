#coding: utf-8

import platform

DEFAULT_ENCODING = 'utf-8'

if platform.system() != 'Linux':
	DEFAULT_ENCODING = 'gbk'