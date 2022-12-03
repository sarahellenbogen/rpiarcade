
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
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=100) 


pygame.init()
pygame.mouse.set_visible(False)
size = 240,320
black = 0, 0, 0
gray = 100, 100, 100
white = 255, 255, 255
red = 255, 0, 0
screen = pygame.display.set_mode(size)
my_font = pygame.font.Font(None, 40)
message_font = pygame.font.Font(None, 30)

# Read for reference: https://pygame-zero.readthedocs.io/en/stable/ptext.html
# create buttons
my_buttons = {  'A':( 50,  220 ),   'B':( 50, 300 ),
                '1':( 120,  220 ),   '2':( 120, 300 ),
              'CLR':( 190,  220 ), 'SEL':( 190, 300 )}
rects = []
surface = []
for my_text, text_pos in my_buttons.items():
    text_surface = my_font.render(my_text, False, black)
    rect = text_surface.get_rect(center=text_pos)
    # rect.inflate(100,100)
    screen.blit(text_surface, rect)
    surface.append(text_surface)
    rects.append(rect)

# keeps track of messages
state = 0
code = ["_", "_"]
i=0
tickets = 0
message = "Scan card or pick item"
ticketStr = "No card scanned"
popUp = " "
canSelect = 1
clock = pygame.time.Clock()
end_time = time.time() + 120
while (time.time() < end_time):

    screen.fill(white)               # Erase the Work space
    for i in range(len(rects)):
        screen.blit(surface[i], rects[i])
    # Create textpad msg
    num_surface = my_font.render(('sel: ' + code[0] + ' ' + code[1]), True, black)
    num_rect = num_surface.get_rect(center=(60, 180))
    screen.blit(num_surface, num_rect)

    num_surface = message_font.render((ticketStr), True, black)
    num_rect = num_surface.get_rect(center=(120, 40))
    screen.blit(num_surface, num_rect)

    num_surface = message_font.render((message), True, black)
    num_rect = num_surface.get_rect(center=(120, 100))
    screen.blit(num_surface, num_rect)

    num_surface = my_font.render((popUp), True, red)
    num_rect = num_surface.get_rect(center=(120, 150))
    screen.blit(num_surface, num_rect)

    if state == 0:
        message = "Scan card or pick item"
        ticketStr = "No card scanned"
        popUp = " "
        canSelect = 1
        #RFID read here if read tickets == read

    elif state == 1:
        popUp = " "


    elif state == 2:
        popUp = "SCAN CARD"
        canSelect = 0
        if (time.time() >= state2start + 5):
            state = 0 

    elif state == 3:
        popUp = " "
        canSelect = 0

    elif state == 4:
        popUp = "VENDING"
        canSelect = 0

    if canSelect == 1:

        for event in pygame.event.get():
            if(event.type is MOUSEBUTTONUP):
                x,y = pygame.mouse.get_pos()
                pos = pygame.mouse.get_pos()
                print(pos)

                if x >= 175 and x <= 205 and y >= 80 and y <= 115:
                    print("A")
                    print(code[0] + code[1])
                    if (code[0] == "_") :
                        code[0] = "A"
                    elif (code[1] == "_") :
                        code[1] = "A"

                elif x >= 175 and x <= 205 and y >= 0 and y <= 30:
                    print("B")
                    print(code[0] + code[1])
                    if (code[0] == "_") :
                        code[0] = 'B'
                    elif (code[1] == "_") :
                        code[1] = 'B'

                elif x >= 105 and x <= 135 and y >= 80 and y <= 115:
                    print("1")
                    print(code[0] + code[1])
                    if (code[0] == "_") :
                        code[0] = "1"
                    elif (code[1] == "_") :
                        code[1] = "1"

                elif x >= 105 and x <= 135 and y >= 0 and y <= 30:
                    print("2")
                    print(code[0] + code[1])
                    if (code[0] == "_") :
                        code[0] = "2"
                    elif (code[1] == "_") :
                        code[1] = "2"

                elif x >= 10 and x <= 75 and y >= 80 and y <= 115:
                    code = ["_", "_"]
                    print("CLR")

                elif x >= 10 and x <= 75 and y >= 0 and y <= 30:
                    if code[0] == "A":
                        if code[1] == "1":
                            message = "This prize is 10 tickets"
                            state = 2
                        if code[1] == "2":
                            message = "This prize is 10 tickets"
                            state = 2

                    if code[0] == "B":
                        if code[1] == "1":
                            message = "This prize is 10 tickets"
                            state = 2
                        if code[1] == "2":
                            message = "This prize is 10 tickets"
                            state == 2

                    if state != 2:
                        state = 0
                    else:
                        state2start = time.time()

                    code = ["_", "_"]
                    print("SEL")
    
    # Render
    screen.blit(pygame.transform.rotate(screen, 180), (0, 0))
    clock.tick(30)
    pygame.display.flip()

# Close program
print("time out")
GPIO.cleanup() 
sys.exit()
