import cv2
import numpy as np
import argparse
import imutils
from imutils.perspective import four_point_transform

class PreprocessImage:

    def __init__(self, image_path, debug=0):
        self.original = cv2.imread(image_path)
        self.image = self.original.copy()
        self.resize()
        self.ratio = self.original.shape[1] / float(self.image.shape[1])

        self.convert_to_grayscale()
        self.blur()
        self.edge_detection()

        if debug > 0:
            cv2.imshow('Original', self.original)
            cv2.imshow('Edged', self.image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        self.find_contours()
        receiptCnt = self.find_receipt_outline()

        # check to see if we should draw the contour of the receipt on the
        # image and then display it to our screen
        if debug > 0:
            output = self.resized.copy()
            cv2.drawContours(output, [receiptCnt], -1, (0, 255, 0), 2)
            cv2.imshow("Receipt Outline", output)
            cv2.waitKey(0)

        # apply a four-point perspective transform to the *original* image to
        # obtain a top-down bird's-eye view of the receipt
        receipt = four_point_transform(self.original, receiptCnt.reshape(4, 2) * self.ratio)

        # show transformed image
        cv2.imshow("Receipt Transform", imutils.resize(receipt, width=500))
        cv2.waitKey(0)

        self.receipt = receipt
    
        

    def resize(self):
        self.resized = imutils.resize(self.image, width=500)
        self.image = self.resized.copy()

    def convert_to_grayscale(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Gray', self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def blur(self):
        self.image = cv2.GaussianBlur(self.image, (3, 3), 0)
        cv2.imshow('Blurred', self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def edge_detection(self):
        self.image = cv2.Canny(self.image, 40, 120)

    def find_contours(self):
        # find contours in the edge map and sort them by size in descending
        # order
        cnts = cv2.findContours(self.image.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        self.cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    def find_receipt_outline(self):
        receiptCnt = None 
        # loop over the contours
        for c in self.cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            #self.draw_contour(self.resized.copy(), approx)

            # if our approximated contour has four points, then we
            # can assume that we have found our screen
            if len(approx) == 4:
                receiptCnt = approx
                return receiptCnt
                

        if receiptCnt is None:
            raise Exception(("Could not find outline of receipt"))
        else:
            return receiptCnt
        
#write a function that draws the countour on an image and displays it
    def draw_contour(self, image, cnt):
        cv2.drawContours(image, [cnt], -1, (0, 255, 0), 2)
        cv2.imshow(f'Contour {len(cnt)}', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    


if __name__ == '__main__':
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
        help="path to input receipt image")
    ap.add_argument("-d", "--debug", type=int, default=-1,
        help="whether or not we are visualizing each step of the pipeline")
    args = vars(ap.parse_args())

    PreprocessImage(args['image'], args['debug'])
    #cv2.imshow('Processed Image', processed_image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()