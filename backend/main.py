from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from datetime import datetime
import base64
from typing import List

from database import add_diagnosis, retrieve_diagnoses, retrieve_diagnosis, delete_diagnosis
from models import DiagnosisSchema, TTSSchema, CropSchema

# Import emergentintegrations
try:
    from emergentintegrations import LlmChat, OpenAITextToSpeech
except ImportError:
    LlmChat = None
    OpenAITextToSpeech = None

load_dotenv()

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

EMERGENT_LLM_KEY = os.getenv("EMERGENT_LLM_KEY")

# Supported crops data
SUPPORTED_CROPS = [
    {
        "name": "Potato",
        "kannada_name": "ಆಲೂಗಡ್ಡೆ",
        "icon": "🥔",
        "diseases": ["Early Blight", "Late Blight", "Healthy"]
    },
    {
        "name": "Tomato",
        "kannada_name": "ಟೊಮ್ಯಾಟೊ",
        "icon": "🍅",
        "diseases": ["Early Blight", "Late Blight", "Healthy"]
    }
]

@app.get("/api/crops", response_model=List[CropSchema])
async def get_crops():
    return SUPPORTED_CROPS

@app.post("/api/diagnose")
async def diagnose_crop(image: UploadFile = File(...)):
    if not LlmChat:
        raise HTTPException(status_code=500, detail="AI module not available")
    
    # Read image content
    contents = await image.read()
    base64_image = base64.b64encode(contents).decode('utf-8')
    
    # Initialize LLM with GPT-5.2 vision
    llm = LlmChat(model="gpt-5.2", api_key=EMERGENT_LLM_KEY)
    
    prompt = """
    Analyze this crop leaf image. Identify the disease (if any).
    Return a JSON object with:
    - disease: Disease name (or 'Healthy')
    - treatment: Short treatment instructions in English
    - prevention: Short prevention tips in English
    - kannada_diagnosis: Disease name and treatment in Kannada
    - crop: Type of crop (Potato/Tomato/etc.)
    """
    
    try:
        # Assuming emergentintegrations supports vision in this way
        response = await llm.achat(prompt, images=[base64_image])
        # In a real scenario, you'd parse the JSON from response.content
        # For this implementation, let's assume it returns a structured dict or we parse it
        import json
        diagnosis_result = json.loads(response.content)
        
        record = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "disease": diagnosis_result.get("disease", "Unknown"),
            "treatment": diagnosis_result.get("treatment", "Consult expert"),
            "prevention": diagnosis_result.get("prevention", "Maintain hygiene"),
            "english": f"{diagnosis_result.get('disease')}. {diagnosis_result.get('treatment')}",
            "kannada": diagnosis_result.get("kannada_diagnosis", "ಮಾಹಿತಿ ಲಭ್ಯವಿಲ್ಲ"),
            "crop": diagnosis_result.get("crop", "Unknown"),
            "image_url": f"data:image/jpeg;base64,{base64_image}" # Simplified for history
        }
        
        saved_record = await add_diagnosis(record)
        return saved_record
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/diagnoses")
async def get_history():
    return await retrieve_diagnoses()

@app.get("/api/diagnoses/{id}")
async def get_diagnosis(id: str):
    diagnosis = await retrieve_diagnosis(id)
    if diagnosis:
        return diagnosis
    raise HTTPException(status_code=404, detail="Diagnosis not found")

@app.delete("/api/diagnoses/{id}")
async def remove_diagnosis(id: str):
    deleted = await delete_diagnosis(id)
    if deleted:
        return {"message": "Diagnosis deleted successfully"}
    raise HTTPException(status_code=404, detail="Diagnosis not found")

@app.post("/api/tts")
async def text_to_speech(data: TTSSchema):
    if not OpenAITextToSpeech:
        raise HTTPException(status_code=500, detail="TTS module not available")
    
    try:
        tts = OpenAITextToSpeech(api_key=EMERGENT_LLM_KEY)
        # Assuming voice selection based on language
        voice = "alloy" # Default
        if data.lang == "kn":
            voice = "shimmer" # Example mapping
            
        audio_content = await tts.generate(data.text, voice=voice)
        base64_audio = base64.b64encode(audio_content).decode('utf-8')
        return {"audio": base64_audio}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
