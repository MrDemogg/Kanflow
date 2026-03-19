from PySide6.QtGui import QColor, QPixmap
from PySide6.QtWidgets import QStackedWidget, QVBoxLayout, QWidget
from qframelesswindow import FramelessWindow, StandardTitleBar
from App.services import DataManager
from App.pages import BoardPage, HomePage, Page, Pages

class CustomTitleBar(StandardTitleBar):
    def __init__(self, parent, title: str, icon: str = "ui/ico512.png"):
        super().__init__(parent)
        self.minBtn.setNormalColor(QColor(255, 255, 255))
        self.maxBtn.setNormalColor(QColor(255, 255, 255))
        self.closeBtn.setNormalColor(QColor(255, 255, 255))
        self.minBtn.setHoverColor(QColor(173, 216, 230))
        self.maxBtn.setHoverColor(QColor(144, 238, 144))
        self.closeBtn.setHoverBackgroundColor(QColor(255, 255,255))
        self.closeBtn.setHoverColor(QColor(255, 102, 102))
        self.setIcon(QPixmap(icon))
        self.setTitle(title)


class MainWindow(FramelessWindow):

    stack: QStackedWidget
    pages: dict[str, QWidget]
    datamanager: DataManager

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("window")
        self.setSystemTitleBarButtonVisible(False)
        self.setStyleSheet("""
        #window { 
            background-color: #212121;
        }
        """)
        self.setTitleBar(CustomTitleBar(self, "Kanflow"))

        # self.stack = QStackedWidget()
        # self.stacklayout = QStackedLayout(self.stack)

        # self.pages = {
        #     "home"
        # }

        central = QWidget()
        mainlay = QVBoxLayout(central)

        self.stack = QStackedWidget()

        self.datamanager = DataManager()

        self.pages: dict[str, Page] = {
            Pages.HOME: HomePage(self.datamanager, self.handleNavigation, self.dataTransfer),
            Pages.BOARD: BoardPage(self.datamanager, self.handleNavigation)
        }

        for page in self.pages.values():
            self.stack.addWidget(page)
        
        self.stack.setCurrentIndex(0)

        mainlay.addWidget(self.stack, stretch=1)

        self.setLayout(mainlay)

        self.titleBar.raise_()

    # def switch_page(self, page_name: str):
    #     if page_name in self.pages:
    #         self.stack.setCurrentWidget(self.pages[page_name])

    def handleNavigation(self, pageName: str):
        self.stack.setCurrentWidget(self.pages[pageName])
        self.pages[pageName].open()
    
    def dataTransfer(self, consumer: str, data: dict):
        self.pages[consumer].acceptData(data)