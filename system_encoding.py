#coding: utf-8

import platform

DEFAULT_ENCODING = 'utf-8'

system_type = platform.system()
if system_type not in ['Linux', 'Darwin']:
	DEFAULT_ENCODING = 'gbk'