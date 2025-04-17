# coc_bot.py
import subprocess
import time
import random
import cv2
import numpy as np

import pytesseract
import re

# --- Utility Functions ---

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

def adb_tap(x, y, jitter=2):
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

# def human_swipe(base_start):
#     """
#     Simulates a human-like swipe from a randomized start position (near base_start) 
#     to an ideal end position with a limited error margin.
    
#     The swipe gesture can be performed in 1, 2, or 3 segments randomly:
#       - If 1 swipe, the movement goes directly from the randomized start to the ideal end.
#       - If 2 swipes, the gesture first swipes in a random direction, then corrects the 
#         movement by swiping from the intermediate point to the ideal end.
#       - If 3 swipes, two random intermediate swipes are performed followed by a 
#         final correction swipe to the ideal end.
    
#     The durations of each swipe are randomized between 500 and 800 milliseconds.
#     """
#     # Randomize the starting point from the base_start within a wide margin.
#     start_x = base_start[0] + random.randint(-200, 200)
#     start_y = base_start[1] + random.randint(-100, 100)

#     # Calculate the ideal end (with a slight vertical movement of around 215 pixels) plus a small random error.
#     end_y = start_y + 270 + random.randint(-20, 20)
#     end_x = start_x + random.randint(-20, 20)

#     # Randomly decide how many swipe segments to execute (1, 2, or 3).
#     swipe_times = random.randint(1, 3)
    
#     if swipe_times == 1:
#         # Single continuous swipe to the ideal end position.
#         total_duration = random.randint(2000, 2200)
#         adb_swipe(start_x, start_y, end_x, end_y, duration=total_duration)
    
#     elif swipe_times == 2:
#         # Two swipes: first swipe in a random direction, then a correction swipe to the ideal end.
#         # Generate a random offset for the intermediate endpoint.
#         random_x = random.randint(-150, 150)
#         random_y = random.randint(-150, 150)
#         intermediate_x = end_x + random_x
#         intermediate_y = end_y + random_y
        
#         # First swipe from the randomized start to the intermediate point.
#         total_duration = random.randint(1500, 2000)
#         adb_swipe(start_x, start_y, intermediate_x, intermediate_y, duration=total_duration)
#         time.sleep(random.uniform(0.5, 1))
        
#         # Second swipe correcting the trajectory back to the ideal end.
#         total_duration = random.randint(1500, 2000)
#         adb_swipe(intermediate_x, intermediate_y, end_x, end_y, duration=total_duration)
    
#     else:
#         # Three swipes: two random intermediate swipes followed by a final correction swipe.
#         # First swipe: move to a first intermediate point.
#         random_x1 = random.randint(-125, 125)
#         random_y1 = random.randint(-125, 125)
#         intermediate1_x = start_x + random_x1
#         intermediate1_y = start_y + random_y1

#         total_duration = random.randint(1000, 1100)
#         adb_swipe(start_x, start_y, intermediate1_x, intermediate1_y, duration=total_duration)
#         time.sleep(random.uniform(0.5, 1))

#         # Second swipe: move from intermediate1 towards a second intermediate point (offset relative to ideal).
#         random_x2 = random.randint(-125, 125)
#         random_y2 = random.randint(-125, 125)
#         intermediate2_x = end_x + random_x2
#         intermediate2_y = end_y + random_y2

#         total_duration = random.randint(1000, 1100)
#         adb_swipe(intermediate1_x, intermediate1_y, intermediate2_x, intermediate2_y, duration=total_duration)
#         time.sleep(random.uniform(0.5, 1))

#         # Third swipe: final correction to the ideal end position.
#         total_duration = random.randint(1000, 1100)
#         adb_swipe(intermediate2_x, intermediate2_y, end_x, end_y, duration=total_duration)

# def human_swipe_up(base_start):
#     # Randomize the starting point from the base_start within a wide margin.
#     start_x = base_start[0] + random.randint(-150, 150)
#     start_y = base_start[1] + random.randint(-100, 100)

