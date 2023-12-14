# main.py

from preprocess import PreprocessImage
from ocr_engine import *
from data_extraction import *
import pytesseract
from PIL import Image
import cv2
import easyocr
import numpy as np
import argparse



def process_receipt(receipt_image_path):
    """
    Process a receipt image and extract information.
    """
    preprocessor = PreprocessImage(receipt_image_path)
    receipt_processed = preprocessor.receipt

    text = extract_ocr_tesseract(receipt_processed)
    
    print(text)

    extract_item_price_pairs(text)

    #Uncomment to see results of method 2
    #boxes = get_tesseract_bounding_boxes(receipt_processed)

    #text= extract_text_with_easyocr(receipt_processed, boxes)

    #for i, textbox in enumerate(text):
        #print(f"Textbox {i}: {textbox}")

    


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
        help="path to input receipt image")
    args = vars(ap.parse_args())

    process_receipt(args['image'])
    
    
