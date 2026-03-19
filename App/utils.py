from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QSize

def setSizeCentered(window: QWidget, size: QSize):
    center = window.frameGeometry().center()

    window.resize(size)

    frame = window.frameGeometry()
    frame.moveCenter(center)
    window.move(frame.topLeft())