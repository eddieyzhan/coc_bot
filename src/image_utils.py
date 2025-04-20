import json
import os
import cv2
import pytesseract
import re
import time
from adb_utils import capture_screen

"""def read_trophies():
    capture_screen("trophy_screen.png")
    img = cv2.imread("trophy_screen.png")
    if img is None:
        print("Error reading captured screen!")
        return None
    
    CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config.json")

    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)

    roi = config["trophy_roi"]
    x1, y1, x2, y2 = roi["x1"], roi["y1"], roi["x2"], roi["y2"]

    # Crop the region of interest (ROI)
    roi = img[y1:y2, x1:x2]

    # Convert to grayscale
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Optionally apply a threshold to darken text
    # You may need to experiment with thresholds or other preprocessing
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    # Use Tesseract to read the text
    # --psm 7 helps Tesseract focus on a single line/number
    config = "--psm 7 -c tessedit_char_whitelist=0123456789"
    text = pytesseract.image_to_string(thresh, config=config)

    # Extract digits from the recognized text
    match = re.findall(r"\d+", text)
    if match:
        trophies_str = match[0]  # e.g. "2922"
        trophies = int(trophies_str)
        return trophies
    else:
        return None"""

def read_trophies():
    capture_screen("trophy_screen.png")
    img = cv2.imread("trophy_screen.png")
    if img is None:
        print("Error reading captured screen!")
        return None

    # Coordinates for the top-left corner where trophies appear.
    # Adjust these (x1, y1, x2, y2) to match your device/screenshot exactly.
    x1, y1 = 215, 170   # top-left corner of ROI
    x2, y2 = 300, 200  # bottom-right corner of ROI

    # Crop the region of interest (ROI)
    roi = img[y1:y2, x1:x2]

    # Convert to grayscale
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Optionally apply a threshold to darken text
    # You may need to experiment with thresholds or other preprocessing
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    eroded_image = cv2.erode(thresh, kernel, iterations=1)
    # Use Tesseract to read the text
    # --psm 7 helps Tesseract focus on a single line/number
    config = "--psm 7 -c tessedit_char_whitelist=0123456789"
    text = pytesseract.image_to_string(eroded_image, config=config)

    # Extract digits from the recognized text
    match = re.findall(r"\d+", text)
    if match:
        trophies_str = match[0]  # e.g. "2922"
        trophies = int(trophies_str)
        return trophies
    else:
        return None
    

def read_ressources():
    capture_screen("resources_screen.png")
    img = cv2.imread("resources_screen.png")
    if img is None:
        print("Error reading captured screen!")
        return None
    x1G, y1G = 170, 150   # top-left corner of ROI FOR GOLD    
    x2G, y2G = 345, 185  # bottom-right corner of ROI FOR GOLD
    x1E, y1E = 170, 205   # top-left corner of ROI FOR ELIXIR
    x2E, y2E = 345, 240  # bottom-right corner of ROI FOR EL
    roi_gold = img[y1G:y2G, x1G:x2G]
    roi_elixir = img[y1E:y2E, x1E:x2E]

    # convert the ROI to HSV color space
    roi_gold_hsv = cv2.cvtColor(roi_gold, cv2.COLOR_BGR2HSV)
    roi_elixir_hsv = cv2.cvtColor(roi_elixir, cv2.COLOR_BGR2HSV)
    # define the lower and upper bounds for the color in bgr
    lower_bound_gold = np.array([10, 40, 201])  # BGR for gold color
    upper_bound_gold = np.array([40, 75, 255])  # BGR for gold color
    lower_bound_elixir = np.array([150, 0, 170])  # BGR for elixir color  
    upper_bound_elixir = np.array([179, 40, 255])  # BGR for elixir color
    
    # create a mask for the gold color
    mask_gold = cv2.inRange(roi_gold_hsv, lower_bound_gold, upper_bound_gold)
    # create a mask for the elixir color
    mask_elixir = cv2.inRange(roi_elixir_hsv, lower_bound_elixir, upper_bound_elixir)

    config = "--psm 7 -c tessedit_char_whitelist=0123456789"
    text_gold = pytesseract.image_to_string(mask_gold, config=config)
    text_elixir = pytesseract.image_to_string(mask_elixir, config=config)
    match_gold = re.findall(r"\d+", text_gold)
    match_elixir = re.findall(r"\d+", text_elixir)
    gold = 0
    elixir = 0
    if match_gold:
        gold_str = match_gold[0]
        gold = int(gold_str)
    if match_elixir:
        elixir_str = match_elixir[0]
        elixir = int(elixir_str)
    print(f"Gold: {gold}, Elixir: {elixir}")    
    ressources = gold + elixir
    return ressources



def read_percentage():
    # Capture the screen and read the percentage from the current attack 
    # mainly to stop the attack before 100% to stay as much as possible in fake legends
    capture_screen("percentage_screen.png")
    img = cv2.imread("percentage_screen.png")
    if img is None:
        print("Error reading captured screen!")
        return None
    # unique. just check on your device if you want to change it
    x1, y1 = 2140, 828  # top-left corner of ROI
    x2, y2 = 2240, 872  # bottom-right corner of ROI
    roi = img[y1:y2, x1:x2]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    eroded_image = cv2.erode(thresh, kernel, iterations=1)
    config = "--psm 7 -c tessedit_char_whitelist=0123456789%"
    text = pytesseract.image_to_string(eroded_image, config=config)
    match = re.findall(r"\d+", text)
    if match:
        percentage_str = match[0]
        percentage = int(percentage_str)
        return percentage
    else:
        return None

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