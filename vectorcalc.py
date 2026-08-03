import numpy as np
from scipy.integrate import quad
import math
import pygame
import pygame.gfxdraw


def summation(points, speed, dt, xy, prevpoint):
    total = 0
    sdt = 0
    m = 1j if xy == 'y' else 1
    for i in range(len(points)):
        total += (points[i] - prevpoint) * m * math.e ** (2 * math.pi * 1j * -1 * speed * sdt) * dt
        sdt += dt
    return total


def get_coefficient(sumx, sumy):
    coord = sumx + sumy
    return (int(coord.real), int(coord.imag))


