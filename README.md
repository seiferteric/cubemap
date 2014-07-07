# Cubemap

This "renders" the 6 faces of a cube from a panorama input image. 

Usefull if you want to tile your panorama onto a 3D cube for viewing.

Basically, translates each point from each face which is a plane in cartesian
coordinates into spherical coordinates and then gets the pixel value from the
image.

## Prerequisite

1. PIL (or pillow)
1. numpy
1. scipy

# Installation

## Mac OS X Mavericks

1. Install homebrew
1. Install a special homebrewed python
````
brew install python
````
1. Install Python Imaging Libraries (PIL) & numpy
````
pip install pillow numpy scipy
````

