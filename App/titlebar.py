from PySide6.QtGui import QColor, QIcon
from qframelesswindow import StandardTitleBar
from . import utils

class DefaultTitleBar(StandardTitleBar):
    def __init__(self, parent, title: str, icon: str = "ui/ico512.png"):
        super().__init__(parent)
        self.minBtn.setNormalColor(QColor(255, 255, 255))
        self.maxBtn.setNormalColor(QColor(255, 255, 255))
        self.closeBtn.setNormalColor(QColor(255, 255, 255))
        self.minBtn.setHoverColor(QColor(173, 216, 230))
        self.maxBtn.setHoverColor(QColor(144, 238, 144))
        self.closeBtn.setHoverBackgroundColor(QColor(255, 255,255))
        self.closeBtn.setHoverColor(QColor(255, 102, 102))
        self.setIcon(QIcon(utils.resource_path(icon)))
        self.setTitle(title)