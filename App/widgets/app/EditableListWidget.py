from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QScrollArea, QSizePolicy, QLabel
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize, Signal
from .DeletableListLabelItem import DeletableListLabelItem
from App import utils

class EditableListWidget(QWidget):
    itemAdded = Signal(str)
    itemRemoved = Signal(str)

    def __init__(self, title: str = "", createIconPath: str = "ui/create.png", parent=None, checkMax = -1):
        super().__init__(parent)

        self.checkMax = checkMax
        self.checkedItems: list[str] = []
        self.itemWidgets: dict[str, DeletableListLabelItem] = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        if title:
            titleLabel = QLabel(title)
            titleLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            layout.addWidget(titleLabel)

        header = QWidget()
        headerLayout = QHBoxLayout(header)
        headerLayout.setContentsMargins(0, 0, 0, 0)

        self.inputField = QLineEdit()
        self.inputField.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.createBtn = QPushButton()
        iconSize = QSize(25, 25)
        self.createBtn.setIcon(QIcon(utils.resource_path(createIconPath)))
        self.createBtn.setIconSize(iconSize)
        self.createBtn.setFixedSize(iconSize + QSize(5, 5))
        self.createBtn.setObjectName("createBtn")
        self.createBtn.setStyleSheet("""
            QPushButton#createBtn {
                background: transparent;
                border: 2px solid #3c8f52;
                border-radius: 10px
            }
            QPushButton#createBtn:hover {
                background: #3c8f52
            }
        """)

        headerLayout.addWidget(self.inputField)
        headerLayout.addWidget(self.createBtn)

        header.setMaximumHeight(45)
        layout.addWidget(header)

        # Scroll area for list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        listContainer = QWidget()
        self.listLay = QVBoxLayout(listContainer)
        self.listLay.setAlignment(Qt.AlignmentFlag.AlignTop)

        scroll.setWidget(listContainer)
        layout.addWidget(scroll)

        # Connect create button
        self.createBtn.clicked.connect(lambda: self.addItem(self.inputField.text()))

    def addItem(self, item: str) -> DeletableListLabelItem | None:
        if not item or item in self.itemWidgets:
            return None
        
        widget = DeletableListLabelItem(item)
        widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        widget.setFixedHeight(40)
        widget.setObjectName("deletableLabel")
        widget.setStyleSheet("""
            QWidget#deletableLabel {
                border: none;
                background: transparent
            }
            QWidget#checkedDeletableLabel {
                border: 2px solid white;
                background: transparent
            }
        """)

        widget.deleteBtn.clicked.connect(lambda _, t=item: self.removeItem(t))
        widget.clicked.connect(lambda l=widget: self.onItemClicked(l))
        self.listLay.addWidget(widget)
        self.itemWidgets[item] = widget
        
        self.itemAdded.emit(item)
        return widget

    def removeItem(self, item: str) -> bool:
        if item in self.checkedItems:
            self.checkedItems.remove(item)
        
        if item in self.itemWidgets:
            widget = self.itemWidgets[item]
            self.listLay.removeWidget(widget)
            widget.deleteLater()
            del self.itemWidgets[item]
            self.itemRemoved.emit(item)
            return True
        return False

    def onItemClicked(self, widget: DeletableListLabelItem):
        
        text = widget.textLabel.text()
        if text in self.checkedItems:
            self.checkedItems.remove(text)
            widget.setObjectName("deletableLabel")
        elif (self.checkMax <= 0 or len(self.checkedItems) < self.checkMax):
            self.checkedItems.append(text)
            widget.setObjectName("checkedDeletableLabel")
        
        widget.setStyleSheet("")
        widget.setStyleSheet(widget.styleSheet())