#     # Calculate the ideal end (with a slight vertical movement of around 215 pixels) plus a small random error.
#     end_y = start_y - 270 + random.randint(-20, 20)
#     end_x = start_x + random.randint(-20, 20)

#     # Randomly decide how many swipe segments to execute (1, 2, or 3).
#     swipe_times = random.randint(1, 3)
    
#     if swipe_times == 1:
#         # Single continuous swipe to the ideal end position.
#         total_duration = random.randint(2000, 2200)
#         adb_swipe(start_x, start_y, end_x, end_y, duration=total_duration)
    
#     elif swipe_times == 2:
#         # Two swipes: first swipe in a random direction, then a correction swipe to the ideal end.
#         # Generate a random offset for the intermediate endpoint.
#         random_x = random.randint(-150, 150)
#         random_y = random.randint(-150, 150)
#         intermediate_x = end_x + random_x
#         intermediate_y = end_y + random_y
        
#         # First swipe from the randomized start to the intermediate point.
#         total_duration = random.randint(1500, 2000)
#         adb_swipe(start_x, start_y, intermediate_x, intermediate_y, duration=total_duration)
#         time.sleep(random.uniform(0.5, 1))
        
#         # Second swipe correcting the trajectory back to the ideal end.
#         total_duration = random.randint(1500, 2000)
#         adb_swipe(intermediate_x, intermediate_y, end_x, end_y, duration=total_duration)
    
#     else:
#         # Three swipes: two random intermediate swipes followed by a final correction swipe.
#         # First swipe: move to a first intermediate point.
#         random_x1 = random.randint(-125, 125)
#         random_y1 = random.randint(-125, 125)
#         intermediate1_x = start_x + random_x1
#         intermediate1_y = start_y + random_y1

#         total_duration = random.randint(1000, 1100)
#         adb_swipe(start_x, start_y, intermediate1_x, intermediate1_y, duration=total_duration)
#         time.sleep(random.uniform(0.5, 1))

#         # Second swipe: move from intermediate1 towards a second intermediate point (offset relative to ideal).
#         random_x2 = random.randint(-125, 125)
#         random_y2 = random.randint(-125, 125)
#         intermediate2_x = end_x + random_x2
#         intermediate2_y = end_y + random_y2

#         total_duration = random.randint(1000, 1100)
#         adb_swipe(intermediate1_x, intermediate1_y, intermediate2_x, intermediate2_y, duration=total_duration)
#         time.sleep(random.uniform(0.5, 1))

