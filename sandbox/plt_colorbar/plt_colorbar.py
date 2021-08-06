import matplotlib.pyplot as plt


image = plt.imread('test200.png')
plt.imshow(image)
vals = []
for i in range(0, 201,1):
    if i < 50:
        val_list = [0.0000033] * 200
    elif i < 100:
        val_list = [0.0000077] * 200
    elif i < 150:
        val_list = [0.0000099] * 200
    vals.append(val_list)


plt.pcolormesh (vals, cmap=plt.get_cmap('jet'), alpha=0.4)# levels=levels сглаживание
plt.axis('off')
plt.colorbar()
plt.show()
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
