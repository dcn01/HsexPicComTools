import time

from PyQt5.QtCore import QThread, pyqtSignal, QWaitCondition, QMutex

from tools.file_opt import fileOpt
from tools.pic_hash import PictureHashCompare


class signalThreading(QThread):
    def __init__(self):
        super().__init__()

    sin_out = pyqtSignal(str)
    sin_work_status = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        # 设置工作状态和初始值
        self.working = True
        self.cond = QWaitCondition()
        self.mutex = QMutex()

        self.pic_com = PictureHashCompare()
        self.file = fileOpt()

    # def __del__(self):
    #     # 线程状态改为和线程终止
    #     self.working = False
    #     self.wait()

    def pause(self):
        """
        线程暂停
        :return:
        """
        self.working = False

    def start_execute_init(self):
        """
        线程开始
        :return:
        """
        self.working = True
        self.cond.wakeAll()

    def get_business_param(self, origin_pic_path, select_pic_path, result_pic_path):
        """
        获取一些业务需要的参数
        :param result_pic_path:
        :param select_pic_path:
        :param origin_pic_path:
        :return:
        """
        self.origin_pic_path = origin_pic_path
        self.select_pic_path = select_pic_path
        self.result_pic_path = result_pic_path

        self.avg_hash = self.pic_com.avg_hash(origin_pic_path)
        self.d_hash = self.pic_com.difference_hash(origin_pic_path)
        self.p_hash = self.pic_com.perception_hash(origin_pic_path)

    def run(self):
        """
        主方法，对比图片使用
        :return:
        """
        while self.working:
            self.mutex.lock()

            if self.working is False:
                self.cond.wait(self.mutex)
                self.sin_out.emit("线程已停止运行")
                self.sin_work_status.emit(False)
                self.mutex.unlock()
                return None

            select_pic_path = self.select_pic_path
            result_pic_path = self.result_pic_path

            select_list = self.file.get_file_list(select_pic_path)
            if len(select_list) > 0:
                for i in range(0, len(select_list)):
                    if self.working is False:
                        self.cond.wait(self.mutex)
                        self.sin_out.emit("程序已结束运行 %s " % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                        self.sin_work_status.emit(False)
                        self.mutex.unlock()
                    file_path = select_list[i]
                    new_avg_hash = self.pic_com.avg_hash(file_path)
                    avg_com = self.pic_com.cmpHash(self.avg_hash, new_avg_hash)
                    if avg_com > 0.70:
                        new_d_hash = self.pic_com.difference_hash(file_path)
                        d_hash_com = self.pic_com.cmpHash(self.d_hash, new_d_hash)
                        if d_hash_com > 0.60:
                            new_p_hash = self.pic_com.perception_hash(file_path)
                            p_hash_com = self.pic_com.cmp2hash(self.p_hash, new_p_hash)
                            if p_hash_com > 0.70:
                                self.file.cope_file(old_file_path=file_path, new_folder_path=result_pic_path)
                                self.sin_out.emit("%s => 已找到一张相似的图片,请前往结果目录查看" %
                                                  (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
                recode_page = "%s => 所有数据检查完了" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                self.sin_out.emit(recode_page)

            self.mutex.unlock()
            self.pause()
        self.sin_out.emit("线程已停止运行(或已完成循环对比)")