import cv2
import numpy as np
import math
import os
import time

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

    # Scaling H unutk menyamai format OpenCV
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

    if (norm1 * norm2 != 0):
        similarity = dot / (norm1 * norm2)
    else:   
        similarity = 0

    return similarity

def compareimage(input_image, data_directory):
    histogram_input = calculate_histogram(input_image)

    sim = []
    list_of_files = os.listdir(data_directory)

    for filename in list_of_files:
        dataset_image = cv2.imread(os.path.join(data_directory, filename))
        dataset_hist = calculate_histogram(dataset_image)

        similarity = cosine_similarity(histogram_input, dataset_hist)
        sim.append(similarity * 100)

    sorted_indices = np.argsort(sim)[::-1]
    sorted_similarities = np.sort(sim)[::-1]

    return sorted_indices, sorted_similarities

def run():
    data_directory = "C:\\Users\\chris\\Documents\\Semester 3 Informatika\\Tubes Algeo 2\\Image"  
    input_image = cv2.imread("63.jpg")
    
    start_time = time.time()
    sorted_indices, sorted_similarities = compareimage(input_image, data_directory,bins=8)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
 
    top_5_indices = sorted_indices[:5]

    for i in range(len(top_5_indices)):
        dataset_image = cv2.imread(os.path.join(data_directory, os.listdir(data_directory)[top_5_indices[i]]))
        print(f"Image {top_5_indices[i]} - Similarity: {sorted_similarities[i]}")
        cv2.imshow(f"Image {top_5_indices[i]} - Similarity: {sorted_similarities[i]}", dataset_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()