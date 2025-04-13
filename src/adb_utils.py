import subprocess
import random
import time

def adb_tap(x, y, jitter=3):
    jitter_x = random.randint(-jitter, jitter)
    jitter_y = random.randint(-jitter, jitter)
    new_x, new_y = x + jitter_x, y + jitter_y
    print(f"adb tap: {new_x}, {new_y} (jitter: {jitter_x}, {jitter_y})")
    cmd = f"adb shell input tap {new_x} {new_y}"
    subprocess.run(cmd, shell=True)

def adb_swipe(x1, y1, x2, y2, duration=300):
    cmd = f"adb shell input swipe {x1} {y1} {x2} {y2} {duration}"
    subprocess.run(cmd, shell=True)

def capture_screen(filename="screen.png"):
    with open(filename, "wb") as f:
        subprocess.run("adb exec-out screencap -p", shell=True, stdout=f)