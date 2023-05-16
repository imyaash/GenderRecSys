# -*- coding: utf-8 -*-
"""
Created on Sat May 13 13:32:43 2023

@author: imyaash-admin
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import keyboard
import csv
import os
import pandas as pd
import shutil

driver = webdriver.Firefox()
driver.get("https://this-person-does-not-exist.com/en")
time.sleep(5)

csvPath = "/imagesData.csv"
imgPath = "/Images/"

if not os.path.isfile(csvPath):
    with open(csvPath, mode = "w", newline = "") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Gender", "Age", "Ethnicity", "Image"])

downloadsFolder = "D:/Downloads/"

while True:
    try:
        chosenGender = random.choice(["male", "female"])
        gender = driver.find_element(By.NAME, "gender")
        gender.send_keys(chosenGender)

        chosenAge = random.choice(["12-18", "19-25", "26-35", "35-50", "50"])
        age = driver.find_element(By.NAME, "age")
        age.send_keys(chosenAge)

        chosenEthnicity = random.choice(["aisan", "black", "white", "indian", "middle eastern", "latino hispanic"])
        ethnicity = driver.find_element(By.NAME, "etnic")
        ethnicity.send_keys(chosenEthnicity)

        reloadButton = driver.find_element(By.ID, "reload-button")
        reloadButton.click()
        time.sleep(7)

        clickDownload = driver.find_element(By.ID, "download")
        clickDownload.click()
        time.sleep(2)

        windowHandles = driver.window_handles
        driver.switch_to.window(windowHandles[-1])

        download = driver.find_element(By.ID, "download")
        download.click()
        time.sleep(15)

        driver.close()

        windowHandles = driver.window_handles
        driver.switch_to.window(windowHandles[0])
        
        fileList = [file for file in os.listdir(downloadsFolder) if file.endswith(".jpeg")]
        fileTime = [os.path.getctime(downloadsFolder + i) for i in fileList]
        fileDf = pd.DataFrame({"filename": fileList, "ctime": fileTime})
        latestFile = fileDf[fileDf.ctime == max(fileDf.ctime)]["filename"].tolist()[0]
        latestFilePath = os.path.join(downloadsFolder, latestFile)
        
        shutil.move(latestFilePath, imgPath + latestFile)
        
        with open(csvPath, mode = "a", newline = "") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([chosenGender, chosenAge, chosenEthnicity, latestFile])
        
        if keyboard.is_pressed("ctrl+z") or keyboard.is_pressed("esc"):
            driver.quit()
            break
    except:
        print("An error occured. Restarting the loop.....")
        continue