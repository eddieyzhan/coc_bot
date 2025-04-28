import random
import time
from image_utils import read_trophies
from game_actions import drop_trophies, find_attack
from adb_utils import adb_tap
from image_utils import wait_for_template
from modes import get_user_input_with_timeout, force_drop_mode, force_loot_mode, normal_mode, legends_mode

def main():
    """Main function that prompts for mode selection and runs the appropriate mode."""
    print("=== Clash of Clans Auto-Farming Tool ===")
    print("Please select a mode:")
    print("1. Force_drop - Force trophy dropping")
    print("2. Force_loot - Force looting without trophy checks")
    print("3. Normal - Normal mode with trophy checks")
    print("4. Legends - Legends mode (currently same as normal)")
    
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