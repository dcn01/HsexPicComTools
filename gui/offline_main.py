# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/jiang/Downloads/offline_page.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_offline_page(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("offline_page")
        self.resize(580, 420)
        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setGeometry(QtCore.QRect(10, 40, 271, 371))
        self.groupBox.setObjectName("groupBox")
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 40, 251, 131))
        self.groupBox_2.setObjectName("groupBox_2")
        self.widget = QtWidgets.QWidget(self.groupBox_2)
        self.widget.setGeometry(QtCore.QRect(10, 20, 231, 101))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.origin_pic_path_line = QtWidgets.QLineEdit(self.widget)
        self.origin_pic_path_line.setObjectName("origin_pic_path_line")
        self.gridLayout.addWidget(self.origin_pic_path_line, 0, 0, 1, 1)
        self.origin_path_button = QtWidgets.QPushButton(self.widget)
        self.origin_path_button.setObjectName("origin_path_button")
        self.gridLayout.addWidget(self.origin_path_button, 0, 1, 1, 1)
        self.select_pic_path_line = QtWidgets.QLineEdit(self.widget)
        self.select_pic_path_line.setObjectName("select_pic_path_line")
        self.gridLayout.addWidget(self.select_pic_path_line, 1, 0, 1, 1)
        self.select_path_button = QtWidgets.QPushButton(self.widget)
        self.select_path_button.setObjectName("select_path_button")
        self.gridLayout.addWidget(self.select_path_button, 1, 1, 1, 1)
        self.result_pic_path_line = QtWidgets.QLineEdit(self.widget)
        self.result_pic_path_line.setObjectName("result_pic_path_line")
        self.gridLayout.addWidget(self.result_pic_path_line, 2, 0, 1, 1)
        self.result_path_button = QtWidgets.QPushButton(self.widget)
        self.result_path_button.setObjectName("result_path_button")
        self.gridLayout.addWidget(self.result_path_button, 2, 1, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 200, 251, 91))
        self.groupBox_3.setObjectName("groupBox_3")
        self.execute_button = QtWidgets.QPushButton(self.groupBox_3)
        self.execute_button.setGeometry(QtCore.QRect(20, 40, 80, 26))
        self.execute_button.setObjectName("execute_button")
        self.clear_log_button = QtWidgets.QPushButton(self.groupBox_3)
        self.clear_log_button.setGeometry(QtCore.QRect(140, 40, 80, 26))
        self.clear_log_button.setObjectName("clear_log_button")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 330, 161, 16))
        self.label.setObjectName("label")
        self.groupBox_4 = QtWidgets.QGroupBox(self)
        self.groupBox_4.setGeometry(QtCore.QRect(300, 10, 261, 401))
        self.groupBox_4.setObjectName("groupBox_4")
        self.log_textBrowser = QtWidgets.QTextBrowser(self.groupBox_4)
        self.log_textBrowser.setGeometry(QtCore.QRect(10, 30, 241, 361))
        self.log_textBrowser.setObjectName("log_textBrowser")
        self.back_index_main_button = QtWidgets.QPushButton(self)
        self.back_index_main_button.setGeometry(QtCore.QRect(10, 10, 80, 26))
        self.back_index_main_button.setObjectName("back_index_main_button")

        self.setWindowTitle("线下查询模式")
        self.groupBox.setTitle("参数设置")
        self.groupBox_2.setTitle("路径设置")
        self.origin_path_button.setText("源文件")
        self.select_path_button.setText("待查询目录")
        self.result_path_button.setText("结果目录")
        self.groupBox_3.setTitle("执行操作")
        self.execute_button.setText("开始执行")
        self.clear_log_button.setText("清空日志")
        self.label.setText("2021年12月23日12:32:55")
        self.groupBox_4.setTitle("日志打印")
        self.back_index_main_button.setText("返回首页")
