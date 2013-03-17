#coding: utf-8

import platform

def get_platform_encoding():
    platform_encoding = 'utf-8'
    if platform.system() not in ['Linux', 'Darwin']:
        platfrom_encoding = 'gbk'
    return platform_encoding
