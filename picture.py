from PIL import Image, ImageDraw
import scipy as sp
import hamming
from scipy.signal import argrelmax
import border
import mix
import recognize as rec
import PIL


def draw(string, dpi, file_name):
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
    img.save(file_name)


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
    q = border.find("temp.png")
    ind = sp.argmin(sp.sum(q, 1), 0)
    up_left = q[ind, 0] + 2
    up_top = q[ind, 1] + 2
    d_right = q[ind+1, 0] - 3
    d_bottom = q[ind-1, 1] - 3

    h_sum = sp.sum(image, 0)
    m = argrelmax(sp.correlate(h_sum, h_sum, 'same'))
    s = sp.average(sp.diff(m))
    m = int(round(d_right - up_left)/s)
    if m % 3 != 0:
        m += 3 - m % 3
    n = int(round(d_bottom - up_top)/s)
    if n % 4 != 0:
        n += 4 - n % 4
    s = int(round(s))+1
    box = (up_left, up_top, d_right, d_bottom)
    region = image.crop(box)
    region = region.resize((s*m, s*n), PIL.Image.ANTIALIAS)
    region.save("0.png")
    pix = region.load()
    matrix = mix.off(rec.matrix(pix, s, m, n))
    str2 = hamming.decode(array_to_str(matrix))

    return hamming.bin_to_str(str2)