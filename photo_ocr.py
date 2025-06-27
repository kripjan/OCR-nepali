import cv2
import easyocr
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Read the original image
image = cv2.imread("input//nine.jpg")

# === Preprocessing ===
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.equalizeHist(gray)

thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY_INV, 11, 2)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
morphed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# Convert back to 3-channel image for EasyOCR (expects BGR or RGB)
preprocessed_image = cv2.cvtColor(morphed, cv2.COLOR_GRAY2BGR)

# Initialize EasyOCR reader
reader = easyocr.Reader(['ne'], gpu=True)

# OCR on the preprocessed image
results = reader.readtext(preprocessed_image, detail=1)

# Convert to PIL format for drawing
image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  # draw on original image
draw = ImageDraw.Draw(image_pil)

# Load Devanagari font
font = ImageFont.truetype("NotoSansDevanagari-Regular.ttf", size=24)

# Draw bounding boxes and Nepali text
for (bbox, text, confidence) in results:
    (top_left, top_right, bottom_right, bottom_left) = bbox
    top_left = tuple(map(int, top_left))
    bottom_right = tuple(map(int, bottom_right))

    draw.rectangle([top_left, bottom_right], outline="green", width=2)
    text_y = max(top_left[1] - 30, 0)
    draw.text((top_left[0], text_y), text, font=font, fill=(0, 255, 0))

    print(f"Detected: {text} (Confidence: {confidence:.2f})")

# Convert back to OpenCV format and save the result
result_img = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
cv2.imwrite("output//nine.jpg", result_img)
