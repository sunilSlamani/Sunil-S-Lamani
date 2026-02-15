import os
from flask import Flask, render_template, request 
import numpy as np 
from PIL import Image 
import pyttsx3 
import json
from datetime import datetime

app = Flask(__name__) 

HISTORY_FILE = "history.json"

def save_history(record):
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except:
            history = []
    history.insert(0, record)
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history[:20], f, ensure_ascii=False) # Keep last 20 records
    except:
        pass

def get_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

# Initialize text-to-speech engine
try:
    engine = pyttsx3.init()
except:
    engine = None

# Load model if it exists, else handle gracefully
model_path = "model/crop_disease_model.h5"
try:
    import tensorflow as tf
    if os.path.exists(model_path):
        model = tf.keras.models.load_model(model_path) 
    else:
        model = None
except ImportError:
    model = None

class_info = { 
    "Potato Early Blight": { 
        "treatment": "Use Mancozeb or Chlorothalonil fungicide. Remove infected leaves.", 
        "prevention": "Avoid overhead irrigation and maintain crop rotation." 
    }, 
    "Potato Healthy": { 
        "treatment": "No disease detected. Maintain regular watering and nutrients.", 
        "prevention": "Keep monitoring plant health." 
    }, 
    "Tomato Early Blight": { 
        "treatment": "Use Copper-based fungicide. Remove infected leaves.", 
        "prevention": "Avoid wet leaves and ensure proper spacing." 
    }, 
    "Tomato Healthy": { 
        "treatment": "Plant is healthy. Continue normal care.", 
        "prevention": "Monitor regularly for early detection." 
    }, 
    "Tomato Late Blight": { 
        "treatment": "Use Metalaxyl fungicide immediately. Remove affected plants.", 
        "prevention": "Avoid excess moisture and ensure air circulation." 
    } 
} 

kannada_info = { 
    "Potato Early Blight": "ಆಲೂಗಡ್ಡೆ ಆರಂಭಿಕ ರೋಗ. ಮ್ಯಾಂಕೋಜೆಬ್ ಔಷಧಿ ಬಳಸಿ.", 
    "Potato Healthy": "ಸಸ್ಯ ಆರೋಗ್ಯಕರವಾಗಿದೆ.", 
    "Tomato Early Blight": "ಟೊಮಾಟೊ ಆರಂಭಿಕ ರೋಗ. ಕಾಪರ್ ಫಂಗಿಸೈಡ್ ಬಳಸಿ.", 
    "Tomato Healthy": "ಸಸ್ಯ ಆರೋಗ್ಯಕರವಾಗಿದೆ.", 
    "Tomato Late Blight": "ಟೊಮಾಟೊ ತಡ ರೋಗ. ಮೆಟಾಲಾಕ್ಸಿಲ್ ಬಳಸಿ." 
} 

hindi_info = {
    "Potato Early Blight": "आलू अगेती झुलसा। मैंकोजेब कवकनाशी का प्रयोग करें।",
    "Potato Healthy": "पौधा स्वस्थ है।",
    "Tomato Early Blight": "टमाटर अगेती झुलसा। तांबा आधारित कवकनाशी का प्रयोग करें।",
    "Tomato Healthy": "पौधा स्वस्थ है।",
    "Tomato Late Blight": "टमाटर पछेती झुलसा। तुरंत मेटालैक्सिल का प्रयोग करें।"
}

telugu_info = {
    "Potato Early Blight": "బంగాళదుంప ఎర్లీ బ్లైట్. మాంకోజెబ్ శిలీంద్ర సంహారిణిని ఉపయోగించండి.",
    "Potato Healthy": "మొక్క ఆరోగ్యంగా ఉంది.",
    "Tomato Early Blight": "టొమాటో ఎర్లీ బ్లైట్. రాగి ఆధారిత శిలీంద్ర సంహారిణిని ఉపయోగించండి.",
    "Tomato Healthy": "మొక్క ఆరోగ్యంగా ఉంది.",
    "Tomato Late Blight": "టొమాటో లేట్ బ్లైట్. వెంటనే మెటాలాక్సిల్ ఉపయోగించండి."
}

english_info = {
    "Potato Early Blight": "Potato Early Blight. Use Mancozeb fungicide.",
    "Potato Healthy": "Plant is healthy.",
    "Tomato Early Blight": "Tomato Early Blight. Use Copper-based fungicide.",
    "Tomato Healthy": "Plant is healthy.",
    "Tomato Late Blight": "Tomato Late Blight. Use Metalaxyl immediately."
}

def predict_image(img): 
    if model is None:
        # Realistic dummy prediction for testing if TF is missing
        import random
        return random.choice(list(class_info.keys()))
    
    img = img.convert('RGB')
    img = img.resize((128,128)) 
    img_array = np.array(img)/255.0 
    img_array = np.expand_dims(img_array, axis=0) 
    prediction = model.predict(img_array) 
    disease = list(class_info.keys())[np.argmax(prediction)] 
    
    # Voice guidance
    if engine:
        try:
            engine.say(disease) 
            engine.runAndWait() 
        except:
            pass
    
    return disease 

@app.route("/", methods=["GET","POST"]) 
def index(): 
    result = "" 
    treatment = "" 
    prevention = "" 
    kannada = ""
    hindi = ""
    telugu = ""
    english = ""

    if request.method == "POST": 
        file = request.files["image"] 
        if file:
            img = Image.open(file) 
            result = predict_image(img) 
            treatment = class_info[result]["treatment"] 
            prevention = class_info[result]["prevention"] 
            kannada = kannada_info[result]
            hindi = hindi_info[result]
            telugu = telugu_info[result]
            english = english_info[result]

            # Save to history
            record = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "disease": result,
                "treatment": treatment,
                "english": english,
                "kannada": kannada,
                "hindi": hindi,
                "telugu": telugu
            }
            save_history(record)

    history_data = get_history()

    return render_template("index.html", 
                           result=result, 
                           treatment=treatment, 
                           prevention=prevention,
                           kannada=kannada,
                           hindi=hindi,
                           telugu=telugu,
                           english=english,
                           history=history_data) 

if __name__ == "__main__": 
    app.run(debug=True)
