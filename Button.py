import pygame

class Button:
    def __init__(self, _screen, _x, _y):
        self.surf = _screen
        self.x = _x
        self.y = _y
        self.rad = 4
        self.pressed = True
        return

    def processEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN: self.pressed = False if self.pressed else True
        return

    def draw(self):
        pygame.draw.circle(self.surf, "slategrey", [self.x, self.y], self.rad)
        actCol = "green" if self.pressed else "red"
        pygame.draw.circle(self.surf, actCol, [self.x, self.y], self.rad-2)
        return