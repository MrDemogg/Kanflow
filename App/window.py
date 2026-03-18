
from PySide6.QtWidgets import QLayout
from qframelesswindow import FramelessWindow

# Класс для обычных (не основных) окон, например диалогов, окна настроек ну и подобное

class Window(FramelessWindow):
    def __init__(self, parent=None, title = "Kanflow"):
        super().__init__(parent=parent)
        from App import CustomTitleBar # видимо CustomTitleBar не успевает подготовится если импортировать в начале файла, так что так
        self.setSystemTitleBarButtonVisible(False)
        self.setTitleBar(CustomTitleBar(self))
        self.setWindowTitle(title)