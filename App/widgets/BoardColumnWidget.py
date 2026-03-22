from PySide6.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QSizePolicy, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon
from .EditableLabel import EditableLabel
from App.services import DataManager
from App import Window, utils

class BoardColumnWidget(QWidget):

    def toggleTopPin(self):
        w: Window = self.window()
        w.toggleStayOnTop()

        self.pinBtn.setChecked(w.windowFlags() & Qt.WindowType.WindowStaysOnTopHint)

    def __init__(self, bid: str, title: str, dataManager: DataManager, isMirror = False, parent=None):
        super().__init__(parent=parent)
        from App import CustomTitleBar

        self.bid = bid
        self.dataManager = dataManager
        self.title = title

        self.mirrorWindow: Window = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        central = QWidget()
        centralLay = QVBoxLayout()
        central.setLayout(centralLay)
        central.setObjectName("Column")
        central.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout.addWidget(central)

        # Фон и рамка всего столбца
        self.setStyleSheet("""
            QWidget#Column {
                background-color: #658C95;
                border: 2px solid white;
                border-radius: 5px;
            }
        """)

        # ==================== Заголовок ====================
        header = QHBoxLayout()
        header.setSpacing(10)
        header.setContentsMargins(0,0,0,0)
        self.titleLabel = EditableLabel(title)
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.titleLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.titleLabel.setFixedHeight(60)          # фиксированная высота по вашему требованию
        self.titleLabel.setFont(QFont("Segoe UI", 25))
        self.titleLabel.editingFinished.connect(lambda: self.changeColumnTitle(self.titleLabel.text()))
        header.addWidget(self.titleLabel, stretch=2)

        imgSize = QSize(50, 50)

        if not isMirror:
            self.externalBtn = QPushButton()
            externalNormalIcon = QIcon(utils.resource_path("ui/external.png"))
            externalHoveredIcon = QIcon(utils.resource_path("ui/external2.png"))
            self.externalBtn.setIcon(externalNormalIcon)
            self.externalBtn.enterEvent = lambda e: self.externalBtn.setIcon(externalHoveredIcon)
            self.externalBtn.leaveEvent = lambda e: self.externalBtn.setIcon(externalNormalIcon)
            self.externalBtn.setIconSize(imgSize)
            self.externalBtn.setFixedSize(imgSize)
            self.externalBtn.clicked.connect(self._copyInWindow)
            self.externalBtn.setObjectName("externalBtn")
            self.externalBtn.setStyleSheet("""
                QPushButton#externalBtn {
                    background: transparent;
                    border: none;
                }
            """)
            self.mirrorWindow = Window(title="Столб")
            self.mirrorWindow.closing.connect(self.externalBtn.show)
            mirrorTitleBar: CustomTitleBar = self.mirrorWindow.titleBar
            mirrorTitleBar.maxBtn.hide()
            self.externalBtn.clicked.connect(self._copyInWindow)
            header.addWidget(self.externalBtn, stretch=1)
        else:
            self.pinBtn = QPushButton()
            self.pinBtn.setIcon(QIcon(utils.resource_path("ui/pin96.png")))
            self.pinBtn.setIconSize(imgSize)
            self.pinBtn.setFixedSize(imgSize)
            self.pinBtn.setObjectName("pinBtn")
            self.pinBtn.setStyleSheet("""
                                        QPushButton#pinBtn {
                                            border-radius: 10px
                                        }
                                        QPushButton#pinBtn:hover {
                                            border: 2px solid #744516;
                                        }
                                      
                                        QPushButton#pinBtn:checked:hover {
                                            border: 2px solid #115723;
                                        }
                                      
                                        QPushButton#pinBtn:checked {
                                            background: rgba(60, 143, 82, 0.5);
                                            border: 2px solid rgba(60, 143, 82, 0.5);
                                        }
                                    """)
            
            self.pinBtn.setCheckable(True)
            self.pinBtn.clicked.connect(self.toggleTopPin)
            header.addWidget(self.pinBtn, stretch=1)

        centralLay.addLayout(header)

        # ==================== Область с вертикальным скроллбаром ====================
        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        contentWidget = QWidget()
        self.contentLayout = QVBoxLayout(contentWidget)
        self.contentLayout.setContentsMargins(10, 10, 10, 10)
        self.contentLayout.setSpacing(10)
        self.contentLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        scrollArea.setWidget(contentWidget)

        scrollArea.setStyleSheet("border: 1px solid gray; border-radius: 5px;")
        contentWidget.setStyleSheet("background-color: #FADEC3;")

        centralLay.addWidget(scrollArea, stretch=1)

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setFixedWidth(280)

    def changeColumnTitle(self, newTitle):
        columns = self.dataManager.data.boards[self.bid].columns
        currColumnIndex = -1
        for i in range(len(columns)):
            if columns[i].title == self.title:
                currColumnIndex = i
            if columns[i].title == newTitle:
                self.titleLabel.setText(self.title)
                if self.mirrorWindow.isVisible():
                    self._copyInWindow()
                return
        
        if currColumnIndex < 0:
            print("Что-то здесь не так")
            return
        
        self.title = newTitle
        self.titleLabel.setText(newTitle)
        columns[currColumnIndex].title = self.title
        self.dataManager.save()

        if self.mirrorWindow.isVisible():
            self._copyInWindow()

    def _copyInWindow(self): # создает как бы урезанную копию себя же которая обрабатывает большинство изменений не сама, а передает в оригинал
        mirrorWindowLay = self.mirrorWindow.layout()
        
        utils.clearLayoutWidgets(mirrorWindowLay)

        self.externalBtn.hide()
        mirror = BoardColumnWidget(self.bid, self.title, self.dataManager, True)
        mirror.titleLabel.editingFinished.disconnect()
        mirror.titleLabel.editingFinished.connect(lambda: self.changeColumnTitle(mirror.titleLabel.text()))
        mirrorWindowLay.addWidget(mirror)
        mirrorWindowLay.setContentsMargins(0, 30, 0, 0)
        self.mirrorWindow.setFixedWidth(self.width())
        self.mirrorWindow.setFixedHeight(self.height() + 30)
        self.mirrorWindow.show()
        for btn in self.mirrorWindow.titleBar.findChildren(QWidget):
            btn.clearFocus()
    
    def deleteLater(self):
        if self.mirrorWindow is None:
            return
        self.mirrorWindow.close()
        return super().deleteLater()

    def updateData(self, bid: str = None, title: str = None):
        self.bid = self.bid if bid is None else bid
        self.title = self.title if title is None else title
        self.titleLabel.setText(self.title)
        if (self.mirrorWindow.isVisible()): self._copyInWindow()