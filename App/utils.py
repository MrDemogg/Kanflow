from PySide6.QtWidgets import QWidget, QLayout
from PySide6.QtCore import QSize

def setSizeCentered(window: QWidget, size: QSize):
    center = window.frameGeometry().center()

    window.resize(size)

    frame = window.frameGeometry()
    frame.moveCenter(center)
    window.move(frame.topLeft())

def clearLayoutWidgets(layout: QLayout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()