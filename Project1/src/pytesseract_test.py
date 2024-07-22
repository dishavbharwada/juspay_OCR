import pytesseract
from PIL import Image
im_file = "Project1/test-files/testImage2.jpeg"
no_noise = "Project1/temp/no_noise.jpg"
img = Image.open(im_file)

ocr_result = pytesseract.image_to_string(img)
print(ocr_result)

print("XXXXXXXXXXXXXXXXX")

img2 = Image.open(no_noise)

ocr_result2 = pytesseract.image_to_string(img2)
print(ocr_result2)