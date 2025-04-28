import time
import random
import math
from adb_utils import adb_tap, capture_screen
from image_utils import wait_for_template, find_template, read_percentage, read_ressources
from coordinates import COORDS, CORDS

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

def return_home():
    print("Waiting for 'return home' indicator...")
    timeout = 240
    start_time = time.time()
    while time.time() - start_time < timeout:
        percentage = read_percentage()
        if percentage is not None:
            if percentage >= 85:
                print("end is near, returning home...stopping")
                adb_tap(205, 845, 20)
                print("Checking for okay button...")
                okay = wait_for_template("templates/okay.png", timeout=5)
                if okay:
                    print("Found Okay button at:", okay)
                    adb_tap(okay[0], okay[1], 20)
        ret_home = wait_for_template("templates/return_home.png", timeout=3)
        if ret_home:
            print("Return home detected at:", ret_home)
            adb_tap(ret_home[0], ret_home[1], 50)
            break
        time.sleep(1)
    else:
        print("Timeout waiting for return home.")
        jitter_x = random.randint(-100, 100)
        jitter_y = random.randint(-20, 20)
        adb_tap(217 + jitter_x, 803 + jitter_y)

"""def drop_trophies():
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
            print("Timeout waiting for return home.")"""


"""def find_attack(drop=False):
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

        break"""

#this find_attack function is used to find a target with at least the targeted amount of ressources
def find_attack(drop):
    print("Searching for 'attack' button...")
    attack_btn = wait_for_template("templates/attack_button.png", timeout=10)
    if attack_btn:
        print("Found attack button at:", attack_btn)
        adb_tap(attack_btn[0], attack_btn[1], 50)
    else:
        print("Attack button not found within 10 seconds. backup")
        adb_tap(218, 947, 60)

    print("Searching for 'find match' button...")
    match_btn = wait_for_template("templates/find_match.png", timeout=3)
    if match_btn:
        print("Found 'find match' button at:", match_btn)
        adb_tap(match_btn[0], match_btn[1], 70)
    else:
        print("Find match button not found within 3 seconds.")
        # Restart the loop if this part fails.
        adb_tap(218, 947, 60)
        okay = wait_for_template("templates/okay.png", timeout=5)
        if okay:
            print("Found Okay button at:", okay)
            time.sleep(random.uniform(0, 1.5))
            for _ in range(random.randint(1, 2)):
                jitter_x = random.randint(-50, 50)
                jitter_y = random.randint(-20, 20)
                adb_tap(okay[0] + jitter_x, okay[1] + jitter_y)
        return
    
    if drop==True:
        drop_attack()
        return
    
    if drop==False:
        while True:   
            if random.randint(0, 1):
                time.sleep(random.uniform(0.5, 1))
                for _ in range(random.randint(1, 2)):
                    random_x = random.randint(600, 1200)
                    random_y = random.randint(100, 500)
                    adb_tap(random_x, random_y)
                    time.sleep(random.uniform(0.5, 1))
            #wait for the next button to appear
            print("Waiting for 'next' button...")
            next_btn = wait_for_template("templates/next_button.png", timeout=15)
            if next_btn:
                print("Found next button at:", next_btn)
                ressources = read_ressources()
                if ressources is not None:
                    if ressources > 1500000:
                        print("ressources are enough")
                        attack()
                        break
                    else:
                        print("ressources are low")
                        adb_tap(next_btn[0], next_btn[1], 50)

"""def drop_attack():
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
            time.sleep(random.uniform(0.25, 0.4))"""

