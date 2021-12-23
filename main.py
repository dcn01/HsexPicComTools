import sys
from PyQt5 import QtCore, QtWidgets
from gui.gui import mainGUI


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    main_window = mainGUI()
    main_window.setMinimumSize(320, 240)
    main_window.setMaximumSize(320, 240)
    # main_window.setWindowIcon(main_window.icon)
    main_window.show()
    sys.exit(app.exec())
