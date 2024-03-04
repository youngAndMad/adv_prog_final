from fastapi import FastAPI,UploadFile
from ai import detect_car_plates, extract_texts_from_directory
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from generator import generate_random_string 

app = FastAPI() # uvicorn main:app --reload

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data_video_path='data/video'
data_image_path='data/image'

os.makedirs(data_video_path, exist_ok=True)
os.makedirs(data_image_path, exist_ok=True)

@app.post("/upload/image")
async def upload_image(file: UploadFile):
    upload_id = generate_random_string()
    directory = os.path.join(data_image_path, upload_id)
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    possible_texts = extract_texts_from_directory(directory)    
    
    os.remove(file_path)
    os.remove(directory)
        
    return {'result': possible_texts}

@app.post("/upload/video")
async def upload_video(file: UploadFile):
    upload_id = generate_random_string()
    directory = os.path.join(data_video_path, upload_id)
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, file.filename)
    
    print(file_path)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    output_path = generate_random_string()
    output_path_directory = os.path.join(data_image_path,output_path)
    
    texts_saved = detect_car_plates(file_path,output_path_directory)
    print(texts_saved)
    
    possible_texts = extract_texts_from_directory(output_path_directory)    
    
    os.remove(file_path)
    os.remove(output_path_directory)
    os.remove(directory)
        
    return {'result': possible_texts}
    