#         # Third swipe: final correction to the ideal end position.
#         total_duration = random.randint(1000, 1100)
#         adb_swipe(intermediate2_x, intermediate2_y, end_x, end_y, duration=total_duration)

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
        left_y = round(0.751 * left_x - 1278.64)
        right_y = round(0.751 * right_x - 1278.64)
        mid_y = round(0.751 * mid_x - 1278.64)
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
    iterations = random.randint(25, 45)
    print(f"Starting trophy drop for {iterations} iterations.")
    for i in range(iterations):
        print(f"\nIteration {i+1}/{iterations}")
        find_attack(True)
        print("Waiting for 'return home' indicator...")
        timeout = 240
        start_time = time.time()
        while time.time() - start_time < timeout:
            ret_home = wait_for_template("templates/return_home.png", timeout=3)
            if ret_home:
                print("Return home detected at:", ret_home)
                time.sleep(random.uniform(1, 2))
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
            time.sleep(random.uniform(0.5, 3))
        else:
            print("Attack button not found within 10 seconds.")
            print("backup")
            jitter_x = random.randint(-60, 60)
            jitter_y = random.randint(-60, 60)
            adb_tap(COORDS["backup_attack"][0] + jitter_x, COORDS["backup_attack"][1] + jitter_y)
            time.sleep(random.uniform(0.5, 3))

        print("Searching for 'find match' button...")
        match_btn = wait_for_template("templates/find_match.png", timeout=3)
        if match_btn:
            print("Found 'find match' button at:", match_btn)
            for _ in range(random.randint(1, 3)):
                jitter_x = random.randint(-70, 70)
                jitter_y = random.randint(-70, 70)
                adb_tap(match_btn[0] + jitter_x, match_btn[1] + jitter_y)
                time.sleep(random.uniform(0.2, 0.3))
            time.sleep(random.uniform(0.5, 2))
        else:
            print("Find match button not found within 3 seconds.")
            # Restart the loop if this part fails.
            continue

        if drop:
            print("Using drop strategy")
            drop_attack()
            break

        # Randomly click the 'next' button 0 to 5 times.
        clicks = random.randint(0, 3)
        for _ in range(clicks):
            random_moves = random.randint(0, 1)
            if random_moves == 1:
                time.sleep(random.uniform(0, 1))
                for _ in range(random.randint(1, 3)):
                    random_x = random.randint(600, 1200)
                    random_y = random.randint(100, 500)
                    adb_tap(random_x, random_y)
                    time.sleep(random.uniform(1, 2))
            next_btn = wait_for_template("templates/next_button.png", timeout=20)
            if next_btn:
                print("Clicking next button at:", next_btn)
                time.sleep(random.uniform(0, 1))
                for _ in range(random.randint(1, 5)):
                    jitter_x = random.randint(-80, 80)
                    jitter_y = random.randint(-50, 50)
                    adb_tap(next_btn[0] + jitter_x, next_btn[1] + jitter_y)
                    time.sleep(random.uniform(0.2, 0.5))
            else:
                print("Next button not found within 20 seconds.")
                time.sleep(240)
                continue

        time.sleep(random.uniform(0, 3))

        attack()

        # # Proceed to the attack phase.
        # attack_strat = random.randint(1, 2)
        # if attack_strat == 1:
        #     print("Using attack strategy 1.")
        #     attack()
        # else:
        #     print("Using attack strategy 2.")
        #     attack2()

        # Break out of the loop if everything is done successfully.
        break

def drop_attack():
    attack_strat = random.randint(1, 3)
    left_x, left_y, right_x, right_y, mid_x, mid_y, rage_mid, rage_top, rage_bot, rage2_right_up, rage2_right_down = get_drop_coords(attack_strat)

    next_btn = wait_for_template("templates/next_button.png", timeout=15)

    print("Capturing hero positions dynamically...")
    king_found = wait_for_template("templates/king.png", timeout=3)

    if king_found:
        print("Found King at:", king_found)
        adb_tap(king_found[0], king_found[1])
        time.sleep(random.uniform(0.75, 1.5))
        placement = random.randint(1, 3)
        if placement == 1:
            print("Dropping King at left drop point.")
            adb_tap(left_x, left_y)
        elif placement == 2:
            print("Dropping King at right drop point.")
            adb_tap(right_x, right_y)
        elif placement == 3:
            print("Dropping King at mid drop point.")
            adb_tap(mid_x, mid_y)
        time.sleep(random.uniform(0, 2))
    
    surrender = wait_for_template("templates/surrender.png", timeout=5)
    
    if surrender:
        print("Found Surrender button at:", surrender)
        jitter_x = random.randint(-100, 100)
        jitter_y = random.randint(-20, 20)
        adb_tap(surrender[0] + jitter_x, surrender[1] + jitter_y)
        time.sleep(random.uniform(0, 1))

        okay = wait_for_template("templates/okay.png", timeout=5)
        if okay:
            print("Found Okay button at:", okay)
            time.sleep(random.uniform(0, 1.5))
            for _ in range(random.randint(1, 2)):
                jitter_x = random.randint(-50, 50)
                jitter_y = random.randint(-20, 20)
                adb_tap(okay[0] + jitter_x, okay[1] + jitter_y)
                time.sleep(random.uniform(0.25, 0.4))
    else:
        print("Surrender button not found, pressing backup end battle button")
        jitter_x = random.randint(-100, 100)
        jitter_y = random.randint(-20, 20)
        adb_tap(217 + jitter_x, 803 + jitter_y)






