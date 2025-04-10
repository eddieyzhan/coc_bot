# coc_bot.py
import subprocess
import time
import random
import cv2
import numpy as np

# --- Utility Functions ---

def adb_tap(x, y, jitter=15):
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

def human_swipe(base_start):
    """
    Performs a swipe gesture with randomized starting and ending points.
    
    - The starting point is randomized within a ±200 pixel offset from the given base_start.
    - The ending point is computed relative to the randomized start:
        • The y-difference (vertical movement) is randomly chosen between 210 and 280 pixels.
        • The x-difference is randomized within ±200 pixels.
    
    Executes the swipe as a single ADB command.
    """
    # Randomize starting point within a ±200 pixel radius of base_start
    start_x = base_start[0] + random.randint(-200, 200)
    start_y = base_start[1] + random.randint(-200, 200)
    
    # Determine end point:
    # The vertical (y) difference is in the range [210, 280]
    # The horizontal (x) difference is randomized within ±200 pixels
    end_x = start_x + random.randint(-200, 200)
    end_y = start_y + random.randint(200, 240)

    total_duration = random.randint(400, 700)
    
    # Execute a single ADB swipe command with the randomized coordinates
    adb_swipe(start_x, start_y, end_x, end_y, duration=total_duration)

def human_swipe_up(base_start):
    """
    Performs a swipe gesture with randomized starting and ending points.
    
    - The starting point is randomized within a ±200 pixel offset from the given base_start.
    - The ending point is computed relative to the randomized start:
        • The y-difference (vertical movement) is randomly chosen between 210 and 280 pixels.
        • The x-difference is randomized within ±200 pixels.
    
    Executes the swipe as a single ADB command.
    """
    # Randomize starting point within a ±200 pixel radius of base_start
    start_x = base_start[0] + random.randint(-200, 200)
    start_y = base_start[1] + random.randint(-200, 200)
    
    # Determine end point:
    # The vertical (y) difference is in the range [210, 280]
    # The horizontal (x) difference is randomized within ±200 pixels
    end_x = start_x + random.randint(-200, 200)
    end_y = start_y - random.randint(210, 280)

    total_duration = random.randint(300, 500)
    
    # Execute a single ADB swipe command with the randomized coordinates
    adb_swipe(start_x, start_y, end_x, end_y, duration=total_duration)


# --- COORDS Dictionary ---
# Use fallback coordinates if dynamic template detection fails.
COORDS = {
    "zoom_out_start": (1130, 310),
    "zoom_out_end": (1090, 525),


    "scroll_down_start": (1130, 310),
    "scroll_down_end": (1090, 525),

    "midpoint_drop": (634, 367),

    "valk_select_fallback": (457, 967),
    "valk_drop_bottom_left": (139, 737),
    "valk_drop_top_middle": (1018, 56),


    "midpoint_dropv2": (1748, 372),
    "valk_drop_bottom_leftv2": (1100, 46),
    "valk_drop_top_middlev2": (2100, 742),

    "rage_fallback1": (1432, 300),
    "rage_fallback2": (1120, 470),
    "rage_fallback3": (967, 650),
    "rage_fallback4": (1300, 500),
    "rage_fallback5": (1000, 670),

    "rage_fallback1v2": (860, 271),
    "rage_fallback2v2": (1110, 470),
    "rage_fallback3v2": (1312, 590),
    "rage_fallback4v2": (766, 482),
    "rage_fallback5v2": (1100, 683),

}

# --- Bot Functions ---

def find_attack():
    print("Searching for 'attack' button...")
    attack_btn = wait_for_template("templates/attack_button.png", timeout=3)
    if attack_btn:
        print("Found attack button at:", attack_btn)
        jitter_x = random.randint(-50, 50)
        jitter_y = random.randint(-50, 50)
        adb_tap(attack_btn[0] + jitter_x, attack_btn[1] + jitter_y)

        time.sleep(random.uniform(0.5, 3))
    else:
        print("Attack button not found within 3 seconds.")

    print("Searching for 'find match' button...")
    match_btn = wait_for_template("templates/find_match.png", timeout=3)
    if match_btn:
        print("Found 'find match' button at:", match_btn)
        for _ in range(random.randint(1, 3)):
            jitter_x = random.randint(-50, 50)
            jitter_y = random.randint(-50, 50)
            adb_tap(match_btn[0] + jitter_x, match_btn[1] + jitter_y)
            time.sleep(random.uniform(0.2, 0.3))
        time.sleep(random.uniform(0.5, 2))
    else:
        print("Find match button not found within 3 seconds.")


    # Randomly click the 'next' button 0 to 5 times.
    clicks = random.randint(0, 2)
    for _ in range(clicks):
        next_btn = wait_for_template("templates/next_button.png", timeout=20)
        if next_btn:
            print("Clicking next button at:", next_btn)
            for _ in range(random.randint(1, 5)):
                jitter_x = random.randint(-50, 50)
                jitter_y = random.randint(-50, 50)
                adb_tap(next_btn[0] + jitter_x, next_btn[1] + jitter_y)
                time.sleep(random.uniform(0.2, 0.3))
            time.sleep(random.uniform(1, 2))
        else:
            print("Next button not found within 20 seconds.")
            break
    
    time.sleep(random.uniform(10, 15))
    # Proceed to the attack phase.
    attack_strat = random.randint(1, 2)
    if attack_strat == 1:
        print("Using attack strategy 1.")
        attack()
    else:
        print("Using attack strategy 2.")
        attack2()

