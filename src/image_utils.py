import cv2
import pytesseract
import re
import time
from adb_utils import capture_screen

def read_trophies():
    capture_screen("trophy_screen.png")
    img = cv2.imread("trophy_screen.png")
    if img is None:
        print("Error reading captured screen!")
        return None

    # Coordinates for the top-left corner where trophies appear.
    # Adjust these (x1, y1, x2, y2) to match your device/screenshot exactly.
    x1, y1 = 230, 165    # top-left corner of ROI
    x2, y2 = 325, 205  # bottom-right corner of ROI

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