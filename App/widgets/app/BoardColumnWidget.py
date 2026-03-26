from PySide6.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QSizePolicy, QHBoxLayout, QPushButton, QDateEdit, QCheckBox
from PySide6.QtCore import Qt, QSize, QDate
from PySide6.QtGui import QFont, QIcon

from ..common import EditableLabel, MirrorableWidget
from .EditableListWidget import EditableListWidget
from App.dialogs import CreationDialog
from App.services import DataManager
from App import utils


class BoardColumnWidget(MirrorableWidget):
    def __init__(self, bid: str, title: str, dataManager: DataManager, parent=None, original=None):
        super().__init__(parent=parent, original=original)

        self.bid = bid
        self.dataManager = dataManager
        self.title = title

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setFixedWidth(280)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        central = QWidget()
        centralLay = QVBoxLayout()
        central.setLayout(centralLay)
        central.setObjectName("Column")
        central.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout.addWidget(central)

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
        header.setContentsMargins(0, 0, 0, 0)
        self.titleLabel = EditableLabel(title)
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.titleLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.titleLabel.setFixedHeight(60)
        self.titleLabel.setFont(QFont("Segoe UI", 25))
        self.titleLabel.editingFinished.connect(lambda: self.onTitleLabelEdit(self.titleLabel.text()))
        header.addWidget(self.titleLabel, stretch=2)

        imgSize = QSize(50, 50)

        if not self.original:
            self.deleteBtn = QPushButton()
            self.deleteBtn.setIcon(QIcon(utils.resource_path("ui/close.png")))
            self.deleteBtn.clicked.connect(self.deleteColumn)
            header.addWidget(self.deleteBtn)

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

        # ==================== Скролл ====================
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

        self.refreshTasks()
    
    def deleteColumn(self):
        from PySide6.QtWidgets import QMessageBox
        from App.pages.BoardPage import BoardPage
        from . import TaskWidget

        confirm = QMessageBox(self)
        confirm.setIcon(QMessageBox.Icon.Warning)
        confirm.setText("Удалить столбец?")
        confirm.setInformativeText(f'Столбец "{self.title}" и все его задачи будут удалены.')
        confirm.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm.exec() == QMessageBox.StandardButton.Yes:
            colIdx = self.colIndex()
            if colIdx < 0:
                return
            if hasattr(self, "mirrorWindow") and self.mirrorWindow and self.mirrorWindow.isVisible():
                self.mirrorWindow.close()

            utils.logger.info(f"Столбец '{self.title}' удален из доски '{self.bid}' вместе с {len(self.dataManager.data.boards[self.bid].columns[colIdx].tasks)} задачами")

            TaskWidget.closeAllTaskMirrorsForColumn(self.bid, colIdx)

            self.dataManager.data.boards[self.bid].columns.pop(colIdx)
            self.dataManager.save()

            # Incremental removal
            boardPage = self.window().findChild(BoardPage)
            if boardPage:
                boardPage.columnsLay.removeWidget(self)
                self.deleteLater()

    def refreshTasks(self):
        from . import TaskWidget
        colIdx = self.colIndex()
        if colIdx < 0:
            utils.clearLayoutWidgets(self.contentLayout)
            return

        tasks = self.dataManager.data.boards[self.bid].columns[colIdx].tasks

        current_widgets = {}
        for i in range(self.contentLayout.count()):
            widget = self.contentLayout.itemAt(i).widget()
            if isinstance(widget, TaskWidget):
                current_widgets[widget.title] = widget

        # Remove widgets not in tasks
        to_remove = []
        for title, widget in current_widgets.items():
            if not any(t.title == title for t in tasks):
                self.contentLayout.removeWidget(widget)
                widget.deleteLater()
                to_remove.append(title)
        for title in to_remove:
            del current_widgets[title]

        # Add new tasks or update existing
        existing_titles = set(current_widgets.keys())
        for taskData in tasks:
            if taskData.title not in existing_titles:
                taskWidget = TaskWidget(self, taskData.title)
                self.contentLayout.addWidget(taskWidget)
                current_widgets[taskData.title] = taskWidget
            else:
                # Update existing
                widget = current_widgets[taskData.title]
                widget.task = taskData
                widget.refresh()

    def updateTasks(self):
        from . import TaskWidget
        for i in range(self.contentLayout.count()):
            widget = self.contentLayout.itemAt(i).widget()
            if isinstance(widget, TaskWidget):
                widget.refresh()

    def onAddTask(self):
        taskCreateDialog = CreationDialog(self.window())
        taskCreateDialog.setMinimumHeight(512)
        taskCreateDialog.setMaximumHeight(1024)
        taskCreateDialog.setBaseSize(QSize(512, 1024))

        dialogLay: QVBoxLayout = taskCreateDialog.layout()

        datePicker = QDateEdit(QDate.currentDate())
        datePicker.setCalendarPopup(True)
        datePicker.setMinimumDate(QDate.currentDate())
        datePicker.setEnabled(False)

        dialogLay.addWidget(datePicker, stretch=1)

        withDateCheckbox = QCheckBox("Конечная дата:")
        withDateCheckbox.setChecked(False)
        withDateCheckbox.toggled.connect(datePicker.setEnabled)
        dialogLay.addWidget(withDateCheckbox, stretch=1)

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

        dialogLay.addWidget(tagPicker, stretch=4)
        dialogLay.addWidget(workersPicker, stretch=4)

        if taskCreateDialog.exec() == 1:
            taskTitle = taskCreateDialog.title
            taskDesc = taskCreateDialog.desc
            checkedTags = tagPicker.checkedItems
            checkedWorkers = workersPicker.checkedItems
            dueDate = datePicker.date().toString() if withDateCheckbox.isChecked() else ""

            self.dataManager.createTask(
                self.bid,
                self.colIndex(),
                taskTitle,
                checkedWorkers,
                checkedTags,
                taskDesc,
                dueDate
            )

            utils.logger.info(f"Задача '{taskTitle}' создана в колонке '{self.title}' доски '{self.bid}' с датой сдачи '{dueDate}'")

            self.refreshTasks()
            paired = self.getPaired()
            if paired:
                paired.refreshTasks()

    def colIndex(self):
        columns = self.dataManager.data.boards[self.bid].columns
        titles = [col.title for col in columns]
        return utils.indexByFirstEqual(titles, self.title)

    def onTitleLabelEdit(self, newTitle: str):
        columns = self.dataManager.data.boards[self.bid].columns
        currIdx = self.colIndex()
        newIdx = utils.indexByFirstEqual([col.title for col in columns], newTitle)

        if newIdx != -1:  # дубликат
            self.titleLabel.setText(self.title)
            return

        if currIdx < 0:
            return

        self.title = newTitle
        self.titleLabel.setText(newTitle)
        columns[currIdx].title = newTitle
        self.dataManager.save()

        utils.logger.info(f"Название колонки поменялось с '{self.title}' на '{newTitle}' в доске '{self.bid}'")

        self.updateTasks()

        paired = self.getPaired()
        if paired:
            paired.titleLabel.setText(newTitle)
            paired.title = newTitle

    def _mirror(self):
        self.externalBtn.hide()
        self.mirrored = BoardColumnWidget(self.bid, self.title, self.dataManager, original=self)


        self.mirrored.titleLabel.editingFinished.disconnect()
        self.mirrored.titleLabel.editingFinished.connect(
            lambda: self.onTitleLabelEdit(self.mirrored.titleLabel.text())
        )

        mirrorWindowLay = self.mirrorWindow.layout()
        mirrorWindowLay.addWidget(self.mirrored)
        mirrorWindowLay.setContentsMargins(0, 30, 0, 0)
        self.mirrorWindow.setFixedWidth(self.width())
        self.mirrorWindow.setFixedHeight(self.height() + 30)

    def updateData(self, bid: str = None, title: str = None):
        # Защита от рекурсии
        if hasattr(self, '_isUpdating') and self._isUpdating:
            return
        self._isUpdating = True

        try:
            changed = False

            if bid is not None and self.bid != bid:
                self.bid = bid
                changed = True

            if title is not None and self.title != title:
                self.title = title
                self.titleLabel.setText(self.title)
                changed = True

            if changed:
                self.updateTasks()

            paired = self.getPaired()
            if paired and paired is not self:
                paired.updateData(bid if bid is not None else None, 
                                  title if title is not None else None)

        finally:
            self._isUpdating = False

    def onMirrorClose(self):
        self.externalBtn.show()