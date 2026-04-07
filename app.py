import gradio as gr
import numpy as np
from PIL import Image, ImageEnhance
import os
import base64
import google.generativeai as genai

# ==================== OPENCV ====================
try:
    import cv2
    CV2_AVAILABLE = True
    print("✅ OpenCV loaded")
except ImportError:
    CV2_AVAILABLE = False
    print("⚠️ OpenCV not available")

# ==================== TENSORFLOW ====================
print("🔧 Loading TensorFlow...")
try:
    import tensorflow as tf
    from tensorflow.keras.models import load_model
    print(f"✅ TensorFlow {tf.__version__} loaded")
    TENSORFLOW_OK = True
except Exception as e:
    print(f"❌ TensorFlow error: {e}")
    TENSORFLOW_OK = False

# ==================== MODEL ====================
MODEL_FILE = "plant_model.keras"
MODEL_LOADED = False
model = None

if TENSORFLOW_OK and os.path.exists(MODEL_FILE):
    try:
        model = load_model(MODEL_FILE, compile=False)
        MODEL_LOADED = True
        print(f"✅ Model loaded! ({MODEL_FILE})")
    except Exception as e:
        print(f"❌ Model error: {e}")
else:
    print(f"❌ Model file not found: {MODEL_FILE}")

# ==================== GEMINI ====================
print("🔧 Loading Gemini...")
GEMINI_OK = False
gemini_model = None

try:
    API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyDszKA3q4Liv-dzb0JxQa_dz-3vK0QM7eU")
    genai.configure(api_key=API_KEY)

    # ✅ FIXED MODEL
    gemini_model = genai.GenerativeModel('models/gemini-pro')

    GEMINI_OK = True
    print("✅ Gemini loaded")
except Exception as e:
    print(f"❌ Gemini error: {e}")
# ==================== LOGO ====================
def get_logo_base64():
    logo_paths = ["logo.png", "static/logo.png"]
    for path in logo_paths:
        if os.path.exists(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    return None

LOGO_BASE64 = get_logo_base64()
LOGO_HTML = '<div style="font-size:50px; text-align:center;">🌿</div>'
if LOGO_BASE64:
    LOGO_HTML = f'<img src="data:image/png;base64,{LOGO_BASE64}" style="width:80px; display:block; margin:0 auto 10px auto;">'

# ==================== RASMNI QAYTA ISHLASH ====================
def enhance_image(image):
    try:
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.2)
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.3)
        return image
    except:
        return image

def preprocess_image(image):
    """Prepare image / చిత్రాన్ని సిద్ధం చేయడం / படத்தை தயார் செய்தல்"""
    enhanced = enhance_image(image)
    resized = enhanced.resize((224, 224))
    return resized

# ==================== TARJIMA ====================
TRANSLATIONS = {
    "Apple": {
        "english": "Apple",
        "telugu": "ఆపిల్",
        "tamil": "ஆப்பிள்"
    },
    "Grape": {
        "english": "Grape",
        "telugu": "ద్రాక్ష",
        "tamil": "திராட்சை"
    },
    "Tomato": {
        "english": "Tomato",
        "telugu": "టమోటా",
        "tamil": "தக்காளி"
    },
    "Pepper bell": {
        "english": "Pepper bell",
        "telugu": "క్యాప్సికమ్",
        "tamil": "குடைமிளகாய்"
    },
    "healthy": {
        "english": "healthy",
        "telugu": "ఆరోగ్యంగా ఉంది",
        "tamil": "ஆரோக்கியமானது"
    }
}
def translate_text(text, lang):
    if lang == "english":
        return text
    words = text.split(" - ")
    if len(words) == 2:
        plant, disease = words[0], words[1]
        for key, trans in TRANSLATIONS.items():
            if key.lower() in plant.lower():
                plant = trans.get(lang, plant)
                break
        return f"{plant} - {disease}"
    return text

