#!/usr/bin/env python
import numpy as np
from scipy import ndimage, misc
import sys, math, os
import argparse


parser = argparse.ArgumentParser(description='Turn a panorama image into a cube map (6 images)')

parser.add_argument("--size", default=512, type=int, help="Size of output image sides")
parser.add_argument("--prefix", default="side_", help="Prefix of output images")
parser.add_argument("--type", default="jpg", help="File Type to save as, jpg, png etc.")
parser.add_argument("--dir", default="./", help="Directory in which to put the output files")
parser.add_argument("input", help="Input panorama file")

args = parser.parse_args()

SIZE = args.size
HSIZE = SIZE / 2.0

im = ndimage.imread(args.input)
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
    misc.imsave(os.path.join(args.dir, "%s%d.%s"%(args.prefix,i,args.type)), side_im)
    
    #Children Exit here
    sys.exit(0)


    
os.waitpid(-1, 0)
