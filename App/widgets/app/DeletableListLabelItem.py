from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from App import utils
from ..common.ClickableWidget import ClickableWidget

class DeletableListLabelItem(ClickableWidget):
    def __init__(self, text="", parent=None):
        super().__init__(parent=parent)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.textLabel = QLabel(text)
        self.textLabel.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.deleteBtn = QPushButton()
        self.deleteBtn.setIcon(QIcon(utils.resource_path("ui/close.png")))
        self.deleteBtn.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.deleteBtn.setObjectName("deleteBtn")
        self.deleteBtn.setStyleSheet("""
            QPushButton#deleteBtn {
                border: 2px solid #A9483B;
                background: transparent;
            }
            QPushButton#deleteBtn:hover {
                background: #A9483B;
            }
        """)
        self.deleteBtn.clicked.connect(self.deleteLater)

        layout.addWidget(self.textLabel, stretch=8)
        layout.addWidget(self.deleteBtn, stretch=1)