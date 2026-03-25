
from PySide6.QtWidgets import QVBoxLayout, QWidget
from PySide6.QtCore import Signal
from qframelesswindow import FramelessWindow

# Класс для обычных (не основных) окон, например диалогов, окна настроек ну и подобное

class Window(FramelessWindow):
    closing = Signal()
    def __init__(self, parent=None, title = "Kanflow"):
        super().__init__(parent)
        from App import DefaultTitleBar # видимо CustomTitleBar не успевает подготовится если импортировать в начале файла, так что так
        self.setSystemTitleBarButtonVisible(False)
        self.setTitleBar(DefaultTitleBar(self, title))

        central = QWidget()
        mainlay = QVBoxLayout(central)
        self.setLayout(mainlay)

        self.titleBar.raise_()
    
    def closeEvent(self, event):
        self.closing.emit()
        return super().closeEvent(event)