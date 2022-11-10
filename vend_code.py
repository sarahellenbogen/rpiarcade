import pygame     # Import pygame graphics library
from pygame.locals import *
import RPi.GPIO as GPIO
import time
import sys
import os
import sys
# import csv
import math

# motor pins
DIRA1 = 19
DIRA2 = 13
DIRB1 = 21
DIRB2 = 20

# GPIO.setmode(GPIO.BCM)

# Setup motor pins
# GPIO.setup(DIRA1, GPIO.OUT) # DIRA1
# GPIO.setup(DIRA2, GPIO.OUT) # DIRA2
# GPIO.setup(DIRB1, GPIO.OUT) # DIRB1
# GPIO.setup(DIRB2, GPIO.OUT) # DIRB2

def A_stop():   # A stop
    GPIO.output(DIRA1, GPIO.LOW)
    GPIO.output(DIRA2, GPIO.LOW)
def B_stop():   # A stop
    GPIO.output(DIRA1, GPIO.LOW)
    GPIO.output(DIRB2, GPIO.LOW)
def A1(pwr):   # A forward
    GPIO.output(DIRA1, GPIO.LOW)
    GPIO.output(DIRA2, GPIO.HIGH)
def B1(pwr):   # B forward
    GPIO.output(DIRB1, GPIO.LOW)
    GPIO.output(DIRB2, GPIO.HIGH)
def A2(pwr):   # A back
    GPIO.output(DIRA1, GPIO.HIGH)
    GPIO.output(DIRA2, GPIO.LOW)
def B2(pwr):   # B back
    GPIO.output(DIRB2, GPIO.HIGH)
    GPIO.output(DIRB2, GPIO.LOW)

os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT 
os.putenv('SDL_FBDEV', '/dev/fb1') #
os.putenv('SDL_MOUSEDRV', 'TSLIB') # Track mouse clicks on piTFT 
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

# TFT buttons
def GPIO17_callback(channel):
    GPIO.cleanup()
    sys.exit()
# GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)
# GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=100) 


pygame.init()
pygame.mouse.set_visible(False)
size = 320, 240
black = 0, 0, 0
white = 255, 255, 255
screen = pygame.display.set_mode(size)
my_font = pygame.font.Font(None, 25)

# Read for reference: https://pygame-zero.readthedocs.io/en/stable/ptext.html
# create buttons
my_buttons = {  'A':(30,  60),   'B':(30,  90),   'C':(30, 120),
                '1':(60,  60),   '2':(60,  90),   '3':(60, 120),
              'CLR':(90,  60), 'SEL':(90,  90),'QUIT':(90, 120)}
rects = []
surface = []
for my_text, text_pos in my_buttons.items():
    text_surface = my_font.render(my_text, True, black)
    rect = text_surface.get_rect(center=text_pos)
    # rect.inflate(100,100)
    screen.blit(text_surface, rect)
    surface.append(text_surface)
    rects.append(rect)

# keeps track of messages
state = 0
code = ["_", "_"]

clock = pygame.time.Clock()
end_time = time.time() + 30
while (time.time() < end_time):
    screen.fill(white)               # Erase the Work space
    for i in range(len(rects)):
        screen.blit(surface[i], rects[i])
    # screen.draw.text("test", (100, 100), color="black", background="gray")
    # Create textpad msg
    num_surface = my_font.render(('sel: ' + code[0] + ' ' + code[1]), True, black)
    num_rect = num_surface.get_rect(center=(60, 30))
    screen.blit(num_surface, num_rect)

    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            if   rects[0].collidepoint(pos):
                print("A")
                print(code[0] + code[1])
                if (code[0] == "_") :
                    code[0] = 'A'
                elif (code[1] == "_") :
                    code[1] = 'A'

            elif rects[1].collidepoint(pos):
                print("B")
                print(code[0] + code[1])
                if (code[0] == "_") :
                    code[0] = 'B'
                elif (code[1] == "_") :
                    code[1] = 'B'

            elif rects[2].collidepoint(pos):
                print("C")
                print(code[0] + code[1])
                if (code[0] == "_") :
                    code[0] = 'C'
                elif (code[1] == "_") :
                    code[1] = 'C'

            elif rects[3].collidepoint(pos):
                print("1")
                print(code[0] + code[1])
                if (code[0] == "_") :
                    code[0] = '1'
                elif (code[1] == "_") :
                    code[1] = '1'

            elif rects[4].collidepoint(pos):
                print("2")
                print(code[0] + code[1])
                if (code[0] == "_") :
                    code[0] = '2'
                elif (code[1] == "_") :
                    code[1] = '2'

            elif rects[5].collidepoint(pos):
                print("3")
                print(code[0] + code[1])
                if (code[0] == "_") :
                    code[0] = '3'
                elif (code[1] == "_") :
                    code[1] = '3'

            elif rects[6].collidepoint(pos):
                code = '__'
                print("CLR")
            elif rects[7].collidepoint(pos):
                code = '__'
                print("SEL")
            elif rects[8].collidepoint(pos):
                print("QUIT")
                GPIO.cleanup()
                sys.exit()
    
    # Render
    clock.tick(30)
    pygame.display.flip()

# Close program
GPIO.cleanup() 
sys.exit()
