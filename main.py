import random
import pygame as py
import math
import numpy as np
import pygame_widgets
from boid import Boid
from pygame_widgets.slider import Slider

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

text_size: int = 10
text_offSet: int = 110
slider_sizeX: int = 80
slider_sizeY: int = 10
slider_offSetX: int = 100
slider_offSetY: int = 20
BLUE = (0, 0, 255)

screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

Allignment_weight_slider = Slider(screen,
                    SCREEN_WIDTH - slider_offSetX,
                    SCREEN_HEIGHT - slider_offSetY, slider_sizeX, slider_sizeY,
                    min=0.0, max=2, step=0.01, initial=0.0, handleColour=BLUE)

Cohesion_weight_slider = Slider(screen,
                    SCREEN_WIDTH - slider_offSetX,
                    SCREEN_HEIGHT - slider_offSetY - slider_offSetY, slider_sizeX, slider_sizeY,
                    min=0.0, max=2, step=0.01, initial=0.0, handleColour=BLUE)

Separation_weight_slider = Slider(screen,
                    SCREEN_WIDTH - slider_offSetX,
                    SCREEN_HEIGHT - slider_offSetY - 2 * slider_offSetY, slider_sizeX, slider_sizeY,
                    min=0.0, max=2, step=0.01, initial=0.0, handleColour=BLUE)

def main() -> None:
    py.init()
    py.display.set_caption("Boid Simulation")
    clock = py.time.Clock()
    font = py.font.Font(None, text_size * 2)

    BOIDS: list[Boid] = []

    def add_boid(x: float = None, y: float = None):
        if x is None: x = random.uniform(0, SCREEN_WIDTH)
        if y is None: y = random.uniform(0, SCREEN_HEIGHT)

        new_boid = Boid(x = x, y = y, size=10, color=(255, 0, 0))

        BOIDS.append(new_boid)

    for _ in range(40):
        add_boid()

    RUNNING: bool = True
    while RUNNING:
        events = py.event.get()
        for event in events:
            if event.type == py.QUIT:
                RUNNING = False

        screen.fill((0, 0, 0))
        delta_time = clock.get_time() / 1000.0

        # Render slider label and value
        Alignment_weight = Allignment_weight_slider.getValue()
        Cohesion_weight = Cohesion_weight_slider.getValue()
        Separation_weight = Separation_weight_slider.getValue()
        
        allignment_label_text = font.render(f"Allignment: {Alignment_weight:.1f}", True, (255, 255, 255))
        cohesion_label_text = font.render(f"Cohesion: {Cohesion_weight:.1f}", True, (255, 255, 255))
        separation_label_text = font.render(f"Separation: {Separation_weight:.1f}", True, (255, 255, 255))
        
        screen.blit(allignment_label_text, (SCREEN_WIDTH - slider_offSetX - text_offSet, SCREEN_HEIGHT - slider_offSetY))
        screen.blit(cohesion_label_text, (SCREEN_WIDTH - slider_offSetX - text_offSet, SCREEN_HEIGHT - slider_offSetY - slider_offSetY))
        screen.blit(separation_label_text, (SCREEN_WIDTH - slider_offSetX - text_offSet, SCREEN_HEIGHT - slider_offSetY - 2 * slider_offSetY))

        Allignment_weight_slider.draw()
        Cohesion_weight_slider.draw()
        Separation_weight_slider.draw()

        for boid in BOIDS:
            boid.set_weights(seperation=Separation_weight, cohesion=Cohesion_weight, alignment=Alignment_weight)
            boid.flock_boid(BOIDS)
            boid.update_boid(delta_time)
            boid.draw_boid(screen)

        pygame_widgets.update(events)
        py.display.update()
        clock.tick(60)

    py.quit()

if __name__ == '__main__':
    main()