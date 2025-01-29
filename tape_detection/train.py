from ultralytics import YOLO

# Load pre-trained model
model = YOLO("yolo11m.pt") 

results = model.train(data="./data.yaml", epochs=100, imgsz=640)