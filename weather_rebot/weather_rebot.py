import os
import os.path
import re
import sys
import requests
import traceback
from datetime import datetime
from bs4 import BeautifulSoup
import logging

FORMAT = "%(asctime)s %(thread)d %(levelname)s %(filename)s:%(lineno)d:%(funcName)s %(message)s"

LOG_FILE = "/var/log/weather_rebot/weather_rebot.log"

LOG_DIR = os.path.dirname(LOG_FILE)
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.FileHandler(LOG_FILE,  mode="a")],
    format=FORMAT
)

logger = logging.getLogger(__name__)


def error_handler(etype, value, tb):
    err_str = '{} {} {}'.format(etype, value, traceback.format_tb(tb))
    logger.error(err_str)

    # make sure exit
    exit(-1)


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36"
}


def get_pm():
    res = requests.get(
        "https://tianqi.moji.com/pm/china/shanghai/shanghai", headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    pm_num = soup.find("div", attrs={"class": "aqi_info_detail"}).em.getText()
    pm_hint = soup.find(
        "div", attrs={"class": "aqi_info_detail"}).span.getText()

    return pm_num, pm_hint


def main():
    sys.excepthook = error_handler

    res = requests.get(
        "https://tianqi.moji.com/weather/china/shanghai/shanghai", headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    cur_temperature = soup.find(
        "div", attrs={"class": "wea_weather clearfix"}).em.getText()
    weather = soup.find(
        "div", attrs={"class": "wea_weather clearfix"}).b.getText()
    hunidity = soup.find(
        "div", attrs={"class": "wea_about clearfix"}).span.getText()
    hint = soup.find("div", attrs={"class": "wea_tips clearfix"}).em.getText()

    tmp_temperature = soup.find("ul", attrs={"class": "days clearfix"})
    two_temperature = tmp_temperature.findAll(
        "li")[2].getText()  # "4° / 9°"  regular: (\d)° \/ (\d)°

    regex = r"(\d*)° \/ (\d*)°"

    matches = list(re.finditer(regex, two_temperature))

    if len(matches) != 1:
        raise Exception("temperatur error")

    if len(matches[0].groups()) != 2:
        raise Exception("temperatur error")

    low_temperature = matches[0].groups()[0]
    high_temperature = matches[0].groups()[1]

    today = datetime.now().strftime("%Y年%m月%d日")

    pm_num, pm_hint = get_pm()

    text = "早上好! 今天是{} ,{}到{}度,{},pm{},{},{}".format(
        today, low_temperature, high_temperature, weather, pm_num, pm_hint, hint
    )

    logger.info(text)

    req_url = "http://tts.baidu.com/text2audio?\
    idx=1&tex={}&cuid=baidu_speech_demo&cod=2&lan=zh&ctp=1&pdt=1&spd=4&per=4&vol=5&pit=5".format(text)

    os.system('mplayer -vo alsa ~/env/voice-station/1.mp3')

    os.system('mplayer -vo alsa "{}"'.format(req_url))


if __name__ == "__main__":
    main()
