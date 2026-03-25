from PySide6.QtWidgets import QLabel, QLineEdit, QApplication, QLayout, QWidget
from PySide6.QtCore import QObject, QEvent, Signal

class EditableLabel(QLabel):

    editingFinished = Signal()

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setText(text)
        self.lineEdit = None
        # self.lineEdit = QLineEdit()
        QApplication.instance().installEventFilter(self)

    def mouseDoubleClickEvent(self, event: QEvent):
        if self.lineEdit is not None:
            return
        
        parent = self.parent()
        if (not isinstance(parent, QWidget)):
            return
        
        layout = parent.layout()
        if (not isinstance(layout, QLayout)):
            return

        self.lineEdit = QLineEdit(self.text(), self.parent())
        # self.lineEdit.setText(self.text())
        # self.lineEdit.setParent(self.parent())
        self.lineEdit.setGeometry(self.geometry()) 
        self.lineEdit.setAlignment(self.alignment())
        self.lineEdit.setFocus()
        self.lineEdit.setSizePolicy(self.sizePolicy())
        self.lineEdit.setFixedSize(self.size())
        self.lineEdit.setFrame(False)
        self.lineEdit.editingFinished.connect(self._finishEditing)
        self.lineEdit.setFont(self.font())

        layout.replaceWidget(self, self.lineEdit)
        self.hide()
        self.lineEdit.show()
        self.lineEdit.setFocus()
        self.lineEdit.selectAll()

    def _finishEditing(self):
        try:
            if (self.lineEdit is None):
                return
            self.setText(self.lineEdit.text())
            parent: QWidget = self.parent()
            layout: QLayout = parent.layout()
            layout.replaceWidget(self.lineEdit, self)
            self.show()
            self.lineEdit.hide()
            self.lineEdit.deleteLater()
            self.lineEdit = None

            self.editingFinished.emit()
        except:
            print("Ошибка которую можно игнорировать") 
            # несмотря на проверку что self.lineEdit != None функция deleteLater так странно работает, что в начале lineEdit мог действительно существовать, 
            # но к момент срабатывания deleteLater lineEdit уже не существует
    
    def eventFilter(self, watched: QObject, event: QEvent):
        if event.type() in (QEvent.Type.MouseButtonPress, QEvent.Type.MouseButtonDblClick):
            if not self.underMouse():
                self._finishEditing()
        return super().eventFilter(watched, event)