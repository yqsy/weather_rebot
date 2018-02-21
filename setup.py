from setuptools import setup


setup(
    name="weather_rebot",
    version="1.0.0",
    license='http://www.apache.org/licenses/LICENSE-2.0',
    description="weather_rebot for raspberry",
    author='yqsy021',
    author_email='yqsy021@126.com',
    url='https://github.com/yqsy/weather_rebot',
    packages=['weather_rebot'],
    install_requires=['beautifulsoup4>=4.6.0',
                      'requests>=2.18.4'],
    entry_points="""
    [console_scripts]
    weather_rebot = weather_rebot.weather_rebot:main
    """,
)
