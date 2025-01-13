from ultralytics import YOLO

# Load a pretrained YOLO11n model

model = YOLO('best.pt')
# Run inference on 'bus.jpg' with arguments
model.predict("1111.jpg",save=True,imgsz=640,conf=0.1)