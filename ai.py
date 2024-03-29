import cv2
import pytesseract
import re
import os
import easyocr

def extract_texts_from_directory(directory):
    reader = easyocr.Reader(['en'])
    resultList = []

    print(directory)
    for filename in os.listdir(directory):
        print(filename)
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
            file_path = os.path.join(directory, filename)
            result = reader.readtext(file_path)
            if result:
                print(f"Text in {filename}:")
                for detection in result:
                    if len(detection[1]) > 3:
                        resultList.append(detection[1])
                    print(detection[1]) 
                print("----")
            else:
                print(f"No text detected in {filename}")
    
    return resultList         
                

def detect_car_plates(video_path, output_path):
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\Tesseract-OCR\\tesseract.exe'

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_skip = max(total_frames // 10, 1)

    text_saved = [] 

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for frame_index in range(0, total_frames, frame_skip):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = cap.read()

        if not ret:
            break

        _, width = frame.shape[:2]

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        canny = cv2.Canny(blurred, 120, 255, 1)

        cnts = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        for i, c in enumerate(cnts):
            x, y, w, h = cv2.boundingRect(c)
            if w >= 3 * h and w <= 6 * h and w <= width / 3 and w >= width / 15:
                roi = gray[y:y+h, x:x+w]
                text = pytesseract.image_to_string(roi, lang='eng', config="--psm 11 --oem 3 -c textord_tabfind_find_tables=0 textord_tabfind_only_strokewidths_below_height_fraction=0")
                text = re.sub(r'\s+', '', text)
                text = re.sub(r'\W', '', text)
                if len(text) > 4:
                    print(f"Detected text: {text}")
                    text_saved.append(text)  

                    cv2.rectangle(frame, (x, y), (x + w, y + h), (36, 255, 12), 2)
                    cropped_region = frame[y:y+h, x:x+w]
                    cv2.imwrite(f"{output_path}/frame_{frame_index}_region_{i}.jpg", cropped_region)


    text_saved = list(set(text_saved))

    cap.release()

    print(f"All detected texts: {text_saved}")
    return text_saved