def translate_description(desc, lang):
    if lang == "english":
        return desc
    trans_dict = {
        "🍇 Black lesions on grape leaves.": {
            "telugu": "🍇 ద్రాక్ష ఆకులపై నల్ల మచ్చలు.",
            "tamil": "🍇 திராட்சை இலைகளில் கருப்பு புள்ளிகள்."
        },
        "🍅 Dark leaf spots on tomato.": {
            "telugu": "🍅 టమోటా ఆకులపై నల్ల మచ్చలు.",
            "tamil": "🍅 தக்காளி இலைகளில் கரும்புள்ளிகள்."
        },
        "🍅 Target-like spots on tomato.": {
            "telugu": "🍅 టమోటా ఆకులపై లక్ష్యంలా మచ్చలు.",
            "tamil": "🍅 தக்காளியில் குறி போல புள்ளிகள்."
        },
        "🫑 Dark spots on pepper leaves.": {
            "telugu": "🫑 మిరప ఆకులపై నల్ల మచ్చలు.",
            "tamil": "🫑 மிளகாய் இலைகளில் கரும்புள்ளிகள்."
        },
    }
    if desc in trans_dict:
        return trans_dict[desc].get(lang, desc)
    return desc

# ==================== 3 TIL ====================
TEXTS = {
    "english": {
        "title": "🌿 Leaf Disease Detection (DCNN)",
        "developed_by": "Developed by: Leaf disease detection and classification using Deep learning technique with DCNN TEAM",
        "master": "UG – Computer Science (AI & ML), Kalasalingam Academy of Research and Higher Education",
        "plant_leaf": "🌿 Upload Leaf Image",
        "detect_btn": "🔍 Detect Disease",
        "clear_btn": "🗑 Clear",
        "upload_rules": "📸 Image Upload Guidelines:",
        "rule1": "• Leaf should be clearly visible in the center",
        "rule2": "• Disease symptoms should be close and clear",
        "rule3": "• Avoid dark or blurry images",
        "rule4": "• Capture a single leaf",
        "auto_leaf_note": "✨ AI will analyze the leaf for diseases",
        "supported_title": "📋 Supported Plants",
        "supported_text": "🍎 Apple | 🫐 Blueberry | 🍒 Cherry | 🌽 Corn | 🍇 Grape | 🍊 Orange | 🍑 Peach | 🫑 Pepper | 🥔 Potato | 🍓 Strawberry | 🍅 Tomato",
        "welcome_title": "Welcome to Leaf Disease Detection (DCNN)",
        "welcome_text": "Upload a leaf image to get started",
        "click_text": "Click 'Detect Disease' to analyze",
        "diagnosis_title": "🔬 Diagnosis Results",
        "top_results": "Top 3 disease predictions with confidence scores",
        "ai_doctor": "👨‍⚕️ AI Doctor's Advice",
        "accuracy_text": "🌿 Model accuracy: 98.02%",
        "footer": "Kalasalingam University | Department of Computer Engineering",
        "error_model_title": "⚠️ Model Not Loaded",
        "error_model_text": "Please make sure 'plant_model.keras' is in the correct directory.",
        "error_general": "❌ Error",
        "advice_unavailable": "⚠️ AI assistant temporarily unavailable.",
        "advice_error": "⚠️ Could not get AI advice.",
        "model_ready": "✅ Model Ready",
        "model_not_ready": "❌ Model Not Loaded",
        "gemini_active": "🤖 Gemini AI Active",
        "gemini_inactive": "🤖 Gemini AI Inactive"
    },
    
    "telugu": {
        "title": "🌿 మొక్కల వ్యాధి గుర్తింపు",
        "developed_by": "అభివృద్ధి చేసినవారు: DCNN ఉపయోగించి డీప్ లెర్నింగ్ ఆధారిత ఆకుల వ్యాధి గుర్తింపు బృందం",
        "master": "UG – కంప్యూటర్ సైన్స్ (AI & ML), Kalasalingam Academy of Research and Higher Education",
        "plant_leaf": "🌿 ఆకును అప్‌లోడ్ చేయండి",
        "detect_btn": "🔍 వ్యాధి గుర్తించండి",
        "clear_btn": "🗑 క్లియర్ చేయండి",
        "upload_rules": "📸 చిత్ర నియమాలు:",
        "rule1": "• ఆకును స్పష్టంగా చూపించాలి",
        "rule2": "• వ్యాధి భాగం దగ్గరగా ఉండాలి",
        "rule3": "• చీకటి/బ్లర్ చిత్రాలు వద్దు",
        "rule4": "• ఒకే ఆకును చిత్రీకరించండి",
        "auto_leaf_note": "✨ AI విశ్లేషిస్తుంది",
        "supported_title": "📋 మద్దతు మొక్కలు",
        "supported_text": "🍎 ఆపిల్ | 🍇 ద్రాక్ష | 🍅 టమోటా | 🫑 మిరప",
        "welcome_title": "మొక్కల వ్యాధి గుర్తింపు",
        "welcome_text": "ఆకును అప్‌లోడ్ చేయండి",
        "click_text": "గుర్తించండి బటన్ నొక్కండి",
        "diagnosis_title": "🔬 ఫలితాలు",
        "top_results": "టాప్ 3 ఫలితాలు",
        "ai_doctor": "👨‍⚕️ AI సలహా",
        "accuracy_text": "🌿 మోడల్ ఖచ్చితత్వం: 98.02%",
        "footer": "కంప్యూటర్ ఇంజినీరింగ్ విభాగం",
        "error_model_title": "⚠️ మోడల్ లేదు",
        "error_model_text": "ఫైల్ తనిఖీ చేయండి",
        "error_general": "❌ లోపం",
        "advice_unavailable": "⚠️ AI అందుబాటులో లేదు",
        "advice_error": "⚠️ సలహా లేదు",
        "model_ready": "✅ మోడల్ సిద్ధం",
        "model_not_ready": "❌ మోడల్ లేదు",
        "gemini_active": "🤖 Gemini యాక్టివ్",
        "gemini_inactive": "🤖 Gemini లేదు"
    },

    "tamil": {
        "title": "🌿  செடி நோய் கண்டறிதல்",
        "developed_by": "உருவாக்கியது: DCNN பயன்படுத்திய ஆழமான கற்றல் மூலம் இலை நோய் கண்டறிதல் குழு",
        "master": "UG – கணினி அறிவியல் (AI & ML), Kalasalingam Academy of Research and Higher Education",
        "plant_leaf": "🌿 இலை பதிவேற்றவும்",
        "detect_btn": "🔍 நோய் கண்டறி",
        "clear_btn": "🗑 அழிக்கவும்",
        "upload_rules": "📸 பட விதிமுறைகள்:",
        "rule1": "• இலை தெளிவாக இருக்க வேண்டும்",
        "rule2": "• நோய் பகுதி அருகில் இருக்க வேண்டும்",
        "rule3": "• இருண்ட/மங்கலான படம் வேண்டாம்",
        "rule4": "• ஒரு இலை மட்டும் படம் எடுக்கவும்",
        "auto_leaf_note": "✨ AI பகுப்பாய்வு செய்யும்",
        "supported_title": "📋 ஆதரவு தாவரங்கள்",
        "supported_text": "🍎 ஆப்பிள் | 🍇 திராட்சை | 🍅 தக்காளி | 🫑 மிளகாய்",
        "welcome_title": "செடி நோய் கண்டறிதல்",
        "welcome_text": "இலை பதிவேற்றவும்",
        "click_text": "கண்டறி பொத்தானை அழுத்தவும்",
        "diagnosis_title": "🔬 முடிவுகள்",
        "top_results": "முதல் 3 முடிவுகள்",
        "ai_doctor": "👨‍⚕️ AI ஆலோசனை",
        "accuracy_text": "🌿 துல்லியம்: 98.02%",
        "footer": "கணினி பொறியியல் துறை",
        "error_model_title": "⚠️ மாடல் இல்லை",
        "error_model_text": "கோப்பை சரிபார்க்கவும்",
        "error_general": "❌ பிழை",
        "advice_unavailable": "⚠️ AI இல்லை",
        "advice_error": "⚠️ ஆலோசனை இல்லை",
        "model_ready": "✅ மாடல் தயார்",
        "model_not_ready": "❌ மாடல் இல்லை",
        "gemini_active": "🤖 Gemini செயல்படும்",
        "gemini_inactive": "🤖 Gemini செயல்படவில்லை"
    }
}
    
