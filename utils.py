import requests
from ultralytics import YOLO
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
from PIL import Image
import hashlib
import re
from connect_firebase import bucket
import cv2
from bson import ObjectId

# Load model classification
def _load_model_cls():
    interpreter = tf.lite.Interpreter(model_path="assets/model.tflite")
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    return (interpreter, input_details, output_details)

# # Load model detection
# def _load_model_yolo():
#     return YOLO('assets/best.pt')
		

# Resize ảnh
def _preprocess_image(img, shape):
    img_rz = img.resize(shape)
    img_rz = img_to_array(img_rz)
    img_rz = img_rz / 255.0
    img_rz = np.expand_dims(img_rz, axis=0)
    return img_rz

def _load_image_from_url(url):
    img = Image.open(requests.get(url, stream=True).raw)
    return img

# Validate Email
def _validate_email(email):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    return False

# Validate Password, password must contain at least 6 characters, must contain at least one digit
def _validate_password(password):
    if len(password) < 6:
        return False
    if not re.search(r"\d", password):
        return False
    return True

# Hash Password
def _hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_image(image_name):
    image = bucket.blob(image_name)
    arr = np.frombuffer(image.download_as_string(), np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return img

def upload_image(image_array):
    image = cv2.imencode('.jpg', image_array)[1].tobytes()
    # TẠO tên ảnh ngẫu nhiên
    image_name = str(ObjectId()) + ".jpg"
    blob = bucket.blob(image_name)
    blob.upload_from_string(image, content_type='image/jpg')
    blob.make_public()
    return blob.public_url