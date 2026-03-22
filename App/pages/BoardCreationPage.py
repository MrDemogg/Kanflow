from qframelesswindow import FramelessDialog
from PySide6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPlainTextEdit, QPushButton, QWidget, QScrollArea, QHBoxLayout, QSizePolicy
from PySide6.QtGui import QFont, QTextCursor, QIcon
from PySide6.QtCore import Qt, QSize
from App.services import DataManager
from App.widgets import DeletableLabel
from App import utils
#from App import CustomTitleBar

class BoardCreationPage(FramelessDialog):

    def __init__(self, datamanager: DataManager, parent=None):
        super().__init__(parent)

        self.datamanager = datamanager

        from App import CustomTitleBar # видимо CustomTitleBar не успевает подготовится если импортировать в начале файла, так что так
        self.setWindowTitle("Настройка доски")
        self.setObjectName("window")
        self.setSystemTitleBarButtonVisible(False)
        self.setStyleSheet("""
        #window { 
            background-color: #212121;
        }
        """)
        self.setTitleBar(CustomTitleBar(self, "Настройка доски"))

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
        self.titleForm.setFont(QFont("Segoe UI", 30, QFont.Bold))

        layout.addWidget(self.titleForm)

        descFormLay = QVBoxLayout()
        descFormLay.setSpacing(0)
        descFormLay.setAlignment(Qt.AlignTop)

        self.descForm = QPlainTextEdit()
        self.descForm.setFixedHeight(200)
        self.descForm.setMaximumBlockCount(2)
        self.descForm.setPlaceholderText("Описание (необязательно)")
        self.descForm.setFont(QFont("Segoe UI", 20))
        self.descForm.textChanged.connect(self._descFormLimit)
        
        descFormLay.addWidget(self.descForm)
        descFormLay.setContentsMargins(0, 10, 0, 0)
        descContainer = QWidget()
        descContainer.setLayout(descFormLay)
        layout.addWidget(descContainer)

        # ------

        tagsContainer = QWidget()
        tagsContainer.setObjectName("tagsContainer")
        tagsContainer.setStyleSheet("""
            QWidget#tagsContainer {
                background: #585858;
                border: 5px solid #3D3D3D;
                border-radius: 15px
            }
        """)
        tagsContainerLay = QVBoxLayout(tagsContainer)

        tagsContainerHeader = QWidget()
        tagsContainerHeaderLay = QHBoxLayout(tagsContainerHeader)
        self.tagInput = QLineEdit()
        self.tagInput.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        tagsCreateButton = QPushButton()
        tagsIconSize = QSize(25, 25)
        tagsCreateButton.setIcon(QIcon(utils.resource_path("ui/create.png")))
        tagsCreateButton.setIconSize(tagsIconSize)
        tagsCreateButton.setFixedSize(tagsIconSize + QSize(5, 5))

        tagsContainerHeaderLay.addWidget(self.tagInput)
        tagsContainerHeaderLay.addWidget(tagsCreateButton)

        tagsContainerHeader.setMaximumHeight(45)
        tagsContainerLay.addWidget(tagsContainerHeader)

        tagsScroll = QScrollArea()
        tagsScroll.setWidgetResizable(True)

        tagsList = QWidget()
        self.tagsListLay = QVBoxLayout(tagsList)
        self.tagsListLay.setAlignment(Qt.AlignmentFlag.AlignTop)

        for tag in datamanager.data.tags:
            self.addTag(tag)

        tagsCreateButton.clicked.connect(lambda: self.addTag(self.tagInput.text()))

        tagsScroll.setWidget(tagsList)

        tagsContainerLay.addWidget(tagsScroll)

        layout.addWidget(tagsContainer)
        # ----

        acceptBtn = QPushButton("Сохранить")
        acceptBtn.clicked.connect(lambda: self.accept() if len(self.titleForm.text().strip()) > 0 else errorLabel.setHidden(False))
        acceptBtn.setFixedHeight(30)

        rejectBtn = QPushButton("Отмена")
        rejectBtn.clicked.connect(lambda: self.reject())
        rejectBtn.setFixedHeight(30)

        layout.addWidget(acceptBtn)
        layout.addWidget(rejectBtn)


        self.titleBar.raise_()
    
    def onTagDestroy(self, tag):
        self.datamanager.data.tags.remove(tag)
        self.datamanager.save()
    
    def addTag(self, tag: str):
        if not tag:
            return
        
        tags = self.datamanager.data.tags
        self.tagInput.clear()
        if any(c.isspace() for c in tag):
            return
        
        if tag not in tags:
            tags.append(tag)
            self.datamanager.save()
        
        deletableLabel = DeletableLabel(tag)
        deletableLabel.deleteBtn.clicked.connect(lambda: self.onTagDestroy(tag))
        deletableLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        deletableLabel.setFixedHeight(70)
        self.tagsListLay.addWidget(deletableLabel)
    
    def removeTag(self, tag: str):
        if tag not in self.datamanager.data.tags:
            return
        
        self.datamanager.data.tags.remove(tag)
        self.datamanager.save()


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