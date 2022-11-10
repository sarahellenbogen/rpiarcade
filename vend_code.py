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

GPIO.setmode(GPIO.BCM)

# Setup motor pins
GPIO.setup(DIRA1, GPIO.OUT) # DIRA1
GPIO.setup(DIRA2, GPIO.OUT) # DIRA2
GPIO.setup(DIRB1, GPIO.OUT) # DIRB1
GPIO.setup(DIRB2, GPIO.OUT) # DIRB2

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
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=100) 


pygame.init()
pygame.mouse.set_visible(False)
size = 320, 240
black = 0, 0, 0
white = 255, 255, 255
screen = pygame.display.set_mode(size)
my_font = pygame.font.Font(None, 25)

# Read for reference: https://pygame-zero.readthedocs.io/en/stable/ptext.html
# create buttons
my_buttons = {  'A':(30,  60),   'B':(60,  60),   'C':(90,  60),
                '1':(30,  90),   '2':(60,  90),   '3':(90,  90),
              'CLR':(30, 120), 'SEL':(60, 120),'QUIT':(90, 120)}
rects = []
surface = []
for my_text, text_pos in my_buttons.items():
    text_surface = my_font.render(my_text, True, black)
    rect = text_surface.get_rect(center=text_pos)
    rect.inflate(100,100)
    screen.blit(text_surface, rect)
    surface.append(text_surface)
    rects.append(rect)

# keeps track of messages
state = 0
letter = '_'
number = '_'

clock = pygame.time.Clock()
end_time = time.time() + 30
while (time.time() < end_time):
    screen.fill(white)               # Erase the Work space
    for i in range(len(rects)):
        screen.blit(surface[i], rects[i])
    # screen.draw.text("test", (100, 100), color="black", background="gray")
    # Create textpad msg
    num_surface = my_font.render(('sel: ' + letter + ' ' + number), True, black)
    num_rect = num_surface.get_rect(center=(60, 30))
    screen.blit(num_surface, num_rect)

    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            if   rects[0].collidepoint(pos):
                letter = 'A'
                print("A")
            elif rects[1].collidepoint(pos):
                letter = 'B'
                print("B")
            elif rects[2].collidepoint(pos):
                letter = 'C'
                print("C")
            elif rects[3].collidepoint(pos):
                number = '1'
                print("1")
            elif rects[4].collidepoint(pos):
                number = '2'
                print("2")
            elif rects[5].collidepoint(pos):
                number = '3'
                print("3")
            elif rects[6].collidepoint(pos):
                number = '_'
                letter = '_'
                print("CLR")
            elif rects[7].collidepoint(pos):
                number = '_'
                letter = '_'
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
