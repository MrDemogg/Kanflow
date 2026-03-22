import json
from pathlib import Path
from enum import StrEnum

class Comment:
    def __init__(self, author: str, content: str, timestamp: int):
        self.author = author
        self.content = content
        self.timestamp = timestamp
    
    def toDict(self):
        return {
            CommentKeys.AUTHOR: self.author,
            CommentKeys.CONTENT: self.content,
            CommentKeys.TIMESTAMP: self.timestamp
        }
        

class Task:
    def __init__(self, title: str, description: str = "", due_date: int = -1,
                 tags: list[str] =None, workers: list[str]=None, comments: list[Comment] | list[dict[str, any]] = None): 
        # как сказал великий чат джпт - если писать, например, tags=[] вместо tags=None, то элемент может случайно стать общим
        self.title = title
        self.description = description
        self.due_date = due_date
        self.tags: list[str] = tags or []
        self.workers: list[str] = workers or []
        if (isinstance(comments, list) and all(isinstance(x, dict) for x in comments)):
            dComments: list[dict[str, any]] = comments
            self.comments = [Comment(comment[CommentKeys.AUTHOR], comment[CommentKeys.CONTENT], comment[CommentKeys.TIMESTAMP]) for comment in dComments]
        else: self.comments: list[Comment] = comments or []
    
    def toDict(self):
        return {
            TaskKeys.TITLE: self.title,
            TaskKeys.DESCRIPTION: self.description,
            TaskKeys.DUE_DATE: self.due_date,
            TaskKeys.TAGS: self.tags,
            TaskKeys.WORKERS: self.workers,
            TaskKeys.COMMENTS: [c.toDict() for c in self.comments]
        }

class Column:
    tasks = []
    def __init__(self, title: str, tasks: list[Task] | list[dict[str, any]] = None):
        self.title = title
        if (isinstance(tasks, list) and all(isinstance(x, dict) for x in tasks)):
            dTasks: list[dict[str, any]] = tasks # d -> dict
            self.tasks = [Task(task[TaskKeys.TITLE], task[TaskKeys.DESCRIPTION], task[TaskKeys.DUE_DATE], task[TaskKeys.TAGS], task[TaskKeys.WORKERS], task[TaskKeys.COMMENTS]) for task in dTasks]
        else: self.tasks: list[Task] = tasks or []
    
    def toDict(self):
        return {
            ColumnKeys.TITLE: self.title,
            ColumnKeys.TASKS: [t.toDict() for t in self.tasks]
        }

class Board:
    def __init__(self, title: str, description="", columns: list[Column] | list[dict[str, any]] = None):
        self.title = title
        self.description = description
        if (isinstance(columns, list) and all(isinstance(x, dict) for x in columns)):
            dColumns: list[dict[str, any]] = columns
            self.columns = [Column(column[ColumnKeys.TITLE], column[ColumnKeys.TASKS]) for column in dColumns]

        else: self.columns: list[Column] = columns or []

    def toDict(self):
        return {
            BoardKeys.TITLE: self.title,
            BoardKeys.DESCRIPTION: self.description,
            BoardKeys.COLUMNS: [c.toDict() for c in self.columns]
        }
    
class Database:
    def __init__(self, boards: dict[str, Board] | dict[str, dict[str, any]] = None, tags: list[str] = None, workers: list[str] = None):
        if (isinstance(boards, dict) and all(isinstance(x, dict) for x in boards.values())):
            dBoards: dict[str, dict[str, any]] = boards
            self.boards = {k: Board(v[BoardKeys.TITLE], v[BoardKeys.DESCRIPTION], v[BoardKeys.COLUMNS]) for k, v in dBoards.items()}
        else: self.boards = boards or {}
        self.tags = tags or []
        self.workers = workers or []
    
    def toDict(self):
        return {
            DataKeys.BOARDS: {k: v.toDict() for k, v in self.boards.items()},
            DataKeys.TAGS: self.tags,
            DataKeys.WORKERS: self.workers
        }
    

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
                            "due_date": число,
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
    
    def uniqueBid(self, title: str) -> str:
        similartitlescount = sum(1 for t in self.data.boards.values() if t.title == title)
        id = title if self.data.boards.get(title) is None else f"{title} ({similartitlescount})"
        id.split()
        return id

    def createBoard(self, title: str, description: str = ""):
        id = self.uniqueBid(title)

        self.data.boards[id] = Board(title, description, [Column("To Do"), Column("In Work"), Column("Done")])

        self.save()


# с созданием классов в начале файла нижние enum'ы вряд ли будут использоваться, устарели, но пусть будут пока
# о я знаю, они нужны будут для сохранения в json

class DataKeys(StrEnum):
    BOARDS = "boards"
    TAGS = "tags"
    WORKERS = "workers"

class BoardKeys(StrEnum):
    TITLE = "title"
    DESCRIPTION = "description"
    COLUMNS = "columns"

class ColumnKeys(StrEnum):
    TITLE = "title"
    TASKS = "tasks"

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
