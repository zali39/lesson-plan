# AI-Powered Python Learning App

This app combines FastAPI and Streamlit to deliver an adaptive, AI-powered experience for learning basic Python programming.

---

## 🚀 Features
- Adaptive quiz engine based on learner performance
- Code execution sandbox
- AI tutor chat (GPT-powered)
- Session tracking and analytics

---

## 🛠️ Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/yourname/ai-python-learning-app.git
cd ai-python-learning-app
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set OpenAI API Key
```bash
export OPENAI_API_KEY=your_api_key_here  # Or use .env
```

### 4. Run FastAPI Backend
```bash
uvicorn main:app --reload
```

### 5. Run Streamlit Frontend
```bash
streamlit run streamlit_ui.py
```

---

## 🌐 Deployment

Use **Render**, **Railway**, or **Heroku**:
- Add a `Procfile` for backend
- Set env var `OPENAI_API_KEY`
- Use `requirements.txt` to install dependencies

Streamlit Cloud:
- Point to `streamlit_ui.py`
- Update `API_BASE` URL to point to your deployed FastAPI endpoint

---

## 📄 License
MIT License
