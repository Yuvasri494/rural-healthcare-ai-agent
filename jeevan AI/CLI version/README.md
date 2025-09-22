# CLI Version
This folder contains the CLI-based Jeevan AI- Rural Healthcare Assistant.
# Jeevan AI - Rural Healthcare Assistant (CLI Version)

🏥 **CLI-based Offline Rural Healthcare AI Assistant**  
This project simulates a Rural Healthcare Assistant that works offline through the Command-Line Interface (CLI). It provides multilingual guidance (English, Hindi, Tamil), symptom diagnosis, first-aid advice, and emergency assistance.

---

## Features

- Multilingual support: English, Hindi, Tamil  
- Symptom diagnosis based on a CSV knowledge base  
- General health advice if exact symptom not found  
- Emergency help simulation with ambulance countdown  
- Offline text-to-speech (TTS) for better accessibility  
- Input via text or voice (voice input requires internet)  
- Simple first-aid guidance  

---
## Detailed Features & Menu Options

### 1. Symptom Diagnosis (🩺)
- **Function:** Enter your symptom description.  
- **Process:**
  1. Choose input method (voice or text).  
  2. AI searches the knowledge base for the closest symptom match.  
  3. Displays:
     - Symptom name  
     - Confidence score (match percentage)  
     - Severity (🏠 Home Care / 👨‍⚕️ Doctor Visit / 🚨 Emergency)  
     - Advice in selected language  
     - First-aid instructions  
- **Fallback:** If voice not recognized, switches to text input automatically.  

---

### 2. Change Language (🌐)
- **Function:** Switch between English, Hindi, or Tamil for menus, messages, and advice.  
- **Supported Languages Codes:**
  - English → `en`  
  - Hindi → `hi`  
  - Tamil → `ta`  

---

### 3. View All Symptoms (📊)
- **Function:** Displays the complete knowledge base of symptoms in the selected language.  
- **Details Shown:** Symptom name, severity indicator (color-coded: Green = Home, Yellow = Doctor, Red = Emergency).  

---

### 4. Emergency Help (🚑)
- **Function:** Provides first-aid instructions and simulates an ambulance arrival countdown.  
- **Steps:**
  1. Displays emergency message and first-aid guidance.  
  2. Countdown simulation for ambulance arrival (5 minutes by default).  
  3. Final message indicating ambulance has arrived.  
- **Accessibility:** TTS reads out emergency messages for offline use.  

---

### 5. Exit (❌)
- **Function:** Ends the CLI session gracefully with a thank-you message.  

---

## Input Methods

1. **Voice Input (🎤)**
   - Requires internet connection.  
   - Uses `speech_recognition` and microphone to capture speech.  
   - Falls back to text input if voice recognition fails.  

2. **Text Input (⌨️)**
   - Fully offline.  
   - Users type symptoms or menu choices manually.  

---

## How It Works

1. User selects language at startup.  
2. Welcome screen shows AI assistant name, greeting, and disclaimer.  
3. User navigates the menu to diagnose symptoms, view all symptoms, change language, or request emergency help.  
4. AI matches input with CSV knowledge base using `fuzzywuzzy`.  
5. Displays advice, severity, first-aid guidance, and speaks text using offline TTS.  
6. Emergency help triggers a simulated countdown for ambulance arrival.  




---

## Requirements

- Python 3.8+  
- Libraries:
  ```text
  pandas
  pyttsx3
  speechrecognition
  colorama
  fuzzywuzzy
  python-Levenshtein
## Screenshots
English Version

Hindi Version

Tamil Version
## Setup Instructions (CLI Version)

1. **Clone Repository:**

```bash
git clone https://github.com/CNI-GenAI-Hackathon2025/track-3-agenticai-Yuvasri494.git
cd track-3-agenticai-Yuvasri494/cli-version
```

2. **Create Virtual Environment:**

```bash
python -m venv .venv
```

3. **Activate Virtual Environment:**

- Windows (PowerShell):
```bash
.venv\Scripts\Activate.ps1
```
- Windows (CMD):
```bash
.venv\Scripts\activate.bat
```
- macOS / Linux:
```bash
source .venv/bin/activate
```

4. **Install Dependencies:**

```bash
pip install -r requirements.txt
```

5. **Run CLI Tool:**

```bash
python healthcare_agent.py
```

6. **Use Options:**
- `1` – Symptom Diagnosis  
- `2` – Change Language  
- `3` – View All Symptoms  
- `4` – Emergency Help  
- `5` – Exit  

---
---

## ⚠️ Known Issues / Limitations (Voice Input)

- **PyAudio Dependency**  
  - Voice input requires **PyAudio**, which may not install easily on all systems.  
  - If PyAudio is missing, the program will automatically fall back to **Text Input Mode (⌨️)**.  
  - Core CLI features work fully offline without voice input.

- **Vosk STT Accuracy**  
  - Vosk-based speech recognition is available, but models for **தமிழ் (Tamil)** and **हिंदी (Hindi)** are limited.  
  - Recognition in these languages may not be fully accurate.  
  - English recognition works better compared to regional languages.

✅ These limitations affect only the **optional voice input**.  
✅ Text input remains **accurate, offline, and stable**.


## Future Improvements

- Enable **voice recognition offline** for Hindi and Tamil.  
- Expand the **knowledge base** with more symptoms and treatments.  
- Add **logging for user interactions** to improve AI advice.  
- Integrate **SMS or WhatsApp notifications** for rural users.  
- Enhance **CLI interface** for color-blind-friendly text and accessibility.  
- Option to **export reports** for doctors or health workers.  

---

## License

MIT License © 2025 Yuvasri
---

