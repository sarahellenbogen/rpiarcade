# reaction_game_v2_hack.py

import subprocess
import shlex
from time import sleep

def display(r, char):
    global process
    buffer = process.stdout.read1(-1)
    print(buffer.decode("utf-8"), end="", flush=True)
    return buffer.decode("utf-8")

def search_for_output(string):
    buffer = ""
    while not (string in buffer):
        print("buffer: " + buffer, end="")
        buffer = buffer + display("", 1)
    print("hello\n")

def run(command):
    process.stdin.write(command)
    process.stdin.flush()
    display("\n", -1)


alive = False

with subprocess.Popen(
    shlex.split("mame pacman -console -nodebug -skip_gameinfo"),
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
) as process:
    sleep(1)
    display("\n", -1)
    sleep(15)
    run(b"cpu = manager.machine.devices[':maincpu'] \n")
    run(b"mem = cpu.spaces['program'] \n")
    display("\n", -1)

    while(True):
        run(b"print(mem:read_i8(0x4e14)) \n")

        search_for_output("[MAME]>")
        sleep(1)