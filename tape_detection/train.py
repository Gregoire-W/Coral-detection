from ultralytics import YOLO

# Load pre-trained model
model = YOLO("yolo11s.pt") 

results = model.train(data="./dataset/data.yaml", epochs=100, imgsz=640)