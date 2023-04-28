# Canny Edge Detecting Algorithm and Gaussian Model for Vehicle Number Plate Detection

This project aims to detect vehicle number plates using the Canny Edge Detection algorithm and a Gaussian model.

## Prerequisites

This project requires the following libraries:

- Flask
- OpenCV
- imutils
- pytesseract
- numpy

You can install these libraries using pip. For example:

```
pip install Flask
pip install opencv-python
pip install imutils
pip install pytesseract
pip install numpy
```

## Usage

To run the application, clone this repository and run `app.py`. 

```
flask run
```

Once the application is running, go to `http://localhost:5000/` in your web browser to access the user interface. Upload an image of a vehicle number plate and click the "Predict" button to detect the number plate.

## Methodology

1. The uploaded image is read using OpenCV and saved in the `static` folder.
2. The image is resized to a width of 300 pixels to reduce processing time.
3. The image is converted to grayscale using OpenCV.
4. Bilateral filtering is applied to the grayscale image to remove noise.
5. The Canny Edge Detection algorithm is applied to the filtered image to detect edges.
6. The contours of the edges are extracted using OpenCV.
7. The contours are sorted by area in descending order.
8. The largest contour that has four corners is identified as the number plate.
9. The number plate is extracted from the image and saved in the `static` folder.
10. The extracted number plate is passed through pytesseract to extract the text.
11. The text and the original image with the number plate highlighted are displayed in the user interface.
