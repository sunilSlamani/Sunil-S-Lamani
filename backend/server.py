from fastapi import FastAPI, APIRouter, UploadFile, File, Form 
from dotenv import load_dotenv 
from starlette.middleware.cors import CORSMiddleware 
from motor.motor_asyncio import AsyncIOMotorClient 
import os 
import logging 
import base64 
import json 
from pathlib import Path 
from pydantic import BaseModel, Field, ConfigDict 
from typing import List, Optional 
import uuid 
from datetime import datetime, timezone 

ROOT_DIR = Path(__file__).parent 
load_dotenv(ROOT_DIR / '.env') 

# MongoDB connection 
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017') 
client = AsyncIOMotorClient(mongo_url) 
db = client[os.environ.get('DB_NAME', 'kisan_sahayak')] 

app = FastAPI() 
api_router = APIRouter(prefix="/api") 

# Configure logging 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
logger = logging.getLogger(__name__) 

# --- Models --- 
class DiagnosisResult(BaseModel): 
    model_config = ConfigDict(extra="ignore") 
    id: str = Field(default_factory=lambda: str(uuid.uuid4())) 
    crop_name: str = "" 
    disease_name: str = "" 
    is_healthy: bool = False 
    confidence: str = "" 
    symptoms: List[str] = [] 
    treatment: List[str] = [] 
    prevention: List[str] = [] 
    description: str = "" 
    description_kn: str = "" 
    disease_name_kn: str = "" 
    crop_name_kn: str = "" 
    treatment_kn: List[str] = [] 
    prevention_kn: List[str] = [] 
    symptoms_kn: List[str] = [] 
    image_base64: str = "" 
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat()) 

class TTSRequest(BaseModel): 
    text: str 
    language: str = "en" 

class CropInfo(BaseModel): 
    name: str 
    name_kn: str 
    icon: str 
    common_diseases: List[str] 
    common_diseases_kn: List[str] 


# --- Crop Catalog --- 
CROP_CATALOG = [ 
    {"name": "Tomato", "name_kn": "ಟೊಮ್ಯಾಟೊ", "icon": "tomato", 
     "common_diseases": ["Early Blight", "Late Blight", "Leaf Mold", "Septoria Leaf Spot", "Spider Mites", "Target Spot", "Yellow Leaf Curl Virus", "Mosaic Virus", "Bacterial Spot"], 
     "common_diseases_kn": ["ಮುಂಚಿನ ಕೊಳೆ", "ತಡವಾದ ಕೊಳೆ", "ಎಲೆ ಅಚ್ಚು", "ಸೆಪ್ಟೋರಿಯಾ ಎಲೆ ಚುಕ್ಕೆ", "ಜೇಡ ಹುಳು", "ಗುರಿ ಚುಕ್ಕೆ", "ಹಳದಿ ಎಲೆ ಸುರುಳಿ ವೈರಸ್", "ಮೊಸಾಯಿಕ್ ವೈರಸ್", "ಬ್ಯಾಕ್ಟೀರಿಯಾ ಚುಕ್ಕೆ"]}, 
    {"name": "Potato", "name_kn": "ಆಲೂಗಡ್ಡೆ", "icon": "potato", 
     "common_diseases": ["Early Blight", "Late Blight"], 
     "common_diseases_kn": ["ಮುಂಚಿನ ಕೊಳೆ", "ತಡವಾದ ಕೊಳೆ"]}, 
    {"name": "Corn (Maize)", "name_kn": "ಜೋಳ", "icon": "corn", 
     "common_diseases": ["Common Rust", "Northern Leaf Blight", "Gray Leaf Spot", "Cercospora Leaf Spot"], 
     "common_diseases_kn": ["ಸಾಮಾನ್ಯ ತುಕ್ಕು", "ಉತ್ತರ ಎಲೆ ಕೊಳೆ", "ಬೂದು ಎಲೆ ಚುಕ್ಕೆ", "ಸೆರ್ಕೊಸ್ಪೊರಾ ಎಲೆ ಚುಕ್ಕೆ"]}, 
    {"name": "Apple", "name_kn": "ಸೇಬು", "icon": "apple", 
     "common_diseases": ["Apple Scab", "Black Rot", "Cedar Apple Rust"], 
     "common_diseases_kn": ["ಸೇಬು ಖರೆ", "ಕಪ್ಪು ಕೊಳೆ", "ಸೀಡರ್ ಸೇಬು ತುಕ್ಕು"]}, 
    {"name": "Grape", "name_kn": "ದ್ರಾಕ್ಷಿ", "icon": "grape", 
     "common_diseases": ["Black Rot", "Esca (Black Measles)", "Leaf Blight"], 
     "common_diseases_kn": ["ಕಪ್ಪು ಕೊಳೆ", "ಎಸ್ಕಾ (ಕಪ್ಪು ದದ್ದು)", "ಎಲೆ ಕೊಳೆ"]}, 
    {"name": "Rice", "name_kn": "ಅಕ್ಕಿ", "icon": "rice", 
     "common_diseases": ["Blast", "Brown Spot", "Sheath Blight", "Bacterial Leaf Blight"], 
     "common_diseases_kn": ["ಬ್ಲಾಸ್ಟ್", "ಕಂದು ಚುಕ್ಕೆ", "ಕವಚ ಕೊಳೆ", "ಬ್ಯಾಕ್ಟೀರಿಯಾ ಎಲೆ ಕೊಳೆ"]}, 
    {"name": "Pepper (Bell)", "name_kn": "ಮೆಣಸಿನಕಾಯಿ", "icon": "pepper", 
     "common_diseases": ["Bacterial Spot"], 
     "common_diseases_kn": ["ಬ್ಯಾಕ್ಟೀರಿಯಾ ಚುಕ್ಕೆ"]}, 
    {"name": "Cherry", "name_kn": "ಚೆರ್ರಿ", "icon": "cherry", 
     "common_diseases": ["Powdery Mildew"], 
     "common_diseases_kn": ["ಪುಡಿ ಶಿಲೀಂಧ್ರ"]}, 
    {"name": "Strawberry", "name_kn": "ಸ್ಟ್ರಾಬೆರಿ", "icon": "strawberry", 
     "common_diseases": ["Leaf Scorch"], 
     "common_diseases_kn": ["ಎಲೆ ಸುಡು"]}, 
    {"name": "Peach", "name_kn": "ಪೀಚ್", "icon": "peach", 
     "common_diseases": ["Bacterial Spot"], 
     "common_diseases_kn": ["ಬ್ಯಾಕ್ಟೀರಿಯಾ ಚುಕ್ಕೆ"]}, 
] 


