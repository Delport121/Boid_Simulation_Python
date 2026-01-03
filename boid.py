import math
import pygame as py
import numpy as np
import random

MAX_SPEED = 80.0
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RANDOM_ANGLE_CHANGE_RANGE = math.pi / 16

class Boid:
    def __init__(self, x, y, size, color: tuple = (255, 0, 0)) -> None:
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

        self.seperation_weight = 1.0
        self.cohesion_weight = 1.0
        self.alignment_weight = 1.0

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

    def align_boid(self, boids: list['Boid']) -> None:
        perception_radius = 50
        desired_velocity = np.array([0.0, 0.0])
        steering_force = np.array([0.0, 0.0])
        total = 0
        
        for boid in boids:
            distance = np.linalg.norm(self.position - boid.position)
            if boid != self and distance < perception_radius:
                desired_velocity += boid.velocity
                total += 1

        if total > 0:
            desired_velocity /= total
            desired_velocity = (desired_velocity / np.linalg.norm(desired_velocity)) * MAX_SPEED # Scale to max speed
            steering_force = desired_velocity - self.velocity
            steering_force = steering_force / np.linalg.norm(steering_force) * MAX_SPEED

        return steering_force
    
    def cohere_boid(self, boids: list['Boid']) -> None:
        perception_radius = 50
        center_of_mass = np.array([0.0, 0.0])
        steering_force = np.array([0.0, 0.0])
        total = 0

        for boid in boids:
            distance = np.linalg.norm(self.position - boid.position)
            if boid != self and distance < perception_radius:
                center_of_mass += boid.position
                total += 1

        if total > 0:
            center_of_mass /= total
            vector_to_center = center_of_mass - self.position
            vector_to_center_norm = (vector_to_center / np.linalg.norm(vector_to_center)) * MAX_SPEED
            steering_force = vector_to_center_norm - self.velocity
            steering_force = steering_force / np.linalg.norm(steering_force) * MAX_SPEED

        return steering_force
    
    def separate_boid(self, boids: list['Boid']) -> None:
        perception_radius = 50
        combined_vector = np.array([0.0, 0.0])
        steering_force = np.array([0.0, 0.0])
        total = 0

        for boid in boids:
            distance = np.linalg.norm(self.position - boid.position)
            if boid != self and distance < perception_radius:
                vector_to_self = self.position - boid.position
                vector_to_self_proportional = vector_to_self / distance**2 # Closer boids contribute more
                combined_vector += vector_to_self_proportional
                total += 1

        if total > 0:
            combined_vector /= total
            steering_force = combined_vector / np.linalg.norm(combined_vector) * MAX_SPEED

        return steering_force

    def flock_boid(self, boids: list['Boid']) -> None:
        self.acceleration = np.array([0.0, 0.0])

        allignment_force = self.align_boid(boids)
        cohesion_force = self.cohere_boid(boids)
        separation_force = self.separate_boid(boids)

        self.acceleration += allignment_force * self.alignment_weight
        self.acceleration += cohesion_force * self.cohesion_weight
        self.acceleration += separation_force * self.seperation_weight

    def update_boid(self, delta_time: float = 1) -> None:
        # # Change velocity direction
        # angle_range = RANDOM_ANGLE_CHANGE_RANGE
        # angle_change = random.uniform(-angle_range, angle_range)

        # # Rotate velocity vector
        # self.velocity = np.array([
        #     self.velocity[0] * math.cos(angle_change) - self.velocity[1] * math.sin(angle_change),
        #     self.velocity[0] * math.sin(angle_change) + self.velocity[1] * math.cos(angle_change)
        # ])

        # TODO: Limit velocity to MAX_SPEED

        # Update boid
        self.velocity += self.acceleration * delta_time
        self.position += self.velocity * delta_time
        
        # Keep within bounds
        self.update_colour()
        self.keep_within_bounds(SCREEN_WIDTH, SCREEN_HEIGHT)

    def set_weights(self, seperation: float, cohesion: float, alignment: float) -> None:
        self.seperation_weight = seperation
        self.cohesion_weight = cohesion
        self.alignment_weight = alignment

    def update_colour(self) -> None:
        speed = np.linalg.norm(self.velocity)
        hue = speed / MAX_SPEED  # Normalize speed to [0, 1] for hue

        # Clamp hue to blue range
        H_MIN = 120 / 360
        H_MAX = 240 / 360
        h = max(H_MIN, min(H_MAX, hue))

        color = hsv_a_rgb(h, 1.0, 1.0)

        self.color = tuple(int(c * 255) for c in color)

    def keep_within_bounds(self, width: int, height: int) -> None:
        if self.position[0] < 0:
            self.position[0] = width
        elif self.position[0] > width:
            self.position[0] = 0

        if self.position[1] < 0:
            self.position[1] = height
        elif self.position[1] > height:
            self.position[1] = 0

def hsv_a_rgb(h, s, v) -> tuple:
    """
    :param h: Hue
    :param s: Saturation
    :param v: Value
    :return: (R,G,B)
    """
    i = int(h * 6)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    i = i % 6
    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q


