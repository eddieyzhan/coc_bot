import random
import time
import threading
import sys
from image_utils import read_trophies
from game_actions import drop_trophies, find_attack
from adb_utils import adb_tap
from image_utils import wait_for_template

def get_user_input_with_timeout(prompt, timeout=10):
    """Get user input with a timeout, compatible with Windows."""
    print(prompt)
    print(f"You have {timeout} seconds to respond before a default value is chosen...")
    
    user_input = [None]
    input_thread = threading.Thread(target=get_input, args=(user_input,))
    input_thread.daemon = True
    input_thread.start()
    input_thread.join(timeout)
    
    if user_input[0] is None:
        print("\nNo input received within the timeout period.")
        return None
    return user_input[0]

def get_input(result_list):
    """Helper function to get input in a separate thread."""
    result_list[0] = input()

def force_drop_mode():
    """Function to handle the force drop mode."""
    iterations_input = get_user_input_with_timeout("How many trophy drop iterations? (Enter a number):")
    
    if iterations_input and iterations_input.isdigit():
        iterations = int(iterations_input)
    else:
        iterations = random.randint(10, 20)
        print(f"Using random iterations: {iterations}")
    
    print(f"Starting trophy drop for {iterations} iterations.")
    for i in range(iterations):
        print(f"\nDrop iteration {i+1}/{iterations}")
        drop_trophies()
    print("Trophy dropping complete.")

def force_loot_mode():
    """Function to handle the force loot mode."""
    iterations_input = get_user_input_with_timeout("How many loot iterations? (Enter a number):")
    
    if iterations_input and iterations_input.isdigit():
        iterations = int(iterations_input)
    else:
        iterations = random.randint(5, 15)
        print(f"Using random iterations: {iterations}")
    
    print(f"Starting loot mode for {iterations} iterations.")
    for i in range(iterations):
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
    
    print("Loot mode complete.")

def normal_mode():
    """Function to handle the normal mode."""
    iterations = random.randint(25, 35)
    print(f"Starting main loop for {iterations} iterations.")
    for i in range(iterations):
        
        attack_btn = wait_for_template("templates/attack_button.png", timeout=10)
        trophies = read_trophies()
        if trophies is not None:
            print(f"Current Trophies: {trophies}")
            if trophies > 4850 and trophies < 5200:
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

    print("Main loop finished.")

def legends_mode():
    """Function to handle the legends mode."""
    # Currently equivalent to normal mode
    normal_mode()

def main():
    """Main function that prompts for mode selection and runs the appropriate mode."""
    print("=== Clash of Clans Auto-Farming Tool ===")
    print("Please select a mode:")
    print("1. force_drop - Force trophy dropping")
    print("2. force_loot - Force looting without trophy checks")
    print("3. normal - Normal mode with trophy checks")
    print("4. legends - Legends mode (currently same as normal)")
    
    mode_input = get_user_input_with_timeout("Enter mode (1-4 or mode name):", 20)
    
    # Process the input to determine the mode
    if mode_input:
        mode_input = mode_input.lower()
        if mode_input in ["1", "force_drop"]:
            print("Selected mode: Force Drop")
            force_drop_mode()
        elif mode_input in ["2", "force_loot"]:
            print("Selected mode: Force Loot")
            force_loot_mode()
        elif mode_input in ["3", "normal"]:
            print("Selected mode: Normal")
            normal_mode()
        elif mode_input in ["4", "legends"]:
            print("Selected mode: Legends")
            legends_mode()
        else:
            print("Invalid selection. Defaulting to Normal mode.")
            normal_mode()
    else:
        print("No selection made. Defaulting to Normal mode.")
        normal_mode()

if __name__ == "__main__":
    main()