# 🏥 Jeevan AI – Rural Healthcare Assistant  

This repository contains **Jeevan AI**, an **offline AI-powered healthcare assistant** designed for **rural communities** with limited internet access.  
It helps users get **basic medical guidance** in **English, Hindi, and Tamil**.  

The project has **two versions**:  
- 📟 **CLI Version** → For computers/laptops (completely offline with voice input/output)  
- 🌐 **Web Version** → For smartphones (offline browser app with text input/output)  

---

## 📂 Repository Structure
```
track-3-agenticai-Yuvasri494/
│── cli-version/        # Command Line Interface version
│── web-version/        # Web-based version
│── assets/             # Common screenshots or demo images
│── README.md           # This main documentation
```

---

## 🔹 Why Two Versions?
- **CLI Version** → For rural clinics or kiosks where a computer is available  
- **Web Version** → For rural smartphone users (runs offline in browser)  

This ensures **both doctors and villagers** can use the tool effectively.  

---

## 🚀 How It Works
1. User selects **language** (English / Hindi / Tamil)  
2. Provides **symptom(s)** as input  
3. System searches knowledge base (CSV) for best match  
4. Gives **basic healthcare advice** (text + optional speech)  
5. Emergency option provides quick help  

---

## 📌 Tech Stack
- **Python 3**  
- **Flask (for web)**  
- **pandas**  
- **fuzzywuzzy + Levenshtein** (fuzzy symptom matching)  
- **pyttsx3 / gTTS** (speech output)  
- **Vosk / SpeechRecognition** (CLI voice input)  

---

## ⚙️ Setup & Run
👉 See detailed instructions in each folder:  
- [CLI Version Guide](./cli-version/README.md)  
- [Web Version Guide](./web-version/README.md)  

---


## 🔮 Future Improvements
- Expand knowledge base (more symptoms & advice)  
- Offline **voice input for web version**  
- Integration with **emergency helplines**  
- Progressive Web App (PWA) for **true offline mobile support**  

---

## ⚠️ Disclaimer
This tool provides **basic healthcare guidance only**.  
For serious or emergency conditions, **consult a certified doctor immediately**.
