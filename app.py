import cv2
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import utils
import numpy as np
from fastapi import FastAPI, HTTPException
from PIL import Image
from Database.Mongo import db
import Database.Model as Model
import io
from bson import ObjectId
import connect_firebase
from fastapi import FastAPI, Depends, HTTPException
from datetime import timedelta
from auth import (
    create_access_token,
    create_refresh_token,
)
import auth


app = FastAPI()

(interpreter, input_details, output_details) = utils._load_model_cls()
# model_yolo = utils._load_model_yolo()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

history_collection = db["History"]
feedback_collection = db["Feedback"]
user_collection = db["User"]
plant_collection = db["Plant"]


@app.get("/api/plants")
async def plant_data():
    try:
        plants = []
        cursor = plant_collection.find()
        for plant in cursor:
            plant_data = {
                "id_leaf": plant["id_leaf"],
                "name": plant["name"],
                "scientific_name": plant["scientific_name"],
                "another_name": plant["another_name"],
                "url_image": plant["url_image"],
                "description": plant["description"],
                "ingredient": plant["ingredient"],
                "uses": plant["uses"],
                "medicine": plant["medicine"],
                "effect_medicine": plant["effect_medicine"],
                "note_use": plant["note_use"]
            }
            plants.append(plant_data)
        return plants
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/plants/{id_leaf}")
async def plant_data(id_leaf: int):
    try:
        plant = plant_collection.find_one({"id_leaf": id_leaf})
        if plant is None:
            raise HTTPException(status_code=404, detail="Not found")
        plant_data = {
            "id_leaf": plant["id_leaf"],
            "name": plant["name"],
            "scientific_name": plant["scientific_name"],
            "another_name": plant["another_name"],
            "url_image": plant["url_image"],
            "description": plant["description"],
            "ingredient": plant["ingredient"],
            "uses": plant["uses"],
            "medicine": plant["medicine"],
            "effect_medicine": plant["effect_medicine"],
            "note_use": plant["note_use"]
        }
        return plant_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/predict")
async def create_upload_file(file: UploadFile = File(...)  ):
    try:
        data = {"success": False}
        image = Image.open(io.BytesIO(await file.read())).convert('RGB')
        if image:
            image_rz = utils._preprocess_image(image, (224, 224))
            interpreter.set_tensor(input_details[0]['index'], image_rz)
            interpreter.invoke()
            status = interpreter.get_tensor(output_details[0]['index'])[0][0]
            prediction = interpreter.get_tensor(output_details[1]['index'])[0]
            plant_id_top1 = np.argmax(prediction)
            plant_id_top2 = np.argsort(prediction)[-2]
            plant_id_top3 = np.argsort(prediction)[-3]
            score_top1 = prediction[plant_id_top1]
            score_top2 = prediction[plant_id_top2]
            score_top3 = prediction[plant_id_top3]
            data["data"] = {
                "status": str(status),
                "plant_id_top1": str(plant_id_top1),
                "plant_id_top2": str(plant_id_top2),
                "plant_id_top3": str(plant_id_top3),
                "score_top1": str(score_top1),
                "score_top2": str(score_top2),
                "score_top3": str(score_top3)
            }
            data["success"] = True
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/history")
async def get_history(
    current_user: Model.TokenData = Depends(auth.get_current_user)
):
    try:
        query = {}
        if current_user:
            query["id_user"] = current_user
        
        histories = []
        cursor = history_collection.find(query)
        for history in cursor:
            history_data = {
                "id_hist": (history["id_hist"]), 
                "id_user": history["id_user"],
                "common_name": history["common_name"],
                "image_url": history["image_url"],
                "plantid": history["plantid"],
                "scientific_name": history["scientific_name"],
                "status": history["status"],
                "timestamp": history["timestamp"]
            }

            histories.append(history_data)
        return histories
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/history/{id_hist}")
async def get_history(
    current_user: Model.TokenData = Depends(auth.get_current_user),
    id_hist: str = None
):
    try:
        query = {}
        query["id_hist"] = id_hist
        query["id_user"] = current_user
        history = history_collection.find_one(query)
        if history is None:
            raise HTTPException(status_code=404, detail="Not found")
        history_data = {
            "id_hist": (history["id_hist"]), 
            "id_user": history["id_user"],
            "common_name": history["common_name"],
            "image_url": history["image_url"],
            "plantid": history["plantid"],
            "scientific_name": history["scientific_name"],
            "status": history["status"],
            "timestamp": history["timestamp"]
        }
        return history_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/history")
