from flask import Flask, render_template, request
import os
import cv2
import imutils
import pytesseract
import numpy as np

app = Flask(__name__)

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def predict():
    _file = request.files['image']
    _file.save('static/uploaded_image.jpg')
    image = cv2.imread('static/uploaded_image.jpg')
    
    cv2.imwrite('static/step_1.jpg', image)
    
    image = imutils.resize(image, width=300)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    cv2.imwrite('static/step_2.jpg', gray_image)
    
    gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17)
    edged = cv2.Canny(gray_image, 30, 200)
    
    cv2.imwrite('static/step_3.jpg', edged)
    
    cnts,new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True) [:30]
    screenCnt = None
    for c in cnts:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
        if len(approx) == 4:
            screenCnt = approx
            x,y,w,h = cv2.boundingRect(c)
            new_img=image[y:y+h,x:x+w]
            cv2.imwrite('static/cropped_image.jpg', new_img)
            break
    
    if screenCnt is not None:
        cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
        
        contours_image = np.copy(image)
        cv2.drawContours(contours_image, cnts, -1, (0, 255, 0), 3)
        cv2.imwrite('static/step_4.jpg', contours_image)
        
        top_30_contours_image = np.copy(image)
        cv2.drawContours(top_30_contours_image, cnts, -1, (0, 255, 0), 3)
        cv2.imwrite('static/step_5.jpg', top_30_contours_image)
        
        plate = pytesseract.image_to_string('static/cropped_image.jpg', lang='eng')
        detected_plate_image = np.copy(image)
        cv2.rectangle(detected_plate_image, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.putText(detected_plate_image, plate, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imwrite('static/step_6.jpg', detected_plate_image)
        
        return render_template(indexpage(), prediction_text='Number Plate: {}'.format(plate))
    else:
        return render_template(indexpage(), prediction_text='Number Plate:  Not recognised')

def indexpage():
    return 'index.html'
