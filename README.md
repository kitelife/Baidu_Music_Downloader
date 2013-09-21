百度音乐下载器
===============

**安装依赖**

- Python2.7解释器(Windows下需要设定环境变量，才能在cmd中使用python命令)

- 安装库requests, beautifulsoup, gevent(使用python包管理器pip install或者easy\_install，ubuntu下还可以使用apt-get install相应的库)


**使用方法(Linux下)**：

- 根据歌手名下载：python baidu_music_downloader.py -s 歌手姓名 [-a] [-d 音乐存储目录]

其中方括号内的选项是可选的，歌手姓名是必须的。选项-a是指定按专辑下载歌手的所有音乐，如果没有-a选项，则下载所有单曲

- 根据歌名下载：python baidu_music_downloader.py -m 歌名 [-d 音乐存储目录]

执行该命令后，会显示一个歌曲列表供用户选择，输入某行前面的数字编号并回车，就会下载那首歌曲。

- 如果想同时下载多个歌手的音乐，则可以先在文件multi\_config.py设定相关配置信息，然后执行：python multi_downloader.py

**使用方法(Windows下)**:

- 与Linux下的使用方法一致，只是需要注意设定配置文件multi_config.py中music_dir一项的值，默认值为linux下用户home目录中Music目录(~/Music)

- Windows下，某些播放器显示出来的歌词可能是乱码，这时就需要对歌词进行转码，[这个小脚本](https://github.com/youngsterxyf/ToolsForMyself/blob/master/change_encoding.py)可供使用。这个脚本会对指定目录下的所有.lrc扩展名的文件从utf-8编码转成gbk编码。(注：该脚本依赖库chardet来检测文件的编码)

**更新**

- 2013-03-17：重构部分代码
- 2013-03-01：百度音乐网站修改了一些前端代码，导致程序失效，修正。
- 2012-11-26：支持单曲下载