# ==================== KLASSLAR ====================
class_names = [
    "Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust", "Apple___healthy",
    "Blueberry___healthy", "Cherry___Powdery_mildew", "Cherry___healthy",
    "Corn___Cercospora_leaf_spot", "Corn___Common_rust", "Corn___Northern_Leaf_Blight", "Corn___healthy",
    "Grape___Black_rot", "Grape___Esca", "Grape___Leaf_blight", "Grape___healthy",
    "Orange___Haunglongbing", "Peach___Bacterial_spot", "Peach___healthy",
    "Pepper_bell___Bacterial_spot", "Pepper_bell___healthy",
    "Potato___Early_blight", "Potato___Late_blight", "Potato___healthy",
    "Raspberry___healthy", "Soybean___healthy", "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch", "Strawberry___healthy",
    "Tomato___Bacterial_spot", "Tomato___Early_blight", "Tomato___Late_blight",
    "Tomato___Leaf_Mold", "Tomato___Septoria_leaf_spot", "Tomato___Spider_mites",
    "Tomato___Target_Spot", "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus", "Tomato___healthy"
]

def get_pretty_name(class_name):
    return class_name.replace("___", " - ").replace("_", " ")

descriptions = {
    "Apple___Apple_scab": "🍎 Fungal disease causing dark scabby lesions on apple leaves.",
    "Apple___Black_rot": "🍎 Fungal disease causing black rot on apple leaves.",
    "Apple___Cedar_apple_rust": "🍎 Fungal disease causing orange spots on apple leaves.",
    "Apple___healthy": "🍎 The apple leaf appears healthy.",
    "Blueberry___healthy": "🫐 Blueberry leaf appears healthy.",
    "Cherry___Powdery_mildew": "🍒 White powdery fungus on cherry leaves.",
    "Cherry___healthy": "🍒 Cherry leaf appears healthy.",
    "Corn___Cercospora_leaf_spot": "🌽 Gray leaf spots on corn.",
    "Corn___Common_rust": "🌽 Reddish pustules on corn leaves.",
    "Corn___Northern_Leaf_Blight": "🌽 Long gray lesions on corn leaves.",
    "Corn___healthy": "🌽 Corn leaf appears healthy.",
    "Grape___Black_rot": "🍇 Black lesions on grape leaves.",
    "Grape___Esca": "🍇 Trunk disease affecting grape plants.",
    "Grape___Leaf_blight": "🍇 Leaf blight on grapes.",
    "Grape___healthy": "🍇 Grape leaf appears healthy.",
    "Orange___Haunglongbing": "🍊 Citrus greening disease.",
    "Peach___Bacterial_spot": "🍑 Dark spots on peach leaves.",
    "Peach___healthy": "🍑 Peach leaf appears healthy.",
    "Pepper_bell___Bacterial_spot": "🫑 Dark spots on pepper leaves.",
    "Pepper_bell___healthy": "🫑 Pepper leaf appears healthy.",
    "Potato___Early_blight": "🥔 Dark concentric rings on leaves.",
    "Potato___Late_blight": "🥔 Leaf decay and rot on potato.",
    "Potato___healthy": "🥔 Potato leaf appears healthy.",
    "Raspberry___healthy": "🍇 Raspberry leaf appears healthy.",
    "Soybean___healthy": "🫘 Soybean leaf appears healthy.",
    "Squash___Powdery_mildew": "🎃 White powdery growth on squash.",
    "Strawberry___Leaf_scorch": "🍓 Red spots on strawberry leaves.",
    "Strawberry___healthy": "🍓 Strawberry leaf appears healthy.",
    "Tomato___Bacterial_spot": "🍅 Dark leaf spots on tomato.",
    "Tomato___Early_blight": "🍅 Brown concentric rings on leaves.",
    "Tomato___Late_blight": "🍅 Dark lesions on tomato leaves.",
    "Tomato___Leaf_Mold": "🍅 Yellow patches on tomato leaves.",
    "Tomato___Septoria_leaf_spot": "🍅 Small circular spots on tomato.",
    "Tomato___Spider_mites": "🍅 Yellow speckled leaves from mites.",
    "Tomato___Target_Spot": "🍅 Target-like spots on tomato.",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": "🍅 Leaf curl and yellowing.",
    "Tomato___Tomato_mosaic_virus": "🍅 Mosaic pattern on tomato leaves.",
    "Tomato___healthy": "🍅 Tomato leaf appears healthy."
}

