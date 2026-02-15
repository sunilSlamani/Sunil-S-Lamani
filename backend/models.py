from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class DiagnosisSchema(BaseModel):
    date: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"))
    disease: str
    treatment: str
    prevention: str
    english: Optional[str] = ""
    kannada: Optional[str] = ""
    crop: Optional[str] = "Unknown"
    image_url: Optional[str] = ""

class TTSSchema(BaseModel):
    text: str
    lang: str = "en" # en or kn

class CropSchema(BaseModel):
    name: str
    kannada_name: str
    icon: str
    diseases: List[str]
