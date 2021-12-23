# 本模块是对文件和文件夹的操作
import os
import shutil
import time

from retrying import retry


class fileOpt(object):

    def delete_file(self, file_path):
        """
        删除单独的文件
        :param file_path: 文件路径
        :return:
        """
        if os.path.exists(file_path):
            os.remove(path=file_path)

    def delete_file_folder(self, file_path):
        """
        删除文件夹
        :param file_path: 文件夹路径
        :return:
        """
        if os.path.exists(file_path):
            os.removedirs(file_path)

    @retry(stop_max_attempt_number=5)
    def wait_file_exists(self, file_path):
        """
        检查路径是否存在该文件
        :param file_path:
        :return:
        """
        try:
            if os.path.exists(file_path):
                return True
            else:
                print("%s 文件不存在或还未生成，请检查或稍后再操作" % file_path)
                time.sleep(2)
                raise
        except:
            raise

    def move_file(self, old_file_path, new_folder_path):
        """
        移动文件到新的文件夹
        :param new_folder_path:
        :param old_file_path:
        :return:
        """
        if os.path.exists(old_file_path) and os.path.exists(new_folder_path):
            try:
                shutil.move(old_file_path, new_folder_path)
            except OSError:
                pass

    def cope_file(self, old_file_path, new_folder_path):
        """
        复制文件到新的文件夹
        :param new_folder_path:
        :param old_file_path:
        :return:
        """
        if os.path.exists(old_file_path) and os.path.exists(new_folder_path):
            try:
                shutil.copy(old_file_path, new_folder_path)
            except OSError:
                pass

    def get_file_list(self, path):
        """
        获取目录下所有的文件路径
        :param path: 目录
        :return:
        """
        file_names = [os.path.join(path, name) for path, subdirs, files in os.walk(path) for name in files]
        img_list=[]
        for i in range(len(file_names)):
            if file_names[i].endswith('jpg') or file_names[i].endswith('png') or file_names[i].endswith('JPG') or file_names[i].endswith('PNG'):
               img_list.append(file_names[i])
        return img_list