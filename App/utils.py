from PySide6.QtWidgets import QWidget, QLayout
from PySide6.QtCore import QSize
import sys
import os

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

def resource_path(relative_path):
    """ Получает абсолютный путь к ресурсу при запуске из .exe или из исходников """
    try:
        # PyInstaller создаёт временную папку и кладёт путь в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)