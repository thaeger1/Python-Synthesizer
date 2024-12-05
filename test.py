import pygame
import numpy as np
from math import pi

# Initialize pygame
pygame.init()

# Set the height and width of the screen
size = [400, 300]
screen = pygame.display.set_mode(size)

MOUSE_SENSE = 30

pygame.display.set_caption("Example code for the draw module")

class Potentiometer:
    def __init__(self, _screen):
        self.screen = _screen

        self.xpos = 64
        self.ypos = 124
        self.rad = 16
        self.theta = 0
        self.value = .5

        self.pressed = False
        self.pressed_y = 0
        return

    def processEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.pressed_y = pygame.mouse.get_pos()[1]
            self.pressed = True
            pass
        if event.type == pygame.MOUSEBUTTONUP:
            self.pressed = False
            pass
        if event.type == pygame.MOUSEMOTION and self.pressed:
            new_val = (self.pressed_y - pygame.mouse.get_pos()[1])
            self.update(new_val)
            pass

    def update(self, _new_val):
        self.theta = min(max(-3*pi/4,self.theta + _new_val/MOUSE_SENSE), 3*pi/4)
        self.value = (2*self.theta)/(3*pi) + .5
        return

    def draw(self):
        pygame.draw.circle(self.screen, "slategrey", [self.xpos, self.ypos], self.rad)
        pygame.draw.aaline(self.screen, "white", [self.xpos, self.ypos], [self.xpos + self.rad*np.sin(self.theta), self.ypos - self.rad*np.cos(self.theta)], True)
        return

pot = Potentiometer(screen)

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

while not done:
    clock.tick(60)

    for event in pygame.event.get():  # User did something
        pot.processEvent(event)
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    # Clear the screen and set the screen background
    screen.fill("white")
    pot.draw()
    pygame.display.flip()

# Be IDLE friendly
pygame.quit()