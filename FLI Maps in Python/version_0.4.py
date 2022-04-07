# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 09:49:04 2021

@author: andre
"""
### VERSION 0.4 ###

# Changes needed:
# TRYA GUI FOR MOST OF THE INPUTS!!! MAKE SURE TO PRELOAD THE MATRIX FIRST
# THEN DO THE RECOLORING OR ANY RANGE CHANGING SO THAT PART IS FAST, I MEAN
# SET THE RESOLUTION AND WINDOW FIRST, THEN PICK A NEW COLOR SCHEME, MAYBE
# IT HAS A DEFAULT ONE AND DEFAULT RANGE BUT YOU CAN CHANGE THAT VIA BUTTONS
# 2. Generally optimize computation time better: use more efficient data
# types,
# 3. Find a way to save the plots as higher resolution (for posters)
# 6. Make higher quality axes and label the color bar
# 7. Make second plotting function with no axis labeling or color bar
# and another one that can just replot it with a different color map or
# interpolation type
# 8. Add a color map input to the plotting function

# FLI of the Standard Map -> x' = x + k Sin(x + y), y' = x + y

import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
import matplotlib.animation as animation


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
# Optional mod 2pi effect, if "True" in the plotting function then mod 2pi
# is taken for each point, if "False" then the mod isn't taken

    v = np.array([masterVec[1:,2], masterVec[1:,3]])
    
    j = 0
# Initializing log array
    vLog = np.array([])
# Calculating the norm of the two normal vectors, then taking the natural log
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
    
    return arrayFLI

### Plotter that takes the FLI map and converts it to a heat map

# Using the same window choice to label the axes with in the plotter
#s = mapFLI(4, 0.1, 0.3, 100, False)
# Interpolator here can "muddy" the image to give it a small sense of
# improved visual quality without having to actually compute more (saves more
# comp time than only increasing the real resolution)
# Choose between: Nearest, Bilinear, or Bicubic
#plt.imshow(s[0], cmap='viridis', extent=[-s[1],s[1],-s[1],s[1]],
#               aspect=1, interpolation='Nearest', vmin=0, vmax=10)
#plt.colorbar()
#plt.show()

def plottercb(s, window, cmap, vi, vf, axis):
    plt.imshow(s, cmap, extent=[-window,window,-window,window],
                   aspect=1, interpolation='Nearest', vmin=vi, vmax=vf)
    plt.axis(axis)
    plt.colorbar()
    plt.tight_layout()
    plt.show()
    
    
# def plotternocb(s, cmap, vi, vf):
#     plt.imshow(s[0], cmap, extent=[-s[1],s[1],-s[1],s[1]],
#                    aspect=1, interpolation='Nearest', vmin=vi, vmax=vf)
#     plt.axis('off')
#     plt.savefig('image.png', bbox_inches='tight',pad_inches = 0)
#     plt.show()
    
#     plt.close()
    
def plotternocb1(s, window, cmap, vi, vf):
    
    plt.axis('off')
    fig = plt.imshow(s, cmap, extent=[-window,window,-window,window],
                   aspect=1, interpolation='Nearest', vmin=vi, vmax=vf)
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)

    plt.savefig('test_output.pdf',
            bbox_inches='tight',
            pad_inches=0,
            format='pdf',
            dpi=600)
    
    
# cool k values: +-1.5, 1.3, 1.2, 1.1, 0.9 (range 0 to 50, to start)
# will need to adjust the way the "window" works if we want a zoomed sequence
# of maps
# s = mapFLI(4, 0.1, -0.9, 100)
# plotternocb1(s, 4, 'jet', 0, 10)

# ANIMATOR
# def plotteranim(s, window, cmap, vi, vf):
    
#     plt.axis('off')
#     fig = plt.imshow(s, cmap, extent=[-window,window,-window,window],
#                    aspect=1, interpolation='Nearest', vmin=vi, vmax=vf)
#     fig.axes.get_xaxis().set_visible(False)
#     fig.axes.get_yaxis().set_visible(False)
    
# fig = plt.figure()
# ims = []

# for i in range(200):
#     k = i/40
#     window = 4
#     s = mapFLI(window, 0.1, k , 10)
#     im = plt.imshow(s, 'jet', extent=[-window,window,-window,window],
#                    aspect=1, interpolation='Nearest', vmin=0, vmax=15, 
#                    animated =True)
#     im.axes.get_xaxis().set_visible(False)
#     im.axes.get_yaxis().set_visible(False)
#     ims.append([im])
    
# ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
#                                 repeat_delay=1000)
# ani.save('dynamic_images.mp4')
# plt.show()



    
    
    
    
    
    
