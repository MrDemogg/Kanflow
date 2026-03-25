from PySide6.QtWidgets import QVBoxLayout, QLabel
from PySide6.QtGui import QFont
from .BoardColumnWidget import BoardColumnWidget
from ..common import MirrorableWidget, ClickableWidget

class TaskWidget(MirrorableWidget, ClickableWidget): # ухты пухты, 2 родительских класса одновременно, папа и папа
    def __init__(self, column: BoardColumnWidget, title: str, parent=None, isMirror=False):
        super().__init__(parent=parent, isMirror=isMirror)

        self.column = column
        self.datamanager = column.dataManager
        self.title = title

        layout = QVBoxLayout(self)

        self.titleLabel = QLabel(self.title)
        titleFont = QFont("Segoe UI", 34)
        self.titleLabel.setFont(titleFont)
    
    def update(self, title: str):
        self.titleLabel.setText(title)

    @property
    def bid(self):
        return self.column.bid

    @property
    def cid(self):
        return self.column._colIndex()
        
