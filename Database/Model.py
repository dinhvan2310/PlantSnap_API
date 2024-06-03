from typing import List, Optional
from pydantic import BaseModel
from bson import ObjectId

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

class TokenRefresh(BaseModel):
    access_token: str
    token_type: str



class Feedback(BaseModel):
    id_user : str
    descriptionIncorrect : bool
    detectedIncorrectly : bool
    feedback : str
    other : bool
    plantid : int
    statusIncorrect : bool
    timestamp : int


class History(BaseModel):
    id_hist : str
    id_user : str
    common_name: str
    image_url : str
    plantid: int
    scientific_name: str
    status: bool
    timestamp: int

class User(BaseModel):
    id_user: str
    email: str
    name: str
    password: str
    photoURL: str

class TokenData(BaseModel):
    id_user: str

class Plant(BaseModel):
    id_leaf: int
    name: str
    scientific_name: str
    another_name: Optional[str] = None
    url_image: List[str]
    description: str
    ingredient: Optional[str] = None
    uses: Optional[str] = None
    medicine: Optional[str] = None
    effect_medicine: Optional[str] = None
    note_use: Optional[str] = None