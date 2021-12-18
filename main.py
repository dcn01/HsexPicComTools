import sys
from PyQt5 import QtCore, QtWidgets
from gui.gui_main import mainUI


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    main_window = mainUI()
    main_window.setMinimumSize(580, 430)
    main_window.setMaximumSize(580, 430)
    main_window.setWindowIcon(main_window.icon)
    main_window.show()
    sys.exit(app.exec())
