#!/usr/bin/env python3

''' Resize image to specified width and proportional height.
    Taken from opensource.com '''

from PIL import Image

name = 'test.jpg' # Add more functionality later

width = 100 # Take as argument

img = Image.open(name)
wpercent = (width / float(img.size[0]))
hsize = int((float(img.size[1]) * float(wpercent)))
img = img.resize((width, hsize), PIL.Image.ANTIALIAS)
img.save('resized_image.jpg')
