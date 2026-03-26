from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QLineEdit, QPlainTextEdit, QDateEdit, QAbstractSpinBox
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt, QDate, QDateTime

from App import utils
from ..common import MirrorableWidget
from App.models.DataModels import *
from .BoardColumnWidget import BoardColumnWidget


class TaskWidget(MirrorableWidget):
    _openMirrors= {}

    def __init__(self, column: BoardColumnWidget, title: str, parent=None, original=None):
        super().__init__(parent=parent, original=original)

        self.column = column
        self.dataManager = column.dataManager
        self.title = title
        self.task: Task = self.dataManager.data.boards[self.bid].columns[self.cid].tasks[self.taskIndex()]

        layout = QVBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.titleLabel = QLabel(self.title)
        self.titleLabel.setFont(QFont("Segoe UI", 34))
        self.dueDate = QDateEdit(QDate.fromString(self.task.due_date))
        self.dueDate.setReadOnly(True) # потом можно сделать это тоже меняемым но пока-что плевать, времени нет
        self.dueDate.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.dueDate.setStyleSheet("""
            QDateEdit {
                background-color: transparent;
                border: none;
            }
            QDateEdit:focus {
                background-color: transparent;
            }
            QDateEdit:hover {
                background-color: transparent;
            }
        """)
        if not self.original:
            self.deleteBtn = QPushButton()
            self.deleteBtn.setIcon(QIcon(utils.resource_path("ui/close.png")))
            self.deleteBtn.clicked.connect(self.onDelete)
            layout.addWidget(self.titleLabel)
            layout.addWidget(self.dueDate)
            layout.addWidget(self.deleteBtn)

            hBottom = QHBoxLayout()

            self.leftBtn = QPushButton()
            self.leftBtn.setIcon(QIcon(utils.resource_path("ui/left.png")))
            self.rightBtn = QPushButton()
            self.rightBtn.setIcon(QIcon(utils.resource_path("ui/right.png")))

            self.leftBtn.clicked.connect(lambda: self.changeCol(self.cid - 1))
            self.rightBtn.clicked.connect(lambda: self.changeCol(self.cid + 1))

            hBottom.addWidget(self.leftBtn)
            hBottom.addWidget(self.rightBtn)

            layout.addLayout(hBottom)
            self.refresh()
            return
        
        self.description = QPlainTextEdit(self.task.description)
        self.description.setReadOnly(True)
        self.comments = QPlainTextEdit()
        self.comments.setReadOnly(True)
        self.commentInput = QLineEdit()
        self.commentInput.setPlaceholderText("Текст комментария")
        self.commentPublishButton = QPushButton("Опубликовать")
        self.commentAuthorInput = QLineEdit()
        self.commentAuthorInput.setPlaceholderText("Как вас зовут")
        self.commentPublishButton.clicked.connect(self.onPublishComment)

        layout.addWidget(self.titleLabel)
        layout.addWidget(self.description)
        layout.addWidget(self.dueDate)
        layout.addWidget(self.comments)
        layout.addWidget(self.commentInput)
        layout.addWidget(self.commentAuthorInput)
        layout.addWidget(self.commentPublishButton)

        self.refresh()

    def changeCol(self, colIndex: int):
        columns = self.dataManager.data.boards[self.bid].columns

        if colIndex < 0 or colIndex >= len(columns):
            return
        
        # ну в 23 часа ночи не грех и нейронку юзнуть по полной
        old_column = self.column

        columns[colIndex].tasks.append(
            columns[self.cid].tasks.pop(self.taskIndex())
        )

        self.dataManager.save()

        utils.logger.info(f"Задача '{self.title}' перемещена из колонки '{old_column.title}' в колонку '{columns[colIndex].title}' в доске '{self.bid}'")

        old_layout = self.column.contentLayout
        new_col_widget = self.column.window().findChildren(BoardColumnWidget)[colIndex]
        new_layout = new_col_widget.contentLayout

        old_layout.removeWidget(self)
        new_layout.addWidget(self)

        self.column = new_col_widget
        self.refresh()

        paired = self.column.getPaired()
        if paired:
            paired.refreshTasks()

        new_paired = new_col_widget.getPaired()
        if new_paired:
            new_paired.refreshTasks()

        old_paired = old_column.getPaired()
        if old_paired:
            old_paired.refreshTasks()
        
    
    def onPublishComment(self):
        comment = Comment(self.commentAuthorInput.text(), self.commentInput.text(), QDateTime.currentDateTime().toSecsSinceEpoch())

        utils.logger.info(f"Комментарий '{self.title}' от '{comment.author}': '{comment.content}'")

        self.commentInput.clear()

        self.task.comments.append(comment)
        self.dataManager.save()

        self.refresh()

    
    def onDelete(self):
        utils.logger.info(f"Задача '{self.title}' удалена из колонки '{self.column.title}' в доске '{self.bid}'")
        self.dataManager.data.boards[self.bid].columns[self.cid].tasks.pop(self.taskIndex())
        self.dataManager.save()

        self.column.contentLayout.removeWidget(self)
        self.deleteLater()

        paired: BoardColumnWidget = self.column.getPaired()
        if paired:
            paired.refreshTasks()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.mirror()
        super().mousePressEvent(event)

    def taskKey(self):
        return (self.bid, self.cid, self.title)

    def mirror(self):
        key = self.taskKey()

        if key in TaskWidget._openMirrors:
            win = TaskWidget._openMirrors[key]
            if win and win.isVisible():
                win.raise_()
                win.activateWindow()
                return

        super().mirror()
        TaskWidget._openMirrors[key] = self.mirrorWindow

    def _mirror(self):
        mirrorLay = self.mirrorWindow.layout()
        utils.clearLayoutWidgets(mirrorLay)
        mirroredTask = TaskWidget(self.column, self.title, original=self)
        mirrorLay.addWidget(mirroredTask)

        self.mirrorWindow.setMinimumSize(420, 280)

        self.refresh()

    @property
    def bid(self):
        return self.column.bid if hasattr(self.column, 'bid') else ""

    @property
    def cid(self):
        return self.column.colIndex()

    def onMirrorClose(self):
        key = self.taskKey()
        TaskWidget._openMirrors.pop(key, None)
        if not self.column or not self.column.isVisible():
            self.mirrorWindow.close()
        super().onMirrorClose() if hasattr(super(), 'onMirrorClose') else None

    def taskIndex(self):
        tasks: list[Task] = self.dataManager.data.boards[self.bid].columns[self.cid].tasks
        titles = [t.title for t in tasks]
        return utils.indexByFirstEqual(titles, self.title)

    def refresh(self):
        self.leftBtn.hide()
        self.rightBtn.hide()
        if self.original:
            self.comments.clear()
            for comment in self.task.comments:
                self.comments.appendPlainText(f"[{QDateTime.fromSecsSinceEpoch(comment.timestamp).toString()}] {comment.author} - {comment.content}")
        elif not self.column.original:
            if self.cid > 0:
                self.leftBtn.show()
            
            if self.cid < (len(self.dataManager.data.boards[self.bid].columns) - 1):
                self.rightBtn.show()

        pass

    def onDataChange(self, newTitle):

        pass

    @classmethod
    def closeAllTaskMirrors(cls):
        for win in list(cls._openMirrors.values()):
            if win:
                win.close()
        cls._openMirrors.clear()

    @classmethod
    def closeAllTaskMirrorsForColumn(cls, bid: str, cid: int):
        """Закрывает все зеркала задач конкретной колонки."""
        toClose = []
        for key, win in list(cls._openMirrors.items()):
            if key[0] == bid and key[1] == cid:
                toClose.append(win)
                cls._openMirrors.pop(key, None)
        for win in toClose:
            if win:
                win.close()