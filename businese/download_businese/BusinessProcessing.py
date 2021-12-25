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

    def goto_picture(self, url, pic_path_save, ip_port=None):
        """
        开始处理页面上的图片
        :param ip_port: 代理ip端口
        :param pic_path_save: 日志存放的文件夹路径
        :param url: url
        :return:
        """
        log_path_pic = pic_path_save + '/' + time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()) + "fail_pic.log"
        log_path_page = pic_path_save + '/' + time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()) + "fail_page.log"
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
                    if fileOpt().wait_file_exists(pic_path_save + '/' + date_list[i]) is False:
                        os.makedirs(pic_path_save + '/' + date_list[i])
                    for n in range(0, 1000):
                        pic_path = pic_path_save + '/' + date_list[i] + '/' + title_list[i] + '_' + author_list[i] + '_' + str(n) + '.jpg'
                        if fileOpt().wait_file_exists(pic_path) is False:
                            with open(pic_path, 'wb+') as f:
                                f.write(pic_content)
                            f.close()
                            break
                else:
                    with open(log_path_pic, 'a+') as f:
                        f.write("图片：%s 获取失败，请手动获取，url: %s 作者：%s " % (title_list[i], author_list[i], url_list[i]))
                        f.close()
        else:
            with open(log_path_pic, 'a+') as f:
                f.write("页面: %s 访问失败，稍后请重新获取" % url)
                f.close()
