import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from App import MainWindow, utils

ico = None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(utils.resource_path("ico32.ico")))
    window = MainWindow()

    # window.setLayout(layout)
    window.show()
    app.exec()