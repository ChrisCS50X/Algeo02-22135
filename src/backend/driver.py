import numpy as np
import matplotlib.pyplot as plt
import cv2
import csv
import math
import os
import pandas as pd
from PIL import Image
from pathlib import Path
import multiprocessing as mp
    
def rgbtogray1(img):
    r, g, b = cv2.split(img)
    gray = 0.299*r + 0.587*g + 0.114*b
    gray = gray.astype(int)
    return gray

def tekstur(imgGray4):
    imgGray = rgbtogray1(imgGray4)
    matrixFrameWork = np.zeros((256, 256), dtype=np.int32)
    for i in range(len(imgGray)):
        for j in range(len(imgGray[0])-1):
            matrixFrameWork[imgGray[i][j]][imgGray[i][j+1]] = matrixFrameWork[imgGray[i][j]][imgGray[i][j+1]] + 1

    contrast = np.sum(np.square(np.arange(256)[:, np.newaxis] - np.arange(256)[np.newaxis, :]) * matrixFrameWork)
    homogeneity = -np.sum(matrixFrameWork * np.log(matrixFrameWork + np.finfo(float).eps))
    entropy = np.sum(matrixFrameWork / (1 + np.abs(np.arange(256)[:, np.newaxis] - np.arange(256)[np.newaxis, :])))

    array = [contrast,homogeneity,entropy]
    return array

def compare(img1,img2):
    hasilDot = np.dot(img1,img2)
    norm1 = np.linalg.norm(img1)
    norm2 = np.linalg.norm(img2)
    return hasilDot/(norm1*norm2)
