import os
import random
import time

from tools.pic_hash import PictureHashCompare
from tools.file_opt import fileOpt
from businese.download_businese.get_element import GetHsexElement


class executeElement(GetHsexElement):

    def __init__(self):
        super().__init__()
        self.pic_cmp = PictureHashCompare()
        self.file = fileOpt()

    def goto_picture(self, url, log_path_flor, ip_port=None):
        """
        开始处理页面上的图片
        :param ip_port: 代理ip端口
        :param log_path_flor: 日志存放的文件夹路径
        :param url: url
        :return:
        """
        video_dict = self.get_pic_and_title(url, ip_port)
        if video_dict is not None:
            title_list = list(video_dict.get('title'))
            url_list = list(video_dict.get('pic_url'))
            author_list = list(video_dict.get('author'))
            date_list = list(video_dict.get("date"))

            for i in range(len(url_list)):
                if url_list[i] is None or url_list[i] == '':
                    continue
                pic_content = self.get_pic_content(url_list[i])
                if pic_content is not None:
                    if fileOpt().wait_file_exists(log_path_flor + '/' + date_list[i]) is False:
                        os.makedirs(log_path_flor + '/' + date_list[i])
                    for n in range(0, 1000):
                        pic_path = log_path_flor + '/' + date_list[i] + '/' + title_list[i] + '_' + author_list[i] + '_'+ str(n) +'.jpg'
                        if fileOpt().wait_file_exists(pic_path) is False:
                            with open(pic_path, 'wb+') as f:
                                f.write(pic_content)
                            f.close()
                            break

