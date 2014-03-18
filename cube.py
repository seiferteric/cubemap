#!/usr/bin/env python
import numpy as np
from scipy import ndimage, misc
import sys, math

SIZE = 512
im = ndimage.imread(sys.argv[1])
side_im = np.zeros((SIZE, SIZE, 3), np.uint8)

for i in range(0,6):
    it = np.nditer(side_im, flags=['multi_index'], op_flags=['readwrite'])
    ps = []
    while not it.finished:
        z = -it.multi_index[0] + SIZE / 2.0
        c = it.multi_index[2]

        if i == 0:
            x = SIZE / 2.0
            y = it.multi_index[1] - SIZE / 2.0
        elif i == 1:
            x = -it.multi_index[1] + SIZE / 2.0
            y = SIZE / 2.0
        elif i == 2:
            x = -SIZE/2.0
            y = -it.multi_index[1] + SIZE / 2.0
        elif i == 3:
            x = it.multi_index[1] - SIZE / 2.0
            y = -SIZE/2.0
        elif i == 4:
            z = SIZE / 2.0
            x = -it.multi_index[1] + SIZE / 2.0
            y = it.multi_index[0] - SIZE / 2.0 
        elif i == 5:
            z = -SIZE / 2.0
            x = -it.multi_index[1] + SIZE / 2.0
            y = -it.multi_index[0] + SIZE / 2.0
        
    
        r = math.sqrt(float(x*x + y*y + z*z))
        theta = math.acos(float(z)/r)
        phi = math.atan2(float(y),x)

        ps.append(phi) 
        ix = (im.shape[1]-1)*phi/(2*math.pi)
        iy = (im.shape[0]-1)*(theta)/math.pi
        it[0] = im[iy, ix, c]
    
    
        it.iternext()
    misc.imsave("out%d.jpg"%i, side_im)
    
