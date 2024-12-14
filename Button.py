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
        if event.type == pygame.MOUSEBUTTONDOWN:
            _pos = pygame.mouse.get_pos()
            if ((_pos[1]-self.y)*(_pos[1]-self.y) + (_pos[0]-self.x)*(_pos[0]-self.x)) > 1.2*self.rad*self.rad: return
            self.pressed = False if self.pressed else True
        return

    def draw(self):
        pygame.draw.circle(self.surf, "slategrey", [self.x, self.y], self.rad)
        actCol = "green" if self.pressed else "red"
        pygame.draw.circle(self.surf, actCol, [self.x, self.y], self.rad-2)
        return