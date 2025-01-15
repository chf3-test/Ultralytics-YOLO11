from ultralytics import YOLO
model = YOLO("new.pt")
model.export(format='onnx', imgsz=640, dynamic=False,device=0) 