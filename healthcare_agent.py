"""
Rural Healthcare AI Assistant
Multilingual offline CLI tool simulating SMS/USSD/IVR experience
"""

import pandas as pd
import pyttsx3
import speech_recognition as sr
from colorama import Fore, Style, init
import os
import sys
import platform
import subprocess
from fuzzywuzzy import fuzz, process
import time
import random

# Initialize colorama
init(autoreset=True)

# Translation dictionary for UI
TRANSLATIONS = {
    'welcome_title': {
        'english': "🏥 RURAL HEALTHCARE AI ASSISTANT 🏥",
        'hindi': "🏥 ग्रामीण स्वास्थ्य एआई सहायक 🏥",
        'tamil': "🏥 கிராமப்புற சுகாதார AI உதவியாளர் 🏥"
    },
    'welcome_msg': {
        'english': "Welcome to your offline healthcare companion!",
        'hindi': "आपके ऑफ़लाइन स्वास्थ्य साथी में आपका स्वागत है!",
        'tamil': "உங்கள் ஆஃப்லைன் சுகாதார உதவியாளருக்கு வரவேற்கிறோம்!"
    },
    'disclaimer': {
        'english': "⚠️ DISCLAIMER: Basic guidance only. Consult doctors for serious cases.",
        'hindi': "⚠️ अस्वीकरण: केवल बुनियादी मार्गदर्शन। गंभीर मामलों में डॉक्टर से संपर्क करें।",
        'tamil': "⚠️ முன்னெச்சரிக்கை: அடிப்படை வழிகாட்டுதல் மட்டுமே. கடுமையான நிகழ்வுகளில் மருத்துவரைக் கலந்தாலோசிக்கவும்."
    },
    'main_menu': {
        'english': ["1. 🩺 Symptom Diagnosis", "2. 🌐 Change Language", "3. 📊 View All Symptoms", "4. 🚑 Emergency Help", "5. ❌ Exit"],
        'hindi': ["1. 🩺 लक्षण निदान", "2. 🌐 भाषा बदलें", "3. 📊 सभी लक्षण देखें", "4. 🚑 आपातकालीन सहायता", "5. ❌ बाहर जाएँ"],
        'tamil': ["1. 🩺 அறிகுறி பரிசோதனை", "2. 🌐 மொழியை மாற்றவும்", "3. 📊 அனைத்து அறிகுறிகளையும் காண்க", "4. 🚑 அவசர உதவி", "5. ❌ வெளியேறு"]
    },
    'describe_symptom': {
        'english': "🩺 Describe your symptom:",
        'hindi': "🩺 अपने लक्षण का वर्णन करें:",
        'tamil': "🩺 உங்கள் அறிகுறியை விவரிக்கவும்:"
    },
    'no_match': {
        'english': "No specific match found for your symptom. Please try a different description or consult a doctor.",
        'hindi': "आपके लक्षण के लिए कोई विशिष्ट मेल नहीं मिला। कृपया कोई अन्य विवरण आज़माएं या डॉक्टर से सलाह लें।",
        'tamil': "உங்கள் அறிகுறிக்கு குறிப்பிட்ட பொருத்தம் கிடைக்கவில்லை. தயவு செய்து வேறு விளக்கத்தை முயற்சிக்கவும் அல்லது மருத்துவரைக் கலந்தாலோசிக்கவும்."
    },
    'general_advice': {
        'english': [
            "💡 General Advice: Rest well and stay hydrated",
            "💡 General Advice: Avoid strenuous activities",
            "💡 General Advice: Apply cold compress if there's swelling",
            "💡 General Advice: Keep the affected area elevated if possible",
            "💡 General Advice: Monitor your symptoms and consult a doctor if they persist"
        ],
        'hindi': [
            "💡 सामान्य सलाह: अच्छी तरह आराम करें और हाइड्रेटेड रहें",
            "💡 सामान्य सलाह: ज़ोरदार गतिविधियों से बचें",
            "💡 सामान्य सलाह: सूजन होने पर ठंडी सिकाई करें",
            "💡 सामान्य सलाह: यदि संभव हो तो प्रभावित क्षेत्र को ऊंचा रखें",
            "💡 सामान्य सलाह: अपने लक्षणों पर नज़र रखें और यदि वे बने रहें तो डॉक्टर से सलाह लें"
        ],
        'tamil': [
            "💡 பொது அறிவுரை: நன்றாக ஓய்வெடுத்து நீரேற்றம் செய்யுங்கள்",
            "💡 பொது அறிவுரை: கடினமான செயல்களைத் தவிர்க்கவும்",
            "💡 பொது அறிவுரை: வீக்கம் இருந்தால் குளிர் அழுத்தம் பயன்படுத்தவும்",
            "💡 பொது அறிவுரை: முடிந்தால் பாதிக்கப்பட்ட பகுதியை உயர்த்தி வைக்கவும்",
            "💡 பொது அறிவுரை: உங்கள் அறிகுறிகளை கண்காணித்து, அவை தொடர்ந்தால் மருத்துவரை அணுகவும்"
        ]
    },
    'thank_you': {
        'english': "✅ Thank you for using Rural Healthcare AI Assistant. Stay healthy!",
        'hindi': "✅ ग्रामीण स्वास्थ्य एआई सहायक का उपयोग करने के लिए धन्यवाद। स्वस्थ रहें!",
        'tamil': "✅ கிராமப்புற சுகாதார AI உதவியாளரைப் பயன்படுத்தியதற்கு நன்றி. ஆரோக்கியமாக இருங்கள்!"
    },
    'voice_fallback': {
        'english': "Voice not recognized. Falling back to text input...",
        'hindi': "वॉइस नहीं पहचाना गया। टेक्स्ट इनपुट पर स्विच कर रहे हैं...",
        'tamil': "குரல் அறியப்படவில்லை. உரை உள்ளீட்டுக்குத் திரும்புகிறது..."
    },
    'emergency_msg': {
        'english': "🚑 Emergency help requested! Ambulance is on the way. Please wait and stay calm.",
        'hindi': "🚑 आपातकालीन सहायता का अनुरोध किया गया! एम्बुलेंस रास्ते में है। कृपया प्रतीक्षा करें और शांत रहें।",
        'tamil': "🚑 அவசர உதவி கோரப்பட்டது! ஆம்புலன்ஸ் வழியில் உள்ளது. தயவு செய்து காத்திருக்கவும் அமைதியாக இருங்கள்."
    },
    'first_aid_emergency': {
        'english': "🩹 First Aid: Check responsiveness, call for help, perform CPR if trained, control bleeding if present.",
        'hindi': "🩹 प्राथमिक उपचार: प्रतिक्रिया जांचें, मदद के लिए बुलाएं, यदि प्रशिक्षित हैं तो सीपीआर करें, रक्तस्राव होने पर उसे नियंत्रित करें।",
        'tamil': "🩹 முதல் உதவி: பதிலளிப்பதை சரிபார்க்கவும், உதவிக்கு அழைக்கவும், பயிற்சி பெற்றவர்கள் CPR செய்யவும், இரத்தப்போக்கு இருந்தால் அதைக் கட்டுப்படுத்தவும்."
    },
    'input_method_prompt': {
        'english': "Choose input method:",
        'hindi': "इनपुट विधि चुनें:",
        'tamil': "உள்ளீட்டு முறையைத் தேர்ந்தெடுக்கவும்:"
    },
    'voice_option': {
        'english': "1. 🎤 Voice input (requires internet)",
        'hindi': "1. 🎤 वॉइस इनपुट (इंटरनेट आवश्यक)",
        'tamil': "1. 🎤 குரல் உள்ளீடு (இணையம் தேவை)"
    },
    'text_option': {
        'english': "2. ⌨️ Text input",
        'hindi': "2. ⌨️ टेक्स्ट इनपुट",
        'tamil': "2. ⌨️ உரை உள்ளீடு"
    },
    'ambulance_arrival_time': {
        'english': "⏳ Estimated ambulance arrival time:",
        'hindi': "⏳ एम्बुलेंस के आने का अनुमानित समय:",
        'tamil': "⏳ ஆம்புலன்ஸ் வரும் மதிப்பிடப்பட்ட நேரம்:"
    },
    'minutes_remaining': {
        'english': "minutes remaining...",
        'hindi': "मिनट बाकी...",
        'tamil': "நிமிடங்கள் மீதமுள்ளன..."
    },
    'ambulance_arrived': {
        'english': "🚑 Ambulance has arrived! Help is here.",
        'hindi': "🚑 एम्बुलेंस आ गई! मदद यहाँ है।",
        'tamil': "🚑 ஆம்புலன்ஸ் வந்துவிட்டது! உதவி இங்கே உள்ளது."
    }
}

