
import cv2
import imutils
import numpy as np
from PIL import Image
from easyocr import easyocr
import streamlit as st
import os.path
from car_plate.configs.configs import CarPartsConfigs, DamageConfigs

class UnetParts:
    def __init__(self, configs: CarPartsConfigs, damage_configs: DamageConfigs):
        self.configs = configs
        self.ocr_model = easyocr.Reader(['en'], gpu=False,user_network_directory='model')




    def recognize_plate(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        bfilter = cv2.bilateralFilter(gray, 11, 11, 17)
        edged = cv2.Canny(bfilter, 30, 200)
        keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE,
                                     cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        location = None
        flag = False
        for contour in contours:

            # cv2.approxPolyDP returns a resampled contour, so this will still return a set of (x, y) points
            approx = cv2.approxPolyDP(contour, 10, True)
            if len(approx) == 4:
                location = approx
                flag = True
                break
        if not flag:
            results = self.ocr_plate(img, full = False)
            if results:
                texts = [len(text[1]) for text in results]
                return [[a] for a in results[texts.index(max(texts))][0]], results[texts.index(max(texts))][1]
            else:
                return 0, ''
        mask = np.zeros(gray.shape, np.uint8)
        cv2.drawContours(mask, [location], 0, 255, -1)
        (x, y) = np.where(mask == 255)
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))
        # Adding Buffer
        cropped_image = img[x1:x2 + 3, y1:y2 + 3]
        text = self.ocr_plate(cropped_image)
        # font = cv2.FONT_HERSHEY_SIMPLEX
        # res = cv2.putText(img, text = text, org = (approx[0][0][0], approx[1][0][1]+60), fontFace = font, fontScale = 1, color = (0, 255, 0), thickness = 5)
        # res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0,255, 0), 3)
        return location, text

    def ocr_plate(self, cropped_image, full=True):
        # ocr_model = PaddleOCR(lang='en', use_angle_cls=True, use_gpu=True)
        # result = ocr_model.ocr(img_path)
        # print(result)
        texts = []
        bboxs = []
        cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        # _, cropped_image = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        results = self.ocr_model.readtext(cropped_image)  # reader.recognize sadece recognize, text detection yok
        if full:
            y, x = cropped_image.shape
            center = y // 2
            # center_x = x // 2
            for (bbox, text, prob) in results:
                # and bbox[0][0] < center_x < bbox[1][0]
                if bbox[1][1] < center < bbox[2][1]:
                    bboxs.append(bbox)
                    texts.append(text)
            return ' '.join(texts)
        else:
            return results

    def draw_plates(self, result, approx, text):
        font = cv2.FONT_HERSHEY_SIMPLEX
        result = cv2.putText(result, text=text,
                             org=(approx[0][0][0], approx[1][0][1] + 60),
                             fontFace=font, fontScale=1, color=(0, 255, 0),
                             thickness=5)
        result = cv2.rectangle(result, tuple(approx[0][0]),
                               tuple(approx[2][0]), (0, 255, 0), 3)
        return result

    def upload_video(self,file_path):
        st.write('Plate recognition starts')
        img = cv2.imread(file_path)
        location, text = self.recognize_plate(img)
        if text:
            img = self.draw_plates(img, location, text)
            cv2.imwrite('temp.png', img)
            image = Image.open('temp.png')
            st.image(image)
            st.write(f'PLATE: {text}')
        else:
            st.write('PLATE NOT FOUND')

    def recognize_plate_only(self, file_path):
        st.write('Plate recognition starts')
        img = cv2.imread(file_path)
        text = self.ocr_plate(img)
        image = Image.open(file_path)
        st.image(image)
        if text:
            st.write(f'PLATE: {text}')
        else:
            st.write('PLATE NOT FOUND')


