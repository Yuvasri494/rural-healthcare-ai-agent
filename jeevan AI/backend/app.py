
# app.py - Fixed Healthcare Backend with Stricter Matching
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
import traceback

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration - Update this to your actual CSV file path
CSV_FILE_PATH = 'healthcare_kb.csv'

def load_symptom_data():
    """
    Load symptom data from CSV file
    Returns a pandas DataFrame with the symptom data
    """
    try:
        # Check if file exists
        if not os.path.exists(CSV_FILE_PATH):
            return None, f"CSV file not found at path: {CSV_FILE_PATH}"
        
        # Read CSV file
        df = pd.read_csv(CSV_FILE_PATH)
        
        # Check if dataframe is empty
        if df.empty:
            return None, "CSV file is empty"
            
        # Validate required columns based on your CSV structure
        required_columns = [
            'symptom_english', 'symptom_hindi', 'symptom_tamil',
            'severity', 'advice_english', 'advice_hindi', 'advice_tamil',
            'first_aid_english', 'first_aid_hindi', 'first_aid_tamil'
        ]
        
        # Check if all required columns exist
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return None, f"Missing required columns: {missing_columns}"
            
        return df, None
        
    except Exception as e:
        error_msg = f"Error loading CSV file: {str(e)}"
        print(error_msg)
        traceback.print_exc()  # Print detailed error for debugging
        return None, error_msg

# Load symptom data once when the app starts
symptom_df, error = load_symptom_data()
if error:
    print(f"Warning: {error}")
    print("Using sample data instead")

