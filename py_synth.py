import pygame
import sounddevice as sd
import numpy as np
from math import pi
# import matplotlib.pyplot as plt

MOUSE_SENSE = 50
# CENT = 1.0005777895

start_idx = 0 # used in output buffer
input_buffer = 0

white_keys = [0,2,4,5,7,9,11,12]
black_keys = [1,3,6,8,10]
octave = 4

get_freq = lambda k : round(440* 2**((k-49)/12),3) # get frequency from key # (1-88)
get_key = lambda f : round(12 * np.log2(f/440) + 49) % 12 # get key from frequency

#####|#####|#####|#####
#####|#####|#####|#####

# pygame setup
pygame.init()
screen = pygame.display.set_mode((900, 600)) # w, h
clock = pygame.time.Clock()
running = True

pygame.font.init()
screen_font = pygame.font.SysFont('ocraextended', 16) # font, font size
osc_font = pygame.font.SysFont('ocraextended', 12)

text_surface = screen_font.render('py_synth v0.02', False, (0, 0, 0)) # text, aa, rgb
octave_label = screen_font.render(f'octave: {str(octave)}', False, (0, 0, 0))
# octave_txt   = screen_font.render(str(octave), False, (0, 0, 0))

#####|#####|#####|#####
#####|#####|#####|#####

# keyboard ui const
class Keyboard:
    def __init__(self, _screen):
        self.synth_screen = _screen

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
        for i in white_keys:
            key_col = (255,0,0) if (self.keys[i] == 1) else self.key_dict[i][1]
            pygame.draw.rect(self.synth_screen, key_col, self.key_dict[i][0])
        for i in black_keys:
            key_col = (255,0,0) if (self.keys[i] == 1) else self.key_dict[i][1]
            pygame.draw.rect(self.synth_screen, key_col, self.key_dict[i][0])
        return

class Potentiometer:
    def __init__(self, _screen, _x, _y, _rad=16):
        self.screen = _screen

        self.xpos = _x
        self.ypos = _y
        self.rad = _rad
        self.theta = 0
        self.value = .5

        self.pressed = False
        self.pressed_y = 0
        return

    def processEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.pressed:
            _pos = pygame.mouse.get_pos()
            if ((_pos[1]-self.ypos)*(_pos[1]-self.ypos) + (_pos[0]-self.xpos)*(_pos[0]-self.xpos)) > self.rad*self.rad: return
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
        return

    def draw(self):
        pygame.draw.circle(self.screen, "slategrey", [self.xpos, self.ypos], self.rad)
        pygame.draw.aaline(self.screen, "white", [self.xpos, self.ypos], [self.xpos+.8*self.rad*np.sin(self.theta), self.ypos-.8*self.rad*np.cos(self.theta)], True)
        return

class Oscillator:
    def __init__(self, _screen):
        self.synth_screen = _screen
        self.waveform = 0 # 0 sin, 2 tri, 3 saw, 4 sqr

        self.fine_txt = osc_font.render('f:0', False, (0,0,0))
        self.coarse_txt = osc_font.render('c:0', False, (0,0,0))
        self.btn_left   = osc_font.render('<', True, (255,255,255))
        self.btn_right  = osc_font.render('>', True, (255,255,255))

        self.osc_x = 10
        self.osc_y = 200
        self.osc_width = 200
        self.osc_height = 100
        self.osc_bw = 4
        self.osc_color = 'honeydew3'

        self.amp = .2
        self.coarse = 0
        self.fine = 0

        self.wavefuncs = [
            lambda t : np.sin(2*pi*t),
            lambda t : 2*np.abs(t-np.floor(t+1/2)) - 1,
            lambda t : (t-np.floor(.5+t)),
            lambda t : np.copysign(np.ones(len(t)).reshape(-1,1),np.sin(2*pi*t))
        ]

        # UI
        self.coarse_pot = Potentiometer(_screen, self.osc_x+self.osc_width*3/5, self.osc_y+self.osc_height/2) # (-12,12) semitones
        self.fine_pot = Potentiometer(_screen, self.osc_x+self.osc_width*4/5, self.osc_y+self.osc_height/2, 12)   # (-100,100) cents
        return

    def processEvent(self, event):
        # check button events (mouse over and pressed)

        self.fine_pot.processEvent(event)
        self.coarse_pot.processEvent(event)

        self.coarse = round(24*(self.coarse_pot.value-.5))
        self.fine   = round(200*(self.fine_pot.value-.5))

        self.fine_txt   = osc_font.render(f'f:{self.fine}', False, (0,0,0))
        self.coarse_txt = osc_font.render(f'c:{self.coarse}', False, (0,0,0))
        return

    def drawWF(self, samples=32):
        pygame.draw.rect(screen, (0,0,0), [self.osc_x+self.osc_width/6 - 10, self.osc_y+self.osc_height/2 - 20, 70, 40])
        pygame.draw.line(screen, (255,255,255), [self.osc_x+self.osc_width/6, self.osc_y+self.osc_height/2], [self.osc_x+self.osc_width/6 + 50, self.osc_y+self.osc_height/2], 3)

        t = np.linspace(0,1,samples).reshape(-1,1)
        wave = np.copy(t)
        wave[:] = self.wavefuncs[self.waveform](t) # swap for waveform here
        m_graph = np.hstack((self.osc_x+self.osc_width/6+50*t,self.osc_y+self.osc_height/2+10*wave))
        pygame.draw.lines(screen, "red", False, m_graph, 3)
        return

    def drawOsc(self):
        pygame.draw.rect(self.synth_screen, (0, 0, 0), [self.osc_x, self.osc_y, self.osc_width, self.osc_height], self.osc_bw) # border
        pygame.draw.rect(self.synth_screen, self.osc_color, [self.osc_x+self.osc_bw, self.osc_y+self.osc_bw, self.osc_width-self.osc_bw*2, self.osc_height-self.osc_bw*2])

        self.fine_pot.draw()
        self.coarse_pot.draw()

        self.synth_screen.blit(self.coarse_txt, (self.osc_x+self.osc_width*3/5 - 12,self.osc_y+20))
        self.synth_screen.blit(self.fine_txt, (self.osc_x+self.osc_width*4/5 - 12,self.osc_y+22))

        pygame.draw.rect(self.synth_screen, (0,0,0), [self.osc_x+self.osc_width-24,self.osc_y+4,8,16])
        self.synth_screen.blit(self.btn_left,  (self.osc_x+self.osc_width-28,self.osc_y+4))
        self.synth_screen.blit(self.btn_right, (self.osc_x+self.osc_width-12,self.osc_y+4))

        self.drawWF()
        return