def attack():
    print("Starting attack sequence...")

    # Step 1: Slight scroll down using human-like random swipe.
    print("Scrolling down slightly...")
    human_swipe(COORDS["scroll_down_start"])

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

    adb_tap(COORDS["valk_drop_bottom_left"][0], COORDS["valk_drop_bottom_left"][1])
    time.sleep(random.uniform(0.5, 0.7))
    adb_tap(COORDS["valk_drop_top_middle"][0], COORDS["valk_drop_top_middle"][1])
    time.sleep(random.uniform(0.5, 0.7))

    
    if king_found:
        print("Found King at:", king_found)
        adb_tap(king_found[0], king_found[1])
        time.sleep(random.uniform(0.15, 0.4))
        adb_tap(COORDS["midpoint_drop"][0], COORDS["midpoint_drop"][1])
        time.sleep(random.uniform(0.15, 0.25))

    if queen_found:
        print("Found Queen at:", queen_found)
        adb_tap(queen_found[0], queen_found[1])
        time.sleep(random.uniform(0.2, 0.4))
        adb_tap(COORDS["midpoint_drop"][0], COORDS["midpoint_drop"][1])
        time.sleep(random.uniform(0.2, 0.4))

    if warden_found:
        print("Found Warden at:", warden_found)
        adb_tap(warden_found[0], warden_found[1])
        time.sleep(random.uniform(0.2, 0.4))
        adb_tap(COORDS["midpoint_drop"][0], COORDS["midpoint_drop"][1])
        time.sleep(random.uniform(0.2, 0.3))

    if royal_champion_found:
        print("Found Royal Champion at:", royal_champion_found)
        adb_tap(royal_champion_found[0], royal_champion_found[1])
        time.sleep(random.uniform(0.1, 0.4))
        adb_tap(COORDS["midpoint_drop"][0], COORDS["midpoint_drop"][1])
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
        adb_tap(COORDS["midpoint_drop"][0], COORDS["midpoint_drop"][1])
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
        adb_tap(COORDS["valk_drop_bottom_left"][0], COORDS["valk_drop_bottom_left"][1])
        time.sleep(random.uniform(0.2, 0.4))
    
    if siege_found:
        print("Found Siege Barracks at:", siege_found)
        adb_tap(siege_found[0], siege_found[1])
        time.sleep(random.uniform(0.2, 0.4))
        adb_tap(COORDS["valk_drop_top_middle"][0], COORDS["valk_drop_top_middle"][1])

    time.sleep(random.uniform(13, 18))

    human_swipe_up(COORDS["scroll_down_start"])

    # Step 4: Tap on the rage spell.
    if rage_found:
        print("Found Rage spell at:", rage_found)
        adb_tap(rage_found[0], rage_found[1])
        time.sleep(random.uniform(0.3, 0.6))
        adb_tap(COORDS["rage_fallback1"][0], COORDS["rage_fallback1"][1])
        time.sleep(random.uniform(0.5, 0.8))
        adb_tap(COORDS["rage_fallback2"][0], COORDS["rage_fallback2"][1])
        time.sleep(random.uniform(0.3, 0.6))
        adb_tap(COORDS["rage_fallback3"][0], COORDS["rage_fallback3"][1])
        time.sleep(random.uniform(2, 4))
        adb_tap(rage_found[0], rage_found[1])
        adb_tap(COORDS["rage_fallback4"][0], COORDS["rage_fallback4"][1])
        time.sleep(random.uniform(0.5, 1))
        adb_tap(COORDS["rage_fallback5"][0], COORDS["rage_fallback5"][1])

