import pygame
import numpy as np
from numpy import pi

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
            if ((_pos[1]-self.y)*(_pos[1]-self.y) + (_pos[0]-self.x)*(_pos[0]-self.x)) > self.rad*self.rad: return
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
        pygame.draw.circle(self.surf, "slategrey", [self.x, self.y], self.rad)
        pygame.draw.aaline(self.surf, "white", [self.x, self.y], [self.x+.8*self.rad*np.sin(self.theta), self.y-.8*self.rad*np.cos(self.theta)], True)
        return

class Oscillator:
    def __init__(self, _screen):
        self.osc_font = pygame.font.SysFont('ocraextended', 12)

        self.w = 200
        self.h = 100
        self.surf = _screen
        self.waveform = 0
        # 0 sin, 2 tri, 3 saw, 4 sqr

        self.fine_txt   = self.osc_font.render('f:0', False, (0,0,0))
        self.coarse_txt = self.osc_font.render('c:0', False, (0,0,0))
        self.btn_left   = self.osc_font.render('<', True, (255,255,255))
        self.btn_right  = self.osc_font.render('>', True, (255,255,255))

        self.x = 10
        self.y = 375

        self.osc_bw = 4
        self.osc_color = 'honeydew3'

        self.amp = .2
        self.coarse = 0
        self.fine = 0

        self.wavefuncs = [
            lambda t : np.sin(2*pi*t),
            lambda t : 2*np.abs(2*(t-np.floor(t+1/2))) - 1,
            lambda t : (t-np.floor(.5+t)),
            lambda t : np.copysign(np.ones(len(t)).reshape(-1,1),np.sin(2*pi*t))
        ]

        # UI
        self.btn_act = Button(_screen, self.x+12, self.y+12)
        self.coarse_pot = Potentiometer(_screen, self.x+self.w*3/5, self.y+self.h/2, 16)     # (-12,12) semitones
        self.fine_pot = Potentiometer(_screen, self.x+self.w*4/5, self.y+self.h/2, 12)   # (-100,100) cents
        self.btnLx = self.w-32
        self.btnRx = self.w-15
        self.btny  = 4
        self.btnw  = 15
        self.btnh  = 16
        return

    def processEvent(self, event):
        self.btn_act.processEvent(event)
        if not(self.btn_act.pressed): return
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if mouse[0] > self.x+self.btnLx and mouse[0] < self.x+self.btnLx+self.btnw and mouse[1] > self.y+self.btny and mouse[1] < self.y+self.btny+self.btnh:
                self.waveform = (self.waveform-1)%4
            if mouse[0] > self.x+self.btnRx and mouse[0] < self.x+self.btnRx+self.btnw and mouse[1] > self.y+self.btny and mouse[1] < self.y+self.btny+self.btnh:
                self.waveform = (self.waveform+1)%4

        self.fine_pot.processEvent(event)
        self.coarse_pot.processEvent(event)
        self.coarse = round(24*(self.coarse_pot.value-.5))
        self.fine   = round(200*(self.fine_pot.value-.5))
        self.coarse_txt = self.osc_font.render(f'c:{self.coarse}', False, (0,0,0))
        self.fine_txt   = self.osc_font.render(f'f:{self.fine}', False, (0,0,0))
        return

    def drawWF(self, samples=32):
        pygame.draw.rect(self.surf, (0,0,0), [self.x+self.w/6 - 10, self.y+self.h/2 - 20, 70, 40])
        pygame.draw.line(self.surf, (255,255,255), [self.x+self.w/6, self.y+self.h/2], [self.x+self.w/6 + 50, self.y+self.h/2], 3)

        t = np.linspace(0,1,samples).reshape(-1,1)
        wave = np.copy(t)
        wave[:] = self.wavefuncs[self.waveform](t) # swap for waveform here
        m_graph = np.hstack((self.x+self.w/6+50*t,self.y+self.h/2+10*wave))
        pygame.draw.lines(self.surf, "red", False, m_graph, 3)
        return

    def drawOsc(self):
        # frame and background
        pygame.draw.rect(self.surf, (0, 0, 0), [self.x, self.y, self.w, self.h], self.osc_bw) # border
        pygame.draw.rect(self.surf, self.osc_color, [self.x+self.osc_bw, self.y+self.osc_bw, self.w-self.osc_bw*2, self.h-self.osc_bw*2])
        # potentiometer and button draws
        self.btn_act.draw()
        self.fine_pot.draw()
        self.coarse_pot.draw()
        # potentiometer labels
        self.surf.blit(self.coarse_txt, (self.x+self.w*3/5 - 12,self.y+20))
        self.surf.blit(self.fine_txt, (self.x+self.w*4/5 - 12,self.y+22))
        # waveform selection buttons
        pygame.draw.rect(self.surf, (0,0,0), [self.x+self.btnLx,self.y+self.btny,self.btnw,self.btnh])
        pygame.draw.rect(self.surf, (0,0,0), [self.x+self.btnRx,self.y+self.btny,self.btnw,self.btnh])
        self.surf.blit(self.btn_left,  (self.x+self.w-28,self.y+4))
        self.surf.blit(self.btn_right, (self.x+self.w-12,self.y+4))

        self.drawWF()
        return

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

