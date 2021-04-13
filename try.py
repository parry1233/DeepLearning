from numpy.core.fromnumeric import size
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

id = ['cat','dog']
value = [1,0]
def Check(value):
    if value == 0:
        return 'Dog'
    else:
        return 'Cat'
for i in range(len(id)):
    print(id[i])
    print(value[i])
    filename = 'KaggleData/sample/'+str(id[i])+'.jpg'
    print(filename)
    print(Check(value[i]))

    img = Image.open(filename)
    draw = ImageDraw.Draw(img)
    draw.text((100,200),Check(value[i]),(255,255,255),size = 1000)
    img.save(str(id[i])+'.png')

