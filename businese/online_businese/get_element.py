# 本页面为具体的处理页面数据
import os

from tools.file_opt import fileOpt
from tools.project_path import pathUtil
from requests_page.get_page_element import GetPage


class GetHsexElement(GetPage):

    def get_pic_and_title(self, url, ip_port):
        element = self.get_page_element(url=url, proxies=ip_port)
        if element is not None:
            ele_list = element.xpath('//div[@id="container"]/div[@class="row body"]/div[@class!="clearfix"]')

            title_xpath = '//div[@class="image"]/@title'
            href_xpath = '//div[@class="image"]/@style'
            author_xpath = '//div[@id="container"]/div[@class="row body"]/div[@class!="clearfix"]/div[' \
                           '@class="thumbnail"]/div[last()]/p/a/text()'

            find_url_list = []
            find_title_list = []
            find_author_list = []

            url_list = []
            title_list = []
            author_list = []

            for n in ele_list:
                find_title_list = n.xpath(title_xpath)
                find_url_list = n.xpath(href_xpath)
                find_author_list = n.xpath(author_xpath)
                break

            for i in range(0, len(ele_list)):
                url = eval(find_url_list[i].replace('background-image: url(', "").replace(')', ""))
                title = find_title_list[i].replace(' ', "")
                author = find_author_list[i]
                # 处理一下名字里是不是有windows保存文件时不支持的特殊字符
                sets = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
                for char in title:
                    if char in sets:
                        title = title.replace(char, '')
                if title.strip() != '':
                    title_list.append(title)
                    url_list.append(url)
                    author_list.append(author.strip())

            value = {"title": title_list,
                     "pic_url": url_list,
                     "author": author_list}
            return value
        return None

    def get_pic_content(self, url):
        """
        获取图片的内容
        :return:
        """
        return self.get_page_element(url=url)

    def get_network_status(self, url, ip_port):
        element = self.get_page_element(url=url, proxies=ip_port)
        if element is None:
            return False
        else:
            return True

    def download_picture(self, pic_url, pic_name):
        """
        下载图片
        :param pic_name:
        :param pic_url:
        :return:
        """
        pic_element = self.get_page_element(url=pic_url)
        if pic_element is not None:
            pic_path = pathUtil().resource_path(os.path.join('res', pic_name + '.jpg'))  # 打包后使用

            with open(pic_path, 'wb+') as f:
                f.write(pic_element)
            f.close()
            if fileOpt().wait_file_exists(pic_path):
                return pic_path
            else:
                return None
        else:
            return None

    def delete_picture(self, pic_name):
        """
        删除临时目录的文件
        :param pic_name:
        :return:
        """
        file_opt = fileOpt()
        path = pathUtil().rootPath
        # pic_path = path + '/file/temp/' + pic_name + '.jpg'  # 代码模式使用
        pic_path = pathUtil().resource_path(os.path.join('res', pic_name + '.jpg'))  # 打包后使用

        file_opt.delete_file(pic_path)

    def move_picture(self, pic_name):
        """
        该方法仅限代码模式使用
        :param pic_name:
        :return:
        """
        file_opt = fileOpt()
        path = pathUtil().rootPath
        pic_path = path + '/file/temp/' + pic_name + '.jpg'
        folder_path = path + '/file/result/'
        file_opt.move_file(pic_path, folder_path)
