import random
import time
from image_utils import read_trophies
from game_actions import drop_trophies, find_attack
from adb_utils import adb_tap
from image_utils import wait_for_template

def main():
    iterations = random.randint(25, 35)
    print(f"Starting main loop for {iterations} iterations.")
    for i in range(iterations):
        print(f"AHHHHHH WE ARE ABOUT TO TEST TROPHIES")
        trophies = read_trophies()
        if trophies is not None:
            print(f"Current Trophies: {trophies}")
            if trophies > 4600 and trophies < 5200:
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
    print("Main loop finished.")

if __name__ == "__main__":
    main()
