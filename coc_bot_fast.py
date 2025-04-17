# coc_bot.py
import subprocess
import time
import random
import cv2
import numpy as np

import pytesseract
import re

# --- Utility Functions ---


def jitter_coord(x, y, jitter_range=10):
    return x + random.randint(-jitter_range, jitter_range), y + random.randint(-jitter_range, jitter_range)


def read_trophies():
    capture_screen("trophy_screen.png")
    img = cv2.imread("trophy_screen.png")
    if img is None:
        print("Error reading captured screen!")
        return None

    # Coordinates for the top-left corner where trophies appear.
    # Adjust these (x1, y1, x2, y2) to match your device/screenshot exactly.
    x1, y1 = 230, 165    # top-left corner of ROI
    x2, y2 = 325, 205  # bottom-right corner of ROI

    # Crop the region of interest (ROI)
    roi = img[y1:y2, x1:x2]

    # Convert to grayscale
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Optionally apply a threshold to darken text
    # You may need to experiment with thresholds or other preprocessing
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    # Use Tesseract to read the text
    # --psm 7 helps Tesseract focus on a single line/number
    config = "--psm 7 -c tessedit_char_whitelist=0123456789"
    text = pytesseract.image_to_string(thresh, config=config)

    # Extract digits from the recognized text
    match = re.findall(r"\d+", text)
    if match:
        trophies_str = match[0]  # e.g. "2922"
        trophies = int(trophies_str)
        return trophies
    else:
        return None

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

def adb_swipe(x1, y1, x2, y2, duration=300):
    """Send a swipe command via ADB."""
    cmd = f"adb shell input swipe {x1} {y1} {x2} {y2} {duration}"
    subprocess.run(cmd, shell=True)

def capture_screen(filename="screen.png"):
    """Capture a screenshot from the device using ADB."""
    with open(filename, "wb") as f:
        subprocess.run("adb exec-out screencap -p", shell=True, stdout=f)

