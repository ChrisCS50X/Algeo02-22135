import cv2
import numpy as np
import math
import os
import time
import csv
import pandas as pd

def calculate_histogram(image):
    # Melakukan normlisasi image dengan membaginya dengan 255
    image = image.astype(np.float32) / 255.0
    hsv_image = np.zeros_like(image, dtype=np.float32)

    # Mencari cmax,cmin,dan delta
    Cmax = np.max(image, axis=2)
    Cmin = np.min(image, axis=2)
    delta = Cmax - Cmin

    # Menghitung H atau Hue
    hsv_image[..., 0] = np.where(delta == 0, 0,np.where(Cmax == image[..., 2], 60 * ((image[..., 1] - image[..., 0]) / (delta + 1e-5) % 6),np.where(Cmax == image[..., 1], 60 * ((image[..., 0] - image[..., 2]) / (delta + 1e-5) + 2),60 * ((image[..., 2] - image[..., 1]) / (delta + 1e-5) + 4))))

    # Menghitung S atau Saturation
    hsv_image[..., 1] = np.where(Cmax == 0, 0, delta / (Cmax + 1e-5))

    # Menghitung V atau Value
    hsv_image[..., 2] = Cmax

    # Scaling H untuk menyamai format OpenCV
    hsv_image[..., 0] *= 0.5

    # Mengkonversi ke bentuk uint8
    hsv_image = (hsv_image * 255).astype(np.uint8)

    # Membuat Histogram dengan memanfaatkan OpenCV
    hist = cv2.calcHist([hsv_image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])

    #Melakukan normalisasi histogram
    hist = cv2.normalize(hist, hist).flatten()

    return hist

def cosine_similarity(histogram1, histogram2):
    # Sesuai rumus cosine similarity, Untuk menghitung dot product dari vektor histogram image 1 dan vektor histogram image 2 
    dot = np.dot(histogram1, histogram2)

    # Melakukan perkalian panjang vektor histogram 1 dan panjang vektor histogram 2
    norm1 = np.linalg.norm(histogram1)
    norm2 = np.linalg.norm(histogram2)

    # Menghandle jika pembaginya adalah 0
    if (norm1 * norm2 != 0):
        similarity = dot / (norm1 * norm2)
    else:   
        similarity = 0

    return similarity

def convert_to_array(string):
    return np.array([float(val) for val in string.split(',')])

def compareimage(input_image, data_directory):
    # Mencari histogram dari gambar yang diinput
    histogram_input = calculate_histogram(input_image)

    # Menyimpan hasil similarity dalam array
    sim = []

    # Menyimpan nama file dalam array
    filenames = []

    # Menampung file dalam folder dataset
    list_of_files = os.listdir(data_directory)

    # Melakukan pengechekan terhadap semua file dalam list_of_files
    for filename in list_of_files:
        dataset_image = cv2.imread(os.path.join(data_directory, filename))
        dataset_hist = calculate_histogram(dataset_image)

        similarity = cosine_similarity(histogram_input, dataset_hist)

        if (similarity > 0.6 ):
            sim.append(similarity * 100)
            filenames.append(filename)

    #Melakukan sort terhadap nama file dan nilai similarity
    sorted_indices = np.argsort(sim)[::-1]
    sorted_similarities = np.sort(sim)[::-1]
    sorted_filenames = [filenames[i] for i in sorted_indices]

    return sorted_indices, sorted_similarities, sorted_filenames

def compare_histo_csv(input_image,csv_directory):
    histogram_input = calculate_histogram(input_image)

    # Menyimpan hasil similarity dalam array
    sim = []

    # Menyimpan nama file dalam array
    filenames = []

    df = pd.read_csv(csv_directory)

    df['histogram'] = df['histogram'].apply(convert_to_array)

    for index, row in df.iterrows():
        histogram,filepath = row['histogram'],row['filepath']
        similarity = cosine_similarity(histogram_input, histogram)

        if (similarity > 0.6 ):
            sim.append(similarity * 100)
            filenames.append(filepath)

    sorted_indices = np.argsort(sim)[::-1]
    sorted_similarities = np.sort(sim)[::-1]
    sorted_filenames = [filenames[i] for i in sorted_indices]

    return sorted_indices, sorted_similarities, sorted_filenames


# Melakukan running program yakni driver_colour
def run():
    data_directory = "C:\\Users\\chris\\Documents\\Semester 3 Informatika\\Tubes Algeo 2\\Image"  
    input_image = cv2.imread("451.jpg")
    
    start_time = time.time()
    sorted_indices, sorted_similarities,sorted_filenames = compareimage(input_image, data_directory)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
 
    top_5_indices = sorted_indices[:5]

    for i in range(len(top_5_indices)):
        dataset_image = cv2.imread(os.path.join(data_directory, os.listdir(data_directory)[top_5_indices[i]]))
        print(f"Image {sorted_filenames[i]} - Similarity: {sorted_similarities[i]}")
        cv2.imshow(f"Image {sorted_filenames[i]} - Similarity: {sorted_similarities[i]}", dataset_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()