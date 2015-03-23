import scipy as sp


def on(matrix, rows, columns):
    h_size = columns // 3
    v_size = rows // 4
    T = sp.zeros((rows, columns))
    for i in range(sp.size(matrix)):
        T[(i // 12) // h_size + (i % 12) // 3 * v_size, (i // 12) % h_size + i % 3 * h_size] = matrix[i]
    return T


def off(matrix):
    h_size = sp.size(matrix, 1) // 3
    v_size = sp.size(matrix, 0) // 4
    size = sp.size(matrix, 0) * sp.size(matrix, 1)
    T = sp.zeros(size)
    for i in range(size):
        T[i] = matrix[(i // 12) // h_size + (i % 12) // 3 * v_size, (i // 12) % h_size + i % 3 * h_size]
    return T