def attack():
    print("Starting attack sequence...")
    attack_strat = random.randint(1, 3)
    left_x, left_y, right_x, right_y, mid_x, mid_y, rage_mid, rage_top, rage_bot, rage2_right_up, rage2_right_down = get_drop_coords(attack_strat)

    # Step 1: Slight scroll down using human-like random swipe.
    # print("Scrolling down slightly...")
    # human_swipe(COORDS["scroll_down_start"])
    
    next_btn = wait_for_template("templates/next_button.png", timeout=15)

    # Step 2: Dynamically search for hero templates.
    print("Capturing hero positions dynamically...")
    valk_found = wait_for_template("templates/valk.png", timeout=2)
    king_found = wait_for_template("templates/king.png", timeout=2)
    queen_found = wait_for_template("templates/queen.png", timeout=2)
    warden_found = wait_for_template("templates/warden.png", timeout=2)
    royal_champion_found = wait_for_template("templates/royal_champion.png", timeout=2)
    siege_found = wait_for_template("templates/siege_barracks.png", timeout=2)
    baby_dragon_found = wait_for_template("templates/baby_dragon.png", timeout=2)
    rage_found = wait_for_template("templates/rage.png", timeout=2)

    # Step 3: Tap on the troops if found.
    if valk_found:
        print("Found Valkyrie at:", valk_found)
        adb_tap(valk_found[0], valk_found[1])
        time.sleep(random.uniform(0.5, 1))
    else:
        print("Valkyrie not found.")
        adb_tap(COORDS["valk_select_fallback"][0], COORDS["valk_select_fallback"][1])
        time.sleep(random.uniform(0.5, 0.7))

    adb_tap(left_x, left_y)
    time.sleep(random.uniform(0.5, 0.7))
    adb_tap(right_x, right_y)
    time.sleep(random.uniform(0.5, 0.7))

    
    if king_found:
        print("Found King at:", king_found)
        adb_tap(king_found[0], king_found[1])
        time.sleep(random.uniform(0.15, 0.4))
        adb_tap(mid_x, mid_y)
        time.sleep(random.uniform(0.15, 0.25))
        adb_tap(mid_x, mid_y)
        time.sleep(random.uniform(0.15, 0.25))


    if queen_found:
        print("Found Queen at:", queen_found)
        adb_tap(queen_found[0], queen_found[1])
        time.sleep(random.uniform(0.2, 0.4))
        adb_tap(mid_x, mid_y)
        time.sleep(random.uniform(0.2, 0.4))
        adb_tap(mid_x, mid_y)
        time.sleep(random.uniform(0.2, 0.4))

    if warden_found:
        print("Found Warden at:", warden_found)
        adb_tap(warden_found[0], warden_found[1])
        time.sleep(random.uniform(0.2, 0.4))
        adb_tap(mid_x, mid_y)
        time.sleep(random.uniform(0.2, 0.3))
        adb_tap(mid_x, mid_y)
        time.sleep(random.uniform(0.2, 0.3))

    if royal_champion_found:
        print("Found Royal Champion at:", royal_champion_found)
        adb_tap(royal_champion_found[0], royal_champion_found[1])
        time.sleep(random.uniform(0.1, 0.4))
        adb_tap(mid_x, mid_y)
        time.sleep(random.uniform(0.15, 0.25))
        adb_tap(mid_x, mid_y)
        time.sleep(random.uniform(0.15, 0.25))

    if valk_found:
        print("Found Valkyrie at:", valk_found)
        adb_tap(valk_found[0], valk_found[1])
        time.sleep(random.uniform(0.2, 0.4))
    else:
        print("Valkyrie not found.")
        adb_tap(COORDS["valk_select_fallback"][0], COORDS["valk_select_fallback"][1])
        time.sleep(random.uniform(0.2, 0.4))

    for _ in range(random.randint(5, 9)):
        adb_tap(mid_x, mid_y)
        time.sleep(random.uniform(0.2, 0.3))

    if warden_found:
        print("Found Warden at:", warden_found)
        time.sleep(random.uniform(0.5, 1))
        adb_tap(warden_found[0], warden_found[1])
        time.sleep(random.uniform(0.2, 0.4))
    
    if king_found:
        print("Found King at:", king_found)
        adb_tap(king_found[0], king_found[1])
        time.sleep(random.uniform(0.2, 0.4))

    if baby_dragon_found:
        print("Found Baby Dragon at:", baby_dragon_found)
        adb_tap(baby_dragon_found[0], baby_dragon_found[1])
        time.sleep(random.uniform(0.2, 0.4))
        adb_tap(left_x, left_y)
        time.sleep(random.uniform(0.2, 0.4))
    
    if siege_found:
        print("Found Siege Barracks at:", siege_found)
        adb_tap(siege_found[0], siege_found[1])
        time.sleep(random.uniform(0.2, 0.4))
        adb_tap(right_x, right_y)

    # human_swipe_up(COORDS["scroll_up_start"])

    time.sleep(random.uniform(9, 11))

    jitter_x = random.randint(-50, 50)
    jitter_y = random.randint(-50, 50)
    if attack_strat == 1:
    # Step 4: Tap on the rage spell.

        if rage_found:
            print("Found Rage spell at:", rage_found)
            adb_tap(rage_found[0], rage_found[1])
            time.sleep(random.uniform(0.3, 0.6))
            adb_tap(COORDS["rage_fallback1"][0] + jitter_x, COORDS["rage_fallback1"][1] + jitter_y)
            time.sleep(random.uniform(0.5, 0.8))
            adb_tap(COORDS["rage_fallback2"][0] + jitter_x, COORDS["rage_fallback2"][1] + jitter_y)
            time.sleep(random.uniform(0.3, 0.6))
            adb_tap(COORDS["rage_fallback3"][0]+ jitter_x, COORDS["rage_fallback3"][1] + jitter_y)
            time.sleep(random.uniform(5, 8))
            adb_tap(rage_found[0], rage_found[1])
            adb_tap(COORDS["rage_fallback4"][0]+ jitter_x, COORDS["rage_fallback4"][1] + jitter_y)
            time.sleep(random.uniform(0.5, 1))
            adb_tap(COORDS["rage_fallback5"][0]+ jitter_x, COORDS["rage_fallback5"][1] + jitter_y)
    elif attack_strat == 2:
        if rage_found:
            print("Found Rage spell at:", rage_found)
            adb_tap(rage_found[0], rage_found[1])
            time.sleep(random.uniform(0.3, 0.6))
            adb_tap(COORDS["rage_fallback1v2"][0] + jitter_x, COORDS["rage_fallback1v2"][1] + jitter_y)
            time.sleep(random.uniform(0.5, 0.8))
            adb_tap(COORDS["rage_fallback2v2"][0] + jitter_x, COORDS["rage_fallback2v2"][1] + jitter_y)
            time.sleep(random.uniform(0.3, 0.6))
            adb_tap(COORDS["rage_fallback3v2"][0] + jitter_x, COORDS["rage_fallback3v2"][1] + jitter_y)
            time.sleep(random.uniform(5, 8))
            adb_tap(rage_found[0], rage_found[1])
            adb_tap(rage_top[0] + 100 + jitter_x, rage_top[1] + 100 + jitter_y)
            time.sleep(random.uniform(0.5, 1))
            adb_tap(rage2_right_down[0] + 150 + jitter_x, rage2_right_down[1] - 50 + jitter_y)
    
    elif attack_strat == 3:
        if rage_found:
            print("Found Rage spell at:", rage_found)
            adb_tap(rage_found[0], rage_found[1])
            time.sleep(random.uniform(0.3, 0.6))
            adb_tap(COORDS["rage_fallback1v2"][0] + jitter_x, COORDS["rage_fallback1v2"][1] + jitter_y)
            time.sleep(random.uniform(0.5, 0.8))
            adb_tap(COORDS["rage_fallback2v2"][0] + jitter_x, COORDS["rage_fallback2v2"][1] + jitter_y)
            time.sleep(random.uniform(0.3, 0.6))
            adb_tap(COORDS["rage_fallback3v2"][0] + jitter_x, COORDS["rage_fallback3v2"][1] + jitter_y)
            time.sleep(random.uniform(5, 8))
            adb_tap(rage_found[0], rage_found[1])
            adb_tap(COORDS["rage_fallback4v2"][0] + jitter_x, COORDS["rage_fallback4v2"][1] + jitter_y)
            time.sleep(random.uniform(0.5, 1))
            adb_tap(COORDS["rage_fallback5v2"][0] + jitter_x, COORDS["rage_fallback5v2"][1] + jitter_y)


