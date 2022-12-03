from pyjoystick.sdl2 import Key, Joystick, run_event_loop

def print_add(joy):
    print('Added', joy)

def print_remove(joy):
    print('Removed', joy)

def key_received(key):
    # print('received', key)
    if key.value == Key.HAT_UP:
        print("up")
    elif key.value == Key.HAT_DOWN:
        print("down")
    if key.value == Key.HAT_LEFT:
        print("left")
    elif key.value == Key.HAT_UPLEFT:
        print("upleft")
    elif key.value == Key.HAT_DOWNLEFT:
        print("downleft")
    elif key.value == Key.HAT_RIGHT:
        print("right")
    elif key.value == Key.HAT_UPRIGHT:
        print("upright")
    elif key.value == Key.HAT_DOWNRIGHT:
        print("downright")

run_event_loop(print_add, print_remove, key_received)