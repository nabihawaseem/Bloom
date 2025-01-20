import os
from groq import Groq
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env for local development
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Retrieve the GROQ_API_KEY securely
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY is not set. Please check your configuration (Streamlit Secrets or .env).")

# Initialize the Groq client
client = Groq(api_key=api_key)

def generate_quiz_questions(user_focus):
    """
    Generates structured and concise quiz questions using the LLM.
    """
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates concise and clear quiz questions to assess eco-friendly and organic lifestyle habits."},
                {"role": "user", "content": f"Generate 5 concise quiz questions focused on {user_focus}. Format each question as: Q1) What is your habit regarding [specific behavior]? Provide no extra text."}
            ],
            model="llama-3.3-70b-versatile",
        )
        raw_questions = response.choices[0].message.content
        questions = [q.strip() for q in raw_questions.split("\n") if q.strip().startswith("Q")]
        return questions[:5]  # Limit to 5 questions
    except Exception as e:
        st.error(f"Error generating quiz questions: {e}")
        return ["Could not generate quiz questions. Please try again."]

def interpret_answers(answers, user_focus):
    """
    Interprets quiz answers and generates personalized recommendations.
    """
    try:
        # Format answers into a readable string for LLM
        answers_str = "\n".join([f"Q{i+1}: {answer}" for i, answer in enumerate(answers.values())])
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant that interprets quiz answers and provides clear, actionable recommendations for improving eco-friendly and organic habits."},
                {"role": "user", "content": f"Here are the answers to the quiz:\n{answers_str}\nThe focus is: {user_focus}. Provide a score (out of 100) and 3-5 tips formatted as: - Tip 1: [actionable advice]."}
            ],
            model="llama-3.3-70b-versatile",
        )
        raw_response = response.choices[0].message.content
        # Parse the score and tips
        lines = raw_response.split("\n")
        score = next((line for line in lines if "Score:" in line), "Score: 50")
        tips = [line for line in lines if line.startswith("- Tip")]
        return {"score": score.split(":")[1].strip(), "tips": tips}
    except Exception as e:
        st.error(f"Error interpreting answers: {e}")
        return {"score": "N/A", "tips": ["Could not generate recommendations. Please try again."]}
