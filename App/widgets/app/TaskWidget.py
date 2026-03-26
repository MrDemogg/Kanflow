from PySide6.QtWidgets import QVBoxLayout, QLabel
from PySide6.QtGui import QFont

from App import utils
from .BoardColumnWidget import BoardColumnWidget
from ..common import MirrorableWidget, ClickableWidget
from App.models.DataModels import *

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

        layout.addWidget(self.titleLabel)

        self.clicked.connect(self.mirror)

    def taskIndex(self):
        tasks: list[Task] = self.datamanager.data.boards[self.bid].columns[self.cid].tasks
        titles: list[str] = [task.title for task in tasks]
        return utils.indexByFirstEqual(titles, self.title)


    def onDataChange(self, newTitle):
        tasks: list[Task] = self.datamanager.data.boards[self.bid].columns[self.cid].tasks
        currTaskIndex = self.taskIndex()
        newTitleIndex = utils.indexByFirstEqual([task.title for task in tasks], newTitle)

        if newTitleIndex != -1:
            self.titleLabel.setText(self.title)
            if self.mirrorWindow.isVisible():
                self.mirror()
            return

        if currTaskIndex < 0:
            print("Что-то здесь не так")
            return
        
        self.title = newTitle
        self.titleLabel.setText(newTitle)

        tasks[currTaskIndex].title = self.title

    def refresh(self):
        self.task: Task = self.datamanager.data.boards[self.bid].columns[self.cid].tasks[self.title]

    @property
    def bid(self):
        return self.column.bid

    @property
    def cid(self):
        return self.column.colIndex()
        
