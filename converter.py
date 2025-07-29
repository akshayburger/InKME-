import cv2
import os
import numpy as np

def text_to_handwriting(sentence):
    letter_imgs = {}
    for i in range(26):
        upper_path = f"output_letters/char_{i:02}.png"
        lower_path = f"output_letters/char_{i+26:02}.png"
        if os.path.exists(upper_path):
            letter_imgs[chr(65 + i)] = cv2.imread(upper_path)
        if os.path.exists(lower_path):
            letter_imgs[chr(97 + i)] = cv2.imread(lower_path)

    if not letter_imgs:
        raise Exception("❌ No letter images found in output_letters/")

    sample_img = next(iter(letter_imgs.values()))
    full_height, full_width = sample_img.shape[:2]
    space_width = full_width // 2

    lines_imgs = []

    for line in sentence.split("\n"):
        line_imgs = []
        for char in line:
            if char == " ":
                space = 255 * np.ones((full_height, space_width, 3), dtype=np.uint8)
                line_imgs.append(space)
            elif char in letter_imgs:
                img = letter_imgs[char]
                if char.islower():
                    scale = 0.75
                    new_h = int(full_height * scale)
                    resized = cv2.resize(img, (full_width, new_h))
                    pad_bottom = full_height - new_h
                    img = cv2.copyMakeBorder(resized, pad_bottom, 0, 0, 0, cv2.BORDER_CONSTANT, value=[255,255,255])
                line_imgs.append(img)
            else:
                print(f"⚠ Skipping unsupported character: {char}")

        if line_imgs:
            line_concat = np.hstack(line_imgs)
            lines_imgs.append(line_concat)

    if lines_imgs:
        max_width = max(line.shape[1] for line in lines_imgs)
        padded_lines = []
        for line in lines_imgs:
            if line.shape[1] < max_width:
                pad_right = max_width - line.shape[1]
                line = cv2.copyMakeBorder(line, 0, 0, 0, pad_right, cv2.BORDER_CONSTANT, value=[255,255,255])
            padded_lines.append(line)
        final = np.vstack(padded_lines)
        cv2.imwrite("output_sentence.png", final)
        print("✅ Saved: output_sentence.png")
    else:
        print("⚠ No valid characters to render.")