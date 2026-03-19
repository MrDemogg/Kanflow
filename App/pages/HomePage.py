from .Page import Page, Pages
from .BoardCreationPage import BoardCreationPage
from PySide6.QtWidgets import QLabel, QVBoxLayout, QPushButton, QScrollArea, QWidget, QHBoxLayout
from App.services import BoardKeys, DataManager
from App.widgets import ClickableWidget
from collections.abc import Callable

class HomePage(Page):

    def __init__(self, datamanager: DataManager = None, navigateHandle: Callable[[str], None] = None, dataTransfer: Callable[[str, dict], None] = None):
        super().__init__(datamanager, navigateHandle, dataTransfer)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Welcome to Kanflow!"))
        createBtn = QPushButton("Create Board")
        createBtn.clicked.connect(self._createDialog)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        self.boardsContainer = QWidget(self)
        self.boardsListLay = QVBoxLayout(self.boardsContainer)
        self.boardsListLay.setSpacing(20)
        self.boardsListLay.setContentsMargins(0, 20, 0, 0)

        scroll.setWidget(self.boardsContainer)

        layout.addStretch()
        layout.addWidget(scroll, stretch=1)
        # btn.clicked.connect(lambda: switch_page_callback("board") if switch_page_callback else None)

        layout.addWidget(createBtn)

        self.updateBoardsList()
    
    def _clearBoardsList(self):
        while self.boardsListLay.count():
            item = self.boardsListLay.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()

    def updateBoardsList(self):
        boards: dict[str, dict[str, any]] = self.datamanager.data

        self._clearBoardsList()

        for key, board in boards.items():
            boardWidget = ClickableWidget(self)
            boardWidget.setObjectName("boardsListItem")
            boardWidget.setFixedHeight(50)
            boardWidget.setStyleSheet("""
                #boardsListItem {
                    border: 5px solid #2E9AFF;
                }
            """)
            boardLay = QHBoxLayout(boardWidget)

            title = QLabel("Title: " + board[BoardKeys.TITLE])
            boardId = QLabel("ID: " + key)
            boardId.setStyleSheet("font-size: 10px; color: gray;")
            desc = QLabel("Desc: " + board[BoardKeys.DESCRIPTION])
            boardLay.addWidget(title)
            boardLay.addWidget(boardId)
            boardLay.addWidget(desc)

            boardWidget.clicked.connect(lambda: self.selectBoard(key))

            self.boardsListLay.addWidget(boardWidget)
    

    def selectBoard(self, key: str) -> None: 
        print(key)
        self.dataTransfer(Pages.BOARD, {"bid": key})
        self.navigateHandle(Pages.BOARD)


    def _createDialog(self):
        boardCreation = BoardCreationPage(self.window())
        status = boardCreation.exec()
        print(status)
        if status == 1:
            print(boardCreation.title)
            self.datamanager.createTable(boardCreation.title, boardCreation.desc)
            self.updateBoardsList()

    def acceptData(self, data):
        return super().acceptData(data)
