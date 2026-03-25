from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import QStackedWidget, QVBoxLayout, QWidget, QApplication
from qframelesswindow import StandardTitleBar, FramelessMainWindow
from App.services import DataManager
from App.pages import BoardPage, HomePage, Page, Pages
from . import utils
from .titlebar import DefaultTitleBar


class MainWindow(FramelessMainWindow):

    stack: QStackedWidget
    pages: dict[str, QWidget]
    datamanager: DataManager

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("window")
        self.setSystemTitleBarButtonVisible(False)
        self.setStyleSheet("""
        #window { 
            background-color: #184B57;
        }
        """)
        self.setTitleBar(DefaultTitleBar(self, "Kanflow"))

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

        mainlay.addWidget(self.stack, stretch=1)

        self.setCentralWidget(central)

        self.titleBar.raise_()

        self.handleNavigation(Pages.HOME)
    
    def closeEvent(self, event):
        self.datamanager.save()
        for widget in QApplication.topLevelWindows():
            if widget is not self:
                widget.close()
        return super().closeEvent(event)

    # def switch_page(self, page_name: str):
    #     if page_name in self.pages:
    #         self.stack.setCurrentWidget(self.pages[page_name])

    def handleNavigation(self, pageName: str):
        self.stack.setCurrentWidget(self.pages[pageName])
        self.pages[pageName].open()
    
    def dataTransfer(self, consumer: str, data: dict):
        self.pages[consumer].acceptData(data)