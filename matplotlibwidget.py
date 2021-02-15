from PyQt5.QtWidgets import*

from matplotlib.backends.backend_qt5agg import FigureCanvas

from matplotlib.figure import Figure

import matplotlib.animation as animation

from config import *
from fouriertransform import FourierTransform

import numpy as np
from math import pi

import threading
import time

class MatplotlibWidget(QWidget):
    
    def __init__(self, parent = None):

        QWidget.__init__(self, parent)

        self.CanvasWindow = parent

        self.canvas = FigureCanvas(Figure(dpi=DPI))
        
        # attach matplotlib canvas to layout
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        self.setLayout(vertical_layout)
        
        # canvas setup
        self.canvas.axis = self.canvas.figure.add_subplot(111)
        self.canvas.figure.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
        self.canvas.axis.spines['top'].set_visible(False)
        self.canvas.axis.spines['left'].set_visible(False)
        self.canvas.axis.set_xlim(AXIS_LIMIT)
        self.canvas.axis.set_ylim(AXIS_LIMIT)

        # variables
        self.pressed = False
        self.plotted = False
        self.pen = False
        self.N = 0
        self.arr_drawing_complex = []
        self.time = []
        self.arr_coordinates = []
        self.line_draw, = self.canvas.axis.plot([], [], c='#eb4034', linewidth=1)
        self.arr_drawing = np.empty((1,2))

        # listeners
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.canvas.mpl_connect('button_release_event', self.on_release)


    def on_press(self, event):
        if len(self.arr_drawing[1:]) > 0:
            self.animation._stop()

        if self.plotted:
            # reset variables
            self.plotted = False
            self.arr_drawing = np.empty((1,2))
            self.N = 0

            # clear and reload subplot
            self.canvas.axis.clear()
            self.canvas.axis.set_xlim(AXIS_LIMIT)
            self.canvas.axis.set_ylim(AXIS_LIMIT)
            self.canvas.draw()

        self.pressed = True
        self.pen = True



    def on_motion(self, event):
        if self.pressed:
            self.plotted = True

            # plot drawing points
            coordinates = [event.xdata, event.ydata]
            self.arr_drawing = np.append(self.arr_drawing, [coordinates], axis=0)
            self.line_draw.set_data(self.arr_drawing[1:,0],self.arr_drawing[1:,1])
            self.canvas.axis.draw_artist(self.line_draw)
            self.canvas.blit(self.canvas.axis.bbox)
            self.canvas.flush_events()


    def on_release(self, event):
        self.pressed = False
        self.line_draw.set_data([],[])

        if len(self.arr_drawing) > 0:
            self.runAnimation()


    def getSizes(self):
        arr_radius = np.array([item['amplitude'] for item in self.ft.arr_epicycles])
        rr_pix = (self.canvas.axis.transData.transform(np.vstack([arr_radius, arr_radius]).T) - self.canvas.axis.transData.transform(np.vstack([np.zeros(self.N), np.zeros(self.N)]).T))
        rpix, _ = rr_pix.T
        size_pt = (2*rpix/DPI*72)**2
        return size_pt


    def runAnimation(self):
        self.animation = animation.FuncAnimation(
                            self.canvas.figure,
                            self.animate,
                            init_func=self.init,
                            interval=ANIMATION_INTERVAL,
                            blit=True)


    def init(self):
        # set new values
        if self.pen:
            self.arr_drawing_complex = [complex(coordinates[0], coordinates[1]) for coordinates in self.arr_drawing[1:]]
        else:
            self.arr_drawing_complex = [complex(coordinates[0], coordinates[1]) for coordinates in self.arr_drawing[:]]
        
        self.N = len(self.arr_drawing_complex)
        self.CanvasWindow.horizontalSlider.setMaximum(self.N)
        self.CanvasWindow.horizontalSlider.setValue(self.N)

        # calculate fourier transform via FFT algorithm
        self.ft = FourierTransform(self.arr_drawing_complex)
        self.ft.toEpicycles()

        # calculate all points in time range from 0 to 2pi
        self.time = np.linspace(0,2*pi,endpoint = False, num=self.N)
        self.arr_coordinates = np.array([self.ft.getPoint(dt) for dt in self.time])

        # create all components responsible for showing animation
        self.circle = self.canvas.axis.scatter([],[], fc='None', ec='#9ac7e4', lw=1)
        self.circle.set_sizes(self.getSizes())
        self.line_connect, = self.canvas.axis.plot([], [], c='#9ac7e4', lw=1)
        self.line_plot, = self.canvas.axis.plot([], [], c='#4c6bd5', lw=2)
        self.line_plot_all, = self.canvas.axis.plot([], [], c='#4c6bd5', lw=0.5)

        return [self.circle, self.line_connect, self.line_plot, self.line_plot_all]


    def animate(self,i):
        s = self.CanvasWindow.horizontalSlider.value()+1

        # update components
        self.circle.set_offsets(self.arr_coordinates[:,:s][i%self.N,:-1])
        self.line_connect.set_data(self.arr_coordinates[:,:s][i%self.N,:,0],self.arr_coordinates[:,:s][i%self.N,:,1])
        self.line_plot.set_data(self.arr_coordinates[:,:s][:i%self.N+1,-1,0],self.arr_coordinates[:,:s][:i%self.N+1,-1,1])
        self.line_plot_all.set_data(self.arr_coordinates[:,:s][:,-1,0],self.arr_coordinates[:,:s][:,-1,1])

        return [self.circle, self.line_connect, self.line_plot, self.line_plot_all]
