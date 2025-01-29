from ultralytics import YOLO
import os

model = YOLO("best.pt")
for i, path in enumerate(os.listdir("./test_imgs/")):
    predictions = model(os.path.join("./test_imgs", path))
    for prediction in predictions:
        prediction.save(f"./predictions/{i+1}.jpg")