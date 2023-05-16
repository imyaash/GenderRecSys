# -*- coding: utf-8 -*-
"""
Created on Mon May 15 19:33:12 2023

@author: imyaash-admin
"""

import cv2
import joblib as jb
import numpy as np
from PIL import Image
import pickle

# Initialising the necessary models
scaler = jb.load("genderNN64Scaler.sav")
genderNN64Scaled = jb.load("genderNN64Scaled.sav")
genderLabelMap = pickle.load(open("genderLabelMap.pkl", "rb"))

# Opening webcam capture
cap = cv2.VideoCapture(0)

while True:
    # Capturing frame-by-frame and processing the frame
    ret, frame = cap.read()
    resized_frame = cv2.resize(frame, (64, 64))
    gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
    pil_image = Image.fromarray(gray_frame)
    np_image = np.array(pil_image)
    flattened_frame = np_image.flatten()
    scaled_frame = scaler.transform([flattened_frame])

    # Making a prediction using the loaded model
    predicted_label = genderNN64Scaled.predict(scaled_frame)
    predicted_gender = genderLabelMap[predicted_label[0]]

    # Displaying the predicted gender on the frame
    cv2.putText(frame, "Gender: " + predicted_gender, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Webcam', frame)

    # Checking for key press
    if cv2.waitKey(200) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()
