import math
import pygame as py
import numpy as np
import random

MAX_SPEED = 20.0
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RANDOM_ANGLE_CHANGE_RANGE = 0#math.pi / 8

class Boid:
    def __init__(self, x, y, size, color) -> None:
        self.size = size
        self.color = color

        self.position = np.array([x,y]) + np.array([0.001,0.001])
        self.velocity = np.array([random.uniform(-MAX_SPEED, MAX_SPEED),
                                   random.uniform(-MAX_SPEED,MAX_SPEED)])
        self.acceleration = np.array([random.uniform(-MAX_SPEED,MAX_SPEED),
                                      random.uniform(-MAX_SPEED,MAX_SPEED)])
        
        self.separation = False
        self.cohesion = False
        self.alignment = False

    def draw_boid(self, screen) -> None:
        angle = math.atan2(self.velocity[1], self.velocity[0])
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

    def update_boid(self, delta_time: float) -> None:
        pass

    def align_boid(self, boids: list['Boid']) -> None:
        perception_radius = 50
        steering_force = np.array([0.0, 0.0])
        total = 0
        
        for boid in boids:
            distance = np.linalg.norm(self.position - boid.position)
            if boid != self and distance < perception_radius:
                steering_force += boid.velocity
                total += 1
                
        if total > 0:
            steering_force /= total
            steering_force = (steering_force / np.linalg.norm(steering_force)) * MAX_SPEED
            steering_force -= self.velocity

        return steering_force
        

    def move_boid(self, delta_time: float = 1) -> None:
        # Change velocity direction
        angle_range = RANDOM_ANGLE_CHANGE_RANGE
        angle_change = random.uniform(-angle_range, angle_range)

        # Rotate velocity vector
        self.velocity = np.array([
            self.velocity[0] * math.cos(angle_change) - self.velocity[1] * math.sin(angle_change),
            self.velocity[0] * math.sin(angle_change) + self.velocity[1] * math.cos(angle_change)
        ])

        # Update position
        self.position += self.velocity * delta_time

        # Keep within bounds
        self.keep_within_bounds(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    def keep_within_bounds(self, width: int, height: int) -> None:
        if self.position[0] < 0:
            self.position[0] = width
        elif self.position[0] > width:
            self.position[0] = 0

        if self.position[1] < 0:
            self.position[1] = height
        elif self.position[1] > height:
            self.position[1] = 0



