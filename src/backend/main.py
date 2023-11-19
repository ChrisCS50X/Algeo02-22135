import base64
from dataclasses import Field
from typing import Optional
from bson import ObjectId
from fastapi import FastAPI, File, UploadFile
from matplotlib import image
from pydantic import BaseModel, BeforeValidator, ConfigDict, parse_obj_as
from enum import Enum
from typing import Annotated
import pymongo
import driver
import os
import cv2
import numpy as np
import CBIR_colour
import csv
from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
import shutil
import time

app = FastAPI()
arrrFIle = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ganti dengan daftar asal yang diizinkan
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class dataTekstur(BaseModel):
    contrast:float
    homogency:float
    entropy:float
    filepath:str


client = pymongo.MongoClient("mongodb+srv://predatorfocus17:muhhul@clusterdata.adbmei2.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database("dataSetImg")
transaction = db.get_collection("transaction")
dataBaseColour = db.get_collection("dataColour")
dataBaseTekstur = db.get_collection("dataTekstur")
dataBaseBaru=db.get_collection("tesss")


sim = []
dataset = []
global_waktu = 0

UPLOAD_FOLDER = "upload_images"
folder_path = os.path.join(UPLOAD_FOLDER)

def delete_files_in_folder(folder_pat):
    for filename in os.listdir(folder_pat):
        file_path = os.path.join(folder_pat, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

# @app.get('/tekstur')
# def get_tekstur(tipe:Optional[Tipe] = None):
#     result_filter = dataBaseTekstur.find({})
#     result_filter = list(result_filter)

#     vektor1 = [33594549,-910456.3650100988,65645.00094583261]
#     arrHasil = []
#     file=[]
#     sim = []
#     for i in range(len(result_filter)):
#         vektor2 = [result_filter[i].get('contrast'),result_filter[i].get('homogency'),result_filter[i].get('entropy')]
#         hasil = driver.compare(vektor1,vektor2)*100
#         sim.append(hasil)
#         file.append(result_filter[i].get('filepath'))
#     sorted_indices = np.argsort(sim)[::-1]
#     sorted_similarities = np.sort(sim)[::-1]
#     sorted_filenames = [file[i] for i in sorted_indices]
#     for i in range(len(result_filter)):
#         sim=[]
#         sim.append(sorted_similarities[i])
#         sim.append(sorted_filenames[i])
#         arrHasil.append(sim)
    
#     return arrHasil
    
@app.post('/tekstur')
def insert_tekstur(data_directory,namaColl):
    list_of_files = os.listdir(data_directory)
    print(data_directory)
    i=0
    dataBaseBaru=db.get_collection(namaColl)
    dataBaseBaru.delete_many({})
    print(len(list_of_files))
    for filename in list_of_files:
        dataset_image = cv2.imread(os.path.join(data_directory, filename))
        dataset_image = cv2.resize(dataset_image,(0,0),fx=0.5,fy=0.5)
        dataset_tekstur = driver.tekstur(dataset_image)
        data = dataTekstur(contrast=dataset_tekstur[0],homogency=dataset_tekstur[1],entropy=dataset_tekstur[2],filepath=filename)
        dataBaseBaru.insert_one(data.dict())

@app.get('/colour')
def get_colour(data_directory):
    list_of_files = os.listdir(data_directory)
    filename = list_of_files[0]
    input_image = cv2.imread(os.path.join(data_directory, filename))
    sorted_indices, sorted_similarities,sorted_filenames = CBIR_colour.compareimage(input_image, data_directory)
    arrHasil=[]
    for i in range(len(sorted_similarities)):
        sim=[]
        sim.append(sorted_similarities[i])
        sim.append(sorted_filenames[i])
        arrHasil.append(sim)


@app.post('/colour')
def insert_colour(data_director):

    list_of_files = os.listdir(data_director)
    array=[]
    pathCSV = os.path.abspath("data.csv")
    pathCSV = os.path.join(pathCSV.replace('\\', '/'))
    for filename in list_of_files:
        dataset_image = cv2.imread(os.path.join(data_director, filename))
        histogram = CBIR_colour.calculate_histogram(dataset_image)
        array.append({
            "histogram":histogram,
            "filepath":filename
        })
    with open(pathCSV, 'w', newline='') as csv_file:
        fieldnames = ['histogram', 'filepath']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in array:
            writer.writerow(row)

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    start_time = time.time()
    image_content = await file.read()
    nparr = np.frombuffer(image_content, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    vektor1 = driver.tekstur(img)

    result_filter = dataBaseBaru.find({})
    result_filter = list(result_filter)

    arrHasil = []
    file=[]
    sim = []
    for i in range(len(result_filter)):
        vektor2 = [result_filter[i].get('contrast'),result_filter[i].get('homogency'),result_filter[i].get('entropy')]
        hasil = driver.compare(vektor1,vektor2)*100
        sim.append(hasil)
        file.append(result_filter[i].get('filepath'))
    sorted_indices = np.argsort(sim)[::-1]
    sorted_similarities = np.sort(sim)[::-1]
    sorted_filenames = [file[i] for i in sorted_indices]
    hasil = []
    for i in range(len(sorted_indices)):
        image = cv2.imread(os.path.join(folder_path, sorted_filenames[i]))
        _,buffer = cv2.imencode('.JPG',image)
        image_encode = base64.b64encode(buffer.tobytes()).decode("utf-8")
        if(sorted_similarities[i]>=60):
            hasil.append({
                "persentase":sorted_similarities[i],
                "images":image_encode
            })
    end_time = time.time()
    global global_waktu 
    global_waktu = end_time - start_time
    return hasil
    
@app.post("/uploadfile2/")
async def create_upload_file(file: UploadFile = File(...)):
    start_time = time.time()
    image_content = await file.read()
    arrHasil = []
    nparr = np.frombuffer(image_content, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    pathCSV = os.path.abspath("data.csv")
    pathCSV = os.path.join(pathCSV.replace('\\', '/'))
    print(pathCSV)
    sorted_indices, sorted_similarities,sorted_filenames = CBIR_colour.compareimagehsv(img, pathCSV)
    hasil = []
    for i in range(len(sorted_indices)):
        image = cv2.imread(os.path.join(folder_path, sorted_filenames[i]))
        _,buffer = cv2.imencode('.JPG',image)
        image_encode = base64.b64encode(buffer.tobytes()).decode("utf-8")
        if(sorted_similarities[i]>=60):
            hasil.append({
                "persentase":sorted_similarities[i],
                "images":image_encode
            })
    print("sukses")
    end_time = time.time()
    global global_waktu 
    global_waktu = end_time - start_time
    return hasil

@app.post("/upload")
async def upload_files(file: UploadFile = File(...)):
    print("tess")
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, file.filename.replace('/', '_'))
    arrrFIle.append(file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())


@app.post("/uploadtodatabase")
async def upload_files_toDB():
    insert_tekstur(folder_path,"tesss")
    insert_colour(folder_path)
    print("sukses")

@app.post("/hapusdataset")
async def upload_files_toDB():
    arrrFIle=[]
    delete_files_in_folder(folder_path)

@app.get("/hasil/{namafile}")
def get_image(namafile:str):
    list_of_files = os.listdir(folder_path)
    for img in list_of_files:
        if img == namafile:
            return (cv2.imread(os.path.join(folder_path, img)))
        
@app.post("/time")
async def timee():
    return global_waktu
        