from fastapi import FastAPI
from ai import detect_car_plates, extract_texts_from_directory
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data_video_path='data_video'
data_image_path='data_image'

# @app.get('/test')
# async def ahahaha():    
#     car_plates = detect_car_plates('data/asdasd.mp4','carplates')
#     result = extract_texts_from_directory('carplates')
#     print(car_plates)
#     print(result)
#     return {
#         'text' : car_plates,
#         'result':result
#     }
    