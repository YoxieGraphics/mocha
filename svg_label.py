from PyQt5.QtGui import QPainter, QColor, QPalette
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWidgets import QLabel

class SvgLabel(QLabel):
    def __init__(self, svg_path, parent=None):
        super().__init__(parent)
        self.svg_path = svg_path
        self.renderer = QSvgRenderer(svg_path)

    def paintEvent(self, event):
        color = self.palette().color(QPalette.WindowText)
        painter = QPainter(self)
        self.renderer.render(painter)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(self.rect(), color)
        painter.end()
