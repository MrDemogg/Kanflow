from App.pages import Page, Pages
from PySide6.QtWidgets import QSizePolicy, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QPlainTextEdit, QWidget, QScrollArea
from App.services import DataManager
from collections.abc import Callable
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QFont
from App.widgets import BoardColumnWidget, TaskWidget
from App import utils
from App.dialogs import CreationDialog
from qframelesswindow import FramelessMainWindow

class BoardPage(Page):
    boardId = ""

    def _leavePage(self):
        TaskWidget.closeAllTaskMirrors()

        utils.clearLayoutWidgets(self.columnsLay)
        self.navigateHandle(Pages.HOME)
    
    def __init__(self, datamanager: DataManager, navigateHandle: Callable[[str], None]):
        super().__init__(datamanager, navigateHandle, None)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 40, 40, 20)
        layout.setSpacing(5)

        headerContainer = QWidget()
        headerContainer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        headerContainer.setMinimumHeight(160)

        headerLay = QHBoxLayout(headerContainer)
        headerLay.setContentsMargins(0, 0, 0, 0)
        headerLay.setSpacing(20)

        leftWidget = QWidget()
        leftWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        leftLayout = QVBoxLayout(leftWidget)
        leftLayout.setContentsMargins(0, 0, 0, 0)
        leftLayout.setSpacing(12)

        # Верхняя строка: кнопка (1/3) + title (2/3)
        topRow = QHBoxLayout()
        topRow.setSpacing(15)

        self.leaveBtn = QPushButton()
        self.leaveBtn.setIcon(QIcon(utils.resource_path("ui/left.png")))
        self.leaveBtn.setIconSize(QSize(50, 50))
        self.leaveBtn.setMinimumSize(60, 60)
        self.leaveBtn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.leaveBtn.clicked.connect(self._leavePage)

        self.title = QLabel("Доска не найдена")
        self.title.setFont(QFont("Segoe UI", 30, QFont.Weight.Bold))
        self.title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        topRow.addWidget(self.leaveBtn, stretch=0)
        topRow.addWidget(self.title, stretch=2)

        leftLayout.addLayout(topRow)

        self.desc = QPlainTextEdit()
        self.desc.setReadOnly(True)
        self.desc.setFont(QFont("Segoe UI", 20))
        self.desc.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.desc.setMinimumHeight(80)
        self.desc.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        leftLayout.addWidget(self.desc, stretch=1)

        headerLay.addWidget(leftWidget, stretch=1)

        self.optionBtn = QPushButton()
        self.optionBtn.setIcon(QIcon(utils.resource_path("ui/options.png")))
        self.optionBtn.setIconSize(QSize(58, 58))
        self.optionBtn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.optionBtn.setMinimumWidth(80)
        self.optionBtn.setMinimumHeight(60)
        self.optionBtn.pressed.connect(self.boardOptions)

        headerLay.addWidget(self.optionBtn)

        headerLine = QWidget()
        headerLine.setFixedHeight(2)
        headerLine.setStyleSheet("background-color: white;")

        layout.addWidget(headerContainer, stretch=2)
        layout.addWidget(headerLine)

        columnsScroll = QScrollArea()
        columnsScroll.setWidgetResizable(True)
        columnsScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        columnsScroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        columns = QWidget()
        columns.setObjectName("columns")
        columns.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        self.columnsLay = QHBoxLayout(columns)
        self.columnsLay.setSpacing(20)
        self.columnsLay.setContentsMargins(10, 10, 10, 10)
        columns.setStyleSheet("""
                              QWidget#columns{
                                background-color: #184B57;
                              }""")

        columns.setContentsMargins(0, 0, 0, 0)
        columnsScroll.setWidget(columns)

        layout.addWidget(columnsScroll, stretch=8)

        createBtn = QPushButton("Создать столбец")
        createBtn.clicked.connect(self.onCreateColumn)

        layout.addWidget(createBtn)

    def onCreateColumn(self):
        self.datamanager.createColumn(self.boardId, "Template")
        self.refresh()
    
    def boardOptions(self):
        boardOptWindow = CreationDialog(self.window())
        boardOptWindow.setFixedSize(QSize(512, 512))
        boardOptWindow.titleForm.setText(self.title.text())
        boardOptWindow.descForm.setPlainText(self.desc.toPlainText())

        status = boardOptWindow.exec()

        if status == 1:
            newTitle = boardOptWindow.title
            newDesc = boardOptWindow.desc
            newId = utils.uniqueId(newTitle, [board.title for board in self.datamanager.data.boards.values()])

            boardData = self.datamanager.data.boards[self.boardId]
            boardData.title = newTitle
            boardData.description = newDesc

            self.title.setText(newTitle)
            self.desc.setPlainText(newDesc)

            self.datamanager.data.boards[newId] = self.datamanager.data.boards.pop(self.boardId)
            self.boardId = newId
            for i in range(self.columnsLay.count()):
                item = self.columnsLay.itemAt(i)
                widget = item.widget()
                if isinstance(widget, BoardColumnWidget):
                    widget.updateData(newId, widget.title)

    def refresh(self):
        utils.clearLayoutWidgets(self.columnsLay)
        
        if self.boardId not in self.datamanager.data.boards:
            self.title.setText("Доска не найдена")
            self.desc.setPlainText("")
            self.optionBtn.hide()
            return
        
        self.optionBtn.show()

        board = self.datamanager.data.boards[self.boardId]
        self.title.setText(board.title)
        self.desc.setPlainText(board.description)

        for columnData in board.columns:
            columnWidget = BoardColumnWidget(self.boardId, columnData.title, self.datamanager)
            self.columnsLay.addWidget(columnWidget)

    def open(self):
        wsize = QSize(1080, 720)
        mainw: FramelessMainWindow = self.window()
        mainw.titleBar.maxBtn.show()
        utils.setSizeCentered(self.window(), wsize)

    def acceptData(self, data: dict):
        if "bid" in data.keys():
            self.boardId = data["bid"]
            self.refresh()
