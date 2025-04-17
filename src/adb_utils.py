import subprocess
import random

def adb_tap(x, y, jitter=1):
    """
    Sends a tap command via ADB at (x, y) with an added random jitter.
    """
    jitter_x = random.randint(-jitter, jitter)
    jitter_y = random.randint(-jitter, jitter)
    new_x, new_y = x + jitter_x, y + jitter_y
    print(f"adb tap: {new_x}, {new_y} (jitter: {jitter_x}, {jitter_y})")
    cmd = f"adb shell input tap {new_x} {new_y}"

    subprocess.run(cmd, shell=True)

def capture_screen(filename="screen.png"):
    """Capture a screenshot from the device using ADB."""
    with open(filename, "wb") as f:
        subprocess.run("adb exec-out screencap -p", shell=True, stdout=f)