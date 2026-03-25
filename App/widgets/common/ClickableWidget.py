from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal, Qt


class ClickableWidget(QWidget):
    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

    def mousePressEvent(self, event):
        # реализуем, как я понял, абстрактную функцию из каких-то далеких предков, хуй знает,
        # event обязательно указывается как аргумент, но вообще не нужен
        self.clicked.emit()
        
        return super().mousePressEvent(event)