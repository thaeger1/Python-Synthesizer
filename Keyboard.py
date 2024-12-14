import numpy as np
import pygame

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
