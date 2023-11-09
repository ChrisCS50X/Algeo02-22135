import cv2
import os
import numpy as np
import math

def RGBtoHSV (imagename):
    #Membaca dan melakukan pre processing
    img = cv2.imread(imagename)
    height, width = img.shape[:2]
    r_channel,g_channel,b_channel = cv2.split(img)

    #Normalisasi
    r_channel = r_channel / 255
    g_channel = g_channel / 255
    b_channel = b_channel / 255

    #Penampung nilai HSV
    hsv = []
    height, width = len(r_channel)

    for y in (height):
        for x in (width):

            #Mencari variabel cmax,cmin,dan delta
            cmax = max(r_channel[x][y],g_channel[x][y],b_channel[x][y])
            cmin = max(r_channel[x][y],g_channel[x][y],b_channel[x][y])
            delta = cmax - cmin  

            # Mengisi lit H, list S, list V dengan perhitungan
            hsv.append(hue(r_channel[x][y],g_channel[x][y],b_channel[x][y],cmax,delta))
            hsv.append(saturation(r_channel[x][y],g_channel[x][y],b_channel[x][y],cmax,delta))
            hsv.append(cmax)

    return hsv

def decompose_block(imagename):
    img = cv2.imread(imagename)
    array = np.array(img)
    new_array = np.array_split(array,3)
    new2_array = [np.array_split(part, 3, axis=1) for part in new_array]
    
    return new2_array

def hue (r,g,b,cmax,delta):
    if(delta == 0):
        h = 0

    elif (cmax == r):
        h = 60 * (((g - b) / delta) % 6)

    elif (cmax == g):
        h = 60 * (((b - r) / delta) + 2)
    
    elif (cmax == b):
        h = 60 * (((r - g) / delta) + 4)

    return h

def saturation (cmax,delta):
    if (cmax == 0):
        s = 0

    elif (cmax != 0):
        s = delta / cmax

    return s

def histogram (vektor):
    hist = np.histogram(vektor,bins=256,range=(0,255))
    return hist

def Similarity(histogram1, histogram2):
    dotproduct = np.dot(histogram1, histogram2)
    euclidian_norm1 = math.sqrt(sum(x**2 for x in histogram1))
    euclidian_norm2 = math.sqrt(sum(x**2 for x in histogram2))

    if ((euclidian_norm1 * euclidian_norm2) != 0): 
        similarity = dotproduct / (euclidian_norm1 * euclidian_norm2)   
    else:
        similarity = 0

    return similarity

