# reaction_game_v2_hack.py

import subprocess
import shlex
from time import sleep

def display(r):
    global process
    print(process.stdout.read1().decode("utf-8"), end=r, flush=True)

with subprocess.Popen(
    shlex.split("mame pacman -console -nodebug -skip_gameinfo"),
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
) as process:
    sleep(1)
    display("\n")

    process.stdin.write(b"cpu = manager.machine.devices[':maincpu'] \n")
    process.stdin.flush()
    display("\n")

    process.stdin.write(b"mem = cpu.spaces['program'] \n")
    process.stdin.flush()
    display("\n")

    sleep(20)
    while(True):
        process.stdin.write(b"print(mem:read_i8(0x4e14)) \n")
        process.stdin.flush()
        # print(process.stdout.read1().decode("utf-8"), end="", flush=True)
        display("")
        sleep(1)