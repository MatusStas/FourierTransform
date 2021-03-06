import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QDialog, QApplication

from config import *

import numpy as np

from random import uniform

class PlaygroundWindow(QDialog):
    
    def __init__(self):

        super(PlaygroundWindow, self).__init__()

        loadUi("./windows/playground-window.ui",self)

        # set up listeners
        self.pushButton.clicked.connect(self.goBack)
        self.pushButton_2.clicked.connect(self.getText)
        self.pushButton_3.clicked.connect(self.generatePoints)
        self.horizontalSlider.valueChanged.connect(self.onValueChanged)


    def goBack(self):
        # stop animation
        try:
            self.MatplotlibWidget.animation._stop()
        except Exception as e:
            pass

        mainwindow = MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)


    def getText(self):
        self.MatplotlibWidget.animation._stop()

        self.MatplotlibWidget.pen = False
        self.MatplotlibWidget.arr_drawing = np.empty((1,2))

        # clear and reload subplot
        self.MatplotlibWidget.canvas.axis.clear()
        self.MatplotlibWidget.canvas.axis.set_xlim(AXIS_LIMIT)
        self.MatplotlibWidget.canvas.axis.set_ylim(AXIS_LIMIT)
        self.MatplotlibWidget.line_draw.set_data([],[])
        self.MatplotlibWidget.canvas.draw()

        
        text = self.textEdit.toPlainText()
        text = text.split('\n')

        # if text[-1] == '':
        #     text.pop()

        arr_temp = []
        for coordinates in text:
            x,y = list(map(float, coordinates.strip().split(',')))
            arr_temp.append([x,y])

        # max_x = max(arr_temp, key=lambda x: x[0])[0]
        # max_y = max(arr_temp, key=lambda x: x[1])[1]
        # min_x = min(arr_temp, key=lambda x: x[0])[0]
        # min_y = min(arr_temp, key=lambda x: x[1])[1]

        # dx = (max_x-min_x)/2+min_x
        # dy = (max_y-min_y)/2+min_y

        # # update coordinates relative to center 0,0
        # arr_drawing = []
        # for coordinates in arr_temp:
        #     x,y = coordinates
        #     arr_drawing.append([x-dx,y-dy])

        # # set axes borders
        # LIMIT = max((max_x-min_x)/2,(max_y-min_y)/2)
        # offset = LIMIT*0.5
        # self.MatplotlibWidget.canvas.axis.set_xlim([-LIMIT-offset,LIMIT+offset])
        # self.MatplotlibWidget.canvas.axis.set_ylim([-LIMIT-offset,LIMIT+offset])

        # self.MatplotlibWidget.arr_drawing = arr_drawing
        self.MatplotlibWidget.arr_drawing = arr_temp
        self.MatplotlibWidget.runAnimation()


    def generatePoints(self):
        ## clear all coordinates from text area
        self.textEdit.clear()

        i = self.horizontalSlider_2.value()
        n = 2**(i+2)
        for _ in range(n):
            x = uniform(-20,20)
            y = uniform(-20,20)
            self.textEdit.append(f'{x}, {y}')


    def onValueChanged(self):
        n = self.horizontalSlider.value()
        self.label_2.setText(str(n))


class SecondWindow(QDialog):
    
    def __init__(self):

        super(SecondWindow, self).__init__()

        loadUi("./windows/second-window.ui",self)

        # set up listeners
        self.pushButton.clicked.connect(self.goBack)


    def goBack(self):
        mainwindow = MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

     

class MainWindow(QMainWindow):
    
    def __init__(self):
        
        super(MainWindow, self).__init__()

        loadUi("./windows/main-window.ui",self)

        # set up listeners
        self.pushButton.clicked.connect(self.goPlaygroundWindow)
        self.pushButton_2.clicked.connect(self.goSecondWindow)
    

    def goPlaygroundWindow(self):
        playground_window = PlaygroundWindow()
        widget.addWidget(playground_window)
        widget.setCurrentIndex(widget.currentIndex()+1)


    def goSecondWindow(self):
        second_window = SecondWindow()
        widget.addWidget(second_window)
        widget.setCurrentIndex(widget.currentIndex()+1)



if __name__ == '__main__':
    sys.setrecursionlimit(5000)

    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    mainwindow = MainWindow()
    widget.addWidget(mainwindow)
    widget.setFixedWidth(WINDOW_WIDTH)
    widget.setFixedHeight(WINDOW_HEIGHT)
    widget.show()
    sys.exit(app.exec_())

