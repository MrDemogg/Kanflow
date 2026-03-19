from qframelesswindow import FramelessDialog
from PySide6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPlainTextEdit, QPushButton, QWidget
from PySide6.QtGui import QFont, QTextCursor
from PySide6.QtCore import Qt
#from App import CustomTitleBar

class BoardCreationPage(FramelessDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        from App import CustomTitleBar # видимо CustomTitleBar не успевает подготовится если импортировать в начале файла, так что так
        self.setWindowTitle("Create")
        self.setObjectName("window")
        self.setSystemTitleBarButtonVisible(False)
        self.setStyleSheet("""
        #window { 
            background-color: #212121;
        }
        """)
        self.setTitleBar(CustomTitleBar(self, "Создание доски"))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 50, 24, 24)
        layout.setSpacing(0)
        
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
        self.titleForm.setFont(QFont("Segoe UI", 30, QFont.Bold))

        layout.addWidget(self.titleForm)

        descFormLay = QVBoxLayout()
        descFormLay.setSpacing(0)
        descFormLay.setAlignment(Qt.AlignTop)

        self.descForm = QPlainTextEdit()
        self.descForm.setFixedHeight(300)
        self.descForm.setMaximumBlockCount(2)
        self.descForm.setPlaceholderText("Описание (необязательно)")
        self.descForm.setFont(QFont("Segoe UI", 20))
        self.descForm.textChanged.connect(self._descFormLimit)
        
        descFormLay.addWidget(self.descForm)
        descFormLay.setContentsMargins(0, 10, 0, 0)
        descContainer = QWidget()
        descContainer.setLayout(descFormLay)
        layout.addWidget(descContainer)

        acceptBtn = QPushButton("Создать")
        acceptBtn.clicked.connect(lambda: self.accept() if len(self.titleForm.text().strip()) > 0 else errorLabel.setHidden(False))

        rejectBtn = QPushButton("Отмена")
        rejectBtn.clicked.connect(lambda: self.reject())

        layout.addWidget(acceptBtn)
        layout.addWidget(rejectBtn)


        self.titleBar.raise_()


    # так будто бы чуть проще, и данные точно свежие будут
    @property
    def title(self) -> str:
        return self.titleForm.text()
    
    @property
    def desc(self) -> str:
        return self.descForm.toPlainText()
    
    def _descFormLimit(self):
        text = self.descForm.toPlainText()
        maxFormLen = 100
        if len(text) > maxFormLen:
            cursor = self.descForm.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            self.descForm.setPlainText(text[:maxFormLen])