import base64
import os
import time
from pathlib import Path

import redis

# Connect to Redis
redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)

# Folder where images are stored
image_folder = "images"


def encode_image_to_base64(image_path):
    """Encodes an image file to base64 format."""
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string


def stream_images():
    """Continuously reads images and publishes them to Redis PubSub."""
    while True:
        # Iterate through all image files in the folder
        for image_file in Path(image_folder).glob(
            "*.*"
        ):  # Adjust if you want to filter by file type (e.g., *.jpg)
            if image_file.is_file():
                # Encode the image
                encoded_image = encode_image_to_base64(image_file)

                # Publish to Redis PubSub
                redis_client.publish("stream-ingestion", encoded_image)

                print(f"Published {image_file.name} to Redis PubSub")

        # Wait before next iteration (optional, adjust the interval)
        time.sleep(0.1)


if __name__ == "__main__":
    stream_images()
