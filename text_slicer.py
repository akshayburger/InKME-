import sys
print(sys.executable)
import cv2
import os
import numpy as np
from PIL import ExifTags

def slice(filename):
    img = cv2.imread(filename)
    if img is None:
        raise FileNotFoundError(f'Make sure "{filename}" is in the same folder')

    rows, cols = 6, 10
    h, w = img.shape[:2]
    cell_h = h // rows
    cell_w = w // cols

    os.makedirs("output_letters", exist_ok=True)

    letter_index = 0
    for r in range(rows):
        for c in range(cols):
            if r in {2, 5} and c >= 6:
                continue

            x1 = c * cell_w
            y1 = r * cell_h
            x2 = x1 + cell_w
            y2 = y1 + cell_h
            cell = img[y1:y2, x1:x2]

            gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (3, 3), 0)
            thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                       cv2.THRESH_BINARY_INV, 15, 10)

            # Remove thin lines
            horiz_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (cell_w // 3, 1))
            vert_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, cell_h // 3))
            remove_h = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horiz_kernel)
            remove_v = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vert_kernel)
            cleaned = cv2.subtract(thresh, remove_h)
            cleaned = cv2.subtract(cleaned, remove_v)

            # Find contours
            contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if contours:
                # Sort by contour area (largest = main letter)
                contours = sorted(contours, key=cv2.contourArea, reverse=True)
                x, y, w_box, h_box = cv2.boundingRect(contours[0])
                isolated = cleaned[y:y + h_box, x:x + w_box]
                final = cv2.resize(isolated, (100, 100), interpolation=cv2.INTER_AREA)
            else:
                final = cleaned

            # Convert back to 3-channel image (optional)
            final = cv2.bitwise_not(final)
            final_bgr = cv2.cvtColor(final, cv2.COLOR_GRAY2BGR)
            cv2.imwrite(f"output_letters/char_{letter_index:02}.png", final_bgr)
            letter_index += 1

    print(f"✅ Clean letters saved in 'output_letters/' folder.")

def correct_image_orientation(image):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == "Orientation":
                break

        exif = dict(image._getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)

    except (AttributeError, KeyError, IndexError):
        # Cases: image doesn't have EXIF data
        pass

    return image
