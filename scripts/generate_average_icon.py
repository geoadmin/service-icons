'''
Taken from
https://stackoverflow.com/questions/17291455/how-to-get-an-average-picture-from-100-pictures-using-pil/17383621#17383621
Sanity check which creates the average image from all the icon images since
I did not want to check if every icons is offset so i just looked at the average
'''
import os

import numpy
from PIL import Image

# Access all PNG files in directory
image_dir = os.path.dirname(os.path.realpath(__file__)) + '/../static/images/default/'
script_dir = os.path.dirname(os.path.realpath(__file__))
allfiles = os.listdir(image_dir)
imlist = [filename for filename in allfiles if filename[-4:] in [".png", ".PNG"]]

# Assuming all images are the same size, get dimensions of first image
print(imlist[0])
w, h = Image.open(image_dir + imlist[0]).size
N = len(imlist)

# Create a numpy array of doubles to store the average (assume RGB images)
arr = numpy.zeros((h, w, 4), numpy.double)

# Build up average pixel intensities, casting each image as an array of doubles
for im in imlist:
    imarr = numpy.array(Image.open(image_dir + im), dtype=numpy.double)
    print(imarr)
    arr = arr + imarr/N

# Round values in array and cast as 8-bit integer
arr = numpy.array(numpy.round(arr), dtype=numpy.uint8)

# Generate, save and preview final image
out = Image.fromarray(arr, mode="RGBA")
out.save(script_dir + "/Average.png")
out.show()
print()
