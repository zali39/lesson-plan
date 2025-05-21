# AI-Powered Python Learning App: Enhanced Scaffold with Adaptive Quiz Logic

# === Backend (FastAPI) ===
from fastapi import FastAPI, Request
from pydantic import BaseModel
import random
import openai
import uuid
from typing import Dict

app = FastAPI()

openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace securely in production

# In-memory user session store (replace with DB in production)
sessions: Dict[str, Dict] = {}

class QuizRequest(BaseModel):
    topic: str
    difficulty: str
    session_id: str

class TutorRequest(BaseModel):
    message: str
    session_id: str

@app.post("/start_session")
def start_session():
    session_id = str(uuid.uuid4())
    sessions[session_id] = {"history": [], "progress": {}, "quiz_history": []}
    return {"session_id": session_id}

@app.post("/generate_quiz")
async def generate_quiz(req: QuizRequest):
    session = sessions[req.session_id]
    weak_topics = [k for k, v in session["progress"].items() if v < 0.5]
    topic_to_use = weak_topics[0] if weak_topics else req.topic
    prompt = f"Create a multiple-choice question on {topic_to_use} for a {req.difficulty} level Python learner."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    quiz_text = response.choices[0].message['content']
    session["last_quiz"] = quiz_text
    session["quiz_history"].append({"topic": topic_to_use, "quiz": quiz_text})
    return {"quiz": quiz_text}

@app.post("/submit_quiz")
async def submit_quiz(request: Request):
    body = await request.json()
    session_id = body["session_id"]
    topic = body["topic"]
    correct = body["correct"]
    progress = sessions[session_id].get("progress", {})
    score = progress.get(topic, 0.5)
    updated_score = min(max(score + 0.1 if correct else score - 0.1, 0), 1)
    sessions[session_id]["progress"][topic] = updated_score
    return {"message": "Score updated", "new_score": updated_score}

@app.post("/tutor")
async def tutor_chat(req: TutorRequest):
    session = sessions[req.session_id]
    chat_history = session.get("history", [])
    chat = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a Python tutor for beginners."},
            *chat_history,
            {"role": "user", "content": req.message}
        ]
    )
    response_msg = chat.choices[0].message['content']
    chat_history.append({"role": "user", "content": req.message})
    chat_history.append({"role": "assistant", "content": response_msg})
    session["history"] = chat_history
    return {"response": response_msg}

# === Curriculum Structure ===
curriculum = [
    {"module": 1, "title": "Intro to Python", "objectives": ["Understand Python syntax", "Set up Python environment"]},
    {"module": 2, "title": "Variables and Data Types", "objectives": ["Declare variables", "Use different data types"]},
    {"module": 3, "title": "Operators and Expressions", "objectives": ["Use arithmetic, comparison and logical operators"]},
    {"module": 4, "title": "Conditional Statements", "objectives": ["Write if-else logic"]},
    {"module": 5, "title": "Loops", "objectives": ["Use for and while loops"]},
    {"module": 6, "title": "Functions", "objectives": ["Define and call functions"]},
    {"module": 7, "title": "Collections", "objectives": ["Use lists, tuples, sets, dictionaries"]},
    {"module": 8, "title": "File Handling", "objectives": ["Read/write to files"]},
    {"module": 9, "title": "Debugging", "objectives": ["Trace and fix errors"]},
    {"module": 10, "title": "Basic OOP (Optional)", "objectives": ["Define classes and objects"]},
]

# === Code Execution Sandbox ===
@app.post("/execute_code")
async def execute_code(req: Request):
    body = await req.json()
    code = body.get("code")
    try:
        exec_globals = {}
        exec(code, exec_globals)
        return {"result": str(exec_globals)}
    except Exception as e:
        return {"error": str(e)}

# === LMS Integration Placeholder ===
@app.get("/lms_export")
def lms_export():
    return {"message": "This would generate SCORM or xAPI-compatible logs or progress files for LMS import."}

# === Run with uvicorn ===
# uvicorn main:app --reload
