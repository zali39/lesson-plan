# Streamlit UI for AI-Powered Python Learning App

import streamlit as st
import requests
import uuid

API_BASE = "http://localhost:8000"  # Adjust if deployed elsewhere

# === Session Management ===
if "session_id" not in st.session_state:
    res = requests.post(f"{API_BASE}/start_session")
    st.session_state.session_id = res.json()["session_id"]

session_id = st.session_state.session_id

st.set_page_config(page_title="AI Python Tutor", layout="wide")
st.title("🧠 AI-Powered Python Learning")

# === Sidebar Navigation ===
st.sidebar.title("Python Topics")
topics = ["Intro to Python", "Variables and Data Types", "Operators and Expressions",
          "Conditional Statements", "Loops", "Functions", "Collections",
          "File Handling", "Debugging", "Basic OOP"]
selected_topic = st.sidebar.radio("Select Topic", topics)
difficulty = st.sidebar.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])

# === Main Layout ===
col1, col2, col3 = st.columns([1.5, 1.5, 2])

# === Learning Panel ===
with col1:
    st.subheader("📘 Learning Panel")
    st.write(f"### {selected_topic}")
    st.markdown("Review the topic and get help from the AI tutor below.")

# === Practice Panel ===
with col2:
    st.subheader("🧪 Practice Panel")
    code_input = st.text_area("Write your Python code below:", "print('Hello, world!')")
    if st.button("Run Code"):
        exec_response = requests.post(f"{API_BASE}/execute_code", json={"code": code_input})
        st.json(exec_response.json())

# === Quiz Panel ===
with col3:
    st.subheader("🧠 Adaptive Quiz")
    if st.button("Generate Quiz"):
        quiz_response = requests.post(f"{API_BASE}/generate_quiz", json={
            "topic": selected_topic,
            "difficulty": difficulty,
            "session_id": session_id
        })
        st.session_state.quiz = quiz_response.json()["quiz"]

    if "quiz" in st.session_state:
        st.markdown(st.session_state.quiz)
        st.radio("Your Answer:", ["A", "B", "C", "D"], key="quiz_answer")
        if st.button("Submit Answer"):
            correct = st.session_state.quiz_answer == "C"  # Dummy check
            score_response = requests.post(f"{API_BASE}/submit_quiz", json={
                "session_id": session_id,
                "topic": selected_topic,
                "correct": correct
            })
            st.success(f"Submitted! New score: {score_response.json()['new_score']:.2f}")

# === AI Tutor Panel ===
st.markdown("---")
st.subheader("🧑‍🏫 Ask the AI Tutor")
tutor_input = st.text_input("Type your question here:")
if st.button("Ask"):
    tutor_response = requests.post(f"{API_BASE}/tutor", json={
        "message": tutor_input,
        "session_id": session_id
    })
    st.markdown(tutor_response.json()["response"])
