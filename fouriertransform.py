import numpy as np
from scipy.fft import fft, ifft
from math import atan2, cos, sin, pi


class FourierTransform:
    def __init__(self, arr_drawing):
        self.arr_fourier = fft(arr_drawing)
        self.arr_epicycles = []


    def toEpicycles(self):
        self.arr_fourier /= len(self.arr_fourier)
        self.arr_epicycles = []
        for i,point in enumerate(self.arr_fourier):
            frequency = i
            amplitude = (point.real**2 + point.imag**2)**0.5
            phase = atan2(point.imag,point.real)
            self.arr_epicycles.append({'frequency':frequency, 'amplitude':amplitude, 'phase':phase})

        self.arr_epicycles.sort(key=lambda x: x['amplitude'], reverse=True)


    def getPoint(self,dt):
        x = 0
        y = 0
        temp = []
        for epicycle in self.arr_epicycles:
            x += epicycle['amplitude']*cos(epicycle['frequency']*dt+epicycle['phase'])
            y += epicycle['amplitude']*sin(epicycle['frequency']*dt+epicycle['phase'])
            temp.append([round(x, 5),round(y, 5)])
        return temp
