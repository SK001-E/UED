# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 14:09:12 2021

@author: Sumit
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import skimage.draw as draw
import math

length = 37
width = 29

#approximate midpoints for the squares for the peaks
P = np.array([181, 123, 216, 140, 383, 265, 175, 210, 284, 365, 320, 385], dtype = int)

os.chdir(r'C:\Users\Sumit\OneDrive - University Of Houston\BNL_trip_UED\indexing')
tempFilename = np.loadtxt('original.dat')
plt.imshow(tempFilename)

for i in range(6):
    arr1=[]
    arr2=[]
    
    for j in range(length):
        for k in range(width):
            arr1.append(P[2*i]-(int(length/2)-j))
            arr2.append(P[2*i+1]-(int(width/2)-k))
            
    a1 = tempFilename[arr1,arr2].reshape((length,width))
            
    filename=('P%d'%(i+1))
    file = open(filename,"wb")
    np.savetxt(file,a1)
    file.close()
            
#always avoid os functions directories with triple quote commenting like #os.chdir(r'C:\Users\Sumit\OneDrive - University Of Houston\BNL_trip_UED\indexing')

"""
d1 = np.array([150.9293333
,116.399
,131.3823333
,89.104
,114.639
,146.1063333
])

a1 = np.array([149.4763333
,159.029
,-83.36833333
,117.7506667
,-12.68733333
,-24.893
])

d2 = np.array([[0]*len(d1)]*len(d1), dtype=float)

for i in range(len(d1)):
    for j in range(len(d1)):
        d2[i,j]=round(math.sqrt((d1[i]**2+d1[j]**2-2*d1[i]*d1[j]*math.cos(math.radians(a1[i]-a1[j])))),2)
"""



#os.chdir(r'C:\Users\Sumit\OneDrive - University Of Houston\BNL_trip_UED\indexing')

"""
file = open('indexing_distance.txt',"wb")
np.savetxt(file,d2)
file.close()
"""

   
      