@app.route('/')
def home():
    """Root endpoint that provides information about the API"""
    return jsonify({
        'message': 'Healthcare AI Assistant API',
        'version': '1.0',
        'endpoints': {
            '/health': 'GET - Health check',
            '/symptoms': 'GET - Get all symptoms (add ?language=english|hindi|tamil)',
            '/diagnose': 'POST - Diagnose symptoms (send JSON with symptom and language)'
        },
        'csv_status': 'loaded' if symptom_df is not None else 'failed',
        'csv_rows': len(symptom_df) if symptom_df is not None else 0
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify the server is running"""
    csv_status = "loaded successfully" if symptom_df is not None else "failed to load"
    csv_rows = len(symptom_df) if symptom_df is not None else 0
    return jsonify({
        'status': 'healthy',
        'csv_status': csv_status,
        'csv_rows': csv_rows,
        'csv_path': CSV_FILE_PATH,
        'csv_columns': list(symptom_df.columns) if symptom_df is not None else []
    })

@app.route('/diagnose', methods=['POST'])
def diagnose():
    """
    Enhanced endpoint for multilingual symptom diagnosis with stricter matching threshold
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
            
        symptom_input = data.get('symptom', '').lower().strip()
        language = data.get('language', 'english')
        
        if not symptom_input:
            return jsonify({'success': False, 'message': 'No symptom provided'}), 400
        
        # Comprehensive symptom data with multilingual patterns
        symptoms_data = {
            "Fever": {
                "patterns": ["fever", "high temperature", "बुखार", "தेজبुखार", "काय्चल", "काय়च्चल्", "veppam"],
                "name": {"english": "Fever", "hindi": "बुखार", "tamil": "காய்ச்சல்"},
                "severity": "H",
                "confidence": 90,
                "advice": {
                    "english": "Take rest and drink plenty of fluids. Use cold compress on forehead.",
                    "hindi": "आराम करें और खूब पानी पिएं। माथे पर ठंडी पट्टी रखें।",
                    "tamil": "ஓய்வு எடுத்து நிறைய நீர் குடிக்கவும். நெற்றியில் குளிர்ந்த ஒத்தடம் கொடுக்கவும்."
                },
                "first_aid": {
                    "english": "Rest in cool place, remove excess clothing, apply wet cloth on forehead",
                    "hindi": "ठंडी जगह आराम करें, अतिरिक्त कपड़े उतारें",
                    "tamil": "குளிர்ந்த இடத்தில் ஓய்வு, கூடுதல் உடைகளை அகற்றவும்"
                }
            },
            "Common Cold": {
                "patterns": ["cold", "sneeze", "sneezing", "सर्दी", "छींक", "சளি", "தुमिमल्"],
                "name": {"english": "Common Cold", "hindi": "सर्दी", "tamil": "சளி"},
                "severity": "H",
                "confidence": 88,
                "advice": {
                    "english": "Stay hydrated and rest well. Gargle with warm salt water.",
                    "hindi": "खूब पानी पिएं और आराम करें। गर्म नमकीन पानी से गरारे करें।",
                    "tamil": "நீர்ச்சत்துடन் இருக்கவும். வெதुவெதுப்பான உப்பு நீरில் கொப்பளிக்கவும்."
                },
                "first_aid": {
                    "english": "Encourage rest and fluid intake, warm salt water gargling",
                    "hindi": "आराम और द्रव सेवन को बढ़ावा दें",
                    "tamil": "ஓய்வு மற்றும் நீர் உட்கொள்ளலை ஊக்குவிக்கவும்"
                }
            },
            "Headache": {
                "patterns": ["headache", "head ache", "head pain", "migraine", "सिर दर्द", "सिरदर्द", "माइग्रेन", "तलैवली", "talai vali", "தலைவலி"],
                "name": {"english": "Headache", "hindi": "सिर दर्द", "tamil": "தலைவலி"},
                "severity": "H",
                "confidence": 88,
                "advice": {
                    "english": "Take rest in dark quiet room. Apply cold compress.",
                    "hindi": "अंधेरे और शांत कमरे में आराम करें। ठंडी सिकाई करें।",
                    "tamil": "இருண்ட அமைதியான அறையில் ஓய்வு எடுக்கவும். குளிர் ஒத்தடம் கொடுக்கவும்."
                },
                "first_aid": {
                    "english": "Lie down in quiet dark room, apply cold compress to head",
                    "hindi": "शांत अंधेरे कमरे में लेट जाएं",
                    "tamil": "அமைதியான இருண்ட அறையில் படுக்கவும்"
                }
            },
            "Stomach Pain": {
                "patterns": ["stomach pain", "stomach ache", "abdominal pain", "belly pain", "पेट दर्द", "पेट में दर्द", "vayitru vali", "வயிற்றுवलि"],
                "name": {"english": "Stomach Pain", "hindi": "पेट दर्द", "tamil": "வயிற்றுவலி"},
                "severity": "D",
                "confidence": 85,
                "advice": {
                    "english": "Avoid solid food for few hours. Take small sips of water.",
                    "hindi": "कुछ घंटों तक ठोस भोजन न लें। थोड़ा-थोड़ा पानी पिएं।",
                    "tamil": "சில மணி நேரம் திட உணவு தவிர்க்கவும். கொஞ்சம் கொஞ்சமாக தண்ணீர் குடிக்கவும்."
                },
                "first_aid": {
                    "english": "Apply gentle heat to abdomen, avoid solid foods",
                    "hindi": "पेट पर हल्की गर्माहट दें",
                    "tamil": "வயிற்றில் மெதுவான சூட்டைக் கொடுக்கவும்"
                }
            },
            "Chest Pain": {
                "patterns": ["chest pain", "heart pain", "cardiac pain", "chest ache", "छाती में दर्द", "छाती दर्द", "हृदय दर्द", "nenju vali", "நेंजু वलি"],
                "name": {"english": "Chest Pain", "hindi": "छाती में दर्द", "tamil": "நெஞ்சு வலி"},
                "severity": "E",
                "confidence": 92,
                "advice": {
                    "english": "Stop all activity. Sit down and rest. Call emergency.",
                    "hindi": "सभी गतिविधियां बंद करें। बैठकर आराम करें। आपातकाल बुलाएं।",
                    "tamil": "அனைத्து செயல्पাடுகளையुम् निறुत्तवुम्। उट्कारन्तु ओय्வु एडुक्कवुम्। अवसर सेवैयै अळैक्कवुम्।"
                },
                "first_aid": {
                    "english": "Have person sit and rest, call emergency services",
                    "hindi": "व्यक्ति को बिठाकर आराम दिलाएं",
                    "tamil": "நபரை உட்காரवैत्तु ओय्वु कोडुक्कवुम्"
                }
            },
            "Cough": {
                "patterns": ["cough", "dry cough", "wet cough", "coughing", "खांसी", "खाँसी", "इरुमल्", "irumal"],
                "name": {"english": "Cough", "hindi": "खांसी", "tamil": "இருமல்"},
                "severity": "H",
                "confidence": 86,
                "advice": {
                    "english": "Drink warm water with honey. Use steam inhalation.",
                    "hindi": "शहद के साथ गर्म पानी पिएं। भाप लें।",
                    "tamil": "தேनுடन् वेतुवेतुप्पान नीर कुडिक्कवुम्। नीरावि पिडिक्कवुम्।"
                },
                "first_aid": {
                    "english": "Warm honey water, steam inhalation",
                    "hindi": "गर्म शहद पानी दें, भाप दिलवाएं",
                    "tamil": "वेतुवेतुप्पान तेन नीर, नीरावि"
                }
            },
            # Add leg pain as a specific symptom
            "Leg Pain": {
                "patterns": ["leg pain", "leg ache", "thigh pain", "calf pain", "पैर दर्द", "पैर में दर्द", "जांघ दर्द", "काल् वलि", "kal vali", "தोडै वलि"],
                "name": {"english": "Leg Pain", "hindi": "पैर दर्द", "tamil": "கால் வலி"},
                "severity": "H",
                "confidence": 87,
                "advice": {
                    "english": "Rest the affected leg. Apply ice if swollen, heat if muscle pain. Elevate the leg.",
                    "hindi": "प्रभावित पैर को आराम दें। सूजन हो तो बर्फ, मांसपेशी दर्द हो तो गर्माहट लगाएं।",
                    "tamil": "பாதிக்கப்பட்ட காலுக்கு ஓய்வு கொடுக்கவும். வீக்கம் இருந்தால் பனி, தசை வலி இருந்தால் வெப்பம் கொடுக்கவும்."
                },
                "first_aid": {
                    "english": "Rest, elevation, ice for swelling or heat for muscle pain",
                    "hindi": "आराम, पैर ऊंचा रखें, स्थिति अनुसार बर्फ या गर्माहट",
                    "tamil": "ஓய்வு, உயர்த்தல், நிலைமைக்கு ஏற்ப பனி அல்லது வெப்பம்"
                }
            }
        }
        
        # STRICTER MATCHING LOGIC with higher threshold
        best_match = None
        highest_score = 0
        
        for symptom_key, symptom_data in symptoms_data.items():
            score = 0
            patterns = symptom_data['patterns']
            
            # Check for exact matches (highest priority)
            for pattern in patterns:
                pattern_lower = pattern.lower()
                if pattern_lower == symptom_input:  # Exact match
                    score += 100
                elif pattern_lower in symptom_input and len(pattern_lower) > 3:  # Pattern is substring
                    score += len(pattern_lower) * 3
                elif symptom_input in pattern_lower and len(symptom_input) > 3:  # Input is substring
                    score += len(symptom_input) * 2
                
            # Check for word-level matches (lower priority)
            input_words = symptom_input.split()
            for word in input_words:
                if len(word) > 2:  # Only consider meaningful words
                    for pattern in patterns:
                        pattern_words = pattern.lower().split()
                        if word in pattern_words:
                            score += len(word) * 1
            
            if score > highest_score:
                highest_score = score
                best_match = symptom_data
        
        # INCREASED THRESHOLD from 1 to 10 for stricter matching
        if best_match and highest_score >= 90:
            return jsonify({
                'success': True,
                'result': best_match
            })
        else:
            messages = {
                'english': 'No matching symptom found. Try using different words or describe more specifically.',
                'hindi': 'कोई मैच नहीं मिला। अलग शब्दों का उपयोग करें या अधिक स्पष्ट रूप से बताएं।',
                'tamil': 'பொருத்தமான அறிகுறி கிடைக்கவில்லை। வேறு சொற்களை முயற்சிக்கவும்।'
            }
            
            return jsonify({
                'success': False,
                'message': messages.get(language, messages['english'])
            })
            
    except Exception as e:
        error_msg = f"Error in diagnosis: {str(e)}"
        print(error_msg)
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@app.route('/symptoms', methods=['GET'])
def get_symptoms():
    """
    Enhanced endpoint to get all symptoms with proper multilingual support
    """
    try:
        language = request.args.get('language', 'english')
        
        # If we couldn't load the CSV, return sample data
        if symptom_df is None:
            sample_symptoms = [
                {
                    'name': {'english': 'Fever', 'hindi': 'बुखार', 'tamil': 'காய்ச்சல்'},
                    'severity': 'H',
                    'advice': {
                        'english': 'Take rest and drink plenty of fluids.',
                        'hindi': 'आराम करें और खूब पानी पिएं।',
                        'tamil': 'ஓய்வு எடுத்து நிறைய நீர் குடிக்கவும்।'
                    }
                },
                {
                    'name': {'english': 'Cough', 'hindi': 'खांसी', 'tamil': 'இருமல்'},
                    'severity': 'H',
                    'advice': {
                        'english': 'Drink warm water with honey.',
                        'hindi': 'शहद के साथ गर्म पानी पिएं।',
                        'tamil': 'தேனுடன் வெதுவெதुப்பான நீர் குடிக்கவும்।'
                    }
                },
                {
                    'name': {'english': 'Leg Pain', 'hindi': 'पैर दर्द', 'tamil': 'கால் வலி'},
                    'severity': 'H',
                    'advice': {
                        'english': 'Rest the leg and apply appropriate treatment.',
                        'hindi': 'पैर को आराम दें और उचित उपचार करें।',
                        'tamil': 'காலுக்கு ஓய்வு கொடுத்து பொருத்தமான சிகிச்சை செய்யவும்।'
                    }
                }
            ]
            return jsonify({
                'success': True,
                'symptoms': sample_symptoms,
                'message': 'Using sample data - CSV not loaded properly'
            })
        
        symptoms_list = []
        for index, row in symptom_df.iterrows():
            symptom_data = {
                'name': {
                    'english': row.get('symptom_english', 'Unknown Symptom'),
                    'hindi': row.get('symptom_hindi', 'अज्ञात लक्षण'),
                    'tamil': row.get('symptom_tamil', 'தெரியாத அறிகுறி')
                },
                'severity': row.get('severity', 'H'),
                'advice': {
                    'english': row.get('advice_english', 'No advice available'),
                    'hindi': row.get('advice_hindi', 'कोई सलाह उपलब्ध नहीं'),
                    'tamil': row.get('advice_tamil', 'ஆலோசனை கிடைக்கவில்லை')
                }
            }
            symptoms_list.append(symptom_data)
        
        return jsonify({
            'success': True,
            'symptoms': symptoms_list
        })
        
    except Exception as e:
        error_msg = f"Error getting symptoms: {str(e)}"
        print(error_msg)
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@app.route("/emergency", methods=["POST"])
def emergency_alert():
    lang = request.json.get("language", "english").lower()

    messages = {
        "english": {
            "message": "🚑 Ambulance is on the way. Please wait and stay calm.",
            "firstAid": "Keep the patient comfortable, check breathing, and avoid giving water if unconscious."
        },
        "hindi": {
            "message": "🚑 एम्बुलेंस रास्ते में है। कृपया प्रतीक्षा करें और शांत रहें।",
            "firstAid": "रोगी को आराम से रखें, सांस की जांच करें और यदि बेहोश हो तो पानी न दें।"
        },
        "tamil": {
            "message": "🚑 ஆம்புலன்ஸ் வழியில் வருகிறது. தயவு செய்து காத்திருந்து அமைதியாக இருங்கள்.",
            "firstAid": "நோயாளியை வசதியாக வைத்திருங்கள், சுவாசத்தைச் சரிபார்க்கவும், மயக்கம் இருந்தால் தண்ணீர் கொடுக்க வேண்டாம்."
        }
    }

    selected = messages.get(lang, messages["english"])
    return jsonify(selected)

if __name__ == '__main__':
    # Print debug information
    print("Starting Healthcare AI Assistant Backend...")
    print(f"Looking for CSV file at: {os.path.abspath(CSV_FILE_PATH)}")
    
    if symptom_df is not None:
        print(f"CSV loaded successfully with {len(symptom_df)} rows")
        print("Available columns:", list(symptom_df.columns))
    else:
        print(f"CSV loading failed: {error}")
        print("Using sample data instead")
    
    # Run the Flask app
    app.run(debug=True, port=5000, host='0.0.0.0')

