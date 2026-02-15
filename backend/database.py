import motor.motor_asyncio
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.kisan_sahayak
diagnosis_collection = database.get_collection("diagnoses")

# Helper to convert Mongo document to dict
def diagnosis_helper(diagnosis) -> dict:
    return {
        "id": str(diagnosis["_id"]),
        "date": diagnosis["date"],
        "disease": diagnosis["disease"],
        "treatment": diagnosis["treatment"],
        "prevention": diagnosis["prevention"],
        "english": diagnosis.get("english", ""),
        "kannada": diagnosis.get("kannada", ""),
        "crop": diagnosis.get("crop", "Unknown"),
        "image_url": diagnosis.get("image_url", "")
    }

async def add_diagnosis(diagnosis_data: dict) -> dict:
    diagnosis = await diagnosis_collection.insert_one(diagnosis_data)
    new_diagnosis = await diagnosis_collection.find_one({"_id": diagnosis.inserted_id})
    return diagnosis_helper(new_diagnosis)

async def retrieve_diagnoses():
    diagnoses = []
    async for diagnosis in diagnosis_collection.find().sort("date", -1):
        diagnoses.append(diagnosis_helper(diagnosis))
    return diagnoses

async def retrieve_diagnosis(id: str) -> dict:
    diagnosis = await diagnosis_collection.find_one({"_id": ObjectId(id)})
    if diagnosis:
        return diagnosis_helper(diagnosis)

async def delete_diagnosis(id: str):
    diagnosis = await diagnosis_collection.find_one({"_id": ObjectId(id)})
    if diagnosis:
        await diagnosis_collection.delete_one({"_id": ObjectId(id)})
        return True