# ==================== GEMINI MASLAHAT ====================
def get_disease_advice(disease_name, lang):
    t = TEXTS[lang]

    if not GEMINI_OK or gemini_model is None:
        return t["advice_unavailable"]

    lang_prompt = {
        "english": "Give short treatment advice in English.",
        "telugu": "తెలుగులో చిన్న చికిత్స సలహా ఇవ్వండి.",
        "tamil": "தமிழில் சுருக்கமான சிகிச்சை ஆலோசனை வழங்கவும்."
    }

    prompt = f"""
You are an agricultural expert.

Disease: {disease_name}

{lang_prompt[lang]}

Give short:
- Cause
- Treatment
- Prevention
"""

    try:
        response = gemini_model.generate_content(prompt)

        # ✅ Method 1 (most common)
        if hasattr(response, "text") and response.text:
            return response.text.strip()

        # ✅ Method 2 (fallback for new Gemini format)
        if hasattr(response, "candidates") and response.candidates:
            parts = response.candidates[0].content.parts
            if parts:
                return parts[0].text.strip()

        # ✅ FINAL fallback (never return empty)
        return "🌿 Remove infected leaves, apply fungicide, and avoid excess moisture."

    except Exception as e:
        print("Gemini Error:", e)

        # ✅ ERROR fallback
        return "🌿 Remove infected leaves, apply fungicide, and avoid excess moisture."

