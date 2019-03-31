# -*- coding: utf-8 -*-
from DataPicker import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Config:
    ImgLoaded = False
    ImgPath   = None
    Rotation  = 0
    Ratio = 3

class MyDataPicker(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyDataPicker, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.statusBar().setSizeGripEnabled(False)
        self.setWindowIcon(QIcon('app.ico'))
        self.setWindowTitle('Data Picker')
        reg_ex = QRegExp("[-+]?[0-9]*\.?[0-9]+")
        startxVal = QRegExpValidator(reg_ex, self.ui.EditStartX)
        endxVal = QRegExpValidator(reg_ex, self.ui.EditEndX)
        startyVal = QRegExpValidator(reg_ex, self.ui.EditStartY)
        endyVal = QRegExpValidator(reg_ex, self.ui.EditEndY)
        self.ui.EditStartX.setValidator(startxVal)
        self.ui.EditEndX.setValidator(endxVal)
        self.ui.EditStartY.setValidator(startyVal)
        self.ui.EditEndY.setValidator(endyVal)

        self.setMaximumSize(QtCore.QSize(800, 400))

        self.ui.SliderZoom.setValue(99)
        self.ui.SliderZoom.valueChanged.connect(self.zoomChangeValue)
        self.ui.BtnLoadImage.clicked.connect(self.loadImage)
        self.ui.BtnClockwise.clicked.connect(self.doClockwise)
        self.ui.BtnAntiClockwise.clicked.connect(self.doAntiClockwise)
        self.ui.BoxProb.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.BtnOrigin.clicked.connect(self.doCoordOrigin)
        self.ui.BtnMaxX.clicked.connect(self.doMaxX)
        self.ui.BtnMaxY.clicked.connect(self.doMaxY)
        self.ui.BtnStart.clicked.connect(self.doStart)
        self.ui.BtnOneStepBack.clicked.connect(self.doOneStepBack)
        self.setMouseTracking(True)
        self.ui.BoxImage.setDataList(self.ui.ListData)
        self.ui.BtnExport2File.clicked.connect(self.doExportData)


    def loadImage(self):
        image = QFileDialog.getOpenFileName(self, 'OpenFile', '', "Image file(*.png)")
        Config.ImgPath = image[0]
        # original image
        self.srcImage = QImage(Config.ImgPath)
        pixmap = QPixmap.fromImage(self.srcImage)
        self.showImage(pixmap)
        Config.ImgLoaded = True
        self.ui.BoxImage.initCache()

    def showImage(self, pixmap_):
        wid = self.ui.BoxImage.width()
        hei = self.ui.BoxImage.height()
        pixmap2 = pixmap_.scaled(wid, hei, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ui.BoxImage.setPixmap(pixmap2)

    def doClockwise(self):
        if Config.ImgPath is None:
            return
        img = QImage(Config.ImgPath)
        Config.Rotation += 1
        transform = QTransform().rotate(Config.Rotation)
        pixmap = QPixmap.fromImage(img)
        pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)

        self.showImage(pixmap)

    def doAntiClockwise(self):
        if Config.ImgPath is None:
            return
        img = QImage(Config.ImgPath)
        Config.Rotation -= 1
        transform = QTransform().rotate(Config.Rotation)
        pixmap = QPixmap.fromImage(img)
        pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)

        self.showImage(pixmap)

    def doCoordOrigin(self):
        if Config.ImgPath is None:
            return
        self.ui.BoxImage.setOrigin(True)

    def doMaxX(self):
        if Config.ImgPath is None:
            return
        self.ui.BoxImage.setMaxX(True)

    def doMaxY(self):
        if Config.ImgPath is None:
            return
        self.ui.BoxImage.setMaxY(True)

    def doStart(self):
        if Config.ImgPath is None:
            return
        sx = self.ui.EditStartX.text()
        sy = self.ui.EditStartY.text()
        ex = self.ui.EditEndX.text()
        ey = self.ui.EditEndY.text()

        if sx.strip() == '' or sy.strip() == '' or ex.strip() == '' or ey.strip() == '':
            QMessageBox.critical(self, 'error', 'Axis values are not entered')
            return

        startx = float(sx)
        starty = float(sy)
        endx = float(ex)
        endy = float(ey)

        if(startx > endx):
            QMessageBox.critical(self, 'error', 'Start X is bigger than End X')
            return

        if (starty > endy):
            QMessageBox.critical(self, 'error', 'Start Y is bigger than End Y')
            return

        self.ui.BoxImage.setAxisRange(startx, endx, starty, endy)
        self.ui.BoxImage.setPointSel(True)

    def doExportData(self):
        path = QFileDialog.getSaveFileName(self, 'Save File')
        if len(path[0].strip()) > 0:
            self.ui.BoxImage.saveFileData(path[0])

    def doOneStepBack(self):
        self.ui.BoxImage.removeOneData()

    def zoomChangeValue(self):
        val = self.ui.SliderZoom.value()
        Config.Ratio = val * 3 / 100

    def setMouseTracking(self, flag):
        def recursive_set(parent):
            for child in parent.findChildren(QtCore.QObject):
                try:
                    child.setMouseTracking(flag)
                except:
                    pass
                recursive_set(child)

        QWidget.setMouseTracking(self, flag)
        recursive_set(self)

    def mouseMoveEvent(self, event):
        super(MyDataPicker, self).mouseMoveEvent(event)
        # change the shape of cursor
        pos = event.pos()
        if self.ui.BoxImage.rect().contains(pos):
            self.setCursor(Qt.CrossCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

        #
        pos = self.mapToGlobal(event.pos())
        self.ui.BoxProb.setPos(pos.x(), pos.y())
        # 截图
        screen = QApplication.primaryScreen()
        wid = self.ui.BoxProb.width()
        hei = self.ui.BoxProb.height()
        if screen is not None:
            image = screen.grabWindow(0, pos.x() - int(wid / 2), pos.y() - int(hei / 2), wid, hei)
            if not image.isNull():
                self.ui.BoxProb.setPixmap(image.scaled(wid * Config.Ratio, hei * Config.Ratio, Qt.KeepAspectRatio, Qt.SmoothTransformation))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    myshow = MyDataPicker()
    myshow.show()
    sys.exit(app.exec_())