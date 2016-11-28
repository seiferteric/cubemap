#!/usr/bin/env python
import numpy as np
from scipy import ndimage, misc
import sys, math, os
import argparse
from PIL import Image


parser = argparse.ArgumentParser(description='Turn a panorama image into a cube map (6 images)')

parser.add_argument("--size", default=512, type=int, help="Size of output image sides")
parser.add_argument("--prefix", default="side_", help="Prefix of output images")
parser.add_argument("--type", default="jpg", help="File Type to save as, jpg, png etc.")
parser.add_argument("--dir", default="./", help="Directory in which to put the output files")
parser.add_argument("--onefile", help="Save output as one concatenated file, still uses intermediate files as temp storage.")
parser.add_argument("--quality", type=int, help="Quality of jpeg output. (Only valid for jpeg format)")
parser.add_argument("input", help="Input panorama file")

args = parser.parse_args()

#This is the output image size (side length, its a square)
SIZE = args.size
HSIZE = SIZE / 2.0

im = ndimage.imread(args.input)
#Create blank image of output size, I am using one 2D
#and one 3D so I only have to iterate over 2 axis, need
# to figure out how to do it properly with nditer...
side_im = np.zeros((SIZE, SIZE), np.uint8)
color_side = np.zeros((SIZE, SIZE, 3), np.uint8)
pids = []
for i in range(0,6):
    #Multiple process to go faster!
    pid = os.fork()
    if pid != 0:
        # Keep track of our children
        pids.append(pid)
        continue
    # This is numpy's way of visiting each point in an ndarray, I guess its fast...
    it = np.nditer(side_im, flags=['multi_index'], op_flags=['readwrite'])
    while not it.finished:
        #Axis
        axA = it.multi_index[0]
        axB = it.multi_index[1]
        #Color is an axis, so we visit each point 3 times for R,G,B actually...
   
        #Here for each face we decide what each axis represents, x, y or z. 
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
    
        #Now that we have x,y,z for point on plane, convert to spherical
        r = math.sqrt(float(x*x + y*y + z*z))
        theta = math.acos(float(z)/r)
        phi = -math.atan2(float(y),x)
        
        #Now that we have spherical, decide which pixel from the input image we want.
        ix = int((im.shape[1]-1)*phi/(2*math.pi))
        iy = int((im.shape[0]-1)*(theta)/math.pi)
        #This is faster than accessing the whole tuple! WHY???
        r = im[iy, ix, 0]
        g = im[iy, ix, 1]
        b = im[iy, ix, 2]
        color_side[axA, axB, 0] = r
        color_side[axA, axB, 1] = g
        color_side[axA, axB, 2] = b

        it.iternext()
    #Save output image using prefix, type and index info.
    if args.quality and args.type == "jpg":
        pimg = Image.fromarray(color_side)
        pimg.save(os.path.join(args.dir, "%s%d.%s"%(args.prefix,i,args.type)), quality=args.quality)
    else:
        misc.imsave(os.path.join(args.dir, "%s%d.%s"%(args.prefix,i,args.type)), color_side)
    
    #Children Exit here
    sys.exit(0)


# Thise seems to work better than waitpid(-1, 0), in that case sometimes the
# files still don't exist and we get an error.
for pid in pids: 
    os.waitpid(pid, 0)

#This is handy if we want just one image our program will parse instead of 6.
if args.onefile:
    ifiles = []
    for i in range(0,6):
        ifiles.append(misc.imread(os.path.join(args.dir, "%s%d.%s"%(args.prefix,i,args.type))))
    onefile = np.concatenate(ifiles, axis=1)
    misc.imsave(args.onefile, onefile)    
    for i in range(0,6):
        os.unlink(os.path.join(args.dir, "%s%d.%s"%(args.prefix,i,args.type)))
