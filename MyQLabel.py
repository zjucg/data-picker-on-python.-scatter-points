from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QFont, QCursor
from PyQt5.QtWidgets import QLabel, QApplication
import win32gui

class MyQLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super(MyQLabel, self).__init__(*args, **kwargs)
        self.posX = 0
        self.posY = 0

    def setPos(self, x_, y_):
        self.posX = x_
        self.posY = y_

    def paintEvent(self, event):
        super(MyQLabel, self).paintEvent(event)
        # 中正间画十字
        painter = QPainter(self)
        painter.setPen(Qt.red)
        x = int(self.width() / 2)
        y = int(self.height() / 2)
        painter.drawLine(x, 0, x, self.height())
        painter.drawLine(0, y, self.width(), y)
        # 画坐标点
        painter.setPen(Qt.black)
        font = QFont()
        font.setPointSize(7)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignLeft | Qt.AlignBottom, ' ({}, {})'.format(self.posX, self.posY))