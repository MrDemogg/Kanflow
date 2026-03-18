import json
from pathlib import Path
from enum import StrEnum


class DataManager:
    """
    Пример структуры данных для хранения информации о досках, колонках, задачах и комментариях.
    [
        "уникальный идентификатор доски": {
            "title": "Название доски",
            "description": "Описание доски",
            "columns": [
                {
                    "pos": 0,
                    "title": "Название колонки",
                    "tasks": [
                        {
                            "title": "Название задачи",
                            "description": "Описание задачи",
                            "workers": ["Имя работника", "Имя работника"],
                            "tags": ["Тег1", "Тег2"],
                            "due_date": "2024-12-31",
                            "comments": [
                                {
                                    "author": "Имя комментатора",
                                    "content": "Текст комментария",
                                    "timestamp": "2024-12-31T23:59:59"
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
    
    data = {}

    def __init__(self, file_path="data/kanflowsettings.json"):
        self.file = Path(file_path)
        self.data = self._load()

    def _load(self) -> dict[str, dict[str, any]]:
        if self.file.exists():
            return json.loads(self.file.read_text(encoding="utf-8"))
        return {}

    def save(self):
        self.file.parent.mkdir(parents=True, exist_ok=True)
        self.file.write_text(json.dumps(self.data, ensure_ascii=False, indent=2))

    def createTable(self, title: str, description: str = ""):
        similartitlescount = sum(1 for t in self.data.values() if t["title"] == title)
        id = title if self.data.get(title) is None else f"{title} ({similartitlescount + 1})"
        id.split()
        self.data[id] = {
            BoardKeys.TITLE: title,
            BoardKeys.DESCRIPTION: description,
            BoardKeys.COLUMNS: []
        }

        self.save()

class BoardKeys(StrEnum):
    TITLE = "title"
    DESCRIPTION = "description"
    COLUMNS = "columns"

class ColumnKeys(StrEnum):
    TITLE = "title"
    TASKS = "tasks"
    POS = "pos"

class TaskKeys(StrEnum):
    TITLE = "title"
    DESCRIPTION = "description"
    WORKERS = "workers"
    TAGS = "tags"
    DUE_DATE = "due_date"
    COMMENTS = "comments"

class CommentKeys(StrEnum):
    AUTHOR = "author"
    CONTENT = "content"
    TIMESTAMP = "timestamp"
