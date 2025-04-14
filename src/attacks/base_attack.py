import random
import time
import cv2
import numpy as np
from adb_utils import adb_tap, adb_swipe
from image_utils import wait_for_template, find_template
from coordinates import COORDS

class BaseAttack:
    def __init__(self, strategy_number):
        self.strategy_number = strategy_number
        self.rage_spots = {
            1: ["rage_fallback1", "rage_fallback2", "rage_fallback3"],
            2: ["rage_fallback1v2", "rage_fallback2v2", "rage_fallback3v2"],
            3: ["rage_fallback4v2", "rage_fallback5v2"]
        }

    def get_drop_coords(self):
        if self.strategy_number == 1:
            left_x = random.randint(78, 110)
            right_x = random.randint(480, 514)
            mid_x = random.randint(269, 310)
            left_y = round(-0.8165 * left_x + 542.68)
            right_y = round(-0.8165 * right_x + 542.68)
            mid_y = round(-0.8165 * mid_x + 542.68)
        elif self.strategy_number == 2:
            left_x = random.randint(120, 150)
            right_x = random.randint(400, 455)
            mid_x = random.randint(260, 300)
            left_y = round(0.865 * left_x + 376.2)
            right_y = round(0.865 * right_x + 376.2)
            mid_y = round(0.865 * mid_x + 376.2)
        elif self.strategy_number == 3:
            left_x = random.randint(1755, 1795)
            right_x = random.randint(2270, 2318)
            mid_x = random.randint(1990, 2060)
            left_y = round(0.751 * left_x - 1278.64)
            right_y = round(0.751 * right_x - 1278.64)
            mid_y = round(0.751 * mid_x - 1278.64)
        
        return (left_x, left_y, right_x, right_y, mid_x, mid_y)

    def deploy_hero(self, template_name, drop_x, drop_y):
        hero_pos = wait_for_template(f"../templates/{template_name}.png", timeout=2)
        if hero_pos:
            print(f"Found {template_name} at:", hero_pos)
            adb_tap(hero_pos[0], hero_pos[1])
            time.sleep(random.uniform(0.15, 0.4))
            adb_tap(drop_x, drop_y)
            adb_tap(drop_x, drop_y)

    def deploy_rage(self):
        rage_pos = wait_for_template("../templates/rage.png", timeout=2)
        if rage_pos:
            print("Deploying rage spells...")
            for spot in self.rage_spots[self.strategy_number]:
                x = COORDS[spot][0] + random.randint(-50, 50)
                y = COORDS[spot][1] + random.randint(-50, 50)
                adb_tap(x, y)
                time.sleep(random.uniform(0.3, 0.6))

    def execute(self):
        raise NotImplementedError("Subclasses must implement execute()")