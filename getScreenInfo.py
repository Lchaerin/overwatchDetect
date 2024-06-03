import mss
import pytesseract
from PIL import Image
import time
import cv2
import re
import logging

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# def preprocess_image(image):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
#     return binary

def extract_numbers(text):
    numbers = re.findall(r'\d+', text)
    return numbers


with mss.mss() as sct:
    monitor = sct.monitors[1]
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    left = monitor["left"]+int(monitor["width"]/33.87*3.6)
    top = monitor["top"] + int(monitor["height"]/19.05*15.6)
    width = int(monitor["width"]/33.867*2.67)
    height = int(monitor["height"]/19.05*0.84)

    monitor_part = {"top": top, "left": left, "width": width, "height": height}
    pre = 0
    while True:
        try:
            screenshot = sct.grab(monitor_part)
            image = Image.frombytes(
                "RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")

            # image_np = np.array(image)
            # processed_image = preprocess_image(image_np)

            text = pytesseract.image_to_string(image)
            current = int(extract_numbers(text)[0])
            # print("Detected text: ", text)
            print("current:", current, " full:",
                  int(extract_numbers(text)[1]))
            if pre > current:
                print("damaged(-)")
            if current > pre:
                print("healed(+)")
            logger.info('.')
            pre = current

        except Exception as e:
            print(f"Cannot detect HP")
            logger.info('.')

        # time.sleep(0.2)
