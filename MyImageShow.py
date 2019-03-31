from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QFont, QCursor
from PyQt5.QtWidgets import QLabel, QListWidgetItem, QMessageBox
import win32gui

class MyFloatPair:
    def __init__(self, x_, y_):
        self.x = x_
        self.y = y_

    def getx(self):
        return self.x

    def gety(self):
        return self.y

class MyImageShow(QLabel):
    def __init__(self, *args, **kwargs):
        super(MyImageShow, self).__init__(*args, **kwargs)
        self.listdata = None
        self.initCache()

    def initCache(self):
        self.originPos = None
        self.origin = False
        self.maxXPos = None
        self.maxX = False
        self.maxYPos = None
        self.maxY = False
        self.points = []
        self.pointSel = False
        self.data = []
        self.startX = 0
        self.endX = 1
        self.startY = 0
        self.endY = 1
        if self.listdata is not None:
            self.listdata.clear()
    def setOriginPos(self, pos_):
        self.originPos = pos_

    def setOrigin(self, flag_):
        self.origin = flag_

    def setMaxX(self, flag_):
        self.maxX = flag_

    def setMaxY(self, flag_):
        self.maxY = flag_

    def setPointSel(self, flag_):
        self.pointSel = flag_

    def setDataList(self, datalist_):
        self.listdata = datalist_

    def setAxisRange(self, sx_, ex_, sy_, ey_):
        self.startX = sx_
        self.endX = ex_
        self.startY = sy_
        self.endY = ey_

    def mousePressEvent(self, event):
        super(MyImageShow, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        super(MyImageShow, self).mouseReleaseEvent(event)
        if self.origin is True:
            self.originPos = event.pos()
            self.origin = False

        if self.maxX is True:
            self.maxXPos = event.pos()
            self.maxX = False

        if self.maxY is True:
            self.maxYPos = event.pos()
            self.maxY = False

        if self.pointSel is True:
            pos = event.pos()
            if self.originPos is None or self.maxXPos is None or self.maxYPos is None:
                QMessageBox.critical(self, 'error', 'Origin, Max X, or Max Y is not specified')
                return
            ratiox = (self.endX - self.startX) / (self.maxXPos.x() - self.originPos.x())
            ratioy = (self.endY - self.startY) / (self.maxYPos.y() - self.originPos.y())
            tmpx = (pos.x() - self.originPos.x()) * ratiox + self.startX
            tmpy = (pos.y() - self.originPos.y()) * ratioy + self.startY
            self.points.append(pos)
            self.data.append(MyFloatPair(tmpx, tmpy))

        self.addAllPoints()

    def addAllPoints(self):
        if self.listdata is not None:
            self.listdata.clear()
            for dd in self.data:
                item = QListWidgetItem("%.4f   %.4f" % (dd.getx(), dd.gety()))
                self.listdata.addItem(item)

    def saveFileData(self, path_):
        with open(path_, 'w') as fd:
            for dd in self.data:
                str = "%.4f   %.4f" % (dd.getx(), dd.gety())
                fd.write(str)

    def removeOneData(self):
        if len(self.points) > 0:
            self.points.pop()
            self.data.pop()
            self.addAllPoints()

    def drawCross(self, pos_, color_):
        painter = QPainter(self)
        painter.setPen(color_)
        x = pos_.x()
        y = pos_.y()
        painter.drawLine(x - 5, y, x + 5, y)
        painter.drawLine(x, y - 5, x, y + 5)

    def paintEvent(self, event):
        super(MyImageShow, self).paintEvent(event)

        if self.originPos is not None:
            self.drawCross(self.originPos, Qt.red)

        if self.maxXPos is not None:
            self.drawCross(self.maxXPos, Qt.red)

        if self.maxYPos is not None:
            self.drawCross(self.maxYPos, Qt.red)

        if self.points is not None:
            for dd in self.points:
                self.drawCross(dd, Qt.green)

        self.update()
