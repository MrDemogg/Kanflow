from PySide6.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QSizePolicy, QHBoxLayout, QPushButton, QDateEdit, QCheckBox
from PySide6.QtCore import Qt, QSize, QDate
from PySide6.QtGui import QFont, QIcon
from ..common import EditableLabel, MirrorableWidget
from . import TaskWidget, EditableListWidget
from App.dialogs import CreationDialog
from App.services import DataManager
from App import utils

class BoardColumnWidget(MirrorableWidget):


    def __init__(self, bid: str, title: str, dataManager: DataManager, parent=None, isMirror=False):
        super().__init__(parent=parent, isMirror=isMirror)

        self.bid = bid
        self.dataManager = dataManager
        self.title = title

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
        self.titleLabel.editingFinished.connect(lambda: self.onTitleLabelEdit(self.titleLabel.text()))
        header.addWidget(self.titleLabel, stretch=2)

        imgSize = QSize(50, 50)

        if not self.isMirror:
            self.externalBtn = QPushButton()
            externalNormalIcon = QIcon(utils.resource_path("ui/external.png"))
            externalHoveredIcon = QIcon(utils.resource_path("ui/external2.png"))
            self.externalBtn.setIcon(externalNormalIcon)
            self.externalBtn.enterEvent = lambda e: self.externalBtn.setIcon(externalHoveredIcon)
            self.externalBtn.leaveEvent = lambda e: self.externalBtn.setIcon(externalNormalIcon)
            self.externalBtn.setIconSize(imgSize)
            self.externalBtn.setFixedSize(imgSize)
            self.externalBtn.setObjectName("externalBtn")
            self.externalBtn.setStyleSheet("""
                QPushButton#externalBtn {
                    background: transparent;
                    border: none;
                }
            """)
            self.externalBtn.clicked.connect(self.mirror)
            header.addWidget(self.externalBtn, stretch=1)

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

        addBtn = QPushButton()
        addBtn.setIcon(QIcon(utils.resource_path("ui/create.png")))
        addBtn.clicked.connect(self.onAddTask)

        centralLay.addWidget(addBtn)

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setFixedWidth(280)
    
    def updateTasks(self):
        for i in range(self.contentLayout.count()):
            item = self.contentLayout.itemAt(i)
            widget = item.widget()
            if isinstance(widget, TaskWidget):
                widget.refresh()

    def onAddTask(self):
        taskCreateDialog = CreationDialog(self.window())
        taskCreateDialog.setFixedWidth(512)
        taskCreateDialog.setMinimumHeight(512)
        taskCreateDialog.setMaximumHeight(1024)
        dialogLay = taskCreateDialog.layout()
        
        datePicker = QDateEdit(QDate.currentDate())
        datePicker.setCalendarPopup(True)
        datePicker.setMinimumDate(QDate.currentDate())
        datePicker.setEnabled(False)

        dialogLay.addWidget(datePicker)

        withDateCheckBox = QCheckBox("Конечная дата:")
        withDateCheckBox.setChecked(False)
        withDateCheckBox.toggled.connect(datePicker.setEnabled)

        tagPicker = EditableListWidget("Тэги", checkMax=3)
        workersPicker = EditableListWidget("Участники", checkMax=3)

        for tag in self.dataManager.data.tags:
            tagPicker.addItem(tag)
        
        for worker in self.dataManager.data.workers:
            workersPicker.addItem(worker)
        
        tagPicker.itemAdded.connect(self.dataManager.addTag)
        tagPicker.itemRemoved.connect(self.dataManager.removeTag)
        workersPicker.itemAdded.connect(self.dataManager.addWorker)
        workersPicker.itemRemoved.connect(self.dataManager.removeWorker)

        dialogLay.addWidget(tagPicker)
        dialogLay.addWidget(workersPicker)

        creationStatus = taskCreateDialog.exec()
        if (creationStatus == 1):
            taskTitle = taskCreateDialog.title
            taskDesc = taskCreateDialog.desc
            checkedTags = tagPicker.checkedItems
            checkedWorkers = tagPicker.checkedItems
            due_date = datePicker.date().toString() if withDateCheckBox.isChecked() else ""
            
            uTitle = self.dataManager.createTask(self.bid, self.colIndex(), taskTitle, checkedWorkers, checkedTags, taskDesc, due_date)
            # unique title

            self.contentLayout.addWidget(
                TaskWidget(self, uTitle)
            )

            if self.mirrorWindow.isVisible():
                self.mirror()


    def colIndex(self):
        columns = self.dataManager.data.boards[self.bid].columns
        titles = [col.title for col in columns]
        return utils.indexByFirstEqual(titles, self.title)


    def onTitleLabelEdit(self, newTitle):
        columns = self.dataManager.data.boards[self.bid].columns
        currColumnIndex = self.colIndex()
        newTitleIndex   = utils.indexByFirstEqual([col.title for col in columns], newTitle)

        if newTitleIndex != -1:
            self.titleLabel.setText(self.title)
            if self.mirrorWindow.isVisible():
                self.mirror()
            return
                
        if currColumnIndex < 0:
            print("Что-то здесь не так")
            return
        
        self.title = newTitle
        self.titleLabel.setText(newTitle)
        columns[currColumnIndex].title = self.title
        self.dataManager.save()

        self.updateTasks()

        if self.mirrorWindow.isVisible():
            self.mirror()
        


    def _mirror(self):
        mirrorWindowLay = self.mirrorWindow.layout()

        self.externalBtn.hide()
        mirror = BoardColumnWidget(self.bid, self.title, self.dataManager, isMirror=True)
        mirror.titleLabel.editingFinished.disconnect()
        mirror.titleLabel.editingFinished.connect(lambda: self.onTitleLabelEdit(mirror.titleLabel.text()))
        mirrorWindowLay.addWidget(mirror)
        mirrorWindowLay.setContentsMargins(0, 30, 0, 0)
        self.mirrorWindow.setFixedWidth(self.width())
        self.mirrorWindow.setFixedHeight(self.height() + 30)

    def updateData(self, bid: str = None, title: str = None):
        self.bid = self.bid if bid is None else bid
        self.title = self.title if title is None else title
        self.titleLabel.setText(self.title)
        self.updateTasks()
        if (self.mirrorWindow.isVisible()): self.mirror()

    def onMirrorClose(self):
        self.externalBtn.show()