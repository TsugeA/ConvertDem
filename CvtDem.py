#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  4 16:05:50 2022

@author: tsuge

This program make Plane Rectangular Coordinate file from Grographic Coordinate file
You have to arrange [Longitude, Latitude, Height] file of GSI dem.
Also, you have to specity the EPSG code of "Plane Rectangular Coordinate System" and 
"Geographic Coordinate System", center coordinate of calculation area, and xy distance of area.
This program read "out.xyz" and write "TopoFile.dat".

"""

from pyproj import Transformer
import numpy as np

#### Input Parameter #### =========================
CenterGrid = [141.148353, 42.499480]    # Center coordinate of calculation area
Xdist, Ydist = 10000., 10000.           # x and y distance of calculation area

EPSGGCS = 4612                          # EPSG code of Geographic Coordinate System
EPSGPRCS = 2454                         # EPSG code of Plane Rectangular Coordinate System


#### Main #### ====================================
## Read file ## ====================
f1 = open('out.xyz','r')
E=[]
while True:
    data=f1.readline()
    if data=='':
        break
    data_in=data.split()
    da=[float(k) for k in data_in]
    E.append(da)

f1.close()

LnLtHtData = np.array(E)


## Transforming Geographic to Plane Rectangular coordinate ## =============
EPSGGCS_to_EPSPRCS = Transformer.from_crs(EPSGGCS, EPSGPRCS)

ypoint, xpoint = EPSGGCS_to_EPSPRCS.transform(LnLtHtData[:,1], LnLtHtData[:,0])
CentY, CentX = EPSGGCS_to_EPSPRCS.transform(CenterGrid[1], CenterGrid[0])


## Making Grid data ## ==============================
UpperX, LowerX = CentX + Xdist / 2, CentX - Xdist / 2
UpperY, LowerY = CentY + Ydist / 2, CentY - Ydist / 2

GridData = np.zeros([len(xpoint), 3])
DN = 0
for m in range(len(xpoint)):
    if (xpoint[m] > LowerX and xpoint[m] < UpperX and ypoint[m] > LowerY and ypoint[m] < UpperY):
        GridData[DN] = np.array([xpoint[m], ypoint[m], LnLtHtData[m,2]])
        DN = DN + 1

GridData[:,0], GridData[:,1] = GridData[:,0] - np.min(GridData[:,0]), GridData[:,1] - np.min(GridData[:,1])
#GridData[:,2] = np.max(GridData[:,2])


## Write output file ## =============================
f2 = open('TopoFile.dat', 'w')
for m in range(DN):
    point = "{:.2f} {:.2f} {:.2f}\n".format(GridData[m,0], GridData[m,1], GridData[m,2])
    f2.write(point)
    
f2.close()
    
