from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ultralytics import YOLO
import cv2
import numpy as np
import base64
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust based on your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load YOLO model
model_path = "best_model.pt"  # Ensure this path is correct
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file {model_path} not found.")

model = YOLO(model_path)

# Utility functions
def read_image_from_upload(file: UploadFile):
    """Reads an uploaded image and converts it to an OpenCV format."""
    contents = file.file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

def detect_mask(image):
    """Runs YOLOv8 detection on the input image."""
    results = model(image)
    detections = []
    mask_img = image.copy()
    no_mask_img = image.copy()

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            class_name = model.names[int(box.cls[0])]
            category = "Pakai Masker" if class_name == "mask" else "Tidak Pakai Masker"
            detections.append({
                "category": category,
                "bounding_box": [x1, y1, x2, y2]
            })
            color = (0, 255, 0) if category == "Pakai Masker" else (0, 0, 255)
            cv2.rectangle(
                mask_img if category == "Pakai Masker" else no_mask_img,
                (x1, y1),
                (x2, y2),
                color,
                2,
            )

    return detections, mask_img, no_mask_img

def encode_image_to_base64(image):
    """Encodes an OpenCV image to base64 format."""
    _, buffer = cv2.imencode(".jpg", image)
    return base64.b64encode(buffer).decode("utf-8")

# Request and response models
class PredictionResponse(BaseModel):
    category: str
    bounding_box: list

class FullResponse(BaseModel):
    detections: list[PredictionResponse]
    mask_image: str
    no_mask_image: str

@app.post("/predict", response_model=FullResponse)
async def predict(file: UploadFile = File(...)):
    try:
        image = read_image_from_upload(file)
        detections, mask_img, no_mask_img = detect_mask(image)
        return {
            "detections": detections,
            "mask_image": encode_image_to_base64(mask_img),
            "no_mask_image": encode_image_to_base64(no_mask_img),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "Mask detection API is running!"}