import scipy as sp


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


def matrix_size(image):
    a = sp.array(image)
    v = a.min(axis=0)
    h = a.min(axis=1)
    w = 0
    for i in range(1, len(v)):
        if v[i - 1] > 150 + v[i]:
            w += 1
    b = 0
    for i in range(1, len(h)):
        if h[i - 1] > 150 + h[i]:
            b += 1
    return w, b