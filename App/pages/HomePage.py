from .Page import Page, Pages
from .BoardCreationPage import BoardCreationPage
from PySide6.QtWidgets import QLabel, QVBoxLayout, QPushButton, QScrollArea, QWidget, QHBoxLayout, QLayout
from PySide6.QtCore import QSize, Qt
from App.services import BoardKeys, DataManager
from App.widgets import ClickableWidget
from collections.abc import Callable

class HomePage(Page):

    def __init__(self, datamanager: DataManager = None, navigateHandle: Callable[[str], None] = None, dataTransfer: Callable[[str, dict], None] = None):
        super().__init__(datamanager, navigateHandle, dataTransfer)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 20, 0, 0)
        createBtn = QPushButton("Create Board")
        createBtn.clicked.connect(self._createDialog)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        self.boardsContainer = QWidget(self)
        self.boardsListLay = QVBoxLayout(self.boardsContainer)
        self.boardsListLay.setSpacing(10)
        self.boardsListLay.setSizeConstraint(QLayout.SetMinimumSize)

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
            boardWidget = ClickableWidget()
            boardWidget.setObjectName("boardsListItem")
            boardWidget.setFixedHeight(100)
            boardWidget.setStyleSheet("""
                QWidget#boardsListItem {
                    border: 5px solid #2E9AFF;
                    border-radius: 10px;
                    background-color: #2C2C2C;
                    padding: 10px;
                }
                QWidget#boardsListItem:hover {
                    background-color: #363636;
                    border-color: #4CC9FF;
                }
            """)
            
            boardLay = QHBoxLayout(boardWidget)
            boardLay.setSpacing(0)

            titleLay = QVBoxLayout()
            title = QLabel("Title: " + board[BoardKeys.TITLE])
            boardId = QLabel("ID: " + key)
            boardId.setAlignment(Qt.AlignmentFlag.AlignTop)
            boardId.setStyleSheet("font-size: 10px; color: gray;")
            titleLay.addWidget(title)
            titleLay.addWidget(boardId)
            titleLay.setSpacing(3)
            desc = QLabel("Desc: " + board[BoardKeys.DESCRIPTION])
            desc.setAlignment(Qt.AlignmentFlag.AlignTop)
            titleLay.setAlignment(Qt.AlignmentFlag.AlignTop)
            boardLay.addLayout(titleLay)
            boardLay.addWidget(desc)
            boardLay.setContentsMargins(boardLay.contentsMargins().left(), 20, boardLay.contentsMargins().right(), boardLay.contentsMargins().bottom())

            boardWidget.clicked.connect(lambda k=key: self.selectBoard(k)) # оказывается ламбда не запоминает значения, а лишь присваивает ссылки, вот те раз
            # благо славненький чат джпт подсказал что от этого можно избавится если присвоить параметр другому параметру

            self.boardsListLay.addWidget(boardWidget)

            for w in (title, boardId, desc):
                w.setAttribute(Qt.WA_TransparentForMouseEvents, True)
    

    def selectBoard(self, key: str) -> None: 
        print(key)
        self.dataTransfer(Pages.BOARD, {"bid": key})
        self.navigateHandle(Pages.BOARD)


    def _createDialog(self):
        boardCreation = BoardCreationPage(self.window())
        boardCreation.setFixedSize(QSize(512,512))
        status = boardCreation.exec()
        print(status)
        if status == 1:
            print(boardCreation.title)
            self.datamanager.createTable(boardCreation.title, boardCreation.desc)
            self.updateBoardsList()

    def acceptData(self, data):
        return super().acceptData(data)