# --- Endpoints --- 

@api_router.get("/crops", response_model=List[CropInfo]) 
async def get_crops(): 
    return CROP_CATALOG 

@api_router.get("/diagnoses", response_model=List[DiagnosisResult]) 
async def get_diagnoses(): 
    diagnoses = [] 
    async for d in db.diagnoses.find().sort("timestamp", -1): 
        d['id'] = str(d.pop('_id')) 
        diagnoses.append(DiagnosisResult(**d)) 
    return diagnoses 

@api_router.get("/diagnoses/{id}", response_model=DiagnosisResult) 
async def get_diagnosis(id: str): 
    from bson import ObjectId 
    d = await db.diagnoses.find_one({"_id": ObjectId(id)}) 
    if d: 
        d['id'] = str(d.pop('_id')) 
        return DiagnosisResult(**d) 
    return None 

@api_router.delete("/diagnoses/{id}") 
async def delete_diagnosis(id: str): 
    from bson import ObjectId 
    result = await db.diagnoses.delete_one({"_id": ObjectId(id)}) 
    return {"deleted": result.deleted_count > 0} 

@api_router.post("/diagnose", response_model=DiagnosisResult) 
async def diagnose_crop(file: UploadFile = File(...), language: str = Form("en")): 
    try: 
        from emergentintegrations.llm.chat import LlmChat, UserMessage, ImageContent 
        from emergentintegrations.llm.openai import OpenAITextToSpeech 

        contents = await file.read() 
        image_b64 = base64.b64encode(contents).decode("utf-8") 

        api_key = os.environ.get("EMERGENT_LLM_KEY", "") 
        llm = LlmChat(model="gpt-5.2", api_key=api_key) 

        system_prompt = """You are an expert agricultural scientist specializing in crop disease detection. 
Analyze the uploaded crop/plant image and return a JSON object with these fields: 
{ 
  "crop_name": "Name of the crop/plant", 
  "disease_name": "Name of the disease, or 'Healthy' if no disease", 
  "is_healthy": true/false, 
  "confidence": "High/Medium/Low", 
  "symptoms": ["list of visible symptoms"], 
  "treatment": ["list of treatment recommendations"], 
  "prevention": ["list of prevention tips"], 
  "description": "Brief description of the diagnosis in English", 
  "description_kn": "Brief description in Kannada", 
  "disease_name_kn": "Disease name in Kannada", 
  "crop_name_kn": "Crop name in Kannada", 
  "treatment_kn": ["treatment list in Kannada"], 
  "prevention_kn": ["prevention list in Kannada"], 
  "symptoms_kn": ["symptoms list in Kannada"] 
}""" 

        messages = [ 
            UserMessage(content=[ 
                {"type": "text", "text": "Diagnose this crop disease."}, 
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}} 
            ]) 
        ] 

        response = await llm.achat(messages, system_prompt=system_prompt, response_format={"type": "json_object"}) 
        diagnosis_data = json.loads(response.content) 
        
        # Add image and timestamp 
        diagnosis_data["image_base64"] = image_b64 
        diagnosis_data["timestamp"] = datetime.now(timezone.utc).isoformat() 

        # Save to DB 
        result = await db.diagnoses.insert_one(diagnosis_data) 
        diagnosis_data["id"] = str(result.inserted_id) 
        
        return DiagnosisResult(**diagnosis_data) 

    except Exception as e: 
        logger.error(f"Diagnosis error: {e}") 
        return None 

@api_router.post("/tts") 
async def text_to_speech(request: TTSRequest): 
    try: 
        from emergentintegrations.llm.openai import OpenAITextToSpeech 
        
        api_key = os.environ.get("EMERGENT_LLM_KEY", "") 
        tts = OpenAITextToSpeech(api_key=api_key) 
        
        # Select voice based on language 
        voice = "alloy" if request.language == "en" else "shimmer" 
        
        audio_content = await tts.generate(request.text, voice=voice) 
        return {"audio": base64.b64encode(audio_content).decode("utf-8")} 
    except Exception as e: 
        logger.error(f"TTS error: {e}") 
        return {"error": str(e)} 

app.include_router(api_router) 

# CORS 
app.add_middleware( 
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"], 
) 

if __name__ == "__main__": 
    import uvicorn 
    uvicorn.run(app, host="0.0.0.0", port=8000)
