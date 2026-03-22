from PySide6.QtWidgets import QWidget
from App.services import DataManager
from collections.abc import Callable
from abc import abstractmethod # ABC обязательный класс для создания классов с абстрактными методами
from enum import StrEnum

# Базовый класс для всех страниц приложения, хотя не уверен, что он нужен, 
# но пока пусть будет, может потом пригодится для общих методов и свойств страниц

class Page(QWidget):
    def __init__(self, datamanager_: DataManager = None, navigateHandle_: Callable[[str], None] = None, dataTransfer_: Callable[[str, dict], None] = None):
        super().__init__()
        self.datamanager = datamanager_
        self.navigateHandle = navigateHandle_
        self.dataTransfer = dataTransfer_

    @abstractmethod
    def acceptData(self, data: dict):
        """Принятие данных"""
        pass

    @abstractmethod
    def open(self):
        """Что-то что должно происходить при открытии страницы"""
        pass

class Pages(StrEnum):
    HOME = "home"
    BOARD = "board"