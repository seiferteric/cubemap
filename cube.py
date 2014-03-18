#!/usr/bin/env python
import numpy as np
from scipy import ndimage, misc
import sys, math, os

SIZE = 512
HSIZE = SIZE / 2.0

im = ndimage.imread(sys.argv[1])
side_im = np.zeros((SIZE, SIZE, 3), np.uint8)

for i in range(0,6):
    pid = os.fork()
    if pid != 0:
        continue 
    it = np.nditer(side_im, flags=['multi_index'], op_flags=['readwrite'])
    while not it.finished:
        axA = it.multi_index[0]
        axB = it.multi_index[1]
        c = it.multi_index[2]
    
        z = -axA + HSIZE

        #if i == 0:
        #    x = HSIZE
        #    y = axB - HSIZE
        #elif i == 1:
        #    x = -axB + HSIZE
        #    y = HSIZE
        #elif i == 2:
        #    x = -HSIZE
        #    y = -axB + HSIZE
        #elif i == 3:
        #    x = axB - HSIZE
        #    y = -HSIZE
        #elif i == 4:
        #    z = HSIZE
        #    x = -axB + HSIZE
        #    y = axA - HSIZE
        #elif i == 5:
        #    z = -HSIZE
        #    x = -axB + HSIZE
        #    y = -axA + HSIZE
        
        if i == 0:
            x = HSIZE
            y = -axB + HSIZE
        elif i == 1:
            x = -HSIZE
            y = axB - HSIZE
        elif i == 2:
            x = axB - HSIZE
            y = HSIZE
        elif i == 3:
            x = -axB + HSIZE
            y = -HSIZE
        elif i == 4:
            z = HSIZE
            x = axB - HSIZE
            y = axA - HSIZE
        elif i == 5:
            z = -HSIZE
            x = axB - HSIZE
            y = -axA + HSIZE
    
        r = math.sqrt(float(x*x + y*y + z*z))
        theta = math.acos(float(z)/r)
        phi = math.atan2(float(y),x)

        ix = (im.shape[1]-1)*phi/(2*math.pi)
        iy = (im.shape[0]-1)*(theta)/math.pi
        it[0] = im[iy, ix, c]
    
    
        it.iternext()
    misc.imsave("out%d.jpg"%i, side_im)
    
    sys.exit(0)


    
os.waitpid(-1, 0)