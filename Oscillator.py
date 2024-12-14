from math import pi
import numpy as np
import pygame
from Potentiometer import Potentiometer
from Button import Button

class Oscillator:
    def __init__(self, _screen):
        self.osc_font = pygame.font.SysFont('ocraextended', 12)

        self.osc_width = 200
        self.osc_height = 100
        self.surf = _screen
        self.waveform = 0 # 0 sin, 2 tri, 3 saw, 4 sqr

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
        self.coarse_pot = Potentiometer(_screen, self.x+self.osc_width*3/5, self.y+self.osc_height/2, 16)     # (-12,12) semitones
        self.fine_pot = Potentiometer(_screen, self.x+self.osc_width*4/5, self.y+self.osc_height/2, 12)   # (-100,100) cents
        self.btnLx = self.osc_width-32
        self.btnRx = self.osc_width-15
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

        # check button events (mouse over and pressed)
        self.fine_pot.processEvent(event)
        self.coarse_pot.processEvent(event)

        self.coarse = round(24*(self.coarse_pot.value-.5))
        self.fine   = round(200*(self.fine_pot.value-.5))

        self.coarse_txt = self.osc_font.render(f'c:{self.coarse}', False, (0,0,0))
        self.fine_txt   = self.osc_font.render(f'f:{self.fine}', False, (0,0,0))
        return

    def drawWF(self, samples=32):
        pygame.draw.rect(self.surf, (0,0,0), [self.x+self.osc_width/6 - 10, self.y+self.osc_height/2 - 20, 70, 40])
        pygame.draw.line(self.surf, (255,255,255), [self.x+self.osc_width/6, self.y+self.osc_height/2], [self.x+self.osc_width/6 + 50, self.y+self.osc_height/2], 3)

        t = np.linspace(0,1,samples).reshape(-1,1)
        wave = np.copy(t)
        wave[:] = self.wavefuncs[self.waveform](t) # swap for waveform here
        m_graph = np.hstack((self.x+self.osc_width/6+50*t,self.y+self.osc_height/2+10*wave))
        pygame.draw.lines(self.surf, "red", False, m_graph, 3)
        return

    def drawOsc(self):

        pygame.draw.rect(self.surf, (0, 0, 0), [self.x, self.y, self.osc_width, self.osc_height], self.osc_bw) # border
        pygame.draw.rect(self.surf, self.osc_color, [self.x+self.osc_bw, self.y+self.osc_bw, self.osc_width-self.osc_bw*2, self.osc_height-self.osc_bw*2])

        self.btn_act.draw()
        self.fine_pot.draw()
        self.coarse_pot.draw()

        self.surf.blit(self.coarse_txt, (self.x+self.osc_width*3/5 - 12,self.y+20))
        self.surf.blit(self.fine_txt, (self.x+self.osc_width*4/5 - 12,self.y+22))

        pygame.draw.rect(self.surf, (0,0,0), [self.x+self.btnLx,self.y+self.btny,self.btnw,self.btnh])
        pygame.draw.rect(self.surf, (0,0,0), [self.x+self.btnRx,self.y+self.btny,self.btnw,self.btnh])
        self.surf.blit(self.btn_left,  (self.x+self.osc_width-28,self.y+4))
        self.surf.blit(self.btn_right, (self.x+self.osc_width-12,self.y+4))

        self.drawWF()
        return