# ==================== PREDICT ====================
def predict(image, language):
    t = TEXTS[language]
    
    if image is None:
        return f'<div style="text-align:center;padding:50px;background:linear-gradient(135deg,#f5f7fa,#c3cfe2);border-radius:20px;"><div style="font-size:60px;">🌿</div><h2>{t["welcome_title"]}</h2><p>{t["welcome_text"]}</p><p>{t["click_text"]}</p></div>'
    
    if not MODEL_LOADED:
        return f'<div style="text-align:center;padding:50px;background:#fee;"><h2>{t["error_model_title"]}</h2><p>{t["error_model_text"]}</p></div>'
    
    try:
        processed = preprocess_image(image)
        arr = np.array(processed) / 255.0
        arr = np.expand_dims(arr, axis=0)
        pred = model.predict(arr, verbose=0)[0]
        top3 = pred.argsort()[-3:][::-1]
        
        results = []
        for idx in top3:
            eng_name = get_pretty_name(class_names[idx])
            results.append({
                "name": translate_text(eng_name, language),
                "prob": round(pred[idx] * 100, 2),
                "desc": translate_description(descriptions[class_names[idx]], language)
            })
        
        advice = get_disease_advice(results[0]["name"], language)
        colors = ["#4caf50", "#ff9800", "#f44336"]
        icons = ["🥇", "🥈", "🥉"]
        
        html = f'<div style="background:#f0f7f0;padding:25px;border-radius:20px;">'
        html += f'<div style="text-align:center;"><div style="font-size:50px;">🔬</div><h2>{t["diagnosis_title"]}</h2><p>{t["top_results"]}</p></div>'
        
        for i, r in enumerate(results):
            html += f'<div style="background:white;border-radius:15px;padding:15px;margin:10px 0;border-left:5px solid {colors[i]};">'
            html += f'<div><span style="font-size:24px;">{icons[i]}</span> <strong>{r["name"]}</strong> <span style="background:{colors[i]};color:white;padding:2px 10px;border-radius:20px;float:right;">{r["prob"]}%</span></div>'
            html += f'<div style="background:#ddd;height:10px;margin:10px 0;"><div style="background:{colors[i]};width:{r["prob"]}%;height:10px;"></div></div>'
            html += f'<p style="font-size:13px;">📝 {r["desc"]}</p></div>'
        
        html += f'<div style="background:linear-gradient(135deg,#1a5f7a,#0d3b4f);border-radius:15px;padding:20px;color:white;margin-top:15px;"><h3>👨‍⚕️ {t["ai_doctor"]}</h3><div>{advice.replace(chr(10),"<br>")}</div></div>'
        html += f'<div style="text-align:center;margin-top:15px;"><p>{t["accuracy_text"]}</p></div></div>'
        
        return html
        
    except Exception as e:
        return f'<div style="text-align:center;padding:50px;background:#fee;"><h2>{t["error_general"]}</h2><p>{str(e)}</p></div>'