# simplified drop_attack function
def drop_attack():
    drop_cord_x = 240
    drop_cord_y = 510
    print("Capturing king position dynamically...")
    king_found = wait_for_template("templates/king.png", timeout=10)
    if king_found:
        print("Found King at:", king_found)
        adb_tap(king_found[0], king_found[1])
        time.sleep(random.uniform(0.75, 1.5))
        print("Dropping King")
        adb_tap(drop_cord_x, drop_cord_y, 30)
    print("searching for 'surrender' button...")
    surrender = wait_for_template("templates/surrender.png", timeout=5)
    if surrender:
        print("Found Surrender button at:", surrender)
        jitter_x = random.randint(-100, 100)
        jitter_y = random.randint(-20, 20)
        adb_tap(surrender[0] + jitter_x, surrender[1] + jitter_y)
    else:
        print("Surrender button not found, pressing backup end battle button")
        jitter_x = random.randint(-100, 100)
        jitter_y = random.randint(-20, 20)
        adb_tap(217 + jitter_x, 803 + jitter_y)
    print("searching for 'okay' button...")
    okay = wait_for_template("templates/okay.png", timeout=5)
    if okay:
        print("Found Okay button at:", okay)
        time.sleep(random.uniform(0, 1.5))
        for _ in range(random.randint(1, 2)):
            jitter_x = random.randint(-50, 50)
            jitter_y = random.randint(-20, 20)
            adb_tap(okay[0] + jitter_x, okay[1] + jitter_y)

"""def attack():
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
            time.sleep(random.uniform(0.3, 0.6))"""

def attack():
    #THIS ARMY USES ONLY THE 4 HEROS, 1 SIEGE, 2 APPRENTICES, 5 VALKS and FULL SKELETON SPELLS
    print("Starting attack sequence...")
    # Step 1: Randomly select an attack strategy (1 or 2). 1 for right side, 2 for left side.
    attack_strat = random.randint(1, 2)
    if attack_strat == 1:
        cord1x = CORDS["RIGHT"][0]
        cord1y = CORDS["RIGHT"][1]
        cord2x = CORDS["TOPRIGHT"][0]
        cord2y = CORDS["TOPRIGHT"][1]
    else:
        cord1x = CORDS["LEFT"][0]
        cord1y = CORDS["LEFT"][1]
        cord2x = CORDS["TOPLEFT"][0]
        cord2y = CORDS["TOPLEFT"][1]

    # we then deploy KING and QUEEN and siege and 1 apprentice on the random side
    adb_tap(CORDS["spell"][0], CORDS["spell"][1], 30)
    time.sleep(random.uniform(0.75, 1))
    adb_tap(cord1x, cord1y, 30)
    time.sleep(random.uniform(0, 0.5))

    adb_tap(CORDS["king"][0], CORDS["king"][1], 30)
    time.sleep(random.uniform(0.75, 1))
    adb_tap(cord1x, cord1y, 30)
    time.sleep(random.uniform(0, 0.5))

    adb_tap(CORDS["queen"][0], CORDS["queen"][1], 30)
    time.sleep(random.uniform(0.75, 1))
    adb_tap(cord1x, cord1y, 30)
    time.sleep(random.uniform(0, 0.5))

    adb_tap(CORDS["siege"][0], CORDS["siege"][1], 30)
    time.sleep(random.uniform(0.75, 1))
    adb_tap(cord1x, cord1y, 30)
    time.sleep(random.uniform(0, 0.5))

    adb_tap(CORDS["apprentice"][0], CORDS["apprentice"][1], 30)
    time.sleep(random.uniform(0.75, 1))
    adb_tap(cord1x, cord1y, 30)
    time.sleep(random.uniform(0, 0.5))
    
    # then we deploy the rest of the troops on the top of the side
    adb_tap(CORDS["spell"][0], CORDS["spell"][1], 20)
    time.sleep(random.uniform(0.75, 1))
    adb_tap(cord2x, cord2y + 100, 10)
    time.sleep(random.uniform(0, 0.5))

    adb_tap(CORDS["warden"][0], CORDS["warden"][1], 10)
    time.sleep(random.uniform(0.75, 1))
    adb_tap(cord2x, cord2y, 30)
    time.sleep(random.uniform(0, 0.5))

    adb_tap(CORDS["apprentice"][0], CORDS["apprentice"][1], 30)
    time.sleep(random.uniform(0.75, 1))
    adb_tap(cord2x, cord2y, 30)
    time.sleep(random.uniform(0, 0.5))

    adb_tap(CORDS["valk"][0], CORDS["valk"][1], 30)
    time.sleep(random.uniform(0.75, 1))
    for _ in range(0,5):
        adb_tap(cord2x, cord2y, 30)
        time.sleep(random.uniform(0, 0.5))
    time.sleep(random.uniform(0, 0.5))

    adb_tap(CORDS["champion"][0], CORDS["champion"][1], 30)
    time.sleep(random.uniform(0.75, 1))
    adb_tap(cord2x, cord2y, 30)
    time.sleep(random.uniform(5, 7))
    adb_tap(CORDS["warden"][0], CORDS["warden"][1], 30)
    time.sleep(random.uniform(0.75, 1))
    adb_tap(CORDS["spell"][0], CORDS["spell"][1], 30)
    time.sleep(random.uniform(0.75, 1))
    rec_cords = (800, 600)  # Define the area for spell drops
    num_clicks = 9  # Number of clicks to perform / 9 since we used 2 spells before
    # Perform the clicks within the defined rectangle for skeleton spells
    spread_evenly_spells(num_clicks, rec_cords[0], rec_cords[1], 1)

