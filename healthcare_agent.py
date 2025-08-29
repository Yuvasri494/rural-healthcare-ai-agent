from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Symptom database with multi-language support
symptom_db = {
    "fever": {
        "en": "You may have an infection. Drink plenty of water, take rest, and consult a doctor if it lasts more than 3 days.",
        "ta": "உங்களுக்கு தொற்று இருக்கலாம். அதிக தண்ணீர் குடிக்கவும், ஓய்வு எடுக்கவும், 3 நாட்களுக்கு மேல் நீடித்தால் மருத்துவரை அணுகவும்.",
        "hi": "आपको संक्रमण हो सकता है। खूब पानी पिएं, आराम करें, और अगर 3 दिन से अधिक रहे तो डॉक्टर से मिलें।"
    },
    "headache": {
        "en": "It may be due to stress or dehydration. Drink water and take rest. If severe, consult a doctor.",
        "ta": "இது மன அழுத்தம் அல்லது நீரிழப்பு காரணமாக இருக்கலாம். தண்ணீர் குடித்து ஓய்வு எடுக்கவும். கடுமையாக இருந்தால் மருத்துவரை அணுகவும்.",
        "hi": "यह तनाव या पानी की कमी के कारण हो सकता है। पानी पिएं और आराम करें। अगर ज्यादा हो तो डॉक्टर से मिलें।"
    },
    "stomach pain": {
        "en": "It may be due to indigestion. Eat light food, drink warm water. If it persists, consult a doctor.",
        "ta": "இது செரிமானக் கோளாறாக இருக்கலாம். எளிதில் செரியும் உணவு சாப்பிடவும், வெந்நீர் குடிக்கவும். நீடித்தால் மருத்துவரை அணுகவும்.",
        "hi": "यह बदहजमी के कारण हो सकता है। हल्का खाना खाएं, गुनगुना पानी पिएं। अगर बना रहे तो डॉक्टर से मिलें।"
    },
    "cough": {
        "en": "You may have a common cold. Drink warm fluids, avoid dust and cold drinks. If it lasts more than a week, consult a doctor.",
        "ta": "உங்களுக்கு சாதாரண சளி இருக்கலாம். சூடான திரவங்கள் குடிக்கவும், தூசி மற்றும் குளிர்பானங்களை தவிர்க்கவும். ஒரு வாரத்திற்கும் மேலாக நீடித்தால் மருத்துவரை அணுகவும்.",
        "hi": "आपको सर्दी हो सकती है। गर्म तरल पदार्थ पिएं, धूल और ठंडे पेय से बचें। अगर यह एक सप्ताह से अधिक रहे तो डॉक्टर से मिलें।"
    },
    "diarrhea": {
        "en": "It may be due to infection or food issue. Drink clean water, take oral rehydration salts. If severe, consult a doctor.",
        "ta": "இது தொற்று அல்லது உணவு பிரச்சனை காரணமாக இருக்கலாம். சுத்தமான தண்ணீர் குடிக்கவும், ஓஆர்எஸ் குடிக்கவும். கடுமையாக இருந்தால் மருத்துவரை அணுகவும்.",
        "hi": "यह संक्रमण या खाने की समस्या के कारण हो सकता है। साफ पानी पिएं, ओआरएस घोल लें। अगर गंभीर हो तो डॉक्टर से मिलें।"
    },

    # Emergency symptoms
    "chest pain": {
        "en": "Possible heart-related issue. First Aid: Sit in a comfortable position, keep calm, avoid movement.",
        "ta": "இதயம் தொடர்பான பிரச்சனை இருக்கலாம். முதலுதவி: வசதியான நிலையில் உட்காரவும், அமைதியாக இருங்கள், அசைவுகளை தவிர்க்கவும்.",
        "hi": "संभवतः हृदय से जुड़ी समस्या। प्राथमिक उपचार: आराम से बैठें, शांत रहें, ज्यादा न हिलें।"
    },
    "difficulty breathing": {
        "en": "Possible severe asthma or heart issue. First Aid: Sit upright, loosen tight clothing, stay calm.",
        "ta": "கடுமையான ஆஸ்துமா அல்லது இதய பிரச்சனை இருக்கலாம். முதலுதவி: நேராக உட்காரவும், இறுக்கமான உடைகளை தளர்த்தவும், அமைதியாக இருங்கள்.",
        "hi": "संभवतः गंभीर दमा या हृदय समस्या। प्राथमिक उपचार: सीधे बैठें, तंग कपड़े ढीले करें, शांत रहें।"
    },
    "unconscious": {
        "en": "Emergency condition. First Aid: Check breathing, keep airway clear, place on side position.",
        "ta": "அவசர நிலை. முதலுதவி: சுவாசத்தை சரிபார்க்கவும், சுவாசக் குழாயை திறந்தவாறு வைத்திருங்கள், பக்கவாட்டில் படுக்கவிடவும்.",
        "hi": "आपात स्थिति। प्राथमिक उपचार: सांस की जांच करें, सांस का रास्ता साफ रखें, मरीज को करवट लिटाएं।"
    },
    "severe bleeding": {
        "en": "Emergency condition. First Aid: Apply direct pressure on wound, keep the person still.",
        "ta": "அவசர நிலை. முதலுதவி: காயத்தில் நேரடியாக அழுத்தம் கொடுக்கவும், அந்த நபரை அசையாமல் வைத்திருங்கள்.",
        "hi": "आपात स्थिति। प्राथमिक उपचार: घाव पर सीधे दबाव डालें, मरीज को स्थिर रखें।"
    }
}

# Emergency keywords
emergency_symptoms = ["chest pain", "difficulty breathing", "unconscious", "severe bleeding"]

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/check', methods=['POST'])
def check_symptom():
    data = request.get_json()
    symptom = data.get("symptom", "").lower()
    lang = data.get("lang", "en")

    if symptom in symptom_db:
        response = symptom_db[symptom][lang]

        # If emergency symptom, add alert
        if symptom in emergency_symptoms:
            if lang == "en":
                response += "\n\n🚨 Emergency alert sent! 🚑 Ambulance will reach in 10 minutes."
            elif lang == "ta":
                response += "\n\n🚨 அவசர எச்சரிக்கை அனுப்பப்பட்டது! 🚑 ஆம்புலன்ஸ் 10 நிமிடங்களில் வரும்."
            elif lang == "hi":
                response += "\n\n🚨 आपातकालीन अलर्ट भेजा गया! 🚑 एम्बुलेंस 10 मिनट में पहुँच जाएगी।"

        return jsonify({"response": response, "emergency": symptom in emergency_symptoms})
    else:
        return jsonify({"response": "Symptom not found in database.", "emergency": False})

if __name__ == '__main__':
    app.run(debug=True)