LABELS = {
    'english': {
        'symptom': "📋 Symptom",
        'confidence': "🎯 Confidence",
        'severity': "⚠️ Severity",
        'advice': "💡 Advice",
        'first_aid': "🩹 First Aid"
    },
    'hindi': {
        'symptom': "📋 लक्षण",
        'confidence': "🎯 भरोसा",
        'severity': "⚠️ गंभीरता",
        'advice': "💡 सलाह",
        'first_aid': "🩹 प्राथमिक उपचार"
    },
    'tamil': {
        'symptom': "📋 அறிகுறி",
        'confidence': "🎯 நம்பிக்கை",
        'severity': "⚠️ தீவிரம்",
        'advice': "💡 அறிவுரை",
        'first_aid': "🩹 முதல் உதவி"
    }
}

class HealthcareAssistant:
    def __init__(self):
        self.df = None
        self.tts_engine = None
        self.recognizer = None
        self.microphone = None
        self.current_language = 'english'
        self.language_codes = {'english': 'en','hindi':'hi','tamil':'ta'}
        self.setup_components()
        self.load_knowledge_base()

    def get_text(self, key):
        return TRANSLATIONS.get(key, {}).get(self.current_language, key)

    def setup_components(self):
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Set first available voice as default
                self.tts_engine.setProperty('voice', voices[0].id)
                # Adjust rate for better clarity
                rate = self.tts_engine.getProperty('rate')
                self.tts_engine.setProperty('rate', max(150, rate - 50))
            print(f"{Fore.GREEN}✅ Offline TTS initialized successfully")
            
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            print(f"{Fore.GREEN}✅ Speech recognition available")
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️ TTS setup warning: {e}")
            print(f"{Fore.YELLOW}   Fallback: Text-only mode available")

    def load_knowledge_base(self):
        try:
            if not os.path.exists('healthcare_kb.csv'):
                print(f"{Fore.RED}Error: healthcare_kb.csv not found!")
                # Create a minimal demo knowledge base
                self.create_demo_knowledge_base()
                print(f"{Fore.GREEN}✅ Created demo knowledge base")
            else:
                self.df = pd.read_csv('healthcare_kb.csv')
                print(f"{Fore.GREEN}✅ Knowledge base loaded: {len(self.df)} symptoms available")
        except Exception as e:
            print(f"{Fore.RED}Error loading knowledge base: {e}")
            self.create_demo_knowledge_base()
            print(f"{Fore.GREEN}✅ Created demo knowledge base as fallback")

    def create_demo_knowledge_base(self):
        """Create a simple demo knowledge base if the main one is not available"""
        data = {
            'symptom_english': ['fever', 'headache', 'chest pain', 'stomach ache', 'cough'],
            'symptom_hindi': ['बुखार', 'सिर दर्द', 'सीने में दर्द', 'पेट दर्द', 'खांसी'],
            'symptom_tamil': ['காய்ச்சல்', 'தலைவலி', 'நெஞ்சு வலி', 'வயிறு வலி', 'இருமல்'],
            'severity': ['H', 'H', 'E', 'D', 'H'],
            'advice_english': [
                'Rest and drink plenty of fluids',
                'Take rest in a dark room and use cold compress',
                'Seek immediate medical attention',
                'Avoid spicy food and drink plenty of water',
                'Stay hydrated and use honey lemon tea'
            ],
            'advice_hindi': [
                'आराम करें और खूब सारे तरल पदार्थ पिएं',
                'अंधेरे कमरे में आराम करें और ठंडी सिकाई का उपयोग करें',
                'तत्काल चिकित्सा सहायता लें',
                'मसालेदार भोजन से बचें और खूब पानी पिएं',
                'हाइड्रेटेड रहें और शहद नींबू की चाय का उपयोग करें'
            ],
            'advice_tamil': [
                'ஓய்வெடுத்து நிறைய திரவங்களை குடிக்கவும்',
                'இருண்ட அறையில் ஓய்வெடுத்துக் குளிர் அழுத்தம் பயன்படுத்தவும்',
                'உடனடியாக மருத்துவ உதவி பெறவும்',
                'காரமான உணவுகளை தவிர்த்து நிறைய தண்ணீர் குடிக்கவும்',
                'நீரேற்றம் செய்து தேன் எலுமிச்சை தேநீர் பயன்படுத்தவும்'
            ],
            'first_aid_english': [
                'Take paracetamol and use cold sponge',
                'Apply cold compress to forehead',
                'Call emergency services immediately',
                'Apply heat to abdomen and avoid solid foods',
                'Use cough drops and stay hydrated'
            ],
            'first_aid_hindi': [
                'पैरासिटामोल लें और ठंडे स्पंज का उपयोग करें',
                'माथे पर ठंडी सिकाई लगाएं',
                'तुरंत आपातकालीन सेवाओं को कॉल करें',
                'पेट पर गर्मी लगाएं और ठोस foods से बचें',
                'खांसी की दवा का use करें और हाइड्रेटेड रहें'
            ],
            'first_aid_tamil': [
                'பாராசிட்டமோல் எடுத்து குளிர் ச்போஞ்ச் பயன்படுத்தவும்',
                'நெற்றியில் குளிர் அழுत்தம் apply செய்யவும்',
                'உடனடியாக அவசர சேவைகளை அழைக்கவும்',
                'வயிற்றில் வெப்பம் apply செய்து திட உணவுகளை தவிர்க்கவும்',
                'இருமல் மாத்திரைகள் பயன்படுத்தி நீரேற்றம் செய்யவும்'
            ]
        }
        self.df = pd.DataFrame(data)
        self.df.to_csv('healthcare_kb.csv', index=False)

    def speak_text(self, text):
        """
        Enhanced offline text-to-speech with multiple fallback options
        """
        # Remove emojis and special characters for cleaner speech
        clean_text = ''.join(c for c in text if c.isalnum() or c.isspace() or c in '.,!?')
        
        if not clean_text.strip():
            return
            
        # Method 1: Try pyttsx3 (cross-platform offline TTS)
        if self.tts_engine:
            try:
                self.tts_engine.say(clean_text)
                self.tts_engine.runAndWait()
                return
            except Exception as e:
                print(f"{Fore.YELLOW}[TTS Warning]: pyttsx3 failed: {e}")
        
        # Method 2: System-specific TTS fallbacks
        system = platform.system()
        try:
            if system == "Windows":
                # Windows SAPI via PowerShell
                cmd = f'powershell -Command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{clean_text}\')"'
                subprocess.run(cmd, shell=True, capture_output=True, timeout=10)
                return
                
            elif system == "Darwin":  # macOS
                subprocess.run(['say', clean_text], timeout=10)
                return
                
            elif system == "Linux":
                # Try espeak first, then festival
                try:
                    subprocess.run(['espeak', clean_text], timeout=10, capture_output=True)
                    return
                except FileNotFoundError:
                    subprocess.run(['festival', '--tts'], input=clean_text, text=True, timeout=10)
                    return
                    
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
            print(f"{Fore.YELLOW}[TTS Info]: System TTS unavailable: {e}")
        
        # Method 3: Text display fallback (always works)
        print(f"{Fore.CYAN}[AUDIO]: {text}")
    
    def select_language(self):
        prompt = "\n🌐 Select language / மொழி / भाषा [1:English, 2:हिंदी, 3:தமிழ்]:"
        print(prompt)
        self.speak_text(prompt)
        while True:
            choice = input("Enter choice (1-3): ").strip()
            if choice=='1': 
                self.current_language='english'
                break
            elif choice=='2': 
                self.current_language='hindi'
                break
            elif choice=='3': 
                self.current_language='tamil'
                break
            else: 
                error_msg = "Invalid. Enter 1-3."
                print(error_msg)
                self.speak_text(error_msg)

    def show_welcome_screen(self):
        print(f"{Fore.GREEN}{Style.BRIGHT}")
        print("="*60)
        title = self.get_text('welcome_title')
        print(title)
        print("="*60)
        welcome = self.get_text('welcome_msg')
        disclaimer = self.get_text('disclaimer')
        print(welcome)
        print(disclaimer)
        print("="*60)
        self.speak_text(title)
        self.speak_text(welcome)
        self.speak_text(disclaimer)
    
    def show_menu(self):
        menu_lines = self.get_text('main_menu')
        for line in menu_lines:
            print(line)
        self.speak_text(" ".join(menu_lines))

    def get_multilingual_input(self, prompt):
        """Get input with choice of voice or text method"""
        print(f"\n{self.get_text('input_method_prompt')}")
        print(self.get_text('voice_option'))
        print(self.get_text('text_option'))
        
        choice = input("Enter choice (1-2): ").strip()
        
        if choice == '1':
            return self.get_voice_input(prompt)
        else:
            return self.get_text_input(prompt)

    def get_voice_input(self, prompt):
        """Get input via voice recognition"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                listen_msg = "🎤 Listening for 10 seconds... speak now"
                print(listen_msg)
                self.speak_text(listen_msg)
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
                text = self.recognizer.recognize_google(audio, language=self.language_codes[self.current_language])
                print(f"📝 You said: {text}")
                self.speak_text(f"You said: {text}")
                return text.lower().strip()
        except (sr.UnknownValueError, sr.WaitTimeoutError):
            fallback_msg = self.get_text('voice_fallback')
            print(fallback_msg)
            self.speak_text(fallback_msg)
            return self.get_text_input(prompt)
        except sr.RequestError:
            error_msg = "❌ Speech recognition service unavailable. Falling back to text input..."
            print(error_msg)
            self.speak_text(error_msg)
            return self.get_text_input(prompt)
        except Exception as e:
            error_msg = f"❌ Error: {e}. Falling back to text input..."
            print(error_msg)
            self.speak_text(error_msg)
            return self.get_text_input(prompt)

    def get_text_input(self, prompt):
        """Get input via text"""
        print(f"\n{prompt}")
        user_input = input("Enter text: ").strip().lower()
        return user_input

    def find_matching_symptom(self, user_input):
        # First check if input is empty or too short
        if not user_input or len(user_input.strip()) < 3:
            return None, 0
            
        col = f"symptom_{self.current_language}"
        if col not in self.df.columns: 
            col = "symptom_english"
            
        symptoms = self.df[col].str.lower().fillna('').tolist()
        
        # Use partial ratio for better matching of partial words
        best_match = process.extractOne(user_input, symptoms, scorer=fuzz.partial_ratio)
        
        if best_match and best_match[1] >= 90:  # Higher threshold for better accuracy
            row = self.df[self.df[col].str.lower().fillna('') == best_match[0]]
            if not row.empty: 
                return row.iloc[0], best_match[1]
                
        return None, 0

    def display_symptom_info(self, row, conf):
        col = f"symptom_{self.current_language}"
        name = row[col] if col in row and not pd.isna(row[col]) else row['symptom_english']

        SEVERITY_TRANSLATIONS = {
            'H': {'english': '🏠 HOME CARE', 'hindi': '🏠 घरेलू देखभाल', 'tamil': '🏠 வீட்டில் பராமரிப்பு'},
            'D': {'english': '👨‍⚕️ DOCTOR VISIT', 'hindi': '👨‍⚕️ डॉक्टर को दिखाएँ', 'tamil': '👨‍⚕️ மருத்துவரை அணுகவும்'},
            'E': {'english': '🚨 EMERGENCY', 'hindi': '🚨 आपातकाल', 'tamil': '🚨 அவசரம்'}
        }

        color_map = {'H': Fore.GREEN, 'D': Fore.YELLOW, 'E': Fore.RED}
        color = color_map.get(row['severity'], Fore.WHITE)
        severity_text = SEVERITY_TRANSLATIONS.get(row['severity'], {}).get(self.current_language, 'UNKNOWN')

        advice_col = f"advice_{self.current_language}"
        advice = row[advice_col] if advice_col in row and not pd.isna(row[advice_col]) else row['advice_english']
        
        first_aid_col = f"first_aid_{self.current_language}"
        first_aid = row[first_aid_col] if first_aid_col in row and not pd.isna(row[first_aid_col]) else row['first_aid_english']

        print(f"\n{Fore.CYAN}{'='*50}")
        labels = LABELS[self.current_language]

        print(f"{labels['symptom']}: {name}")
        self.speak_text(f"{labels['symptom']}: {name}")

        print(f"{labels['confidence']}: {conf}%")
        self.speak_text(f"{labels['confidence']}: {conf} percent")

        print(f"{labels['severity']}: {color}{severity_text}")
        self.speak_text(f"{labels['severity']}: {severity_text}")

        print(f"{labels['advice']}: {advice}")
        self.speak_text(f"{labels['advice']}: {advice}")

        print(f"{labels['first_aid']}: {first_aid}")
        self.speak_text(f"{labels['first_aid']}: {first_aid}")

        print(f"{Fore.CYAN}{'='*50}")

    def display_general_advice(self):
        """Display general health advice when no specific symptom is matched"""
        print(f"\n{Fore.YELLOW}{'='*50}")
        print(f"💡 {self.get_text('no_match')}")
        self.speak_text(self.get_text('no_match'))
        
        # Show 2-3 random general advice items
        general_advice = self.get_text('general_advice')
        selected_advice = random.sample(general_advice, min(3, len(general_advice)))
        
        for advice in selected_advice:
            print(f"{Fore.YELLOW}{advice}")
            self.speak_text(advice)
            
        print(f"{Fore.YELLOW}{'='*50}")

    def view_all_symptoms(self):
        print(f"\n📊 Symptoms in DB:")
        self.speak_text("Symptoms in database")
        col = f"symptom_{self.current_language}"
        if col not in self.df.columns: 
            col = "symptom_english"
            
        for _, r in self.df.iterrows():
            sev = r['severity']
            color = {'H': Fore.GREEN, 'D': Fore.YELLOW, 'E': Fore.RED}.get(sev, Fore.WHITE)
            name = r[col] if not pd.isna(r[col]) else r['symptom_english']
            print(f"{color}• {name} ({sev})")
        self.speak_text("Displayed all symptoms")

    def handle_emergency(self):
        """Handle emergency request with ambulance alert and first aid instructions"""
        emergency_msg = self.get_text('emergency_msg')
        first_aid_msg = self.get_text('first_aid_emergency')
        
        # Display emergency message with red background for attention
        print(f"{Fore.RED}{Style.BRIGHT}")
        print("!" * 60)
        print(emergency_msg)
        print("!" * 60)
        print(f"{Fore.YELLOW}{first_aid_msg}")
        print(f"{Fore.RED}{Style.BRIGHT}" + "!" * 60)
        
        # Speak the emergency messages
        self.speak_text(emergency_msg)
        time.sleep(2)
        self.speak_text(first_aid_msg)
        
        # Countdown to simulate waiting for ambulance
        arrival_time_msg = self.get_text('ambulance_arrival_time')
        print(f"\n{Fore.CYAN}{arrival_time_msg}")
        self.speak_text(arrival_time_msg)
        
        minutes_remaining_text = self.get_text('minutes_remaining')
        for i in range(5, 0, -1):
            countdown_msg = f"{i} {minutes_remaining_text}"
            print(f"{Fore.CYAN}{countdown_msg}")
            self.speak_text(countdown_msg)
            time.sleep(1)
            
        ambulance_arrived_msg = self.get_text('ambulance_arrived')
        print(f"{Fore.GREEN}{ambulance_arrived_msg}")
        self.speak_text(ambulance_arrived_msg)

    def run(self):
        self.select_language()
        self.show_welcome_screen()
        
        while True:
            self.show_menu()
            choice = input("Enter choice (1-5): ").strip()
            
            if choice == '1':
                user_input = self.get_multilingual_input(self.get_text('describe_symptom'))
                if not user_input or len(user_input.strip()) < 3:
                    print("Please provide a more detailed description of your symptom.")
                    self.speak_text("Please provide a more detailed description of your symptom.")
                    continue
                    
                row, conf = self.find_matching_symptom(user_input)
                if row is not None: 
                    self.display_symptom_info(row, conf)
                else: 
                    self.display_general_advice()
                    
            elif choice == '2':
                self.select_language()
                
            elif choice == '3':
                self.view_all_symptoms()
                
            elif choice == '4':
                self.handle_emergency()
                
            elif choice == '5':
                msg = self.get_text('thank_you')
                print(msg)
                self.speak_text(msg)
                break
                
            else: 
                print("Invalid. Enter 1-5.")
                self.speak_text("Invalid. Enter 1 to 5.")

def main():
    try:
        assistant = HealthcareAssistant()
        assistant.run()
    except KeyboardInterrupt:
        print("\n👋 Exiting... Stay safe!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
