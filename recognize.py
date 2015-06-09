import scipy as sp
from PIL import Image


def get_value(image, x, y, size):
    sum_xy = 0
    sum_x = 0
    sum_y = 0
    sum_x2 = 0
    k = 0
    a = 0
    for i in range(y, y + size):
        for j in range(x, x + size):
            if image[j, i] < 100:
                sum_xy += i * j
                sum_x += j
                sum_y += i
                sum_x2 += j * j
                k += 1
    if k != 0:
        a = (k * sum_xy - sum_x * sum_y) / (k * sum_x2 - sum_x * sum_x)

    if 0 <= a <= 1:
        return 0
    else:
        return 1


def matrix(image, x, y, size, width, height):
    v = sp.zeros((height, width))
    for i in range(height):
        for j in range(width):
            v[i, j] = get_value(image, x + j * size, y + i * size, size)

    return v