async def add_history(
    current_user: Model.TokenData = Depends(auth.get_current_user),
    common_name: str = Form(...),
    plantid: int = Form(...),
    scientific_name: str = Form(...),
    status: bool = Form(...),
    timestamp: int = Form(...),
    file: UploadFile = File(...)   
):
    try:
        contents = await file.read()
        image_arr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(image_arr, cv2.IMREAD_COLOR)
        image_url = utils.upload_image(image)

        history_data = {
            "id_hist": str(ObjectId()),
            "id_user": current_user,
            "common_name": common_name,
            "image_url": image_url,
            "plantid": plantid,
            "scientific_name": scientific_name,
            "status": status,
            "timestamp": timestamp
        }
        history = Model.History(**history_data)

        history_dict = history.model_dump()
        history_collection.insert_one(history_dict)

        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@app.delete("/api/history/{id_hist}")
async def delete_history(current_user: Model.TokenData = Depends(auth.get_current_user), id_hist: str = None):
    try:
        query = {}
        query["id_hist"] = id_hist
        query["id_user"] = current_user
        rs = history_collection.delete_one(query)

        if rs.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Not found")

        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.post("/api/feedback")
async def get_feedback(
    current_user: Model.TokenData = Depends(auth.get_current_user),  
    descriptionIncorrect: bool = Form(...),
    detectedIncorrectly: bool = Form(...),
    feedback: str = Form(None),
    other: bool = Form(...),
    plantid: int = Form(...),
    statusIncorrect: bool = Form(...),
    timestamp: int = Form(...)
):
    feedback_data = {
        "id_user": current_user,
        "descriptionIncorrect": descriptionIncorrect,
        "detectedIncorrectly": detectedIncorrectly,
        "feedback": feedback if feedback else "",
        "other": other,
        "plantid": plantid,
        "statusIncorrect": statusIncorrect,
        "timestamp": timestamp
    }
    feedback = Model.Feedback(**feedback_data)
    feedback_dict = feedback.model_dump()
    feedback_collection.insert_one(feedback_dict)

    return feedback

@app.post("/api/signup")
async def signup(email: str = Form(...), password: str = Form(...), name: str = Form(...)):
    password = utils._hash_password(password)
    
    user = user_collection.find_one({"email": email})
    if user is not None:
        raise HTTPException(status_code=400, detail="Email already exists")
    user_data = {
        "id_user": str(ObjectId()),
        "email": email,
        "password": password,
        "name": name,
        "photoURL": 'https://firebasestorage.googleapis.com/v0/b/database-cd253.appspot.com/o/assets%2F360_F_359589186_JDLl8dIWoBNf1iqEkHxhUeeOulx0wOC5.jpg?alt=media&token=34bdad97-c307-4d05-a20d-b9cf3b3208a7'
    }
    user = Model.User(**user_data)

    # Thêm user vào MongoDB
    user_dict = user.model_dump()
    user_collection.insert_one(user_dict)

    return JSONResponse(content={"message": "Success"})
    
@app.post("/api/login")
async def login(email: str = Form(...), password: str = Form(...)):
    password = utils._hash_password(password)
    query = {"email": email, "password": password}
    user = user_collection.find_one(query)

    if user is None:
        raise HTTPException(status_code=404, detail="Not found")

    access_token_expires = timedelta(days=auth.ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"sub": user["id_user"]}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": user["id_user"]})

    return JSONResponse(
        content={
            "access_token": access_token,
            "token_type": "bearer",
            "refresh_token": refresh_token
        }
    )
    

@app.get("/api/user")
async def get_user(current_user: Model.TokenData = Depends(auth.get_current_user)):
    user = user_collection.find_one({"id_user": current_user})
    return JSONResponse(content={"user_id": user['id_user'], "email": user['email'], "displayName": user['name'], "photoURL": user['photoURL']})
    
@app.put("/api/user")
async def update_user(
    current_user: Model.TokenData = Depends(auth.get_current_user),
    name: str = Form(...),
    file: UploadFile = File(...) 
):
    contents = await file.read()
    image_arr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(image_arr, cv2.IMREAD_COLOR)

    image_url = utils.upload_image(image)
    user_collection.update_one({"id_user": current_user}, {"$set": {"name": name, "photoURL": image_url}})
    return JSONResponse(content={"message": "Success"})