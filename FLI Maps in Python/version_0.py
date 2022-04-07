# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 13:38:09 2021

@author: andre

"""
### VERSION 0 ###

# Things to do in next version:
# 1. Try to figure out a way to change the INSERT thing for comp time
# 2. Generally optimize computation time better: use more efficient data
# types, try to find a way to calc the norm using a numpy class instead of by
# hand.
# 3. Turn the matrix slicer into a function with the space and resolution 
# variables as inputs
# 4. Turn ploter into a function so it's easier to call from the console
# 5. Find a way to save the plots as higher resolution (for posters)
# 6. Try an interpolator perhaps to artificially improve resolution to save 
# computation time (just for looks)
# 7. Revert k and n to inputs in the matrix or plotting function, whichever is
# easiest to use
# 8. Have a max value for the FLI to be to artificially improve the color
# diversity in the map


# FLI of the Standard Map -> x' = x + k Sin(x + y), y' = x + y

import numpy as np
import matplotlib.pyplot as plt


# FLI value function for the Standard Map: Choose a 'k' value, Pick initial
# conditions 'xi' and 'yi', Pick number of iterations 'N'

def FLI(xi, yi):
# Parameter k
    k = -0.9
# Number of iterations of the list (since the first element of the list will be
# the initial conditions of the regular vector and the normal vector, the while
# loop can be set to the actual number of iterations and not n - 1)
    n = 100
# Initial conditions of standard map that will come from a grid
    x0 = xi
    y0 = yi
# Initial conditions for a normal vector to the standard map
    v0x = 1
    v0y = 0
# Initial vector creation and iterator i
    i = 0
    masterVec = np.array([[x0, y0, v0x, v0y]])
    while i < n:
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
# Length of one of the v vectors since it gets used twice
    vLength = len(v[0])
# Homemaking the euclidean norm then log mapper in the same loop (there's pro
# probably a numpy class that would work but I couldn't figure it out)
    j = 0
# Making sure the norm vector has the same length as the previous ones
# LOOK INTO USING SOME REPLACE THING INSTEAD OF INSERT
    vLog = np.ones_like(v[0])
    while j < vLength:
    # Euclidean norm calc
        norms = np.sqrt(v[0,j] * v[0,j] + v[1,j] * v[1,j])
    # Natural log of the norm
        logs = np.log(norms)
    # Inserting solutions into log array
        vLog = np.insert(vLog, j, logs, axis=0)
        j+=1
# Deleting all the ones created at the beginning making sure length is correct    
    vLog = vLog[0:vLength]
    #print('Concatenated vector of logs \n', vLog)

    vMax = np.amax(vLog)
    #print('Maximum from the log array \n', vMax)

    return vMax

# Creating grid of initial conditions based on 'space,' and 'resolution'
# parameters where 'space' determines the scale of the square and 'resolution'
# gives the quality of the map
space = 4
resolution = 0.01
x = np.arange(-space, space, resolution)
y = np.arange(-space, space, resolution)
xi, yi = np.meshgrid(x, y, indexing='ij')
# Saving the lengths since they get used both to iterate through the grid
# and to maintain the shape of the map
xLength = len(x)
yLength = len(y)


testarray = np.array([])
for i in range(xLength):
    for j in range(yLength):
        testarray = np.append(testarray, FLI(xi[i,j], yi[i,j]))
testarray = testarray.reshape(xLength,yLength)


plt.imshow(testarray, cmap='viridis', 
           extent=[-space,space,-space,space], aspect=1)
plt.colorbar()
plt.show()

