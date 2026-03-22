from .Page import Page, Pages
from .BoardCreationPage import BoardCreationPage
from PySide6.QtWidgets import QLabel, QVBoxLayout, QPushButton, QScrollArea, QWidget, QHBoxLayout, QLayout
from PySide6.QtCore import QSize, Qt, QPoint, QTimer
from PySide6.QtGui import QIcon
from App.services import DataManager, Board
from App.widgets import ClickableWidget
from collections.abc import Callable
from App import utils

class HomePage(Page):

    def __init__(self, datamanager: DataManager, navigateHandle: Callable[[str], None], dataTransfer: Callable[[str, dict], None]):
        super().__init__(datamanager, navigateHandle, dataTransfer)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 20, 0, 0)
        self.createBtn = QPushButton(parent=self)
        self.createBtn.clicked.connect(self._createDialog)
        self.createBtn.setIcon(QIcon(utils.resource_path("ui/createboard.png")))
        self.createBtn.setIconSize(QSize(80, 80))
        self.createBtn.adjustSize()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        self.boardsContainer = QWidget(self)
        self.boardsContainer.setObjectName("boardsContainer")
        self.boardsListLay = QVBoxLayout(self.boardsContainer)
        self.boardsListLay.setSpacing(10)
        self.boardsListLay.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.boardsListLay.addStretch()
        self.boardsListLay.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.boardsContainer.setStyleSheet("""
                                           QWidget#boardsContainer {
                                            background-color: #516469; 
                                            border: 2px solid white; 
                                            border-radius: 5px;
                                           }""")

        scroll.setWidget(self.boardsContainer)

        layout.addStretch()
        layout.addWidget(scroll, stretch=1)
        # btn.clicked.connect(lambda: switch_page_callback("board") if switch_page_callback else None)

        # layout.addWidget(createBtn)
        self.createBtn.show()

        self.updateBoardsList()
        QTimer.singleShot(0, self.windowSizeUpdate) # без небольшой задержки по вызову бывает баг с смещением по ширине у кнопки
    
    
    def windowSizeUpdate(self):
        rightBottomCorner = self.boardsContainer.mapTo(self, self.boardsContainer.rect().bottomRight()) - QPoint(self.createBtn.width(), self.createBtn.height())
        self.createBtn.move(rightBottomCorner)
        self.createBtn.raise_()
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.windowSizeUpdate()
    
    # def _clearBoardsList(self):
    #     while self.boardsListLay.count():
    #         item = self.boardsListLay.takeAt(0)
    #         widget = item.widget()
    #         if widget:
    #             widget.setParent(None)
    #             widget.deleteLater()

    def updateBoardsList(self):
        boards: dict[str, Board] = self.datamanager.data

        utils.clearLayoutWidgets(self.boardsListLay)

        for key, board in boards.items():
            boardWidget = ClickableWidget()
            boardWidget.setObjectName("boardsListItem")
            boardWidget.setFixedHeight(100)
            boardWidget.setStyleSheet("""
                QWidget#boardsListItem {
                    border: 5px solid #5B6073;
                    border-radius: 10px;
                    background-color: #2C2C2C;
                    padding: 10px;
                }
                QWidget#boardsListItem:hover {
                    background-color: #363636;
                    border-color: #C7CCE1;
                }
            """)
            
            boardLay = QHBoxLayout(boardWidget)
            boardLay.setSpacing(0)

            titleLay = QVBoxLayout()
            title = QLabel("Title: " + board.title)
            boardId = QLabel("ID: " + key)
            boardId.setAlignment(Qt.AlignmentFlag.AlignTop)
            boardId.setStyleSheet("font-size: 10px; color: gray;")
            titleLay.addWidget(title)
            titleLay.addWidget(boardId)
            titleLay.setSpacing(3)
            desc = QLabel("Desc: " + board.description)
            desc.setAlignment(Qt.AlignmentFlag.AlignTop)
            titleLay.setAlignment(Qt.AlignmentFlag.AlignTop)
            boardLay.addLayout(titleLay)
            boardLay.addWidget(desc)
            boardLay.setContentsMargins(boardLay.contentsMargins().left(), 20, boardLay.contentsMargins().right(), boardLay.contentsMargins().bottom())

            boardWidget.clicked.connect(lambda k=key: self.selectBoard(k)) # оказывается ламбда не запоминает значения, а лишь присваивает ссылки, вот те раз
            # благо славненький чат джпт подсказал что от этого можно избавится если присвоить параметр другому параметру

            self.boardsListLay.addWidget(boardWidget)

            for w in (title, boardId, desc):
                w.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
    

    def selectBoard(self, key: str) -> None: 
        print(key)
        self.dataTransfer(Pages.BOARD, {"bid": key})
        self.navigateHandle(Pages.BOARD)


    def _createDialog(self):
        boardCreation = BoardCreationPage(self.window())
        boardCreation.setFixedSize(QSize(512,512))
        status = boardCreation.exec()
        if status == 1:
            self.datamanager.createBoard(boardCreation.title, boardCreation.desc)
            self.updateBoardsList()

    def acceptData(self, data):
        return super().acceptData(data)
    
    def open(self):
        wsize = QSize(500, 500)
        utils.setSizeCentered(self.window(), wsize)
