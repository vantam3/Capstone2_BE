# Capstone2_BE

# 📘 SpeakPro – Backend System (Django)

This is the backend of **SpeakPro – Intelligent English Speaking Assistant**, built using Django REST Framework. It handles functionalities such as:
- User registration/login and profile management
- Speech input and AI-powered pronunciation analysis
- Voice feedback with Google TTS
- Conversational practice with Mistral AI

---

## 🚀 Setup Instructions

### 1️⃣ Step 1: Clone the repository
```bash
git clone https://github.com/vantam3/Capstone2_BE.git
cd speakpro
```

### 2️⃣ Step 2: Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate         # On macOS/Linux
venv\Scripts\activate          # On Windows
```

### 3️⃣ Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Step 4: Create a `.env` configuration file
In the root folder, create a `.env` file with the following content:
```
GOOGLE_API_KEY=your_google_tts_key
MISTRAL_API_KEY=your_mistral_key
DATABASE_URL=mysql://username:password@localhost:3306/speakpro
```

> 📌 You will need to register for Google Cloud and Mistral AI to obtain your API keys.

### 5️⃣ Step 5: Migrate and run the development server
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

---

## 🧠 Tech Stack

| Component        | Technology                          |
|------------------|--------------------------------------|
| Programming Language | Python 3.x                      |
| Framework        | Django, Django REST Framework       |
| AI TTS & NLP     | Google Text-to-Speech API, Mistral AI |
| Database         | MySQL                               |
| Supporting Tools | python-dotenv, GitHub               |

---

## ✅ Key Features
- 🎤 Real-time pronunciation analysis from speech input (AI-powered)
- 🔊 Voice sample feedback using Google TTS
- 🤖 Conversational practice with Mistral AI
- 📈 Progress tracking and scoring
- 🔐 Authentication, role management, and user profile features

---

📬 **Development Team Contact**
- Email: vtam0805@gmail.com (Scrum Master)
- Duy Tan University – Capstone 2, CMU-SE 2025
