import numpy as np


def func_test(width_min, height_min, width_max, height_max, arr):
    i_min = min(width_min, height_min)
    i_max = min(width_max, height_max)

    for i in range(i_min, i_max, 5):
        for x in range(width_min, width_max, 5):
            x = x + 2
            for y in range(height_min + i, height_max, 5):
                y = y + 2
                # print(f"Нужно замерить дистанцию")
                print(f"x={x},y={y}")
                arr[x, y] = arr[x - 2, y - 2] = \
                    arr[x - 2, y - 1] = arr[x - 2, y] = \
                    arr[x - 2, y + 1] = arr[x - 2, y + 2] = \
                    arr[x - 1, y - 2] = \
                    arr[x - 1, y - 1] = arr[x - 1, y] = \
                    arr[x - 1, y + 1] = arr[x - 1, y + 2] = \
                    arr[x, y - 2] = arr[x, y - 1] =  \
                    arr[x, y + 1] = arr[x, y + 2] = \
                    arr[x + 1, y - 2] = \
                    arr[x + 1, y - 1] = arr[x + 1, y] = \
                    arr[x + 1, y + 1] = arr[x + 1, y + 2] = \
                    arr[x + 2, y - 2] = \
                    arr[x + 2, y - 1] = arr[x + 2, y] = \
                    arr[x + 2, y + 1] = arr[x + 2, y + 2] = 1

                break
    return arr


if __name__ == '__main__':
    zeors_array = np.zeros((10, 10))
    arr = func_test(0, 0, 9, 9, zeors_array)
    print(arr)
