from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from App import Window, utils, DefaultTitleBar
from qframelesswindow.titlebar import SvgTitleBarButton
from qframelesswindow.titlebar.title_bar_buttons import TitleBarButtonState

class MirrorMaxButton(SvgTitleBarButton):
    def __init__(self, iconPath, parent=None):
        super().__init__(iconPath, parent=parent)
        self._isMax = False
        self.setNormalColor(Qt.GlobalColor.white)
        self.setHoverColor(Qt.GlobalColor.lightGray)
        self.setPressedColor(Qt.GlobalColor.gray)

    def setMaxState(self, isMax: bool):
        self._isMax = isMax
        self.setState(TitleBarButtonState.NORMAL)
    
    def setIconColor(self, color):
        """Менять цвет иконки"""
        self.setNormalColor(color)
        self.update()
    
    def setIconHoverColor(self, color):
        """Менять цвет иконки при hover"""
        self.setHoverColor(color)
        self.update()
    
    def paintEvent(self, e):
        from PySide6.QtGui import QPainter
        from PySide6.QtSvg import QSvgRenderer
        from PySide6.QtCore import QRectF
        
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        color, bgColor = self._getColors()

        # draw background
        painter.setBrush(bgColor)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())

        # draw icon
        color = color.name()
        pathNodes = self._svgDom.elementsByTagName('path')
        for i in range(pathNodes.length()):
            element = pathNodes.at(i).toElement()
            element.setAttribute('stroke', color)

        renderer = QSvgRenderer(self._svgDom.toByteArray())
        
        # Правильное центрирование и масштабирование
        rect = QRectF(self.rect())
        new_width = rect.width() * 0.6
        new_height = rect.height() * 0.7
        
        # Центрируем относительно центра кнопки
        x = (rect.width() - new_width) / 2
        y = (rect.height() - new_height) / 2
        
        scaled_rect = QRectF(x, y, new_width, new_height)
        renderer.render(painter, scaled_rect)

class MirrorTitleBar(DefaultTitleBar):
    def __init__(self, parent, onMax, title: str, icon: str = "ui/ico512.png"):
        super().__init__(parent, title, icon)
        newMaxBtn = MirrorMaxButton(utils.resource_path("ui/pin.svg"), parent=self)
        newMaxBtn.clicked.connect(onMax)
        self.hBoxLayout.replaceWidget(self.maxBtn, newMaxBtn)

class MirrorableWidget(QWidget):
    def __init__(self, parent=None, isMirror=False, mirrorTitle=""):
        super().__init__(parent=parent)

        self.isMirror = isMirror
        if isMirror:
            self.mirrorWindow: Window = None
        else:
            self.mirrorWindow = Window(title=mirrorTitle)
            self.mirrorWindow.closing.connect(self.onMirrorClose)

            self.mirrorWindow.setTitleBar(MirrorTitleBar(self.mirrorWindow, self.toggleTopPin, mirrorTitle, "ui/ico512.png"))

    def toggleTopPin(self):
        target_window = self.window() if self.isMirror else self.mirrorWindow
        if target_window is None:
            print("toggleTopPin: target_window is None")
            return

        target_window.toggleStayOnTop()
        self.pinned = bool(target_window.windowFlags() & Qt.WindowType.WindowStaysOnTopHint)
    
    def mirror(self):
        if (self.isMirror): return
        mirrorWindowLay = self.mirrorWindow.layout()
        utils.clearLayoutWidgets(mirrorWindowLay)

        self._mirror()

        self.mirrorWindow.show()
        for btn in self.mirrorWindow.titleBar.findChildren(QWidget):
            btn.clearFocus()
    
    def deleteLater(self): 
        if self.mirrorWindow is not None:
            self.mirrorWindow.close()

        return super().deleteLater()
    
    def _mirror(self):
        """Что нужно сделать дополнительно во время создания зеркала акромя чего-то основного"""
        pass

    def onMirrorClose(self):
        pass