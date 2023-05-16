# -*- coding: utf-8 -*-
"""
Created on Mon May 15 18:03:18 2023

@author: imyaash-admin
"""

# Importing the libraries
from processor import loadImagesDF
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.neural_network import MLPClassifier as NN
import joblib as jb
import pickel as pk

# Loading the data
data64 = loadImagesDF("imagesData.csv", "Image", (64, 64), True)

# Initialising the Label Encoder and encoding the labels
genderEncoder = LabelEncoder()
genderLabel = genderEncoder.fit_transform(data64.Gender)
genderLabelMap = dict(zip(genderEncoder.transform(genderEncoder.classes_), genderEncoder.classes_))

# Initialising the StandardScaler and scaling the images
imageData64 = data64.drop(columns = ["Gender", "Age", "Ethnicity"]).values
scaler = StandardScaler()
imageData64Scaled = scaler.fit_transform(imageData64)

# Building the model
genderNN64Scaled = NN(
    hidden_layer_sizes = (
        2048, 4096, 2048
        ),
    activation = "relu",
    solver = "adam",
    max_iter = 100,
    verbose = True,
    early_stopping = True,
    validation_fraction = 0.1,
    n_iter_no_change = 20
    )
genderNN64Scaled.fit(imageData64Scaled, genderLabel)

# Saving the model
pk.dump(genderLabelMap, open("genderLabelMap.pkl"))
jb.dump(scaler, "genderNN64Scaler.sav")
jb.dump(genderNN64Scaled, "genderNN64Scaled.sav")
