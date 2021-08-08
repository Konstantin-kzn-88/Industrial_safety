import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from PIL import Image


# 1. Построить изображение с данными с нулевым альфа каналом
im = plt.imread('test.png')
implot = plt.imshow(im)
vals = np.random.randint(3, size=(200, 200))
plt.pcolormesh(vals, cmap=plt.get_cmap('jet'), alpha=0)  # levels=levels сглаживание
# plt.axis('off')
plt.colorbar()
plt.savefig('saved_figure.png')
plt.clf()
# 2. Построить по данными цветовую карту с альфа равным 1
vals = np.random.randint(3, size=(200, 200))
plt.pcolormesh(vals, cmap=plt.get_cmap('jet'), alpha=1)  # levels=levels сглаживание
# plt.axis('off')
plt.colorbar()
plt.savefig('saved_figure.png')
img = Image.open('saved_figure.png')
pixdata = img.load()
width, height = img.size
for y in range(height):
    for x in range(width):
        print(pixdata[x,y])
img.save("saved_figure.png", "PNG")
# 3.Наложить два изображения
# filename = 'saved_figure2.png'
# ironman = Image.open(filename, 'r')
# filename1 = 'saved_figure.png'
# bg = Image.open(filename1, 'r')
# text_img = Image.new('RGBA', (600,500), (0, 0, 0, 0))
# text_img.paste(bg, (0,0))
# text_img.paste(ironman, (0,0), mask=ironman)
# text_img.save("ball.png", format="png")




# import matplotlib.pyplot as plt
#
# fig, ax = plt.subplots()
#
# sc = ax.scatter([1, 2], [1, 2], c=[1, 3], cmap='hsv')
# ax.set_ylabel('YLabel', loc='top')
# ax.set_xlabel('XLabel', loc='left')
#
# cbar = fig.colorbar(sc)
# cbar.set_label("ZLabel", loc='top')
#
# plt.show()

# import matplotlib.pyplot as plt
# im = plt.imread('test.png')
# implot = plt.imshow(im)
# plt.plot([100,200,300],[200,150,200], color = (0.1, 0.2, 0.9, 0.5))
# plt.show()
