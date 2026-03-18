from .Page import Page
from PySide6.QtWidgets import QVBoxLayout, QLabel
from App.services import BoardKeys, ColumnKeys, TaskKeys, DataManager
from collections.abc import Callable

class BoardPage(Page):
    boardId = ""
    
    def __init__(self, datamanager: DataManager = None, navigateHandle: Callable[[str], None] = None, dataTransfer: Callable[[str, dict], None] = None):
        super().__init__(datamanager, navigateHandle, dataTransfer)

        self.vlayout = QVBoxLayout(self)
        self.errorMsg = QLabel("Board not found")
        self.title = QLabel()
        self.vlayout.addWidget(self.errorMsg)
        self.vlayout.addWidget(self.title)
    
    def update(self):
        if (self.boardId not in self.datamanager.data):
            self.errorMsg.show()
            return
        self.errorMsg.hide()

        board = self.datamanager.data[self.boardId]

        self.title.setText(board[BoardKeys.TITLE])
        self.title.setBaseSize(20, 20)

    def acceptData(self, data: dict):
        if "bid" in data.keys():
            self.boardId = data["bid"]
            self.update()