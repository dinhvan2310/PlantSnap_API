from bson import ObjectId
import firebase_admin
from firebase_admin import credentials, storage
import numpy as np
import cv2
# Đường dẫn đến tệp JSON chứng chỉ
cred = credentials.Certificate('database-cd253-firebase-adminsdk-c3mzf-cd49b6f928.json')

# Khởi tạo ứng dụng Firebase
firebase_admin.initialize_app(cred, {
    'storageBucket': 'database-cd253.appspot.com'
})

bucket = storage.bucket()