def find_template(template_path, threshold=0.85):
    """
    Capture the screen and search for the template image.
    Returns the center coordinates of the match if confidence ≥ threshold; otherwise None.
    """
    capture_screen()
    screen = cv2.imread("screen.png")
    template = cv2.imread(template_path)
    if screen is None or template is None:
        print(f"Error: Could not load images for {template_path}.")
        return None
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val >= threshold:
        t_h, t_w = template.shape[:2]
        return (max_loc[0] + t_w // 2, max_loc[1] + t_h // 2)
    return None

def wait_for_template(template_path, timeout=3, threshold=0.85):
    """
    Searches for a template image on screen for up to `timeout` seconds.
    If found, returns the coordinates (with random jitter ±10 pixels); otherwise, returns None.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        coords = find_template(template_path, threshold)
        if coords:
            return (coords[0], coords[1])
    return None


def get_drop_coords(number=1):
    rage_mid = (1202, 104)
    rage_top = (1197, 238)
    rage_bot = (1190, 725)

    rage2_right_up = (935, 345)
    rage2_right_down = (935, 570)

    rage2_left_up = (1400, 345)
    rage2_left_down = (1400, 570)


    if number == 1:
        print("Using attack strategy 1.")
        left_x = random.randint(78, 110)
        right_x = random.randint(480, 514)
        mid_x = random.randint(269, 310)
        left_y = round(-0.8165 * left_x + 542.68)
        right_y = round(-0.8165 * right_x + 542.68)
        mid_y = round(-0.8165 * mid_x + 542.68)
        return left_x, left_y, right_x, right_y, mid_x, mid_y, rage_mid, rage_top, rage_bot, rage2_right_up, rage2_right_down
    elif number == 2:
        print("Using attack strategy 2.")   
        left_x = random.randint(120, 150)
        right_x = random.randint(350, 400)
        mid_x = random.randint(220, 280)
        left_y = round(0.865 * left_x + 376.2)
        right_y = round(0.865 * right_x + 376.2)
        mid_y = round(0.865 * mid_x + 376.2)
        return left_x, left_y, right_x, right_y, mid_x, mid_y, rage_mid, rage_top, rage_bot, rage2_right_up, rage2_right_down
    elif number == 3:
        print("Using attack strategy 3.")
        left_x = random.randint(1755, 1795)
        right_x = random.randint(2270, 2318)
        mid_x = random.randint(1990, 2060)
        left_y = round(0.74 * left_x - 1120)
        right_y = round(0.74 * right_x - 1120)
        mid_y = round(0.74 * mid_x - 1120)
        return left_x, left_y, right_x, right_y, mid_x + 5, mid_y, rage_mid, rage_top, rage_bot, rage2_left_up, rage2_left_down
        




# --- COORDS Dictionary ---
# Use fallback coordinates if dynamic template detection fails.
COORDS = {
    "drop_attack1": (198, 466),
    "drop_attack2": (751, 68),
    "drop_attack3": (209, 556),
    "drop_attack4": (454, 729),
    "drop_attack5": (2217, 490),
    "drop_attack6": (400, 320),
    "drop_attack7": (2070, 330),



    "backup_attack": (218, 947),
    "zoom_out_start": (1130, 310),
    "zoom_out_end": (1090, 525),


    "scroll_down_start": (1130, 275),
    "scroll_up_start": (1130, 350),

    "midpoint_drop": (600, 381),

    "valk_select_fallback": (457, 967),
    "valk_drop_bottom_left": (220, 650),
    "valk_drop_top_middle": (1010, 70),


    "midpoint_dropv2": (1790, 360),
    "valk_drop_bottom_leftv2": (1466, 66),
    "valk_drop_top_middlev2": (2260, 718),

    "rage_fallback1": (1432, 300),
    "rage_fallback2": (1120, 470),
    "rage_fallback3": (967, 650),
    "rage_fallback4": (1300, 500),
    "rage_fallback5": (1180, 710),

    "rage_fallback1v2": (900, 300),
    "rage_fallback2v2": (1200, 490),
    "rage_fallback3v2": (1312, 590),
    "rage_fallback4v2": (766, 482),
    "rage_fallback5v2": (1100, 683),

}

# --- Bot Functions ---
def drop_trophies():
    iterations = random.randint(15, 25)
    print(f"Starting trophy drop for {iterations} iterations.")
    for i in range(iterations):
        print(f"\nIteration {i+1}/{iterations}")
        find_attack(True)
        print("Waiting for 'return home' indicator...")
        timeout = 180
        start_time = time.time()
        while time.time() - start_time < timeout:
            ret_home = wait_for_template("templates/return_home.png", timeout=3)
            if ret_home:
                print("Return home detected at:", ret_home)
                time.sleep(random.uniform(0, 0.5))
                for _ in range(random.randint(2, 2)):
                    jitter_x = random.randint(-50, 50)
                    jitter_y = random.randint(-50, 50)
                    adb_tap(ret_home[0] + jitter_x, ret_home[1] + jitter_y)
                    time.sleep(random.uniform(0.2, 0.3))
                time.sleep(random.uniform(0.5, 1))
                break
            time.sleep(1)
        else:
            print("Timeout waiting for return home.")



def find_attack(drop=False):
    while True:
        time.sleep(random.uniform(0, 1))
        print("Searching for 'attack' button...")
        attack_btn = wait_for_template("templates/attack_button.png", timeout=10)
        if attack_btn:
            print("Found attack button at:", attack_btn)
            jitter_x = random.randint(-50, 50)
            jitter_y = random.randint(-50, 50)
            adb_tap(attack_btn[0] + jitter_x, attack_btn[1] + jitter_y)
            time.sleep(random.uniform(0, 1))
        else:
            print("Attack button not found within 10 seconds.")
            print("backup")
            jitter_x = random.randint(-60, 60)
            jitter_y = random.randint(-60, 60)
            adb_tap(COORDS["backup_attack"][0] + jitter_x, COORDS["backup_attack"][1] + jitter_y)
            time.sleep(random.uniform(0, 1))

        print("Searching for 'find match' button...")
        match_btn = wait_for_template("templates/find_match.png", timeout=3)
        if match_btn:
            print("Found 'find match' button at:", match_btn)
            for _ in range(random.randint(1, 3)):
                jitter_x = random.randint(-70, 70)
                jitter_y = random.randint(-70, 70)
                adb_tap(match_btn[0] + jitter_x, match_btn[1] + jitter_y)
                time.sleep(random.uniform(0.2, 0.3))
            time.sleep(random.uniform(0, 1))
        else:
            print("Find match button not found within 3 seconds.")
            # Restart the loop if this part fails.
            continue

        if drop:
            print("Using drop strategy")
            drop_attack()
            break

        # Randomly click the 'next' button 0 to 5 times.
        clicks = random.randint(0, 1)
        for _ in range(clicks):
            random_moves = random.randint(0, 1)
            if random_moves == 1:
                time.sleep(random.uniform(0, 1))
                for _ in range(random.randint(1, 3)):
                    random_x = random.randint(600, 1200)
                    random_y = random.randint(100, 500)
                    adb_tap(random_x, random_y)
                    time.sleep(random.uniform(0, 1))
            next_btn = wait_for_template("templates/next_button.png", timeout=20)
            if next_btn:
                print("Clicking next button at:", next_btn)
                time.sleep(random.uniform(0, 0.5))
                for _ in range(random.randint(1, 5)):
                    jitter_x = random.randint(-80, 80)
                    jitter_y = random.randint(-50, 50)
                    adb_tap(next_btn[0] + jitter_x, next_btn[1] + jitter_y)
            else:
                print("Next button not found within 20 seconds.")
                time.sleep(180)
                continue

        time.sleep(random.uniform(0, 0.5))

        attack()

        break

def drop_attack():
    attack_strat = random.randint(1, 3)
    left_x, left_y, right_x, right_y, mid_x, mid_y, rage_mid, rage_top, rage_bot, rage2_right_up, rage2_right_down = get_drop_coords(attack_strat)

    next_btn = wait_for_template("templates/next_button.png", timeout=15)

    adb_tap(1654 + random.randint(-7, 7), 965 + random.randint(-7, 7))

    time.sleep(random.uniform(0.2, 0.5))

    
    adb_tap(random.randint(1000, 1700), random.randint(100, 400))


    time.sleep(random.uniform(0.3, 0.7))

    jitter_x = random.randint(-50, 50)
    jitter_y = random.randint(-10, 10)
    adb_tap(229 + jitter_x, 805 + jitter_y)

    okay = wait_for_template("templates/okay.png", timeout=5)
    if okay:
        print("Found Okay button at:", okay)
        time.sleep(random.uniform(0, 0.5))
        for _ in range(random.randint(1, 2)):
            jitter_x = random.randint(-50, 50)
            jitter_y = random.randint(-20, 20)
            adb_tap(okay[0] + jitter_x, okay[1] + jitter_y)
            time.sleep(random.uniform(0.25, 0.4))

    


def attack():
    print("Starting attack sequence...")
    attack_strat = random.randint(2, 3)
    left_x, left_y, right_x, right_y, mid_x, mid_y, rage_mid, rage_top, rage_bot, rage2_right_up, rage2_right_down = get_drop_coords(attack_strat)

    # Step 1: Slight scroll down using human-like random swipe.
    # print("Scrolling down slightly...")
    # human_swipe(COORDS["scroll_down_start"])
    
    next_btn = wait_for_template("templates/next_button.png", timeout=15)

    jitter_x = random.randint(-40, 40)
    jitter_y = random.randint(-40, 40)

    # adb_tap(457 + jitter_x, 977 + jitter_y)
    # time.sleep(random.uniform(0.5, 1))

    # adb_tap(left_x, left_y)
    # time.sleep(random.uniform(0.5, 0.7))
    # adb_tap(right_x, right_y)
    # time.sleep(random.uniform(0.5, 0.7))

    # === Baby Dragon + Left ===
    adb_tap(*jitter_coord(592, 975))
    time.sleep(random.uniform(0.1, 0.3))
    adb_tap(left_x, left_y)
    time.sleep(random.uniform(0.1, 0.3))

    
    adb_tap(*jitter_coord(941, 946))
    time.sleep(random.uniform(0.15, 0.4))
    adb_tap(mid_x, mid_y)
    time.sleep(random.uniform(0.15, 0.25))
    adb_tap(mid_x, mid_y)
    time.sleep(random.uniform(0.15, 0.25))

    # === Tap Queen ===
    adb_tap(*jitter_coord(1084, 951))
    time.sleep(random.uniform(0.15, 0.3))
    adb_tap(mid_x, mid_y)
    time.sleep(random.uniform(0.15, 0.3))
    adb_tap(mid_x, mid_y)
    time.sleep(random.uniform(0.15, 0.3))

    # === Tap Warden ===
    adb_tap(*jitter_coord(1230, 942))
    time.sleep(random.uniform(0.15, 0.3))
    adb_tap(mid_x, mid_y)
    time.sleep(random.uniform(0.15, 0.3))
    adb_tap(mid_x, mid_y)
    time.sleep(random.uniform(0.15, 0.3))

    # === Tap Royal Champion ===
    adb_tap(*jitter_coord(1376, 949))
    time.sleep(random.uniform(0.1, 0.3))
    adb_tap(mid_x, mid_y)
    time.sleep(random.uniform(0.15, 0.25))
    adb_tap(mid_x, mid_y)
    time.sleep(random.uniform(0.15, 0.25))

    # === Tap Valkyrie ===
    adb_tap(*jitter_coord(457, 977))
    time.sleep(random.uniform(0.2, 0.3))

    # === Tap Middle Range 5-9 ===
    for _ in range(random.randint(5, 9)):
        adb_tap(mid_x, mid_y)
        time.sleep(random.uniform(0.1, 0.2))
    

    # === Siege + Right ===
    adb_tap(*jitter_coord(786, 992))
    time.sleep(random.uniform(0.1, 0.3))
    adb_tap(mid_x, mid_y)

    # === Warden Again ===
    time.sleep(random.uniform(0.5, 0.8))
    adb_tap(*jitter_coord(1230, 942))
    time.sleep(random.uniform(0.2, 0.4))

    # === King Again ===
    adb_tap(*jitter_coord(941, 946))
    time.sleep(random.uniform(0.2, 0.4))

    if attack_strat == 2:
        adb_tap(1654 + random.randint(-7, 7), 965 + random.randint(-7, 7))

        # Click 4 specific points with 0.2–0.4 sec delay
        for x, y in [(988, 704), (791, 448), (1122, 535), (1026, 608), (1036, 360), (1351, 686)]:
            time.sleep(random.uniform(0.2, 0.4))
            adb_tap(x + random.randint(-7, 7), y + random.randint(-7, 7))

    elif attack_strat == 3:
        # Select starting point with 7 jitter
        adb_tap(1654 + random.randint(-7, 7), 965 + random.randint(-7, 7))

        # Click 4 new coordinates with same timing
        for x, y in [(1258, 270), (1380, 483), (1408, 685), (1300, 522), (1285, 644)]:
            time.sleep(random.uniform(0.2, 0.4))
            adb_tap(x + random.randint(-7, 7), y + random.randint(-7, 7))



    # === Rage Sequence ===


    if attack_strat == 1:
        time.sleep(random.uniform(9, 11))
        jitter_x = random.randint(-10, 10)
        jitter_y = random.randint(-10, 10)
        adb_tap(*jitter_coord(1513, 970))
        time.sleep(random.uniform(0.3, 0.6))
        adb_tap(COORDS["rage_fallback1"][0] + jitter_x, COORDS["rage_fallback1"][1] + jitter_y)
        time.sleep(random.uniform(0.5, 0.8))
        adb_tap(COORDS["rage_fallback2"][0] + jitter_x, COORDS["rage_fallback2"][1] + jitter_y)
        time.sleep(random.uniform(0.3, 0.6))
        adb_tap(COORDS["rage_fallback3"][0] + jitter_x, COORDS["rage_fallback3"][1] + jitter_y)
        time.sleep(random.uniform(5, 8))
        adb_tap(*jitter_coord(1513, 970))
        adb_tap(COORDS["rage_fallback4"][0] + jitter_x, COORDS["rage_fallback4"][1] + jitter_y)
        time.sleep(random.uniform(0.5, 1))
        adb_tap(COORDS["rage_fallback5"][0] + jitter_x, COORDS["rage_fallback5"][1] + jitter_y)

    elif attack_strat == 2:

        # Wait 18–21 seconds
        time.sleep(random.uniform(9, 12))
        adb_tap(*jitter_coord(1513, 970))
        # Rage drop at 3 locations
        for x, y in [(1013, 307), (1035, 513), (1055, 689)]:
            adb_tap(x + random.randint(-7, 7) + 15, y + random.randint(-7, 7))

    elif attack_strat == 3:


        # Wait 18–21 seconds
        time.sleep(random.uniform(9, 12))
        adb_tap(*jitter_coord(1513, 970))

        # Rage drop at 3 new locations
        for x, y in [(1258, 270), (1380, 483), (1408, 685)]:
            adb_tap(x + random.randint(-7, 7) - 40 , y + random.randint(-7, 7))


def main():
    iterations = random.randint(25, 35)
    print(f"Starting main loop for {iterations} iterations.")
    for i in range(iterations):
        attack_btn = wait_for_template("templates/attack_button.png", timeout=10)
        print(f"AHHHHHH WE ARE ABOUT TO TEST TROPHIES")
        trophies = read_trophies()
        print(f"Current Trophies: {trophies}")
        print(f"AHHHHHH WE GOT TROPHIES")
        if trophies is not None:
            print(f"Current Trophies: {trophies}")
            if trophies > 4800 and trophies < 5200:
                drop_trophies()
                # Optionally, wait some time after dropping trophies before proceeding.
                continue  # Skip this iteration and re-check trophy count next time.
            else:
                tries = 0
                while trophies > 5200 and trophies < 2000 and tries < 3:
                    print(f"Misread detected (trophies = {trophies}). Retrying read ({tries + 1}/3)...")
                    trophies = read_trophies()
                    tries += 1

        print(f"\nIteration {i+1}/{iterations}")
        find_attack(False)
        print("Waiting for 'return home' indicator...")
        timeout = 180
        start_time = time.time()
        while time.time() - start_time < timeout:
            ret_home = wait_for_template("templates/return_home.png", timeout=3)
            if ret_home:
                print("Return home detected at:", ret_home)
                time.sleep(random.uniform(0, 0.5))
                for _ in range(random.randint(2, 2)):
                    jitter_x = random.randint(-50, 50)
                    jitter_y = random.randint(-50, 50)
                    adb_tap(ret_home[0] + jitter_x, ret_home[1] + jitter_y)
                    time.sleep(random.uniform(0.2, 0.3))
                break
        else:
            print("Timeout waiting for return home.")
            jitter_x = random.randint(-100, 100)
            jitter_y = random.randint(-20, 20)
            adb_tap(217 + jitter_x, 803 + jitter_y)

    print("Main loop finished.")

if __name__ == "__main__":
    main()
