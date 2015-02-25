import scipy as sp
from PIL import Image, ImageDraw

fsize = 100
s = 20
A = sp.random.randint(2, size=(fsize))

m = int(round(sp.sqrt(fsize)*0.84/3)*3)
n = int(round(fsize/m/4)*4)

m_left = round((2480-m*s)/2)
m_top = round((3508-n*s)/2)

h_size = m/3
v_size = n/4

C = sp.arange(0, fsize, 1)


def line(im, value, x, y, size, width):
    d = ImageDraw.Draw(im)
    if value == 0:
        d.line([(x, y), (x + size, y + size)], fill=0, width=width)
    else:
        d.line([(x + size, y), (x, y + size)], fill=0, width=width)


def draw_matrix(im, M):
    for i in range(n):
        for j in range(m):
            line(im, M[i, j], s*j+m_left, s*i+m_top, s, 2)


def mix(M):
    T = sp.zeros((n, m))
    for i in range(fsize):
        T[(i//12)//h_size+(i%12)//3*v_size, (i//12)%h_size+i%3*h_size] = M[i]
    return T



img = Image.new("L", (2480, 3508))
d = ImageDraw.Draw(img)
d.rectangle([(0, 0), img.size], fill=255)
B = mix(A)
print(B)
draw_matrix(img, B)
img.save("/home/mm/test/1.png")