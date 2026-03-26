from PySide6.QtWidgets import QWidget, QLayout
from PySide6.QtCore import QSize
import sys
import os

def setSizeCentered(window: QWidget, size: QSize):
    center = window.frameGeometry().center()

    window.setMinimumSize(size)
    window.resize(size)
    window.setBaseSize(size)

    frame = window.frameGeometry()
    frame.moveCenter(center)
    window.move(frame.topLeft())

def uniqueId(id: str, ids: list[str]) -> str:
    similaridscount = sum(1 for t in ids if t == id)
    _id = id if similaridscount == 0 else f"{id} ({similaridscount})"
    _id.split()
    return _id

def indexByFirstEqual(arr: list, o):
    return next((i for i in range(len(arr)) if arr[i] == o), -1)

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