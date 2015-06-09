from numpy import correlate, average, diff
from scipy.signal import argrelmax


def find(x):
    m = argrelmax(correlate(x, x, 'same'))
    return average(diff(m))