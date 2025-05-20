from ultralytics import YOLO
import cv2

# Load model YOLOv5 pretrained
model = YOLO('yolov5s.pt')  # hoặc 'yolov8n.pt' nếu dùng YOLOv8

def detect_person(image_path):
    results = model(image_path)
    for r in results:
        for cls in r.boxes.cls:
            if int(cls) == 0:  # class 0 = 'person'
                return True
    return False