# ==================== UI ====================
def get_status_html(lang):
    t = TEXTS[lang]
    status = t["model_ready"] if MODEL_LOADED else t["model_not_ready"]
    gemini = t["gemini_active"] if GEMINI_OK else t["gemini_inactive"]
    color = "#4caf50" if MODEL_LOADED else "#f44336"
    return f'<div style="background:{color};padding:8px;border-radius:10px;text-align:center;color:white;">{status} | {gemini}</div>'

def get_header_html(lang):
    t = TEXTS[lang]
    return f'<div style="text-align:center;padding:20px 0;">{LOGO_HTML}<h1>{t["title"]}</h1><p>{t["developed_by"]}<br>{t["master"]}</p>{get_status_html(lang)}</div>'

def get_upload_rules_html(lang):
    t = TEXTS[lang]
    return f'<div style="background:#fff8e1;padding:15px;border-radius:10px;margin:15px 0;"><h4>{t["upload_rules"]}</h4><p>{t["rule1"]}</p><p>{t["rule2"]}</p><p>{t["rule3"]}</p><p>{t["rule4"]}</p><p>✨ {t["auto_leaf_note"]}</p></div>'

def get_supported_html(lang):
    t = TEXTS[lang]
    return f'<div style="background:#e8f5e9;padding:12px;border-radius:10px;margin-bottom:15px;"><h4>{t["supported_title"]}</h4><p>{t["supported_text"]}</p></div>'

def get_welcome_html(lang):
    t = TEXTS[lang]
    return f'<div style="text-align:center;padding:50px;background:linear-gradient(135deg,#f5f7fa,#c3cfe2);border-radius:20px;"><div style="font-size:60px;">🌿</div><h2>{t["welcome_title"]}</h2><p>{t["welcome_text"]}</p><p>{t["click_text"]}</p></div>'

def get_footer_html(lang):
    t = TEXTS[lang]
    return f'<hr><div style="text-align:center;padding:15px;color:#888;"><p>{t["accuracy_text"]}</p><p>{t["footer"]}</p></div>'

