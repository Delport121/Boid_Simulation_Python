import random
import pygame as py
import math
import numpy as np
from boid import Boid



def main() -> None:
    py.init()
    py.display.set_caption("Boid Simulation")
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = py.time.Clock() 

    BOIDS: list[Boid] = []

    def add_boid(x: float = None, y: float = None):
        if x is None: x = random.uniform(0, SCREEN_WIDTH)
        if y is None: y = random.uniform(0, SCREEN_HEIGHT)

        new_boid = Boid(x = x, y = y, size=10, color=(255, 0, 0))


        BOIDS.append(new_boid)

    for _ in range(30):
        add_boid()

    RUNNING: bool = True
    while RUNNING:
        for event in py.event.get():
            if event.type == py.QUIT:
                RUNNING = False

        screen.fill((0, 0, 0))
        delta_time = clock.get_time() / 1000.0


        for boid in BOIDS:
            boid.flock_boid(BOIDS)
            boid.update_boid(delta_time)
            boid.draw_boid(screen)

        py.display.update()
        clock.tick(60)

    py.quit()



if __name__ == '__main__':
    main()