from PyQt5.QtWidgets import*

from matplotlib.backends.backend_qt5agg import FigureCanvas

from matplotlib.figure import Figure

import matplotlib.animation as animation

from config import *
from fouriertransform import FourierTransform

import numpy as np
from math import pi



class MatplotlibWidget(QWidget):
    
    def __init__(self, parent = None):

        QWidget.__init__(self, parent)

        self.CanvasWindow = parent

        self.canvas = FigureCanvas(Figure(dpi=DPI))
        
        # clip matplotlib canvas to layout
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        self.setLayout(vertical_layout)
        
        # canvas setup
        self.canvas.axis = self.canvas.figure.add_subplot(111)
        self.canvas.axis.set_xlim([-10, 10])
        self.canvas.axis.set_ylim([-10, 10])

        # variables
        self.pressed = False
        self.plotted = False
        self.arr_drawing = []
        self.arr_drawing_complex = []
        self.arr_radius = []
        self.N = None
        self.point_drawn = self.canvas.axis.scatter([],[], c='#eb4034', s=1)

        # listeners
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.canvas.mpl_connect('button_release_event', self.on_release)


    def on_press(self, event):
        if len(self.arr_drawing) > 0:
            self.animation._stop()

        if self.plotted:
            # reset
            self.plotted = False
            self.arr_drawing = []

            # clear and reload subplot
            self.canvas.axis.clear()
            self.canvas.axis.set_xlim([-10, 10])
            self.canvas.axis.set_ylim([-10, 10])
            self.canvas.draw()

        self.pressed = True


    def on_motion(self, event):
        if self.pressed:
            self.plotted = True

            # reset slider
            if self.CanvasWindow.horizontalSlider.value() > 0:
                self.CanvasWindow.horizontalSlider.setMaximum(0)

            # plot drawing points 
            self.arr_drawing.append([event.xdata, event.ydata])
            self.point_drawn.set_offsets(self.arr_drawing)
            self.canvas.axis.draw_artist(self.point_drawn)
            self.canvas.blit(self.canvas.axis.bbox)
            self.canvas.flush_events()


    def on_release(self, event):
        self.pressed = False
        self.CanvasWindow.horizontalSlider.setMaximum(len(self.arr_drawing))
        self.N = len(self.arr_drawing)

        if len(self.arr_drawing) > 0:
            self.arr_drawing_complex = [complex(coordinates[0], coordinates[1]) for coordinates in self.arr_drawing]
            
            ft = FourierTransform(self.arr_drawing_complex)
            ft.toEpicycles()
            
            self.arr_radius = []
            for i in ft.arr_epicycles:
                self.arr_radius.append(i['amplitude'])
            self.arr_radius = np.array([self.arr_radius])

            time = np.linspace(0,2*pi,endpoint = False, num=len(ft.arr_epicycles))
            
            self.xxx = []
            for dt in time:
                self.xxx.append(ft.getPoint(dt))

            self.animation = animation.FuncAnimation(
                                self.canvas.figure,
                                self.animate,
                                init_func=self.init,
                                interval=25,
                                blit=True)


    def init(self):
        # calculate radius in pixels
        rr_pix = (self.canvas.axis.transData.transform(np.vstack([self.arr_radius, self.arr_radius]).T) - self.canvas.axis.transData.transform(np.vstack([np.zeros(self.N), np.zeros(self.N)]).T))
        rpix, _ = rr_pix.T
        size_pt = (2*rpix/DPI*72)**2

        self.circle = self.canvas.axis.scatter([],[],
                        facecolor='None',
                        edgecolor='#9ac7e4',
                        linewidth=1,
                        s=0)

        self.circle.set_sizes(size_pt)

        self.line, = self.canvas.axis.plot([], [],
                        c='#9ac7e4',
                        linewidth=1)

        self.point_plotted = self.canvas.axis.scatter([],[], c='#4c6bd5', s=5)
        return [self.line, self.circle, self.point_plotted]


    def animate(self,i):
        # print(i)
        self.point_drawn.set_offsets(self.arr_drawing)

        # circles
        temp = list(self.xxx[i%self.N][:-1])
        temp.insert(0, [0,0])
        temp = np.array(temp)
        self.circle.set_offsets(temp)

        self.point_plotted.set_offsets(self.arr_drawing[:i%self.N+1])

        # tempx = [[1,2,3],[2,3,5]]
        # tempy = [[2,3,5],[1,2,3]]
        tempx = []
        tempy = []
        for j in temp:
            x,y = j
            tempx.append(x)
            tempy.append(y)

        self.line.set_xdata(tempx)
        self.line.set_ydata(tempy)

        return [self.point_drawn, self.line, self.circle, self.point_plotted]