# def attack2():
#     print("Starting attack sequence...")

#     # Step 1: Slight scroll down using human-like random swipe.
#     # print("Scrolling down slightly...")
#     # human_swipe(COORDS["scroll_down_start"])

#     # Step 2: Dynamically search for hero templates.
#     print("Capturing hero positions dynamically...")
#     valk_found = wait_for_template("templates/valk.png", timeout=2)
#     king_found = wait_for_template("templates/king.png", timeout=2)
#     queen_found = wait_for_template("templates/queen.png", timeout=2)
#     warden_found = wait_for_template("templates/warden.png", timeout=2)
#     royal_champion_found = wait_for_template("templates/royal_champion.png", timeout=2)
#     siege_found = wait_for_template("templates/siege_barracks.png", timeout=2)
#     baby_dragon_found = wait_for_template("templates/baby_dragon.png", timeout=2)
#     rage_found = wait_for_template("templates/rage.png", timeout=2)

#     # Step 3: Tap on the troops if found.
#     if valk_found:
#         print("Found Valkyrie at:", valk_found)
#         adb_tap(valk_found[0], valk_found[1])
#         time.sleep(random.uniform(0.5, 1))
#     else:
#         print("Valkyrie not found.")
#         adb_tap(COORDS["valk_select_fallbackv2"][0], COORDS["valk_select_fallbackv2"][1])
#         time.sleep(random.uniform(0.3, 0.7))

