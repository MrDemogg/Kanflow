from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from App import utils

class DeletableLabel(QWidget):
    def __init__(self, text="", parent=None):
        super().__init__(parent=parent)
        
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.textLabel = QLabel(text)
        self.deleteBtn = QPushButton()
        self.deleteBtn.setIcon(QIcon(utils.resource_path("ui/close.png")))
        delIconSize = QSize(25, 25)
        self.deleteBtn.setIconSize(delIconSize)
        self.deleteBtn.setFixedSize(delIconSize + QSize(5, 5))
        self.deleteBtn.setObjectName("deleteBtn")
        self.deleteBtn.setStyleSheet("""
            QPushButton#deleteBtn {
                border: 2px solid #A9483B;
                border-radius: 15px;
                background: transparent
            }
            QPushButton#deleteBtn:hover {
                background: #A9483B
            }
        """)
        self.deleteBtn.clicked.connect(self.deleteLater)
        
        layout.addWidget(self.textLabel)
        layout.addWidget(self.deleteBtn)