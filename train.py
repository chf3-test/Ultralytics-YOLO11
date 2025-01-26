from ultralytics import YOLO

# Load a model
# model = YOLO("yolo11n.yaml")  # build a new model from YAML
model = YOLO("yolo11l.pt")  # load a pretrained model (recommended for training)
# model = YOLO("yolo11n.yaml").load("yolo11n.pt")  # build from YAML and transfer weights

# Train the model
results = model.train(data="dataset.yaml", 
                      epochs=50, 
                      imgsz=640,
                      workers=0,
                      device=0,
                      batch=0.999,
                      cos_lr=True,
                      dropout=0.1,
                      iou=0.6,
                      patience=50,
                      conf=0.5,
                      half=False)