def spread_evenly_spells(num_clicks, width, height, delay=0.1):
  """
  Performs clicks randomly within grid cells covering the rectangle
  to encourage better spatial distribution.

  Args:
    click_func: The function to call for performing a click, accepting x and y.
    num_clicks: The total number of clicks to perform (e.g., 11).
    width: The width of the rectangle (e.g., 800).
    height: The height of the rectangle (e.g., 600).
    delay: Optional delay in seconds between clicks.
  """
  # Determine grid dimensions (aim for roughly num_clicks cells)
  # Try to make the grid squarish
  num_rows = int(math.floor(math.sqrt(num_clicks)))
  num_cols = int(math.ceil(num_clicks / num_rows))

  # Ensure we have at least num_clicks cells, adjust if needed
  while num_rows * num_cols < num_clicks:
      num_cols +=1 # Prioritize adding columns if aspect ratio is wide

  cell_width = width / num_cols
  cell_height = height / num_rows

  # Create a list of all possible grid cell indices (row, col)
  all_cells = [(r, c) for r in range(num_rows) for c in range(num_cols)]

  # Randomly shuffle the cells
  random.shuffle(all_cells)

  # Select the first num_clicks cells from the shuffled list
  selected_cells = all_cells[:num_clicks]

  for i, (row, col) in enumerate(selected_cells):
    # Calculate the boundaries of the current cell
    cell_x_start = col * cell_width
    cell_y_start = row * cell_height
    # Use max(0, ...) and min(width/height - 1, ...) to prevent out-of-bounds
    # due to floating point inaccuracies if using floats directly.
    # randint expects integers.
    min_x = max(0, int(cell_x_start))
    max_x = max(min_x, int(cell_x_start + cell_width) - 1) # Ensure max >= min
    min_y = max(0, int(cell_y_start))
    max_y = max(min_y, int(cell_y_start + cell_height) - 1) # Ensure max >= min

    # Ensure the range is valid (at least one pixel)
    max_x = min(max_x, width - 1)   # Clamp max_x to rectangle bounds
    max_y = min(max_y, height - 1)  # Clamp max_y to rectangle bounds
    if max_x < min_x: max_x = min_x # Handle cases where cell width < 1 pixel
    if max_y < min_y: max_y = min_y # Handle cases where cell height < 1 pixel


    # Generate random coordinates *within* this cell
    random_x = random.randint(min_x, max_x)
    random_y = random.randint(min_y, max_y)

    # Perform the click using the provided function
    adb_tap(800 + random_x, 200 + random_y)

    # Optional delay
    if delay > 0:
        time.sleep(delay)