m_osc = Oscillator(screen)

# make keyboard, pass screen so keyboard can draw
m_kb = Keyboard(screen)

#####|#####|#####|#####
#####|#####|#####|#####

device = sd.default.device
samplerate = sd.query_devices(device, 'output')['default_samplerate']

def callback(outdata, frames, time, status):
    if (status): print(status)
    global start_idx
    idx = np.where(m_kb.keys==1)[0]
    outdata[:] = 0
    if (len(idx) != 0):
        for key in idx:
            m_freq = get_freq(12*octave+key+m_osc.coarse-8) # -8 to align with A4 tuning (key 49)
            m_freq *= 1 if (m_osc.fine==0) else 2**(m_osc.fine/1200) # or CENT**(m_osc.fine)

            t = (start_idx + np.arange(frames)) / samplerate
            t = t.reshape(-1, 1)

            if (m_osc.waveform==0): outdata[:] += .2 * np.sin(2*pi * m_freq * t) # SIN WAVE
            if (m_osc.waveform==1): outdata[:] += .2 * np.abs(t*m_freq-np.floor(t*m_freq+1/2)) - .1 # TRI WAVE
            if (m_osc.waveform==2): outdata[:] += .2 * (t*m_freq - np.floor(.5 + t*m_freq)) # SAW WAVE
            if (m_osc.waveform==3): outdata[:] += .2 * np.copysign(np.ones(len(outdata)).reshape(-1,1), np.sin(2*pi * m_freq * t)) # SQR WAVE

    start_idx += frames
    return

m_stream = sd.OutputStream(device=device, channels=1, callback=callback, samplerate=samplerate)
m_stream.start() # open stream w/callback

#####|#####|#####|#####
#####|#####|#####|#####

while running:
    for event in pygame.event.get():
        m_osc.processEvent(event)

        m_kb.clearKeys()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:     m_kb.keys[0]  = 1
        if keys[pygame.K_s]:     m_kb.keys[1]  = 1
        if keys[pygame.K_x]:     m_kb.keys[2]  = 1
        if keys[pygame.K_d]:     m_kb.keys[3]  = 1
        if keys[pygame.K_c]:     m_kb.keys[4]  = 1
        if keys[pygame.K_v]:     m_kb.keys[5]  = 1
        if keys[pygame.K_g]:     m_kb.keys[6]  = 1
        if keys[pygame.K_b]:     m_kb.keys[7]  = 1
        if keys[pygame.K_h]:     m_kb.keys[8]  = 1
        if keys[pygame.K_n]:     m_kb.keys[9]  = 1
        if keys[pygame.K_j]:     m_kb.keys[10] = 1
        if keys[pygame.K_m]:     m_kb.keys[11] = 1
        if keys[pygame.K_COMMA]: m_kb.keys[12] = 1

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHTBRACKET:
            octave = min(octave+1,7)
            octave_label = screen_font.render(f'octave: {str(octave)}', False, (0, 0, 0)) # text, aa, rgb
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFTBRACKET:
            octave = max(octave-1,1)
            octave_label = screen_font.render(f'octave: {str(octave)}', False, (0, 0, 0)) # text, aa, rgb

        if event.type == pygame.QUIT:
            running = False

    ### RENDER GAME HERE ###
    screen.fill("lightseagreen")
    
    m_kb.drawKeys()
    m_osc.drawOsc()

    screen.blit(text_surface, (10,10))
    screen.blit(octave_label, (800,10))

    pygame.display.flip()  # flip() the display to put your work on screen
    clock.tick(30)         # limits FPS to 60

pygame.quit()

# pygame colors list
# https://python-sounddevice.readthedocs.io/en/0.3.14/examples.html
# https://upload.wikimedia.org/wikipedia/commons/0/0c/Vector_Video_Standards8.svg

# from win32api import GetSystemMetrics
# # sceen resolution get (for later)
# screen_res = [GetSystemMetrics(0), GetSystemMetrics(1)]
# print(screen_res[0]/screen_res[1])