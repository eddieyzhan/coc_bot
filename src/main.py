import random
import time
from image_utils import read_trophies
from game_actions import drop_trophies, find_attack, drop_attack, return_home
from adb_utils import adb_tap
from image_utils import wait_for_template

"""def main():
    iterations = random.randint(25, 35)
    print(f"Starting main loop for {iterations} iterations.")
    for i in range(iterations):
        attack_btn = wait_for_template("templates/attack_button.png", timeout=10)
        trophies = read_trophies()
        print(f"Current Trophies: {trophies}")
        if trophies is not None:
            print(f"Current Trophies: {trophies}")
            if trophies > 4700 and trophies < 5200:
                drop_trophies()
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
        timeout = 180
        start_time = time.time()
        while time.time() - start_time < timeout:
            ret_home = wait_for_template("templates/return_home.png", timeout=3)
            if ret_home:
                print("Return home detected at:", ret_home)
                time.sleep(random.uniform(0.1, 0.5))
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

    print("Main loop finished.")"""

def main():
    # check trophies
    trophies = read_trophies()
    if trophies is None:
        print("Error reading trophies!")
        return
    print(f"Current Trophies: {trophies}")

    if trophies > 4970 and trophies < 5000:
        print("Starting drop strategy...")
        # Drop strategy: Attack until trophies are below 4920
        while trophies > 4915:
            find_attack(True)
            time.sleep(0.5)
            return_home()
            time.sleep(0.5)
            #WAIT FOR THE ATT BUTTON TO APPEAR
            wait_for_template("templates/attack_button.png", timeout=10)
            time.sleep(0.5)
            #check trophies again
            trophies = read_trophies()
            print(f"Current Trophies: {trophies}")
            if trophies < 4920:
                print("Trophies are low, stopping drop strategy.")
                break
    
    elif trophies > 4900 and trophies < 4970:
            print("Starting attack loop...")
            find_attack(False)
            time.sleep(0.5)
            return_home()
            time.sleep(0.5)
    else:
        print("misread detected")
        return    
    
if __name__ == "__main__":
    main()