class Keyboard:
    def __init__(self, _screen):
        self.synth_screen = _screen

        self.white_keys = [0,2,4,5,7,9,11,12]
        self.black_keys = [1,3,6,8,10]

        self.kb_width       = 310
        self.kb_height      = 100
        self.kb_buffer      = 8
        self.kb_borderwidth = 4
        self.kb_keygap      = 38
        self.kb_ypos        = 490

        self.keys           = np.zeros(13)
        self.wkey_width     = 36
        self.bkey_width     = 30
        self.key_ypos       = self.kb_ypos + self.kb_borderwidth
        self.key_len        = 92
        self.bkey_len       = np.floor(self.key_len*.6)

        self.key_light = (255,255,255)
        self.key_dark  = (0,  0,  0  )
        self.key_dict = {
            0  : [[self.kb_buffer+self.kb_borderwidth                                                                            , self.key_ypos, self.wkey_width, self.key_len ], self.key_light],
            1  : [[self.kb_buffer+self.kb_borderwidth                    + self.kb_keygap/2 + (self.wkey_width-self.bkey_width)/2, self.key_ypos, self.bkey_width, self.bkey_len], self.key_dark ],
            2  : [[self.kb_buffer+self.kb_borderwidth + 1*self.kb_keygap                                                         , self.key_ypos, self.wkey_width, self.key_len ], self.key_light],
            3  : [[self.kb_buffer+self.kb_borderwidth + 1*self.kb_keygap + self.kb_keygap/2 + (self.wkey_width-self.bkey_width)/2, self.key_ypos, self.bkey_width, self.bkey_len], self.key_dark ],
            4  : [[self.kb_buffer+self.kb_borderwidth + 2*self.kb_keygap                                                         , self.key_ypos, self.wkey_width, self.key_len ], self.key_light],
            5  : [[self.kb_buffer+self.kb_borderwidth + 3*self.kb_keygap                                                         , self.key_ypos, self.wkey_width, self.key_len ], self.key_light],
            6  : [[self.kb_buffer+self.kb_borderwidth + 3*self.kb_keygap + self.kb_keygap/2 + (self.wkey_width-self.bkey_width)/2, self.key_ypos, self.bkey_width, self.bkey_len], self.key_dark ],
            7  : [[self.kb_buffer+self.kb_borderwidth + 4*self.kb_keygap                                                         , self.key_ypos, self.wkey_width, self.key_len ], self.key_light],
            8  : [[self.kb_buffer+self.kb_borderwidth + 4*self.kb_keygap + self.kb_keygap/2 + (self.wkey_width-self.bkey_width)/2, self.key_ypos, self.bkey_width, self.bkey_len], self.key_dark ],
            9  : [[self.kb_buffer+self.kb_borderwidth + 5*self.kb_keygap                                                         , self.key_ypos, self.wkey_width, self.key_len ], self.key_light],
            10 : [[self.kb_buffer+self.kb_borderwidth + 5*self.kb_keygap + self.kb_keygap/2 + (self.wkey_width-self.bkey_width)/2, self.key_ypos, self.bkey_width, self.bkey_len], self.key_dark ],
            11 : [[self.kb_buffer+self.kb_borderwidth + 6*self.kb_keygap                                                         , self.key_ypos, self.wkey_width, self.key_len ], self.key_light],
            12 : [[self.kb_buffer+self.kb_borderwidth + 7*self.kb_keygap                                                         , self.key_ypos, self.wkey_width, self.key_len ], self.key_light]
        }
        return

    def clearKeys(self):
        self.keys = np.zeros(13)
        return

    def drawKeys(self):
        pygame.draw.rect(self.synth_screen, (0, 0, 0), [self.kb_buffer, self.kb_ypos, self.kb_width, self.kb_height], self.kb_borderwidth) # border
        pygame.draw.rect(self.synth_screen, (50, 50, 50), [self.kb_buffer+self.kb_borderwidth, self.kb_ypos+self.kb_borderwidth, self.kb_width-2*self.kb_borderwidth, self.kb_height-2*self.kb_borderwidth]) # backboard
        for i in self.white_keys:
            key_col = (255,0,0) if (self.keys[i] == 1) else self.key_dict[i][1]
            pygame.draw.rect(self.synth_screen, key_col, self.key_dict[i][0])
        for i in self.black_keys:
            key_col = (255,0,0) if (self.keys[i] == 1) else self.key_dict[i][1]
            pygame.draw.rect(self.synth_screen, key_col, self.key_dict[i][0])
        return

class X3OSC:
    def __init__(self):
        pass

class Envelop:
    def __init__(self):
        pass

class LFO:
    def __init__(self):
        pass