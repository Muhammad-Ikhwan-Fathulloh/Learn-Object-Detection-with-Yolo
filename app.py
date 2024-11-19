import base64
import json

import cv2
import numpy as np
import redis
from ultralytics import YOLO

# Connect to Redis
redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)

# Load the custom YOLOv8 model
model = YOLO("best_model.pt")  # Replace with the path to your custom model


def decode_base64_image(encoded_data):
    """Decodes a base64 encoded image back to OpenCV format."""
    image_data = base64.b64decode(encoded_data)
    np_arr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img


def process_image(image):
    """Runs the YOLOv8 model on the image and returns results."""
    results = model(image)
    detected_objects = []

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            detected_object = {"xyxy": [x1, y1, x2, y2]}
            detected_objects.append((detected_object))

    # for i in range(len(results.xyxy)):
    #     left, top, right, bottom = results.xyxy[i].cpu().numpy()
    #     conf = results.conf[i].item()
    #     class_id = results.cls[i].item()
    #     class_name = model.names[class_id]
    #
    #     detected_object = {
    #         "xywh": [left, top, right, bottom],
    #         "class_name": class_name,
    #         "confidence": conf,
    #     }
    #     detected_objects.append(detected_object)

    return detected_objects


def listen_and_serve():
    """Listens to the Redis PubSub and serves the model."""
    pubsub = redis_client.pubsub()
    pubsub.subscribe("stream-ingestion")

    for message in pubsub.listen():
        if message["type"] == "message":
            encoded_image = message["data"].decode("utf-8")

            # Decode the base64 image
            image = decode_base64_image(encoded_image)

            # Run inference with YOLOv8
            objects = process_image(image)

            # Prepare the result JSON
            result = json.dumps({"objects": objects})

            # Publish the result to Redis PubSub with topic 'ai-result'
            redis_client.publish("ai-result", result)
            print(f"Published AI result to 'ai-result': {result}")


if __name__ == "__main__":
    listen_and_serve()
