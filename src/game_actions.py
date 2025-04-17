import time
import random
from adb_utils import adb_tap, capture_screen
from image_utils import wait_for_template, find_template
from coordinates import COORDS

def jitter_coord(x, y, jitter_range=10):
    return x + random.randint(-jitter_range, jitter_range), y + random.randint(-jitter_range, jitter_range)

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

    adb_tap(1500 + random.randint(-7, 7), 970 + random.randint(-7, 7))

    time.sleep(random.uniform(0.2, 0.5))
    
    adb_tap(random.randint(1000, 1700), random.randint(100, 400))

    time.sleep(random.uniform(0.3, 0.7))

    jitter_x = random.randint(-50, 50)
    jitter_y = random.randint(-20, 20)
    adb_tap(140 + jitter_x, 805 + jitter_y)

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
    
    next_btn = wait_for_template("templates/next_button.png", timeout=15)

    jitter_x = random.randint(-40, 40)
    jitter_y = random.randint(-40, 40)

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
        for x, y in [(1013, 307), (1035, 513), (1055, 689), (1409, 477), (1421, 679)]:
            adb_tap(x + random.randint(-7, 7) + 15, y + random.randint(-7, 7))
            time.sleep(random.uniform(0.3, 0.6))

    elif attack_strat == 3:


        # Wait 18–21 seconds
        time.sleep(random.uniform(9, 12))
        adb_tap(*jitter_coord(1513, 970))

        # Rage drop at 3 new locations
        for x, y in [(1258, 270), (1380, 483), (1408, 685), (900, 400), (980, 600)]:
            adb_tap(x + random.randint(-7, 7) - 40 , y + random.randint(-7, 7))
            time.sleep(random.uniform(0.3, 0.6))