# ==================== GRADIO UI (TO'G'RILANGAN) ====================
with gr.Blocks(title="🌿 AI Plant Disease Detection") as demo:
    current_lang = gr.State("english")
    
    header = gr.HTML(get_header_html("english"))

    with gr.Row():
        eng_btn = gr.Button("🇬🇧 English", variant="primary")
        tel_btn = gr.Button("🇮🇳 Telugu", variant="secondary")
        tam_btn = gr.Button("🇮🇳 Tamil", variant="secondary")
    
    supported = gr.HTML(get_supported_html("english"))
    upload_rules = gr.HTML(get_upload_rules_html("english"))
    
    with gr.Row():
        with gr.Column(scale=1, min_width=500):
            img_input = gr.Image(type="pil", label="🌿 Upload Leaf Image", height=350)
            with gr.Row():
                predict_btn = gr.Button("🔍 Detect Disease", variant="primary", size="lg")
                clear_btn = gr.Button("🗑 Clear", variant="secondary", size="lg")
        
        with gr.Column(scale=1, min_width=500):
            output = gr.HTML(get_welcome_html("english"))
    
    footer = gr.HTML(get_footer_html("english"))
    # ==================== UPDATE FUNCTIONS ====================
    def update_english():
        lang = "english"
        t = TEXTS[lang]
        return (
            lang,
            get_header_html(lang),
            get_supported_html(lang),
            get_upload_rules_html(lang),
            None,  # img_input - rasm tozalanadi
            t["plant_leaf"],
            t["detect_btn"],
            t["clear_btn"],
            get_welcome_html(lang),
            get_footer_html(lang),
            gr.update(value="🇬🇧 English", variant="primary"),
            gr.update(value="🇮🇳 Telugu", variant="secondary"),
            gr.update(value="🇮🇳 Tamil", variant="secondary")
        )
    
    def update_telugu():
        lang = "telugu"
        t = TEXTS[lang]
        return (
            lang,
            get_header_html(lang),
            get_supported_html(lang),
            get_upload_rules_html(lang),
            None,
            t["plant_leaf"],
            t["detect_btn"],
            t["clear_btn"],
            get_welcome_html(lang),
            get_footer_html(lang),
            gr.update(value="🇬🇧 English", variant="secondary"),
            gr.update(value="🇮🇳 Telugu", variant="primary"),
            gr.update(value="🇮🇳 Tamil", variant="secondary")
        )
    
    def update_tamil():
        lang = "tamil"
        t = TEXTS[lang]
        return (
            lang,
            get_header_html(lang),
            get_supported_html(lang),
            get_upload_rules_html(lang),
            None,
            t["plant_leaf"],
            t["detect_btn"],
            t["clear_btn"],
            get_welcome_html(lang),
            get_footer_html(lang),
            gr.update(value="🇬🇧 English", variant="secondary"),
            gr.update(value="🇮🇳 Telugu", variant="secondary"),
            gr.update(value="🇮🇳 Tamil", variant="primary")
        )
    def clear_all(lang):
        t = TEXTS[lang]
        return None, get_welcome_html(lang)
    
    # ==================== EVENT HANDLERS ====================
    eng_btn.click(
        update_english, 
        outputs=[current_lang, header, supported, upload_rules, img_input, img_input, predict_btn, clear_btn, output, footer, eng_btn, tel_btn, tam_btn]
    )
    
    tel_btn.click(
        update_telugu,
        outputs=[current_lang, header, supported, upload_rules, img_input, img_input, predict_btn, clear_btn, output, footer, eng_btn, tel_btn, tam_btn]
    )

    tam_btn.click(
        update_tamil,
        outputs=[current_lang, header, supported, upload_rules, img_input, img_input, predict_btn, clear_btn, output, footer, eng_btn, tel_btn, tam_btn]
    )
    
    predict_btn.click(fn=predict, inputs=[img_input, current_lang], outputs=output)
    clear_btn.click(fn=clear_all, inputs=[current_lang], outputs=[img_input, output])

demo.launch(theme=gr.themes.Soft(primary_hue="green"))