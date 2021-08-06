
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

sc = ax.scatter([1, 2], [1, 2], c=[1, 3], cmap='jet')
ax.set_ylabel('YLabel', loc='top')
ax.set_xlabel('XLabel', loc='left')

cbar = fig.colorbar(sc)
cbar.set_label("ZLabel", loc='top')

plt.show()

# import matplotlib.pyplot as plt
# im = plt.imread('test.png')
# implot = plt.imshow(im)
# plt.plot([100,200,300],[200,150,200], color = (0.1, 0.2, 0.9, 0.5))
# plt.show()
