import pygame
import sounddevice as sd
import numpy as np
from math import pi

from Utilities import Oscillator, Keyboard

# CENT = 1.0005777895
start_idx = 0 # used in output buffer
input_buffer = 0
octave = 4

get_freq = lambda k : round(440* 2**((k-49)/12),3) # get frequency from key # (1-88)
get_key = lambda f : round(12 * np.log2(f/440) + 49) % 12 # get key from frequency

#####|#####|#####|#####
#####|#####|#####|#####

# pygame setup
pygame.init()
screen = pygame.display.set_mode((900, 600)) # w, h
pygame.display.set_caption("pysynth")
clock = pygame.time.Clock()
running = True

pygame.font.init()
screen_font = pygame.font.SysFont('ocraextended', 16) # font, font size

text_surface = screen_font.render('v0.03', False, (0, 0, 0)) # text, aa, rgb
octave_label = screen_font.render(f'octave: {str(octave)}', False, (0, 0, 0))

#####|#####|#####|#####
#####|#####|#####|#####

m_kb = Keyboard(screen)
m_osc = Oscillator(screen)

# triple osc
class X3OSC:
    def __init__(self):
        pass

# adsr env
class Envelope:
    def __init__(self, _x, _y, _w, _h):
        self.x = _x
        self.y = _y
        self.w = _w
        self.h = _h

        self.attack  = 0
        self.decay   = 0
        self.sustain = 1
        self.release = 0
        return

#####|#####|#####|#####
#####|#####|#####|#####

device = sd.default.device
samplerate = sd.query_devices(device, 'output')['default_samplerate']

def callback(outdata, frames, time, status):
    if not(m_osc.btn_act.pressed): outdata[:] = 0; return
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
            if (m_osc.waveform==1): outdata[:] += .2 * np.abs(2.*(t*m_freq-np.floor(t*m_freq+.5))) - .1 # TRI WAVE
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

    pygame.draw.rect(screen, (200,200,200), [0,0,900,40])
    screen.blit(text_surface, (10,10))
    screen.blit(octave_label, (800,10))

    pygame.display.flip()  # flip() the display to put your work on screen
    clock.tick(120)         # limits FPS to 60

pygame.quit()