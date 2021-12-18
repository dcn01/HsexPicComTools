# 本模块为获取页面
import random
import time

import requests
from PyQt5.QtCore import pyqtSignal, QObject
from lxml import etree
from requests import Session
from retrying import retry

from tools.Enum_tools import user_agent


class GetPage(QObject):
    log_out = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.p = None
        self.re = Session()
        self.headers = {"user-agent": user_agent.chrome_macos.value}
        self.count_i = 0

    @retry(stop_max_attempt_number=5)  # 引入的第三方模块，用于失败自动重试,重试10次结束
    def get_page_element(self, url, proxies=None):
        """
        获取页面信息并返回
        :param url: url
        :param proxies: 代理ip，请传入字典形式 {'http': 'http://199.1.1.1:1234'}
        :return: html格式化过的页面元素
        """
        if proxies is not None:
            if "：" in proxies:
                proxies = proxies.replace("：", ":")
            if "socks5h" not in proxies:
                self.p = {"https": "socks5h://" + proxies,
                           "http": "socks5h://" + proxies}

        self.re.close()  # 避免重试时有太多连接，开始时就先关闭一下
        sleep_time = random.randint(3, 5)
        time.sleep(sleep_time)  # 稍微等待以下，减小服务器压力
        element = None
        try:
            self.count_i = self.count_i + 1
            element = self.re.get(url=url, stream=True, timeout=(20, 300), headers=self.headers, proxies=self.p)
        except requests.RequestException as e:
            print(e)
            if self.count_i >= 5:
                self.count_i = 0
                return None
        if element is None or element == '':
            return None
        if element.status_code != 200:
            print("返回的页面状态码异常:%d" % element.status_code)
            return None
        element.encoding = 'utf-8'
        if 'text/html' in element.headers.get('Content-Type'):
            # 如果是html的，就格式化一下return
            html_element = etree.HTML(element.text)
            return html_element
        else:
            # 不是网页就是文件啦，直接返回内容
            return element.content
