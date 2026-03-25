from qframelesswindow import FramelessDialog
from PySide6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPlainTextEdit, QPushButton, QWidget
from PySide6.QtGui import QFont, QTextCursor
from PySide6.QtCore import Qt
from App.services import DataManager

class CreationDialog(FramelessDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        from App import DefaultTitleBar
        self.setWindowTitle("Настройка доски")
        self.setObjectName("window")
        self.setSystemTitleBarButtonVisible(False)
        self.setStyleSheet("""
        #window { 
            background-color: #212121;
        }
        """)
        self.setTitleBar(DefaultTitleBar(self, "Настройка доски"))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 50, 24, 24)
        layout.setSpacing(10)
        
        errorLabel = QLabel("Название обязательно должно быть указано!")
        errorLabel.setStyleSheet("color: red;")
        errorLabel.setHidden(True)
        layout.addWidget(errorLabel)

        self.titleForm = QLineEdit()
        self.titleForm.setMaxLength(30)
        self.titleForm.setClearButtonEnabled(True)
        self.titleForm.setPlaceholderText("Название")
        self.titleForm.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.titleForm.setFixedHeight(60)
        self.titleForm.setFont(QFont("Segoe UI", 30))

        layout.addWidget(self.titleForm, stretch=2)

        descFormLay = QVBoxLayout()
        descFormLay.setSpacing(0)
        descFormLay.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.descForm = QPlainTextEdit()
        self.descForm.setMinimumHeight(200)
        self.descForm.setMaximumBlockCount(2)
        self.descForm.setPlaceholderText("Описание (необязательно)")
        self.descForm.setFont(QFont("Segoe UI", 20))
        self.descForm.textChanged.connect(self._descFormLimit)
        
        descFormLay.addWidget(self.descForm)
        descFormLay.setContentsMargins(0, 10, 0, 0)
        descContainer = QWidget()
        descContainer.setLayout(descFormLay)
        layout.addWidget(descContainer, stretch=4)

        acceptBtn = QPushButton("Сохранить")
        acceptBtn.clicked.connect(lambda: self.accept() if len(self.titleForm.text().strip()) > 0 else errorLabel.setHidden(False))
        acceptBtn.setFixedHeight(30)

        rejectBtn = QPushButton("Отмена")
        rejectBtn.clicked.connect(lambda: self.reject())
        rejectBtn.setFixedHeight(30)

        layout.addWidget(acceptBtn)
        layout.addWidget(rejectBtn)


        self.titleBar.raise_()
    
    # так будто бы чуть проще, и данные точно свежие будут
    # а вот я сейчас сюда вернулся и не понимаю нахуя мне в этом случае property
    @property
    def title(self) -> str:
        return self.titleForm.text()
    
    @property
    def desc(self) -> str:
        return self.descForm.toPlainText()
    
    def _descFormLimit(self):
        text = self.descForm.toPlainText()
        maxFormLen = 50
        if len(text) > maxFormLen:
            cursor = self.descForm.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            self.descForm.setPlainText(text[:maxFormLen])