#     adb_tap(COORDS["valk_drop_bottom_leftv2"][0], COORDS["valk_drop_bottom_leftv2"][1])
#     time.sleep(random.uniform(0.3, 0.7))
#     adb_tap(COORDS["valk_drop_top_middlev2"][0], COORDS["valk_drop_top_middlev2"][1])
#     time.sleep(random.uniform(0.3, 0.7))

    
#     if king_found:
#         print("Found King at:", king_found)
#         adb_tap(king_found[0], king_found[1])
#         time.sleep(random.uniform(0.15, 0.4))
#         adb_tap(COORDS["midpoint_dropv2"][0], COORDS["midpoint_dropv2"][1])
#         time.sleep(random.uniform(0.15, 0.25))

#     if queen_found:
#         print("Found Queen at:", queen_found)
#         adb_tap(queen_found[0], queen_found[1])
#         time.sleep(random.uniform(0.2, 0.4))
#         adb_tap(COORDS["midpoint_dropv2"][0], COORDS["midpoint_dropv2"][1])
#         time.sleep(random.uniform(0.2, 0.4))

#     if warden_found:
#         print("Found Warden at:", warden_found)
#         adb_tap(warden_found[0], warden_found[1])
#         time.sleep(random.uniform(0.2, 0.4))
#         adb_tap(COORDS["midpoint_dropv2"][0], COORDS["midpoint_dropv2"][1])
#         time.sleep(random.uniform(0.2, 0.3))

#     if royal_champion_found:
#         print("Found Royal Champion at:", royal_champion_found)
#         adb_tap(royal_champion_found[0], royal_champion_found[1])
#         time.sleep(random.uniform(0.1, 0.4))
#         adb_tap(COORDS["midpoint_dropv2"][0], COORDS["midpoint_dropv2"][1])
#         time.sleep(random.uniform(0.15, 0.25))

