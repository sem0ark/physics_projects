from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QMainWindow
from ui_main_tag import Ui_MainWindow_tagged

import sys

if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    # window = QMainWindow()
    # window.resize(250, 150)
    # window.show()

    MainWindow = QMainWindow()
    ui = Ui_MainWindow_tagged()
    ui.setupUi(MainWindow)
    ui.tag_all()
    MainWindow.show()

    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)