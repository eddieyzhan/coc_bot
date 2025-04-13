import time
import random
from adb_utils import adb_tap, adb_swipe, capture_screen
from image_utils import wait_for_template, find_template
from coordinates import COORDS

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
        right_x = random.randint(400, 455)
        mid_x = random.randint(260, 300)
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

def drop_trophies():
    iterations = random.randint(25, 45)
    print(f"Starting trophy drop for {iterations} iterations.")
    for i in range(iterations):
        print(f"\nIteration {i+1}/{iterations}")
        find_attack(True)
        print("Waiting for 'return home' indicator...")
        timeout = 180
        start_time = time.time()
        while time.time() - start_time < timeout:
            ret_home = wait_for_template("../templates/return_home.png", timeout=3)
            if ret_home:
                print("Return home detected at:", ret_home)
                time.sleep(random.uniform(0.5, 1))
                for _ in range(random.randint(2, 3)):
                    jitter_x = random.randint(-50, 50)
                    jitter_y = random.randint(-50, 50)
                    adb_tap(ret_home[0] + jitter_x, ret_home[1] + jitter_y)
                    time.sleep(random.uniform(0.75, 1))
                time.sleep(random.uniform(0.5, 1))
                break
            time.sleep(1)
        else:
            print("Timeout waiting for return home.")

def find_attack(drop=False):
    while True:
        time.sleep(random.uniform(0, 1))
        print("Searching for 'attack' button...")
        attack_btn = wait_for_template("../templates/attack_button.png", timeout=10)
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
        match_btn = wait_for_template("../templates/find_match.png", timeout=3)
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
            next_btn = wait_for_template("../templates/next_button.png", timeout=20)
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

    next_btn = wait_for_template("../templates/next_button.png", timeout=15)

    print("Capturing hero positions dynamically...")
    king_found = wait_for_template("../templates/king.png", timeout=3)

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
    
    surrender = wait_for_template("../templates/surrender.png", timeout=5)
    
    if surrender:
        print("Found Surrender button at:", surrender)
        jitter_x = random.randint(-100, 100)
        jitter_y = random.randint(-20, 20)
        adb_tap(surrender[0] + jitter_x, surrender[1] + jitter_y)
        time.sleep(random.uniform(0, 1))

        okay = wait_for_template("../templates/okay.png", timeout=5)
        if okay:
            print("Found Okay button at:", okay)
            time.sleep(random.uniform(0, 1.5))
            for _ in range(random.randint(1, 2)):
                jitter_x = random.randint(-50, 50)
                jitter_y = random.randint(-20, 20)
                adb_tap(okay[0] + jitter_x, okay[1] + jitter_y)
                time.sleep(random.uniform(0.25, 0.4))
    else:
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
    
    next_btn = wait_for_template("../templates/next_button.png", timeout=15)

    # Step 2: Dynamically search for hero templates.
    print("Capturing hero positions dynamically...")
    valk_found = wait_for_template("../templates/valk.png", timeout=2)
    king_found = wait_for_template("../templates/king.png", timeout=2)
    queen_found = wait_for_template("../templates/queen.png", timeout=2)
    warden_found = wait_for_template("../templates/warden.png", timeout=2)
    royal_champion_found = wait_for_template("../templates/royal_champion.png", timeout=2)
    siege_found = wait_for_template("../templates/siege_barracks.png", timeout=2)
    baby_dragon_found = wait_for_template("../templates/baby_dragon.png", timeout=2)
    rage_found = wait_for_template("../templates/rage.png", timeout=2)

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
