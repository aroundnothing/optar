import scipy as sp
import hamming
import mix
import recognize as rec
from PIL import Image, ImageDraw


def line(image, value, x, y, size, width, m):
    d = ImageDraw.Draw(image)
    if value == 0:
        d.line([(x + m, y + m), (x - m + size, y - m + size)], fill=0, width=width)
    else:
        d.line([(x - m + size, y + m), (x + m, y - m + size)], fill=0, width=width)


def draw_matrix(image, matrix, margin_left, margin_top, size, m):
    for i in range(sp.size(matrix, 0)):
        for j in range(sp.size(matrix, 1)):
            line(image, matrix[i, j], size * j + margin_left, size * i + margin_top, size, 1, int(0.5*m))


def str_to_bin(string):
    t = bin(int.from_bytes(string.encode(), 'big'))
    t = t[2:]
    return t


def bin_to_str(string):
    t = int(string, 2)
    return t.to_bytes((t.bit_length() + 7) // 8, 'big').decode()


def array_to_str(array):
    st = ""
    for i in range(sp.size(array)):
        if D[i] == 1:
            st += "1"
        else:
            st += "0"
    return st


f = "Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Ut pharetra lacinia " \
    "libero, eget placerat ante rutrum non. Morbi dapibus id leo nec pulvinar. Nulla et metus a ipsum pellentesque " \
    "euismod. Fusce ut fermentum nisi, vitae vehicula purus. Ut eu tincidunt risus. Cras condimentum varius orci in " \
    "tempor. Etiam blandit, purus et aliquam lobortis, ante ipsum varius mi, eu accumsan urna tellus in neque. Maecenas" \
    " in neque augue. Donec mi arcu, pretium ac diam et, rutrum porta magna. Ut hendrerit eros ut tellus vehicula, " \
    "vitae tempus justo volutpat. Nulla tincidunt tortor vel ex malesuada, sit amet euismod ligula pretium. Vestibulum " \
    "tempor ligula eget lectus eleifend, in suscipit mauris varius. In finibus suscipit dolor, sit amet dignissim dui " \
    "tincidunt at. Cras a ipsum ex. Duis malesuada vulputate libero, et eleifend libero."

str1 = hamming.encode(str_to_bin(f))

dpi = 106
mm = dpi / 25.4
s = int(2*mm)
c_width = int(210*mm)
c_height = int(297*mm)

m = int(round(sp.sqrt(len(str1)) / 4 + 1) * 3)
n = int(round(len(str1) / m / 4 + 1) * 4)

m_left = round((c_width - m * s) / 2)
m_top = round((c_height - n * s) / 2)

A = sp.array(list(str1))
B = mix.on(A, n, m)

img = Image.new("L", (c_width, c_height))
d = ImageDraw.Draw(img)
d.rectangle([(0, 0), img.size], fill=255)
d.rectangle([(int(m_left/4), int(m_top/4)), (int(m_left/4)+int(m_top/2), int(m_top/4)+int(m_top/2))], fill=0)
w = 2
d.line([(m_left-w, m_top-w), (m_left+s*m+w, m_top-w)], fill=0, width=w)
d.line([(m_left-w, m_top-w), (m_left-w, m_top+s*n+w)], fill=0, width=w)
d.line([(m_left+s*m+w, m_top-w), (m_left+s*m+w, m_top+s*n+w)], fill=0, width=w)
d.line([(m_left-w, m_top+s*n+w), (m_left+s*m+w, m_top+s*n+w)], fill=0, width=w)
draw_matrix(img, B, m_left, m_top, s, mm)
img.save("1.png")
pix = img.load()

m1, n1 = rec.matrix_size(img)

D = mix.off(rec.matrix(pix, m_left, m_top, s, m, n))

str2 = array_to_str(D)

str2 = hamming.decode(str2)
print(bin_to_str(str2))




