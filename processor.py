# -*- coding: utf-8 -*-
"""
Created on Sun May 14 10:01:50 2023

@author: imyaash-admin
"""

import pandas as pd
import numpy as np
from PIL import Image

def loadImagesDF(csvPath, filenameCol, resize = None, grayscale = False):
    # Load CSV file into DataFrame
    print("Loading the CSV file")
    try:
        df = pd.read_csv(csvPath)
    except FileNotFoundError:
        print("Could not find CSV file")
        return None

    # Load images from filename column
    print("Loading the Images, resizing and converting to greyscale")
    images = []
    for filename in df[filenameCol]:
        try:
            img = Image.open("Images/" + filename)
            if resize is not None:
                img = img.resize(resize)
            if grayscale:
                img = img.convert("L")
            images.append(img)
        except FileNotFoundError:
            print("Could not find image file:", filename)
            images.append(None)

    # Convert images to numpy arrays and flatten them
    print("Converting the image to an array and flattening the array")
    flattenedImages = []
    for img in images:
        if img is None:
            flattenedImages.append(None)
        else:
            flattened = np.array(img).flatten()
            flattenedImages.append(flattened)

    # Create DataFrame from flattened images
    print("Creating the DataFrame")
    imgDf = pd.DataFrame(flattenedImages)

    # Check that label columns have same number of rows as image columns
    labelCols = ["Gender", "Age", "Ethnicity"]
    if len(df) != len(imgDf):
        print("Number of images does not match number of labels")
        return None
    elif not all(col in df.columns for col in labelCols):
        print("Missing label columns in CSV file")
        return None

    # Add labels to processed images DataFrame
    labelDf = df[labelCols]
    imgDf = pd.concat([imgDf, labelDf], axis=1)

    print("Done")

    return imgDf
