from App.pages import Page, Pages
from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton
from App.services import BoardKeys, DataManager
from collections.abc import Callable
from PySide6.QtCore import QSize
from App import utils

class BoardPage(Page):
    boardId = ""
    
    def __init__(self, datamanager: DataManager, navigateHandle: Callable[[str], None]):
        super().__init__(datamanager, navigateHandle, None)

        layout = QVBoxLayout(self)
        self.title = QLabel("Board not found")
        leaveBtn = QPushButton("Вернутся в меню")
        leaveBtn.clicked.connect(lambda: navigateHandle(Pages.HOME))
        leaveBtn.setFixedWidth(150)
        leaveBtn.setFixedHeight(50)
        layout.addWidget(leaveBtn)
        layout.addWidget(self.title)
        layout.setContentsMargins(40, 40, 40, 40)
    
    def update(self):
        if (self.boardId not in self.datamanager.data):
            return

        board = self.datamanager.data[self.boardId]

        self.title.setText(board[BoardKeys.TITLE])
        self.title.setBaseSize(20, 20)

    def open(self):
        wsize = QSize(1080, 720)
        utils.setSizeCentered(self.window(), wsize)

    def acceptData(self, data: dict):
        if "bid" in data.keys():
            self.boardId = data["bid"]
            self.update()