import time

from businese.threading_execute import signalThreading
from gui.hsexbusinses import *
from gui.proxysetting import *


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


class mainUI(mainWindowsGUI):
    def __init__(self):
        super(mainUI, self).__init__()
        self.proxy_ip_port = None
        self.origin_pic_file_path = None
        self.log_path_flor = None

        self.th = signalThreading()  # 实例化爬虫主程序
        self.sw = settingWindows()  # 实例代理设置页

        # 以下为执行爬虫的信号槽
        self.actionsocks5.triggered.connect(self.open_proxy_setting)
        self.sw.signal.connect(self.get_ip_port)  # 显示设置了代理的日志
        self.start_execute_button.clicked.connect(self.start_execute)
        self.start_execute_button.clicked.connect(self.button_status)
        self.end_execute_button.clicked.connect(self.stop_execute)
        self.th.sin_out.connect(self.print_logs)  # 执行了第几页的日志

        # 以下为没有太大联动的信号槽
        self.origin_pic_path_button.clicked.connect(self.get_origin_pic_file_path)
        self.log_save_path_button.clicked.connect(self.set_log_save_path)
        self.clear_log_button.clicked.connect(self.clear_log_print)
        self.actionabout.triggered.connect(self.about_msg)
        self.actionhelp.triggered.connect(self.help_msg)

    def get_origin_pic_file_path(self):
        """
        获取需要查找的封面图片
        :return:
        """
        pic_name = QFileDialog.getOpenFileName(self, '选取源文件路径', os.getcwd(), '*.jpg;;*.png')
        self.origin_pic_file_path = pic_name[0]
        self.origin_pic_path_line.setText(self.origin_pic_file_path)
        self.print_logs("源图片路径：%s " % self.origin_pic_file_path)

    def set_log_save_path(self):
        """
        获取需要查找的封面图片
        :return:
        """
        self.log_path_flor = QFileDialog.getExistingDirectory(self, '设置日志路径存放地址', os.getcwd())
        self.log_save_path_line.setText(self.log_path_flor)
        self.print_logs("已设置日志路径：%s " % self.log_path_flor)

    def print_logs(self, text):
        """
        打印日志的方法
        :param text:
        :return:
        """
        if type(text) == tuple or type(text) == list:
            for i in text:
                content = '序号:'
                for n in range(len(i)):
                    content = content + str(i) + ', '
                self.log_print_box.insertPlainText(content + '\n')
        else:
            self.log_print_textbox.insertPlainText(text + '\n')

    def clear_log_print(self):
        """
        清空日志输出区域
        :return:
        """
        self.log_print_textbox.clear()

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
        start_page = self.start_path_line.text()
        end_page = self.end_path_line.text()
        page_list.append(start_page)
        page_list.append(end_page)
        return page_list

    def open_proxy_setting(self):
        self.sw.show()

    def get_ip_port(self, ip_port):
        self.proxy_ip_port = ip_port
        if self.proxy_ip_port is None or self.proxy_ip_port == '':
            self.print_logs("未设置代理ip")
        else:
            self.print_logs("已设置代理IP：%s" % self.proxy_ip_port)

    def start_execute(self):
        """
        主方法，对比图片使用
        :return:
        """
        # 先清理一下日志界面
        self.clear_log_print()

        page_list = self.get_line_edit_page()

        star_number = page_list[0]
        end_number = page_list[1]

        if star_number is None or star_number == '':
            self.print_logs("请输入开始页")
        if end_number is None or end_number == '':
            self.print_logs("请输入结束页")
        if self.origin_pic_file_path is None or self.origin_pic_file_path == '':
            self.print_logs("请选择源图片")
        if self.log_path_flor is None or self.log_path_flor == '':
            self.print_logs("请设置日志存放文件夹")
        else:
            ip_port = None
            if self.open_proxy_button.isChecked():
                if self.proxy_ip_port is None or self.proxy_ip_port == '':
                    self.print_logs("还未设置代理IP,请前往“设置”-“本地代理”完善信息")
                    return None
                else:
                    ip_port = self.proxy_ip_port
            if int(star_number) <= int(end_number):
                self.th.start_execute_init()  # 线程启动
                self.th.get_bussinese_param(start_page_num=star_number, end_page_num=int(end_number) + 1,
                                            origin_pic_path=self.origin_pic_file_path, log_path_flor=self.log_path_flor,
                                            proxy_ip_port=ip_port)
                self.th.start()
                self.print_logs("开始进行对比，从第 %s 页执行到第 %s 页" % (star_number, end_number))
            else:
                self.print_logs("开始页大于结束页，请重新设置，要求开始页小于结束页")

    def stop_execute(self):
        """
        停止执行
        :return:
        """
        self.th.pause()
        self.print_logs("已发出停止指令，当前正在处理的请求完成后便会停止")


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    main_window = mainUI()
    main_window.setMinimumSize(580, 430)
    main_window.setMaximumSize(580, 430)
    main_window.show()
    sys.exit(app.exec())

