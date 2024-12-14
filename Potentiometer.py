# from py_synth import MOUSE_SENSE
import pygame
import numpy as np
from math import pi

MOUSE_SENSE = 50

class Potentiometer:
    def __init__(self, _screen, _x, _y, _rad):
        self.x = _x
        self.y = _y
        self.rad = _rad
        self.theta = 0
        self.value = .5

        # self.surf = pygame.Surface([int(self.rad*2), int(self.rad*2)], pygame.SRCALPHA)
        self.surf = _screen

        self.pressed = False
        self.pressed_y = 0
        return

    def processEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.pressed:
            _pos = pygame.mouse.get_pos()
            if ((_pos[1]-(self.y+self.rad))*(_pos[1]-(self.y+self.rad)) + (_pos[0]-(self.x+self.rad))*(_pos[0]-(self.x+self.rad))) > self.rad*self.rad: return
            self.pressed_y = _pos[1]
            self.pressed = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.pressed = False
        if event.type == pygame.MOUSEMOTION and self.pressed:
            new_val = (self.pressed_y - pygame.mouse.get_pos()[1])
            self.update(new_val)

    def update(self, _new_val):
        self.theta = min(max(-3*pi/4,self.theta + _new_val/MOUSE_SENSE), 3*pi/4)
        self.value = (2*self.theta)/(3*pi) + .5
        self.pressed_y = pygame.mouse.get_pos()[1]
        return

    def draw(self):
        pygame.draw.circle(self.surf, "slategrey", [self.x+self.rad, self.y+self.rad], self.rad)
        pygame.draw.aaline(self.surf, "white", [self.x+self.rad, self.y+self.rad], [self.x+self.rad+.8*self.rad*np.sin(self.theta), self.y+self.rad-.8*self.rad*np.cos(self.theta)], True)
        return
