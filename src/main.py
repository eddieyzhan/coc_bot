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
        attack_btn = wait_for_template("templates/attack_button.png", timeout=10)
        trophies = read_trophies()
        print(f"Current Trophies: {trophies}")
        if trophies is not None:
            print(f"Current Trophies: {trophies}")
            if trophies > 4600 and trophies < 5200:
                drop_trophies()
                time.sleep(random.uniform(0, 1))
                continue
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
                for _ in range(random.randint(1, 2)):
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