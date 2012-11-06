百度音乐下载器
===============

**使用方法(Linux下)**：

- 命令行输入：python getBaiduMusic.py 歌手姓名 [-a] [-d 音乐存储目录]

其中[]内的选项是可选的，歌手姓名是必须的，且必须紧接getBaiduMusic.py。选项-a是指定按专辑下载歌手的所有音乐，如果没有-a选项，则下载所有单曲

- 如果想同时下载多个歌手的音乐，则可以先在文件config.py设定相关配置信息，然后执行：python piliangDownloader.py
