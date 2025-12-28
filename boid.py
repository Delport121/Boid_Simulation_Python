import math
import pygame as py
import numpy as np
import random

MAX_SPEED = 2.0

class Boid:
    def __init__(self, x, y, size, color) -> None:
        self.size = size
        self.color = color

        self.position = np.array([x,y]) + np.array([0.001,0.001])
        self.direction = np.array([random.uniform(-MAX_SPEED, MAX_SPEED),
                                   random.uniform(-MAX_SPEED,MAX_SPEED)])
        self.acceleration = np.array([random.uniform(-MAX_SPEED,MAX_SPEED),
                                      random.uniform(-MAX_SPEED,MAX_SPEED)])

    def draw(self, screen) -> None:
        angle = math.atan2(self.direction[1], self.direction[0])
        points = [
            # Upper dot
            (float(self.position[0] + self.size * math.cos(angle)),
             float(self.position[1] + self.size * math.sin(angle))),
            # Left lower dot
            (float(self.position[0] + self.size * math.cos(angle + 2.5 * math.pi / 3)),
             float(self.position[1] + self.size * math.sin(angle + 2.5 * math.pi / 3))),
            # mid point
            (float(self.position[0]), float(self.position[1])),
            # Right lower dot
            (float(self.position[0] + self.size * math.cos(angle - 2.5 * math.pi / 3)),
             float(self.position[1] + self.size * math.sin(angle - 2.5 * math.pi / 3)))
        ]

        py.draw.polygon(screen, self.color, points)