import os
import sys
import time

from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox

from gui.online_main import Ui_online_main
from gui.index_main import Ui_index_main
from gui.offline_main import Ui_offline_page
from gui.proxysetting_main import proxySocksSetting
from businese.offline_businese.threading_execute_offline import signalThreading
from businese.online_businese.threading_execute import signalThreading as signalThreadingByOnline, getNetWorkStatus
from gui.downlaod_main import Ui_pic_download_main
from businese.download_businese.threading_execute import getNetWorkStatus as net_download


class downLoadPage(Ui_pic_download_main):
    def __init__(self):
        super().__init__()
        self.proxy_ip_port = None
        self.net = net_download()
        self.sw = settingWindows()  # 实例代理设置页

        self.save_pic_path_button.clicked.connect(self.set_pic_save_path)
        self.network_check_button.clicked.connect(self.test_net)
        self.net.sin_work_status.connect(self.check_network)
        self.sw.signal.connect(self.get_ip_port)
        self.actionscoks5.triggered.connect(self.open_proxy_setting)

    def print_logs(self, text):
        self.log_textBrowser.insertPlainText(text + '\n')

    def set_pic_save_path(self):
        """
        获取需要查找的封面图片
        :return:
        """
        pic_path_floder = QFileDialog.getExistingDirectory(self, '设置图片路径存放地址', os.getcwd())
        self.save_pic_path_line.setText(pic_path_floder)
        self.print_logs("已设置图片存放路径：%s " % pic_path_floder)

    def test_net(self):
        if self.open_proxy_radioButton.isChecked():
            if self.proxy_ip_port is None or self.proxy_ip_port == '':
                self.print_logs("还未设置代理IP,请前往“设置”-“本地代理”完善信息")
                self.network_check_button.setEnabled(True)
                return None
            else:
                ip_port = self.proxy_ip_port
                self.net.get_network_status(ip_port=ip_port)
        self.net.start()
        self.network_check_button.setEnabled(False)
        self.print_logs("%s 开始检查网络，请稍后......" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    def check_network(self, result):
        if self.open_proxy_radioButton.isChecked():
            if result is True:
                self.print_logs("%s 代理IP网络正常，成功访问目标网站！" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            else:
                self.print_logs("%s 代理IP网络异常，请检查网络或更新代理IP设置！" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        else:
            if result is True:
                self.print_logs("%s 网络正常，成功访问目标网站！" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            else:
                self.print_logs("%s 网络异常，请检查网络或设置代理ip后再尝试！" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        self.network_check_button.setEnabled(True)

    def open_proxy_setting(self):
        self.sw.show()

    def get_ip_port(self, ip_port):
        self.proxy_ip_port = ip_port
        if self.proxy_ip_port is None or self.proxy_ip_port == '':
            self.print_logs("未设置代理ip")
        else:
            self.print_logs("已设置代理IP：%s" % self.proxy_ip_port)


class settingWindows(proxySocksSetting):
    """
    设置代理IP的窗口
    """

    def __init__(self):
        super(settingWindows, self).__init__()
        self.proxy_gui = proxySocksSetting().__init__()

        # 信号槽
        self.sumbit_button.clicked.connect(self.get_ip_port)

    def get_ip_port(self):
        ip_port = self.ip_port_lineEdit.text()
        self.signal.emit(ip_port)
        self.close()


class offLinePage(Ui_offline_page):
    """
    线下查询页面
    """
    def __init__(self):
        super().__init__()
        self.th_offline = signalThreading()

        # 线下查询页面信号槽
        self.origin_path_button.clicked.connect(self.get_origin_pic_file_path_by_offline)
        self.select_path_button.clicked.connect(self.get_select_pic_path_by_offline)
        self.result_path_button.clicked.connect(self.get_result_pic_path_by_offline)
        self.execute_button.clicked.connect(self.execute_offline)
        self.th_offline.sin_out.connect(self.print_logs_by_offline)
        self.th_offline.sin_work_status.connect(self.execute_status)
        self.clear_log_button.clicked.connect(self.clear_log)

    def get_origin_pic_file_path_by_offline(self):
        """
        获取需要查找的封面图片
        :return:
        """
        pic_name = QFileDialog.getOpenFileName(self, '选取源文件路径', os.getcwd(), '*.jpg;;*.png')
        self.origin_pic_file_path = pic_name[0]
        self.origin_pic_path_line.setText(self.origin_pic_file_path)
        self.print_logs_by_offline("源图片路径：%s " % self.origin_pic_file_path)

    def get_select_pic_path_by_offline(self):
        """
        获取存储大量图片的地址
        :return:
        """
        self.log_path_flor = QFileDialog.getExistingDirectory(self, '设置日志路径存放地址', os.getcwd())
        self.select_pic_path_line.setText(self.log_path_flor)
        self.print_logs_by_offline("目标图片路径：%s " % self.log_path_flor)

    def get_result_pic_path_by_offline(self):
        """
        获取存储大量图片的地址
        :return:
        """
        self.log_path_flor = QFileDialog.getExistingDirectory(self, '设置日志路径存放地址', os.getcwd())
        self.result_pic_path_line.setText(self.log_path_flor)
        self.print_logs_by_offline("结果保存路径：%s " % self.log_path_flor)

    def print_logs_by_offline(self, text):
        """
        打印日志的方法
        :param text:
        :return:
        """
        self.log_textBrowser.insertPlainText(text + '\n')

    def clear_log(self):
        self.log_textBrowser.clear()

    def execute_offline(self):
        origin_pic_path = self.off_line_page.origin_pic_path_line.text()
        select_pic_path = self.off_line_page.select_pic_path_line.text()
        result_pic_path = self.off_line_page.result_pic_path_line.text()

        if len(origin_pic_path) == 0:
            self.print_logs_by_offline("请设置源图片路径")
        elif len(select_pic_path) == 0:
            self.print_logs_by_offline("请设置查询目录")
        elif len(result_pic_path) == 0:
            self.print_logs_by_offline("请设置结果目录")
        else:
            self.th_offline.get_business_param(origin_pic_path=origin_pic_path,
                                               select_pic_path=select_pic_path,
                                               result_pic_path=result_pic_path)
            self.th_offline.start_execute_init()
            self.th_offline.start()
            self.print_logs_by_offline("%s => 开始执行" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

    def stop_execute(self):
        """
        停止执行
        :return:
        """
        self.th.pause()
        self.print_logs("已发出停止指令，当前正在处理的请求完成后便会停止")
        self.start_execute_button.setText("请等待程序结束")
        self.start_execute_button.setEnabled(False)

    def execute_button_status(self):
        if self.th.working is True and self.start_execute_button.text() == '开始执行':
            self.start_execute()
        elif self.th.working is True and self.start_execute_button.text() == '结束执行':
            self.stop_execute()
        elif self.th.working is False and self.start_execute_button.text() == '开始执行':
            self.start_execute()
        else:
            self.start_execute_button.setText("开始执行")

    def execute_status(self, sin_work_status=True):
        if sin_work_status is False:
            self.start_execute_button.setText("开始执行")
            self.start_execute_button.setEnabled(True)


class onLinePage(Ui_online_main):
    """
    线上查询页面
    """
    def __init__(self):
        super().__init__()
        # 以下为线上查询
        self.proxy_ip_port = None
        self.origin_pic_file_path = None
        self.log_path_flor = None

        self.th = signalThreadingByOnline()  # 实例化爬虫主程序
        self.sw = settingWindows()  # 实例代理设置页
        self.net = getNetWorkStatus()

        # 以下为执行爬虫的信号槽
        self.actionsocks5.triggered.connect(self.open_proxy_setting)
        self.sw.signal.connect(self.get_ip_port)  # 显示设置了代理的日志
        self.execute_button.clicked.connect(self.execute_button_status_online)
        self.th.sin_work_status.connect(self.execute_status_online)
        self.th.sin_out.connect(self.print_logs_online)  # 执行了第几页的日志

        # 以下为没有太大联动的信号槽
        self.origin_pic_path_button.clicked.connect(self.get_origin_pic_file_path_online)
        self.log_path_button.clicked.connect(self.set_log_save_path_online)
        self.clear_log_button.clicked.connect(self.clear_log_print_online)
        self.actionabout.triggered.connect(self.about_msg)
        self.network_check_button.clicked.connect(self.test_net)
        self.net.sin_work_status.connect(self.check_network)

    # 以下为线上模式的方法
    def get_origin_pic_file_path_online(self):
        """
        获取需要查找的封面图片
        :return:
        """
        pic_name = QFileDialog.getOpenFileName(self, '选取源文件路径', os.getcwd(), '*.jpg;;*.png')
        self.origin_pic_file_path = pic_name[0]
        self.origin_pic_path_line.setText(self.origin_pic_file_path)
        self.print_logs_online("源图片路径：%s " % self.origin_pic_file_path)

    def set_log_save_path_online(self):
        """
        获取需要查找的封面图片
        :return:
        """
        self.log_path_flor = QFileDialog.getExistingDirectory(self, '设置日志路径存放地址', os.getcwd())
        self.log_path_line.setText(self.log_path_flor)
        self.print_logs_online("已设置日志路径：%s " % self.log_path_flor)

    def print_logs_online(self, text):
        """
        打印日志的方法
        :param text:
        :return:
        """
        self.log_textBrowser.insertPlainText(text + '\n')

    def clear_log_print_online(self):
        """
        清空日志输出区域
        :return:
        """
        self.log_textBrowser.clear()

    def about_msg(self):
        QMessageBox.about(self, "关于", "     此工具主要用于查找91Porn.com的视频封面，访问的是镜像网站hsex.men。此工具仅做学习交流使用。")

    def help_msg(self):
        QMessageBox.about(self, "帮助", "     如果您的电脑支持访问外网，那么就无需设置代理。该工具暂时只支持scoks5本地代理")

    def get_line_edit_page(self):
        """
        获取开始页和结束页
        :return:
        """
        page_list = []
        start_page = self.start_page_num_line.text()
        end_page = self.end_page_num_line.text()
        page_list.append(start_page)
        page_list.append(end_page)
        return page_list

    def open_proxy_setting(self):
        self.sw.show()

    def get_ip_port(self, ip_port):
        self.proxy_ip_port = ip_port
        if self.proxy_ip_port is None or self.proxy_ip_port == '':
            self.print_logs_online("未设置代理ip")
        else:
            self.print_logs_online("已设置代理IP：%s" % self.proxy_ip_port)

    def start_execute_online(self):
        """
        主方法，对比图片使用
        :return:
        """
        # 先清理一下日志界面
        self.clear_log_print_online()

        page_list = self.get_line_edit_page()

        star_number = page_list[0]
        end_number = page_list[1]

        if star_number is None or star_number == '':
            self.print_logs_online("请输入开始页")
        elif end_number is None or end_number == '':
            self.print_logs_online("请输入结束页")
        elif self.origin_pic_file_path is None or self.origin_pic_file_path == '':
            self.print_logs_online("请选择源图片")
        elif self.log_path_flor is None or self.log_path_flor == '':
            self.print_logs_online("请设置日志存放文件夹")
        else:
            ip_port = None
            if self.open_proxy_radioButton.isChecked():
                if self.proxy_ip_port is None or self.proxy_ip_port == '':
                    self.print_logs_online("还未设置代理IP,请前往“设置”-“本地代理”完善信息")
                    return None
                else:
                    ip_port = self.proxy_ip_port
            if int(star_number) <= int(end_number):
                self.th.start_execute_init()  # 线程启动,工作状态设置为True
                self.th.get_businese_param(start_page_num=star_number, end_page_num=int(end_number) + 1,
                                           origin_pic_path=self.origin_pic_file_path, log_path_flor=self.log_path_flor,
                                           proxy_ip_port=ip_port)
                self.th.start()
                self.print_logs_online("开始进行对比，从第 %s 页执行到第 %s 页" % (star_number, end_number))
                self.execute_button.setText("结束执行")
            else:
                self.print_logs_online("开始页大于结束页，请重新设置，要求开始页小于结束页")

    def stop_execute_online(self):
        """
        停止执行
        :return:
        """
        self.th.pause()
        self.print_logs_online("已发出停止指令，当前正在处理的请求完成后便会停止")
        self.execute_button.setText("请等待程序结束")
        self.execute_button.setEnabled(False)

    def execute_button_status_online(self):
        if self.th.working is True and self.execute_button.text() == '开始执行':
            self.start_execute_online()
        elif self.th.working is True and self.execute_button.text() == '结束执行':
            self.stop_execute_online()
        elif self.th.working is False and self.execute_button.text() == '开始执行':
            self.start_execute_online()
        else:
            self.execute_button.setText("开始执行")

    def execute_status_online(self, sin_work_status=True):
        if sin_work_status is False:
            self.execute_button.setText("开始执行")
            self.execute_button.setEnabled(True)

    def test_net(self):
        if self.open_proxy_radioButton.isChecked():
            if self.proxy_ip_port is None or self.proxy_ip_port == '':
                self.print_logs_online("还未设置代理IP,请前往“设置”-“本地代理”完善信息")
                self.network_check_button.setEnabled(True)
                return None
            else:
                ip_port = self.proxy_ip_port
                self.net.get_network_status(ip_port=ip_port)
        self.net.start()
        self.network_check_button.setEnabled(False)
        self.print_logs_online("%s 开始检查网络，请稍后......" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    def check_network(self, result):
        if self.open_proxy_radioButton.isChecked():
            if result is True:
                self.print_logs_online("%s 代理IP网络正常，成功访问目标网站！" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            else:
                self.print_logs_online("%s 代理IP网络异常，请检查网络或更新代理IP设置！" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        else:
            if result is True:
                self.print_logs_online("%s 网络正常，成功访问目标网站！" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            else:
                self.print_logs_online("%s 网络异常，请检查网络或设置代理ip后再尝试！" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        self.network_check_button.setEnabled(True)


class mainGUI(Ui_index_main):
    """
    主窗口
    """
    def __init__(self):
        super().__init__()
        self.off_line_page = offLinePage()  # 线下模式
        self.on_line_page = onLinePage()  # 线上模式
        self.download_page = downLoadPage()  # 资源下载模式

        # 主界面信号槽
        self.offline_model_button.clicked.connect(self.open_offline_page)
        self.online_model_button.clicked.connect(self.open_online_page)
        self.pic_download_model_button.clicked.connect(self.open_download_page)

        # 线上模式
        self.on_line_page.back_index_page_button.clicked.connect(self.back_main_page_by_online)

        # 线下模式
        self.off_line_page.back_index_main_button.clicked.connect(self.back_main_page_by_offline)

        # 资源下载页
        self.download_page.back_index_main_button.clicked.connect(self.back_main_page_by_download)

        timer = QTimer(self)
        timer.timeout.connect(self.showtime_by_offline)
        timer.timeout.connect(self.showtime_by_online)
        timer.start()

    def open_offline_page(self):
        """
        从首页跳转到线下查询页面
        :return:
        """
        self.close()
        self.off_line_page.show()

    def open_online_page(self):
        """
        从首页跳转至线上查询页面
        :return:
        """
        self.close()
        self.on_line_page.show()

    def open_download_page(self):
        """
        进入下载模式
        :return:
        """
        self.close()
        self.download_page.show()

    def back_main_page_by_download(self):
        self.show()
        self.download_page.close()

    def back_main_page_by_offline(self):
        self.show()
        self.off_line_page.close()

    def back_main_page_by_online(self):
        self.show()
        self.on_line_page.close()

    def showtime_by_online(self):
        datetime = QDateTime.currentDateTime()
        text = datetime.toString()
        self.on_line_page.time_lable.setText(text)

    def showtime_by_offline(self):
        datetime = QDateTime.currentDateTime()
        text = datetime.toString()
        self.off_line_page.label.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_gui = mainGUI()
    main_gui.show()
    sys.exit(app.exec_())