def attack2():
    print("Starting attack sequence...")

    # Step 1: Slight scroll down using human-like random swipe.
    print("Scrolling down slightly...")
    human_swipe(COORDS["scroll_down_start"])

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
        adb_tap(COORDS["valk_select_fallbackv2"][0], COORDS["valk_select_fallbackv2"][1])
        time.sleep(random.uniform(0.3, 0.7))

    adb_tap(COORDS["valk_drop_bottom_leftv2"][0], COORDS["valk_drop_bottom_leftv2"][1])
    time.sleep(random.uniform(0.3, 0.7))
    adb_tap(COORDS["valk_drop_top_middlev2"][0], COORDS["valk_drop_top_middlev2"][1])
    time.sleep(random.uniform(0.3, 0.7))

    
    if king_found:
        print("Found King at:", king_found)
        adb_tap(king_found[0], king_found[1])
        time.sleep(random.uniform(0.15, 0.4))
        adb_tap(COORDS["midpoint_dropv2"][0], COORDS["midpoint_dropv2"][1])
        time.sleep(random.uniform(0.15, 0.25))

    if queen_found:
        print("Found Queen at:", queen_found)
        adb_tap(queen_found[0], queen_found[1])
        time.sleep(random.uniform(0.2, 0.4))
        adb_tap(COORDS["midpoint_dropv2"][0], COORDS["midpoint_dropv2"][1])
        time.sleep(random.uniform(0.2, 0.4))

    if warden_found:
        print("Found Warden at:", warden_found)
        adb_tap(warden_found[0], warden_found[1])
        time.sleep(random.uniform(0.2, 0.4))
        adb_tap(COORDS["midpoint_dropv2"][0], COORDS["midpoint_dropv2"][1])
        time.sleep(random.uniform(0.2, 0.3))

    if royal_champion_found:
        print("Found Royal Champion at:", royal_champion_found)
        adb_tap(royal_champion_found[0], royal_champion_found[1])
        time.sleep(random.uniform(0.1, 0.4))
        adb_tap(COORDS["midpoint_dropv2"][0], COORDS["midpoint_dropv2"][1])
        time.sleep(random.uniform(0.15, 0.25))

    if valk_found:
        print("Found Valkyrie at:", valk_found)
        adb_tap(valk_found[0], valk_found[1])
        time.sleep(random.uniform(0.2, 0.4))
    else:
        print("Valkyrie not found.")
        adb_tap(COORDS["valk_select_fallbackv2"][0], COORDS["valk_select_fallbackv2"][1])
        time.sleep(random.uniform(0.2, 0.4))

    for _ in range(random.randint(5, 9)):
        adb_tap(COORDS["midpoint_dropv2"][0], COORDS["midpoint_dropv2"][1])
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
        adb_tap(COORDS["valk_drop_bottom_leftv2"][0], COORDS["valk_drop_bottom_leftv2"][1])
        time.sleep(random.uniform(0.2, 0.4))
    
    if siege_found:
        print("Found Siege Barracks at:", siege_found)
        adb_tap(siege_found[0], siege_found[1])
        time.sleep(random.uniform(0.2, 0.4))
        adb_tap(COORDS["valk_drop_top_middlev2"][0], COORDS["valk_drop_top_middlev2"][1])

    time.sleep(random.uniform(8, 13))

    human_swipe_up(COORDS["scroll_down_start"])

    # Step 4: Tap on the rage spell.
    if rage_found:
        print("Found Rage spell at:", rage_found)
        adb_tap(rage_found[0], rage_found[1])
        time.sleep(random.uniform(0.3, 0.6))
        adb_tap(COORDS["rage_fallback1v2"][0], COORDS["rage_fallback1v2"][1])
        time.sleep(random.uniform(0.5, 0.8))
        adb_tap(COORDS["rage_fallback2v2"][0], COORDS["rage_fallback2v2"][1])
        time.sleep(random.uniform(0.3, 0.6))
        adb_tap(COORDS["rage_fallback3v2"][0], COORDS["rage_fallback3v2"][1])
        time.sleep(random.uniform(2, 4))
        adb_tap(rage_found[0], rage_found[1])
        adb_tap(COORDS["rage_fallback4v2"][0], COORDS["rage_fallback4v2"][1])
        time.sleep(random.uniform(0.5, 1))
        adb_tap(COORDS["rage_fallback5v2"][0], COORDS["rage_fallback5v2"][1])
     

def main():
    iterations = random.randint(25, 35)
    print(f"Starting main loop for {iterations} iterations.")
    for i in range(iterations):
        print(f"\nIteration {i+1}/{iterations}")
        time.sleep(random.uniform(1, 3))
        find_attack()
        print("Waiting for 'return home' indicator...")
        timeout = 180
        start_time = time.time()
        while time.time() - start_time < timeout:
            ret_home = wait_for_template("templates/return_home.png", timeout=3)
            if ret_home:
                print("Return home detected at:", ret_home)
                for _ in range(random.randint(1, 3)):
                    jitter_x = random.randint(-50, 50)
                    jitter_y = random.randint(-50, 50)
                    adb_tap(ret_home[0] + jitter_x, ret_home[1] + jitter_y)
                    time.sleep(random.uniform(0.2, 0.3))
                time.sleep(random.uniform(0.5, 1))
                break
            time.sleep(1)
        else:
            print("Timeout waiting for return home.")
        time.sleep(random.uniform(1, 10))
    print("Main loop finished.")

if __name__ == "__main__":
    main()
