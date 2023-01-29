# import the modules
import os
from os import listdir

from PIL import Image, ImageOps;
import numpy as np;
 
total = list()

counter = 0

# 0 is non demented
# 1 is mild demented
# 2 is moderate demented

# get the path/directory
folder_dir = r"C:\IQHack 2023\Training\Test"
print('Start')
for images in os.listdir(folder_dir):
    
        temp = Image.open(folder_dir + "\\" + images)
        img = ImageOps.grayscale(temp)

        data = np.array(img).ravel()
        data = np.append(data, (2))
        total.append(data)

np.savetxt("Test.csv", total, delimiter=",")
print("Done")