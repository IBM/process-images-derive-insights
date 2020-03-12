import cv2
import os
from os import path
import numpy as np
   
def preprocessing(filepath):
    
    img = cv2.imread(filepath,0)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_blur = cv2.bilateralFilter(img, d = 7, sigmaSpace = 75, sigmaColor =75)
    # Convert to grayscale 
    img_gray = cv2.cvtColor(img_blur, cv2.COLOR_RGB2GRAY)
    # Apply the thresholding
    a = img_gray.max()  
    _, thresh = cv2.threshold(img_gray, a/2+60, a,cv2.THRESH_BINARY_INV)
    # Apply Image Dilation to for definite areas
    kernel = np.ones((27,27), np.uint8)
    img_dilation = cv2.dilate(thresh, kernel, iterations=1) 
    contours, hierarchy = cv2.findContours(
                                   image = img_dilation, 
                                   mode = cv2.RETR_TREE, 
                                   method = cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)# Draw the contour 
    img_copy = img.copy()
    final = cv2.drawContours(img_copy, contours, contourIdx = -1, 
                             color = (255, 0, 0), thickness = 2)
    cv2.imwrite("./userapp/images/sections.jpg", final)
    for contour in contours:
      (x,y,w,h) = cv2.boundingRect(contour)
      cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

    i = 0
    images = []
    for contour in contours:  
        (x,y,w,h) = cv2.boundingRect(contour)
        crop_img = img[y:y+h, x:x+w] 
        images.append(crop_img)
        i = i + 1
        #plt.figure(i+1)
    i = 0
    images_split = {}
    img_file_paths = []
    for image in images:
      img_name = "image"+str(i)+".jpg" 
      img_file_path = os.path.join("./userapp/images",img_name)
      img_file_path_send = os.path.join("/images",img_name)
      images_split[i] = image
      i = i + 1
      cv2.imwrite(img_file_path, image)
      img_file_paths.append(img_file_path_send)

    img_file_paths.append("/images/sections.jpg")  
    return img_file_paths

