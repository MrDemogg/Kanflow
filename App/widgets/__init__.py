# думаю сделать тут стилизованные виджеты, копирки обычных с тем же функционалом, но красивше

# ну, если до этого дойдет...

# И не только стилизованные виджеты получается
from .common import ClickableWidget, EditableLabel, MirrorableWidget
from .app import BoardColumnWidget, DeletableListLabelItem, EditableListWidget, TaskWidget

__all__ = ["ClickableWidget", "BoardColumnWidget", "EditableLabel", "DeletableListLabelItem", "EditableListWidget", "TaskWidget", "MirrorableWidget"]