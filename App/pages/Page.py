from PySide6.QtWidgets import QWidget
from App.services import DataManager
from collections.abc import Callable
from abc import ABC, abstractmethod # ABC обязательный класс для создания классов с абстрактными методами

# Базовый класс для всех страниц приложения, хотя не уверен, что он нужен, 
# но пока пусть будет, может потом пригодится для общих методов и свойств страниц

class Page(QWidget, ABC):
    datamanager: DataManager | None = None
    navigateHandle: Callable[[str], None] = None
    dataTransfer: Callable[[str, dict], None] = None
    def __init__(self, datamanager_: DataManager = None, navigateHandle_: Callable[[str], None] = None, dataTransfer_: Callable[[str, dict], None] = None):
        super().__init__()
        self.datamanager = datamanager_
        self.navigateHandle = navigateHandle_
        self.dataTransfer = dataTransfer_

    @abstractmethod
    def acceptData(self, data: dict):
        """Принятие данных"""
        pass
