import pygame
import sounddevice as sd
import numpy as np
# import matplotlib.pyplot as plt
# # from win32api import GetSystemMetrics

# sceen resolution get (for later)
# # screen_res = [GetSystemMetrics(0), GetSystemMetrics(1)]
# # print(screen_res[0]/screen_res[1])

octave = 4
start_idx = 0 # used in output buffer

#####|#####|#####|#####
#####|#####|#####|#####

# get frequency from key # (1-88)
def get_freq(n):
    return round(440 * 2**((n-49)/12),3)

# get key from frequency
def get_key(f):
    return round(12 * np.log2(f/440) + 49) % 12

#####|#####|#####|#####
#####|#####|#####|#####

# keyboard ui const
class Keyboard:

    def __init__(self):
        self.kb_width = 300
        self.kb_height = 100
        self.kb_buffer = 8
        self.kb_borderwidth = 4
        self.kb_keygap = 37 # (width - 2*borderwidth)/8
        
        self.keys = np.zeros(13)

    def clearKeys(self):
        self.keys = np.zeros(13)

# make keyboard
m_kb = Keyboard()

#####|#####|#####|#####
#####|#####|#####|#####

_device = sd.default.device
samplerate = sd.query_devices(_device, 'output')['default_samplerate']

# open stream w/callback
def callback(outdata, frames, time, status):
    if (status): print(status)
    global start_idx
    idx = np.where(m_kb.keys==1)[0]
    outdata[:] = 0

    if (len(idx) != 0):
        for key in idx:
            m_freq = get_freq(12*octave+key)
            t = (start_idx + np.arange(frames)) / samplerate
            t = t.reshape(-1, 1)
            outdata[:] += .2 * np.sin(2 * np.pi * m_freq * t)
    start_idx += frames

m_stream = sd.OutputStream(device=_device, channels=1, callback=callback, samplerate=samplerate)
m_stream.start()

#####|#####|#####|#####
#####|#####|#####|#####

# pygame setup
pygame.init()
screen = pygame.display.set_mode((900, 600))
clock = pygame.time.Clock()
running = True

pygame.font.init()
my_font = pygame.font.SysFont('ocraextended', 16)
text_surface = my_font.render('py_synth v0.0', False, (0, 0, 0)) # text, aa, rgb

key_pos = {
    0 : m_kb.kb_buffer+m_kb.kb_borderwidth,
    1 : m_kb.kb_buffer+m_kb.kb_borderwidth + m_kb.kb_keygap/2,
    2 : m_kb.kb_buffer+m_kb.kb_borderwidth + 1*m_kb.kb_keygap,
    3 : m_kb.kb_buffer+m_kb.kb_borderwidth + 1*m_kb.kb_keygap + m_kb.kb_keygap/2,
    4 : m_kb.kb_buffer+m_kb.kb_borderwidth + 2*m_kb.kb_keygap,
    5 : m_kb.kb_buffer+m_kb.kb_borderwidth + 3*m_kb.kb_keygap,
    6 : m_kb.kb_buffer+m_kb.kb_borderwidth + 3*m_kb.kb_keygap + m_kb.kb_keygap/2,
    7 : m_kb.kb_buffer+m_kb.kb_borderwidth + 4*m_kb.kb_keygap,
    8 : m_kb.kb_buffer+m_kb.kb_borderwidth + 4*m_kb.kb_keygap + m_kb.kb_keygap/2,
    9 : m_kb.kb_buffer+m_kb.kb_borderwidth + 5*m_kb.kb_keygap,
    10 : m_kb.kb_buffer+m_kb.kb_borderwidth + 5*m_kb.kb_keygap + m_kb.kb_keygap/2,
    11 : m_kb.kb_buffer+m_kb.kb_borderwidth + 6*m_kb.kb_keygap,
    12 : m_kb.kb_buffer+m_kb.kb_borderwidth + 7*m_kb.kb_keygap
}

while running:
    # poll for events
    for event in pygame.event.get():

        m_kb.clearKeys()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]: m_kb.keys[0] = 1
        if keys[pygame.K_s]: m_kb.keys[1] = 1
        if keys[pygame.K_x]: m_kb.keys[2] = 1
        if keys[pygame.K_d]: m_kb.keys[3] = 1
        if keys[pygame.K_c]: m_kb.keys[4] = 1
        if keys[pygame.K_v]: m_kb.keys[5] = 1
        if keys[pygame.K_g]: m_kb.keys[6] = 1
        if keys[pygame.K_b]: m_kb.keys[7] = 1
        if keys[pygame.K_h]: m_kb.keys[8] = 1
        if keys[pygame.K_n]: m_kb.keys[9] = 1
        if keys[pygame.K_j]: m_kb.keys[10] = 1
        if keys[pygame.K_m]: m_kb.keys[11] = 1
        if keys[pygame.K_COMMA]: m_kb.keys[12] = 1

        if event.type == pygame.QUIT:
            running = False

    screen.fill("lightseagreen")

    # RENDER YOUR GAME HERE

    # keyboard UI
    pygame.draw.rect(screen, (0, 0, 0), [m_kb.kb_buffer, 490, m_kb.kb_width, m_kb.kb_height]) #, kb_borderwidth)
    for i in range (8): # white keys
        pygame.draw.rect(screen, (255, 255, 255), [m_kb.kb_buffer+m_kb.kb_borderwidth + i*m_kb.kb_keygap, 494, 34, 92])
    for i in range (6): # black keys
        if i == 2: continue
        pygame.draw.rect(screen, (0, 0, 0), [m_kb.kb_buffer+m_kb.kb_borderwidth + i*m_kb.kb_keygap + m_kb.kb_keygap/2, 494, 30, 92*.6])

    active = np.where(m_kb.keys==1)[0]
    for key in active:
        if key in [1,3,6,8,10]:
            pygame.draw.rect(screen, (255, 0, 0), [key_pos[key], 494, 30, 92*.6])
        else:
            pygame.draw.rect(screen, (255, 0, 0), [key_pos[key], 494, 34, 92])

    screen.blit(text_surface, (0,0))

    pygame.display.flip()  # flip() the display to put your work on screen
    clock.tick(20)         # limits FPS to 60

pygame.quit()