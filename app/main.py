import pytesseract
from PIL import Image
import easyocr

# For Tesseract
text_tesseract = pytesseract.image_to_string(Image.open('research/receipt.jpeg'))

# For EasyOCR
reader = easyocr.Reader(['en'])  # specify the language
text_easyocr = reader.readtext('research/receipt.jpeg', detail=0)

print(text_tesseract)
print(text_easyocr)