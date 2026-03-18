import sys
from PySide6.QtWidgets import QApplication
from App import MainWindow

ico = None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    # window.setLayout(layout)
    window.show()
    app.exec()