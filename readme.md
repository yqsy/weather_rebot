
<!-- TOC -->

- [1. 用途](#1-用途)
- [2. 说明](#2-说明)

<!-- /TOC -->

<a id="markdown-1-用途" name="1-用途"></a>
# 1. 用途

树莓派播报天气信息.爬墨迹天气的数据,使用mplayer播放.

<a id="markdown-2-说明" name="2-说明"></a>
# 2. 说明

持久文件
```
# 日志
/var/log/weather_rebot/weather_rebot.log
```


```bash
# 创建日志目录
sudo mkdir /var/log/weather_rebot
sudo chown $(id -u):$(id -g) /var/log/weather_rebot

# 创建起床音乐
mkdir ~/env/voice-station
cd ~/env/voice-station
# 1.mp3

# 启动
python3 weather_rebot.py
```
