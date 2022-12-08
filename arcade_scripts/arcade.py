# reaction_game_v2_hack.py

import subprocess
import shlex
from time import sleep
import io

# rfid libs
import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_B
from adafruit_pn532.spi import PN532_SPI

# SPI connection:
spi = busio.SPI(board.SCK_1, MOSI = board.MOSI_1, MISO =  board.MISO_1)
cs_pin = DigitalInOut(board.D16)
pn532 = PN532_SPI(spi, cs_pin, debug=False)
# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

NOTHING = 0
PACMAN = 1
SPACE = 2
GALA = 3

def display(char):
    global process
    buffer = process.stdout.read1(char).decode("utf-8")
    # print(buffer, end="", flush=True)
    return buffer

def search_for_output(string):
    global process
    buffer = ""
    while not (string in buffer):
        buffer = buffer + display(1)
    display(-1)

def runraw(command, resp):
    global process
    process.stdin.write(bytes(command + "\n", 'utf-8'))
    # print(command)
    process.stdin.flush()
    sleep(.16)
    string = display(-1)
    if resp:
        return string.split('\n')[0]

def run(command, resp):
    if resp:
        return int(runraw(command, resp))
    else:
        runraw(command, resp)
        

def death():
    global game
    
    run("emu.pause()", False)
    
    score = 0

    if game == PACMAN:
        temp = run("print(mem:read_u8(0xee83))", True)
        score *= 100
        score += (temp >> 4) * 10
        score += temp & 0xF
        temp = run("print(mem:read_u8(0xee82))", True)
        score *= 100
        score += (temp >> 4) * 10
        score += temp & 0xF
        sleep(0.16)
        score *= 100
        temp = run("print(mem:read_u8(0xee81))", True)
        score += (temp >> 4) * 10
        score += temp & 0xF
        sleep(0.16)
        score *= 100
        temp = run("print(mem:read_u8(0xee80))", True)
        score += (temp >> 4) * 10
        score += temp & 0xF

        score /= 10
        score = int(score)

    if game == SPACE:
        temp = run("print(mem:read_u8(0x20f8))", True)
        score *= 100
        score += (temp >> 4) * 10
        score += temp & 0xF
        sleep(0.16)
        score *= 100
        temp = run("print(mem:read_u8(0x20f7))", True)
        score += (temp >> 4) * 10
        score += temp & 0xF
        sleep(0.16)
        score *= 100
        temp = run("print(mem:read_u8(0x20f6))", True)
        score += (temp >> 4) * 10
        score += temp & 0xF

    if game == GALA:
        score *= 10
        temp = run("print(mem:read_u8(0x83FF))", True)
        if temp != 36:
            score += temp
        sleep(0.16)
        
        score *= 10
        temp = run("print(mem:read_u8(0x83FE))", True)
        if temp != 36:
            score += temp
        sleep(0.16)

        score *= 10
        temp = run("print(mem:read_u8(0x83FD))", True)
        if temp != 36:
            score += temp
        sleep(0.16)

        score *= 10
        temp = run("print(mem:read_u8(0x83FC))", True)
        if temp != 36:
            score += temp
        sleep(0.16)

        score *= 10
        temp = run("print(mem:read_u8(0x83FB))", True)
        if temp != 36:
            score += temp
        sleep(0.16)

        score *= 10
        temp = run("print(mem:read_u8(0x83FA))", True)
        if temp != 36:
            score += temp
        sleep(0.16)

        score *= 10
        temp = run("print(mem:read_u8(0x83F9))", True)
        if temp != 36:
            score += temp
        sleep(0.16)

        score *= 10
        temp = run("print(mem:read_u8(0x83F8))", True)
        if temp != 36:
            score += temp
        sleep(0.16)

    # print("score: " + str(score))

    key = b"\xFF\xFF\xFF\xFF\xFF\xFF"
    uid = None
    authenticated = False
    check = False
    while not check:
        while not authenticated:
            while uid is None:
                # display message
                run("manager.machine:popmessage('tap card to collect your " + str(score) + " tickets')", False)
                # Check if a card is available to read
                uid = pn532.read_passive_target(timeout=2)

            authenticated = pn532.mifare_classic_authenticate_block(uid, 4, MIFARE_CMD_AUTH_B, key)
            if not authenticated:
                run("manager.machine:popmessage('tap card again')", False)
                uid = None
            
        # read points on card
        cardpoints = int.from_bytes(pn532.mifare_classic_read_block(4), "big")
        
        # write new points to card
        newpoints = score + cardpoints
        data = newpoints.to_bytes(16, 'big')
        pn532.mifare_classic_write_block(4, data)

        # read points from card
        check = int.from_bytes(pn532.mifare_classic_read_block(4), "big") == newpoints

    run("manager.machine:popmessage('you had " + str(cardpoints) + " tickets you now have " + str(newpoints) + " tickets!')", False)

    sleep(2)

    run("emu.unpause()", False)


alive = False
with subprocess.Popen(
    shlex.split("mame -console -nodebug -skip_gameinfo"),
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
) as process:
    sleep(1)
    display(-1)

    while(True):
        rom = runraw("print(emu.romname())", True)
        if rom == "pacman":
            if game != PACMAN:
                sleep(10)
                run("cpu = manager.machine.devices[':maincpu']", False)
                sleep(1)
                run("mem = cpu.spaces['program']", False)
                sleep(1)
                run("s = manager.machine.screens[':screen']", False)
                game = PACMAN
        elif rom == "invaderl":
            if game != SPACE:
                sleep(10)
                run("cpu = manager.machine.devices[':maincpu']", False)
                sleep(1)
                run("mem = cpu.spaces['program']", False)
                sleep(1)
                run("s = manager.machine.screens[':screen']", False)
                game = SPACE
        elif rom == "galagao":
            if game != GALA:
                sleep(10)
                run("cpu = manager.machine.devices[':maincpu']", False)
                sleep(1)
                run("mem = cpu.spaces['program']", False)
                sleep(1)
                run("s = manager.machine.screens[':screen']", False)
                game = GALA
        else:
            game = NOTHING
        
        if game == PACMAN:
            lives = run("print(mem:read_u8(0x4e14))", True)
            if lives == 3:
                alive = True
            if lives == 0 and alive:
                alive = False
                death()

        if game == SPACE:
            lives = run("print(mem:read_u8(0x20ef))", True)
            if lives == 1:
                alive = True
            if lives == 0 and alive:
                alive = False
                death()
        
        if game == GALA:
            lives = run("print(mem:read_u8(0x9820))", True)
            if lives == 2:
                alive = True
            if lives == 255 and alive:
                alive = False
                death()

        sleep(.5)
