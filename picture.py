from PIL import Image, ImageDraw
import scipy as sp
import hamming
from scipy.signal import argrelmax
import border
import mix
import recognize as rec


def draw(string, dpi):
    binary_str = hamming.encode(hamming.str_to_bin(string))
    mm = dpi / 25.4
    s = int(2*mm)
    c_width = int(210*mm)
    c_height = int(297*mm)
    m = int(round(sp.sqrt(len(binary_str)) / 4 + 1) * 3)
    n = int(round(len(binary_str) / m / 4 + 1) * 4)

    m_left = int(round((c_width - m * s) / 2))
    m_top = int(round((c_height - n * s) / 2))

    A = sp.array(list(binary_str))
    B = mix.on(A, n, m)

    img = Image.new("L", (c_width, c_height))
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), img.size], fill=255)
    d.rectangle([(int(m_left/4), int(m_top/4)), (int(m_left/4)+int(m_top/2), int(m_top/4)+int(m_top/2))], fill=0)
    w = 1
    d.line([(m_left, m_top), (m_left+s*m, m_top)], fill=0, width=w)
    d.line([(m_left, m_top), (m_left, m_top+s*n)], fill=0, width=w)
    d.line([(m_left+s*m, m_top), (m_left+s*m, m_top+s*n)], fill=0, width=w)
    d.line([(m_left, m_top+s*n), (m_left+s*m, m_top+s*n)], fill=0, width=w)
    draw_matrix(img, B, m_left, m_top, s, mm)
    img.save("1.png")


def line(image, value, x, y, size, width, m):
    d = ImageDraw.Draw(image)
    if value == 0:
        d.line([(x + m, y + m), (x - m + size, y - m + size)], fill=0, width=width)
    else:
        d.line([(x - m + size, y + m), (x + m, y - m + size)], fill=0, width=width)


def draw_matrix(image, matrix, margin_left, margin_top, size, m):
    for i in range(sp.size(matrix, 0)):
        for j in range(sp.size(matrix, 1)):
            line(image, matrix[i, j], size * j + margin_left, size * i + margin_top, size, 2, int(0.5*m))


def array_to_str(array):
    st = ""
    for i in range(sp.size(array)):
        if array[i] == 1:
            st += "1"
        else:
            st += "0"
    return st


def decode(file_name):
    border.rotate(file_name)
    image = Image.open("temp.png")
    pix = image.load()
    q = border.find(file_name)
    m_left = q[1, 0] + 1
    m_top = q[1, 1] + 1

    h_sum = sp.sum(image, 0)
    m = argrelmax(sp.correlate(h_sum, h_sum, 'same'))
    s = int(round(sp.average(sp.diff(m))))
    m = (q[2, 0]-q[1, 0])/s
    n = (q[0, 1]-q[1, 1])/s

    matrix = mix.off(rec.matrix(pix, m_left, m_top, s, m, n))

    str2 = hamming.decode(array_to_str(matrix))

    return hamming.bin_to_str(str2)