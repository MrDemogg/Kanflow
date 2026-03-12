# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtGui import QColor, QIcon, QPixmap
from PySide6.QtWidgets import QApplication, QFrame, QHBoxLayout, QLabel, QPushButton, QScrollArea, QVBoxLayout, QWidget
from qframelesswindow import FramelessWindow, Qt, StandardTitleBar, AcrylicWindow, QMainWindow

ico = None

class CustomTitleBar(StandardTitleBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.minBtn.setNormalColor(QColor(255, 255, 255))
        self.maxBtn.setNormalColor(QColor(255, 255, 255))
        self.closeBtn.setNormalColor(QColor(255, 255, 255))
        self.minBtn.setHoverColor(QColor(173, 216, 230))
        self.maxBtn.setHoverColor(QColor(144, 238, 144))
        self.closeBtn.setHoverBackgroundColor(QColor(255, 255,255))
        self.closeBtn.setHoverColor(QColor(255, 102, 102))
        self.setIcon(QPixmap("ui/ico512.png"))



class Window(FramelessWindow):

    listelements = []
    items_container: QWidget
    items_layout: QVBoxLayout

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Kanflow")
        self.setObjectName("mainWindow")
        self.setSystemTitleBarButtonVisible(False)
        self.setStyleSheet("""
        #mainWindow { 
            background-color: #212121;
        }
        """)
        self.setTitleBar(CustomTitleBar(self))

        central = QWidget()
        layout = QVBoxLayout(central)

        # Область прокрутки
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        # Контейнер для элементов
        self.items_container = QWidget()
        self.items_layout = QVBoxLayout(self.items_container)
        self.items_layout.setAlignment(Qt.AlignTop)
        self.items_layout.setSpacing(20)
        self.items_layout.setContentsMargins(0, 20, 0, 0)

        scroll.setWidget(self.items_container)
        layout.addWidget(scroll, stretch=1)

        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add)

        layout.addWidget(add_button)

        self.setLayout(layout)

        self.titleBar.raise_()
    
    def add(self):
        id = self.items_layout.count()
        element = QWidget()
        element.setObjectName(f"elem{id}")
        element.setStyleSheet("""
        #elem{id} {
            width: 100%;
            height: 50px;        
        }
        """)
        element_layout = QHBoxLayout(element)
        elembtn = QPushButton(f"Close{id}")
        elembtn.clicked.connect(lambda: self.remove(id))
        element_layout.addWidget(elembtn)
        self.items_layout.addWidget(element)
    
    def remove(self, id):
        element = self.findChild(QWidget, f"elem{id}")
        if element:
            self.items_layout.removeWidget(element)
            element.deleteLater()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ico = QIcon("ui/ico32.ico")
    app.setWindowIcon(ico)
    window = Window()


    # window.setLayout(layout)
    window.show()
    app.exec()
