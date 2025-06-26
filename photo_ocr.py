import cv2
import easyocr
from PIL import Image, ImageDraw, ImageFont
import numpy as np

reader = easyocr.Reader(['ne'], gpu=True) 
image = cv2.imread("plate.jpg")
results = reader.readtext(image, detail=1)

# Convert to PIL format
image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
draw = ImageDraw.Draw(image_pil)

font = ImageFont.truetype("NotoSansDevanagari-Regular.ttf", size=24)  

# Draw bounding boxes and Nepali text
for (bbox, text, confidence) in results:
    (top_left, top_right, bottom_right, bottom_left) = bbox
    top_left = tuple(map(int, top_left))
    bottom_right = tuple(map(int, bottom_right))

    draw.rectangle([top_left, bottom_right], outline="green", width=2)
    draw.text((top_left[0], top_left[1] - 30), text, font=font, fill=(0, 255, 0))

    print(f"Detected: {text} (Confidence: {confidence:.2f})")

# Convert back to OpenCV and save
result_img = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
cv2.imwrite("ocr_result_nepali.jpg", result_img)
