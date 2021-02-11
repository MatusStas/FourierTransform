import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QDialog, QApplication

from config import *

class PlaygroundWindow(QDialog):
    
    def __init__(self):

        super(PlaygroundWindow, self).__init__()

        loadUi("./windows/playground-window.ui",self)

        # set up listeners
        self.pushButton.clicked.connect(self.goBack)
        self.pushButton_2.clicked.connect(self.getText)
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


    def onValueChanged(self):
        print(self.horizontalSlider.value())


    def getText(self):
        print(self.textEdit.toPlainText())

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


# To Do
# - read points from textEdit
# - generate points from radio button (random function)