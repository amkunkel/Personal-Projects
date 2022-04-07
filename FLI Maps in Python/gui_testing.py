# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 17:05:32 2021

@author: andre
"""

import sys
import matplotlib
import numpy as np
from numpy import linalg as LA
matplotlib.use('Qt5Agg')
from PyQt5 import QtWidgets, QtCore, QtGui

from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg, 
                                                NavigationToolbar2QT)
from matplotlib.figure import Figure

class matplotCanvas(FigureCanvasQTAgg):
    
    def __init__(self, parent=None, width=10, height=20, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(matplotCanvas, self).__init__(fig)
        
class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        def FLI(xi, yi, k, N, mod):
            vix = 1
            viy = 0
            i = 0
            masterVec = np.array([[xi, yi, vix, viy]])
            while i < N:
                xcoord = (masterVec[i,0] + k * np.sin(masterVec[i,0]
                                                      + masterVec[i,1]))
                ycoord = masterVec[i,0] + masterVec[i,1]
                vxcoord = ((1 + k * np.cos(masterVec[i,0] 
                                       + masterVec[i,1])) * masterVec[i,2] 
                       + k * np.cos(masterVec[i,0] + masterVec[i,1]) 
                       * masterVec[i,3])
                vycoord = masterVec[i,2] + masterVec[i,3]
                masterVec = np.append(masterVec, 
                                      [[xcoord, ycoord, vxcoord, vycoord]], 
                                 axis=0)
                i+=1
            if mod==True:
                v = (np.array([masterVec[1:,2], masterVec[1:,3]])) % (2*np.pi)
            elif mod==False:
                v = np.array([masterVec[1:,2], masterVec[1:,3]])
            j = 0
            vLog = np.array([])
            while j < len(v[0]):
                tempVec = np.array([v[0,j], v[1,j]])
                vLog = np.append(vLog, np.log(LA.norm(tempVec)))
                j+=1
            vMax = np.amax(vLog)
            return vMax

        def mapFLI(window, resolution, kParameter, iterations, mod):
            x = np.arange(-window, window, resolution)
            y = np.arange(-window, window, resolution)
            xi, yi = np.meshgrid(x, y, indexing='ij')
            xLength = len(x)
            yLength = len(y)
            arrayFLI = np.array([])
            for i in range(xLength):
                for j in range(yLength):
                    arrayFLI = np.append(arrayFLI, FLI(xi[i,j], yi[i,j], 
                                                       kParameter, 
                                                       iterations, mod))
            arrayFLI = arrayFLI.reshape(xLength, yLength)
            return arrayFLI, window
        
        s = mapFLI(4, 0.1, 1, 10, False)

        sc = matplotCanvas(self, width=10, height=20, dpi=100)
        sc.axes.imshow(s[0], cmap='viridis', extent=[-s[1],s[1],-s[1],s[1]],
                       aspect=1, interpolation='Nearest', vmin=0, vmax=10)
        
        toolbar = NavigationToolbar2QT(sc, self)
        
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)
        
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        self.show()
        
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
