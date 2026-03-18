from qframelesswindow import FramelessDialog
from PySide6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPlainTextEdit, QPushButton
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
        self.setTitleBar(CustomTitleBar(self))

        layout = QVBoxLayout(self)
        dialogName = QLabel("Создание доски")
        errorLabel = QLabel("Название обязательно должно быть указано!")
        errorLabel.setStyleSheet("color: red;")
        errorLabel.setHidden(True)
        layout.addWidget(dialogName)
        layout.addWidget(errorLabel)

        self.titleForm = QLineEdit()
        self.titleForm.setMaxLength(30)
        self.titleForm.setClearButtonEnabled(True)

        layout.addWidget(self.titleForm)

        self.descForm = QPlainTextEdit()
        self.descForm.setMaximumHeight(10)
        layout.addWidget(self.descForm)

        acceptBtn = QPushButton("Создать")
        acceptBtn.clicked.connect(lambda: self.accept() if len(self.titleForm.text().strip()) > 0 else errorLabel.setHidden(False))

        rejectBtn = QPushButton("Отмена")
        rejectBtn.clicked.connect(lambda: self.reject())

        layout.addWidget(acceptBtn)
        layout.addWidget(rejectBtn)


    # так будто бы чуть проще, и данные точно свежие будут
    @property
    def title(self) -> str:
        return self.titleForm.text()
    
    @property
    def desc(self) -> str:
        return self.descForm.toPlainText()

        