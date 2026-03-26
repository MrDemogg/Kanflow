import json
from pathlib import Path
from App.models.DataModels import *
from App import utils

class DataManager:
    """
    Пример структуры данных для хранения информации о досках, колонках, задачах и комментариях.
    [
        "уникальный идентификатор доски": {
            "title": "Название доски",
            "description": "Описание доски",
            "columns": [
                {
                    "title": "Название колонки",
                    "tasks": [
                        {
                            "title": "Название задачи",
                            "description": "Описание задачи",
                            "workers": ["Имя работника", "Имя работника"],
                            "tags": ["Тег1", "Тег2"],
                            "due_date": строка,
                            "comments": [
                                {
                                    "author": "Имя комментатора",
                                    "content": "Текст комментария",
                                    "timestamp": число
                                },
                                ...
                            ]
                        },
                        ...
                    ]
                },
                ...
            ]
        },
        ...
    ]
    """
    
    data: Database = None

    def __init__(self, file_path="data/kanflowdata.json"):
        self.file = Path(file_path)
        self._load()

    def _load(self) -> dict[str, Board]:
        if self.file.exists():
            data: dict[str, any] = json.loads(self.file.read_text(encoding="utf-8"))
            boardsData: dict[str, dict[str, any]] = data[DataKeys.BOARDS]
            tagsData: dict[str] = data[DataKeys.TAGS]
            workersData: dict[str] = data[DataKeys.WORKERS]
            self.data = Database(boardsData, tagsData, workersData)
        else: self.data = Database()

    def save(self):
        self.file.parent.mkdir(parents=True, exist_ok=True)
        self.file.write_text(json.dumps(self.data.toDict(), ensure_ascii=True, indent=2))

    def createBoard(self, title: str, description: str = "") -> str:
        id = utils.uniqueId(title, [board.title for board in self.data.boards.values()])

        self.data.boards[id] = Board(title, description, [Column("To Do"), Column("In Work"), Column("Done")])

        self.save()

        return id
    
    def createColumn(self, bid: str, title: str):
        id = utils.uniqueId(title, [column.title for column in self.data.boards[bid].columns])

        self.data.boards[bid].columns.append(Column(id))

        self.save()

    def createTask(self, bid: str, cindex, title: str, workers: list[str] = None, tags: list[str] = None, description: str = "", due_date: str = None):
        column = self.data.boards[bid].columns[cindex]
        uniquetitle = utils.uniqueId(title, [t.title for t in column.tasks])
        column.tasks.append(
            Task (
                uniquetitle,
                description,
                due_date,
                tags,
                workers
            )
        )

        self.save()

        return uniquetitle

    def addTag(self, tag: str):
        if (tag not in self.data.tags):
            self.data.tags.append(tag)
            self.save()
    
    def addWorker(self, worker: str):
        if (worker not in self.data.workers):
            self.data.workers.append(worker)
            self.save()
    
    def removeTag(self, tag: str):
        if tag in self.data.tags:
            self.data.tags.remove(tag)
            self.save()

    def removeWorker(self, worker: str):
        if worker in self.data.workers:
            self.data.workers.remove(worker)
            self.save()