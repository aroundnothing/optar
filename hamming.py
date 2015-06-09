import scipy as sp

tr_matrix = sp.array([[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                      [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0],
                      [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]])


def str_to_bin(string):
    return "".join(["{0:08b}".format(x) for x in bytearray(string)])


def bin_to_str(string):
    binaries = [string[8*i:8*i+8] for i in xrange(len(string)//8)]
    decimals = [int(x, 2) for x in binaries]
    return str(bytearray(decimals))


def str_to_list_8(string, k):
    st = []
    for i in range(k):
        t = list(string[i * 8: (i + 1) * 8])
        t[0:0] = '0'
        t[1:1] = '0'
        t[3:3] = '0'
        t[7:7] = '0'
        st.append(t)
    for i in range(k):
        for j in range(12):
            st[i][j] = int(st[i][j])
    return st


def list_to_string(list, k, n):
    st = ""
    for i in range(k):
        for j in range(n):
            st += str(list[i][j])
    return st


def str_to_list_12(string, k):
    st = []
    for i in range(k):
        t = list(string[i * 12: (i + 1) * 12])
        st.append(t)
    for i in range(k):
        for j in range(12):
            st[i][j] = int(st[i][j])
    return st


def encode(string):

    for i in range(8 - len(string) % 8):
        string += "0"

    k = int(len(string) / 8)
    st = str_to_list_8(string, k)

    for i in range(k):
        b = sp.array(st[i]).reshape(12, 1)
        c = sp.dot(tr_matrix, b) % 2
        st[i][0] = c[0][0]
        st[i][1] = c[1][0]
        st[i][3] = c[2][0]
        st[i][7] = c[3][0]

    st1 = list_to_string(st, k, 12)

    return st1


def decode(string):
    k = int(len(string) / 12)
    st = str_to_list_12(string, k)

    for i in range(k):
        b = sp.array(st[i]).reshape(12, 1)
        c = sp.dot(tr_matrix, b) % 2
        t = str(c[0][0]) + str(c[1][0]) + str(c[2][0]) + str(c[3][0])
        t = int(t, 2)
        if t > 0:
            st[i][t-1] = abs(st[i][t-1] - 1)

    st1 = list_to_string(st, k, 12)
    st2 = []
    for i in range(k):
        t = list(st1[i * 12: (i + 1) * 12])
        t[0:2] = []
        t[1:2] = []
        t[4:5] = []
        st2.append(t)
    st1 = ""
    for i in range(k):
        for j in range(8):
            st1 += str(st2[i][j])
    return st1



