import cv2
import pytesseract
from PIL import Image
import easyocr
LEVELS = {
    'page_num': 1,
    'block_num': 2,
    'par_num': 3,
    'line_num': 4,
    'word_num': 5
}
def get_tesseract_bounding_boxes(image):
    custom_config = r'--psm 4' 
    boxes_data = pytesseract.image_to_data(image, config=custom_config, output_type=pytesseract.Output.DICT)

    boxes = []
    for i in range(len(boxes_data['text'])):
         if int(boxes_data['conf'][i]) > 10:
            x, y, w, h = boxes_data['left'][i], boxes_data['top'][i], boxes_data['width'][i], boxes_data['height'][i]
            boxes.append((x, y, w, h))
    return boxes




def extract_text_with_easyocr(image, boxes):
    reader = easyocr.Reader(['en'])  # Set English as Language``
    text_results = []

    for box in boxes:
        x, y, w, h = box
        # Cropping the region of interest from the original image
        roi = image[y:y+h, x:x+w]
        # Use EasyOCR to extract text from the cropped region
        text = reader.readtext(roi, detail=0, paragraph=False)
        text_results.append(' '.join(text))

    return text_results


def extract_text_with_tesseract(image_path, bounding_boxes):
    # Load the image
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    extracted_texts = []
    for box in bounding_boxes:
        x, y, w, h = box

        # Crop and preprocess the region of interest (ROI)
        roi = image_rgb[y:y+h, x:x+w]
        roi = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)  # Convert to grayscale
        roi = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]  # Apply thresholding

        # Perform OCR on the preprocessed ROI
        custom_config = r'--oem 1 --psm 7'  # LSTM-based OCR, treating the image as a single text line
        text = pytesseract.image_to_string(roi, config=custom_config)
        extracted_texts.append(text.strip())

    return extracted_texts

def extract_ocr_tesseract(receipt):  
    options = "--psm 4"
    text = pytesseract.image_to_string(cv2.cvtColor(receipt,cv2.COLOR_BGR2RGB), config=options)
    return text