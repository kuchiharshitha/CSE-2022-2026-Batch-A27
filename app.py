
from flask import Flask, render_template, request, jsonify
import torch
import base64
import numpy as np
import cv2

app = Flask(__name__)

# Load YOLO model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/detect')
def detect():
    return render_template("detect.html")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json['image']

    img_data = base64.b64decode(data.split(',')[1])
    np_arr = np.frombuffer(img_data, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    results = model(frame)
    detections = results.pandas().xyxy[0]

    height, width, _ = frame.shape
    output = []

    for _, row in detections.iterrows():
        label = row['name']
        x1, x2 = int(row['xmin']), int(row['xmax'])
        center = (x1 + x2) // 2

        if center < width // 3:
            direction = "left"
        elif center > 2 * width // 3:
            direction = "right"
        else:
            direction = "center"

        distance = "near" if row['confidence'] > 0.5 else "far"

        output.append({
            "label": label,
            "xmin": int(row['xmin']),
            "ymin": int(row['ymin']),
            "xmax": int(row['xmax']),
            "ymax": int(row['ymax']),
            "sentence": f"{label} is {distance} on your {direction}"
        })

    return jsonify(output)

if __name__ == "__main__":
=======
from flask import Flask, render_template, request, jsonify
import torch
import base64
import numpy as np
import cv2

app = Flask(__name__)

# Load YOLO model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/detect')
def detect():
    return render_template("detect.html")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json['image']

    img_data = base64.b64decode(data.split(',')[1])
    np_arr = np.frombuffer(img_data, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    results = model(frame)
    detections = results.pandas().xyxy[0]

    height, width, _ = frame.shape
    output = []

    for _, row in detections.iterrows():
        label = row['name']
        x1, x2 = int(row['xmin']), int(row['xmax'])
        center = (x1 + x2) // 2

        if center < width // 3:
            direction = "left"
        elif center > 2 * width // 3:
            direction = "right"
        else:
            direction = "center"

        distance = "near" if row['confidence'] > 0.5 else "far"

        output.append({
            "label": label,
            "xmin": int(row['xmin']),
            "ymin": int(row['ymin']),
            "xmax": int(row['xmax']),
            "ymax": int(row['ymax']),
            "sentence": f"{label} is {distance} on your {direction}"
        })

    return jsonify(output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
