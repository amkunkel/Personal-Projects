# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 15:54:44 2021

@author: andre
"""

### VERSION 0.2 ###

# Changes needed:
### DONE Try to figure out a way to change the INSERT thing for comp time
# 2. Generally optimize computation time better: use more efficient data
# types,
### DONE try to find a way to calc the norm using a numpy class instead of by
# hand.
# 3. Find a way to save the plots as higher resolution (for posters)
# 4. Have a max value for the FLI to be to artificially improve the color
# diversity in the map
# 5. Add the Mod 2pi thing?
# 6. Make higher quality axes and label the color bar
# 7. Make second plotting function with no axis labeling or color bar
# and another one that can just replot it with a different color map or
# interpolation type
# 8. Add a color map input to the plotting function
### DONE Make sure the log used by numpy is actually the natural log

# FLI of the Standard Map -> x' = x + k Sin(x + y), y' = x + y

import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt

### To use: run function plotFLI in the console for best results ###
### Parameters are: (window, resolution, kParameter, iterations) ###
# window: the x and y axes that goes from -window to +window
# resolution: roughly corresponds to the density of the grid of initial
#             conditions where a lower value yields a higher density of points
#             at the cost of computation time
# kParameter: refer to literature on the standard map
# iterations: number of times the map is iterated over, generally needs to be
#             in the magnitude of ~100 to show interesting results


# FLI value function for the Standard Map: Choose a 'k' value, Pick initial
# conditions 'xi' and 'yi', Pick number of iterations 'N'

def FLI(xi, yi, k, N):
# Number of iterations of the list (since the first element of the list will be
# the initial conditions of the regular vector and the normal vector, the while
# loop can be set to the actual number of iterations and not n - 1)
# Initial xi, yi conditions of standard map that will come from a grid
# Initial conditions for a normal vector to the standard map
    vix = 1
    viy = 0
# Initial vector creation and iterator i
    i = 0
    masterVec = np.array([[xi, yi, vix, viy]])
    while i < N:
    # Standard map iterator
        xcoord = masterVec[i,0] + k * np.sin(masterVec[i,0] + masterVec[i,1])
        ycoord = masterVec[i,0] + masterVec[i,1]
    # Normal vector iterator
        vxcoord = ((1 + k * np.cos(masterVec[i,0] 
                               + masterVec[i,1])) * masterVec[i,2] 
               + k * np.cos(masterVec[i,0] + masterVec[i,1]) * masterVec[i,3])
        vycoord = masterVec[i,2] + masterVec[i,3]
    # Appending subsiquent vectors
        masterVec = np.append(masterVec, [[xcoord, ycoord, vxcoord, vycoord]], 
                         axis=0)
        i+=1
# Normal vectors taken from the iterated master vector, note the initial
# conditions at the first part have been sliced off
    v = np.array([masterVec[1:,2], masterVec[1:,3]])
        
    # testing out mod 2 pi
    
    v = v % (2*np.pi)
    
    j = 0
# Initializing log array
    vLog = np.array([])
    
    ### OLD HOMEMADE NORM CALCULATOR ###
    # while j < len(v[0]):
    # # Euclidean norm calc
    #     norms = np.sqrt(v[0,j] * v[0,j] + v[1,j] * v[1,j])
    # # Natural log of the norm
    #     logs = np.log(norms)
    # # Inserting solutions into log array
    #     vLog = np.append(vLog, logs)
    #     j+=1
    
    ### NEW LOOP WITH NUMPY NORM CALC ###
    while j < len(v[0]):
    # Temporary vector for the norm and log calc
        tempVec = np.array([v[0,j], v[1,j]])
    # Natural log of the norm and nserting solutions into log array
        vLog = np.append(vLog, np.log(LA.norm(tempVec)))
        j+=1
    # Taking the max of the array of logs to find the FLI value   
    vMax = np.amax(vLog)

    return vMax

### Creates a grid of initial conditions and passes them through the FLI
### calculator

def mapFLI(window, resolution, kParameter, iterations):
# Creating grid of initial conditions based on 'window,' and 'resolution'
# 'window' changes the x and y axes to go from -window to +window symetrically
# 'resolution' corresponds to the density of the grid, so a lower value yields
# a higher resolution map at the cost of computation time
    x = np.arange(-window, window, resolution)
    y = np.arange(-window, window, resolution)
    xi, yi = np.meshgrid(x, y, indexing='ij')
# Saving the lengths since they get used both to iterate through the grid
# and to maintain the shape of the map
    xLength = len(x)
    yLength = len(y)
# Iterating through the grid of initial conditions and applying the FLI
# calculator to each point and saving the result in a 1D array
    arrayFLI = np.array([])
    for i in range(xLength):
        for j in range(yLength):
            arrayFLI = np.append(arrayFLI, FLI(xi[i,j], yi[i,j], 
                                               kParameter, iterations))
# Since we iterated through the matrix like reading book, reshaping the array
# yields a matrix of the same shape just with scalars in each index instead of
# 2D points from the meshgrid
    arrayFLI = arrayFLI.reshape(xLength, yLength)
    
    return arrayFLI, window

### Plotter that takes the FLI map and converts it to a heat map

def plotFLI(window, resolution, kParameter, iterations):
# Using the same window choice to label the axes with in the plotter
    s = mapFLI(window, resolution, kParameter, iterations)[1]
# Interpolator here can "muddy" the image to give it a small sense of
# improved visual quality without having to actually compute more (saves more
# comp time than only increasing the real resolution)
# Choose between: Nearest, Bilinear, or Bicubic
    plt.imshow(mapFLI(window, resolution, kParameter, iterations)[0], 
               cmap='viridis', extent=[-s,s,-s,s],
               aspect=1, interpolation='Nearest', norm=[0,1])
    plt.colorbar()
    plt.show()

