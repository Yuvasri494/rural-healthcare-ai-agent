# 🌐 Rural Healthcare AI Assistant (Web Version)

This is the **Web-based Offline Version** of the *Rural Healthcare AI Assistant*, designed for **rural smartphone users without internet access**.  
It provides **symptom diagnosis, multilingual support, and voice output** — all running locally on the user’s device.  

---

## 🚀 Features
- ✅ **Works Offline** (no internet needed, except optional TTS downloads)  
- ✅ **Supports Multiple Languages** (English, தமிழ், हिंदी)  
- ✅ **Symptom Diagnosis** using fuzzy matching with medical knowledge base (`symptoms.csv`)  
- ✅ **Voice Output** with `gTTS` (offline playback after generation)  
- ✅ **Simple & Mobile-friendly UI** (via `index.html`)  
- ✅ **Flask Backend** to handle symptom queries  

---

## 📂 Project Structure
```
web-version/
├── app.py               # Flask backend
├── requirements.txt     # Dependencies
├── symptoms.csv         # Knowledge base
├── templates/
│   └── index.html       # Web UI
```

---

## ⚙️ Requirements
All required Python libraries are listed in `requirements.txt`.  

Main dependencies:
- `flask`  
- `flask-cors`  
- `pandas`  
- `fuzzywuzzy`  
- `python-Levenshtein`  
- `gtts`  

---

## 📥 Installation & Setup



Follow these steps to test the **Rural Healthcare AI Assistant (Web Version)** locally:

---

### 1️⃣ Open the Project
- Download or clone this repo:
  ```bash
  git clone https://github.com/Yuvasri494/track-3-agenticai-Yuvasri494.git
  cd track-3-agenticai-Yuvasri494/web-version
  ```

---

### 2️⃣ Setup Python Environment
- Create a virtual environment:
  ```bash
  python -m venv .venv
  ```
- Activate it:
  - **Windows (PowerShell):**
    ```bash
    .venv\Scripts\activate
    ```
  - **Linux/Mac:**
    ```bash
    source .venv/bin/activate
    ```

---

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 4️⃣ Run the Web App
```bash
python app.py
```

---

### 5️⃣ Open in Browser
- Go to: 👉 `http://127.0.0.1:5000`
- You will see a simple input box (English, हिंदी, தமிழ் supported).
- Then open index.html with live server
---

### 6️⃣ Test Inputs
Try typing:
- `headache` (English)  
- `सीने में दर्द` (Hindi for chest pain)  
- `மயக்கம்` (Tamil for dizziness)  

The system will:
- Match your input to the closest symptom in **symptoms.csv**  
- Show basic healthcare advice on screen  
- Play voice output (using **gTTS**)  

---

### 7️⃣ Exit
- Press **CTRL+C** in the terminal to stop the server.  

---

⚠️ **Note**: Voice *input* (speech-to-text) is not included in the offline web version. Only **text input + voice output** is supported.


## 👥 Target Users
- Rural and semi-urban communities with **limited internet**  
- People with **low access to doctors**  
- Support for **regional languages** to improve accessibility  

---
## ⚠️ Known Issues / Limitations (Web Version)

- **Browser Compatibility**  
  - Voice input uses the **Web Speech API**, which is **not fully supported in Microsoft Edge**.  
  - ✅ Voice input works best in **Google Chrome**.  
  - ❌ In Edge or some other browsers, voice input may not work.  

- **Offline Mode**  
  - Core text input features and symptom diagnosis run **fully offline**.  
  - Voice input requires browser support (currently stable in Chrome).

## 🔮 Future Improvements
- 📌 Add **offline voice recognition** (currently only text input works offline)  
- 📌 Expand **medical knowledge base** with more symptoms & conditions  
- 📌 Add **emergency contact integration** for quick help  
- 📌 Improve **UI/UX for mobile users**  
- 📌 Deploy as a **Progressive Web App (PWA)** for offline-first experience  

---

## ⚠️ Disclaimer
This tool is for **basic healthcare guidance only**.  
It is **NOT a replacement for professional doctors**.  
Always consult a medical professional for serious or emergency cases.  


