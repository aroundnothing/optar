import scipy as sp
from PIL import Image, ImageDraw

A = sp.random.randint(2, size=(4, 4))
m = sp.size(A, 0)
n = sp.size(A, 1)
print(A)
s = 10


def line(im, value, x, y, size, width):
    d = ImageDraw.Draw(im)
    if value == 0:
        d.line([(x, y), (x + size, y + size)], fill=0, width=width)
    else:
        d.line([(x + size, y), (x, y + size)], fill=0, width=width)


def draw_matrix(im, M):
    for i in range(m):
        for j in range(n):
            line(im, M[i, j], s*i, s*j, s, 2)


img = Image.new("L", (s*m, s*n))
d = ImageDraw.Draw(img)
d.rectangle([(0, 0), img.size], fill=255)

draw_matrix(img, A)
img.save("/home/mm/test/1.png")