#     if valk_found:
#         print("Found Valkyrie at:", valk_found)
#         adb_tap(valk_found[0], valk_found[1])
#         time.sleep(random.uniform(0.2, 0.4))
#     else:
#         print("Valkyrie not found.")
#         adb_tap(COORDS["valk_select_fallbackv2"][0], COORDS["valk_select_fallbackv2"][1])
#         time.sleep(random.uniform(0.2, 0.4))

#     for _ in range(random.randint(5, 9)):
#         adb_tap(COORDS["midpoint_dropv2"][0], COORDS["midpoint_dropv2"][1])
#         time.sleep(random.uniform(0.2, 0.3))

#     if warden_found:
#         print("Found Warden at:", warden_found)
#         time.sleep(random.uniform(0.5, 1))
#         adb_tap(warden_found[0], warden_found[1])
#         time.sleep(random.uniform(0.2, 0.4))
    
#     if king_found:
#         print("Found King at:", king_found)
#         adb_tap(king_found[0], king_found[1])
#         time.sleep(random.uniform(0.2, 0.4))

#     if baby_dragon_found:
#         print("Found Baby Dragon at:", baby_dragon_found)
#         adb_tap(baby_dragon_found[0], baby_dragon_found[1])
#         time.sleep(random.uniform(0.2, 0.4))
#         adb_tap(COORDS["valk_drop_bottom_leftv2"][0], COORDS["valk_drop_bottom_leftv2"][1])
#         time.sleep(random.uniform(0.2, 0.4))
    
#     if siege_found:
#         print("Found Siege Barracks at:", siege_found)
#         adb_tap(siege_found[0], siege_found[1])
#         time.sleep(random.uniform(0.2, 0.4))
#         adb_tap(COORDS["valk_drop_top_middlev2"][0], COORDS["valk_drop_top_middlev2"][1])

#     time.sleep(random.uniform(9, 11))

#     # human_swipe_up(COORDS["scroll_up_start"])

#     # Step 4: Tap on the rage spell.
#     if rage_found:
#         print("Found Rage spell at:", rage_found)
#         adb_tap(rage_found[0], rage_found[1])
#         time.sleep(random.uniform(0.3, 0.6))
#         adb_tap(COORDS["rage_fallback1v2"][0], COORDS["rage_fallback1v2"][1])
#         time.sleep(random.uniform(0.5, 0.8))
#         adb_tap(COORDS["rage_fallback2v2"][0], COORDS["rage_fallback2v2"][1])
#         time.sleep(random.uniform(0.3, 0.6))
#         adb_tap(COORDS["rage_fallback3v2"][0], COORDS["rage_fallback3v2"][1])
#         time.sleep(random.uniform(2, 4))
#         adb_tap(rage_found[0], rage_found[1])
#         adb_tap(COORDS["rage_fallback4v2"][0], COORDS["rage_fallback4v2"][1])
#         time.sleep(random.uniform(0.5, 1))
#         adb_tap(COORDS["rage_fallback5v2"][0], COORDS["rage_fallback5v2"][1])
     

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
                time.sleep(random.uniform(0, 1))
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
        timeout = 240
        start_time = time.time()
        while time.time() - start_time < timeout:
            ret_home = wait_for_template("templates/return_home.png", timeout=3)
            if ret_home:
                print("Return home detected at:", ret_home)
                time.sleep(random.uniform(0.5, 1))
                for _ in range(random.randint(2, 2)):
                    jitter_x = random.randint(-50, 50)
                    jitter_y = random.randint(-50, 50)
                    adb_tap(ret_home[0] + jitter_x, ret_home[1] + jitter_y)
                    time.sleep(random.uniform(0.2, 0.3))
                break
            time.sleep(1)
        else:
            print("Timeout waiting for return home.")
            jitter_x = random.randint(-100, 100)
            jitter_y = random.randint(-20, 20)
            adb_tap(217 + jitter_x, 803 + jitter_y)

    print("Main loop finished.")

if __name__ == "__main__":
    main()
