import pygame

MOUSE_SENSE = 50

class Slider:
    def __init__(self, _screen, _x, _y, _w, _h): # add _min, _max
        self.surf = _screen
        self.x = _x
        self.y = _y
        self.w = _w
        self.h = _h

        self.pressed = False
        self.pressed_y = 0
        self.value = 1
        return

    def processEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.pressed:
            _pos = pygame.mouse.get_pos()
            _val = self.y + self.h - (self.h/10 + .8*self.value*self.h)

            if not((_pos[1]<=_val+3 and _pos[1]>=_val-3) and (_pos[0]<=self.x+3*self.w/4 and _pos[0]>=self.x+self.w/4)): return
            self.pressed_y = _pos[1]
            self.pressed = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.pressed = False
        if event.type == pygame.MOUSEMOTION and self.pressed:
            new_val = (self.pressed_y - pygame.mouse.get_pos()[1])/MOUSE_SENSE
            self.value = min(max(0,self.value+new_val),1)
            self.pressed_y = pygame.mouse.get_pos()[1]
        return

    def draw(self):
        _val = self.y + self.h - (self.h/10 + .8*self.value*self.h)
        pygame.draw.rect(self.surf, (50, 50, 50), [self.x, self.y, self.w, self.h])
        pygame.draw.aaline(self.surf, (0,0,0), [self.x+self.w/2, self.y+self.h/10], [self.x+self.w/2, self.y+9*self.h/10], True)
        pygame.draw.line(self.surf, (255,255,255), [self.x+self.w/4, _val], [self.x+3*self.w/4, _val], 3)
        return