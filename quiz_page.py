# quiz_page.py
import streamlit as st
from backend.llm_helper import generate_quiz_questions, interpret_answers

def render():
    """
    Renders the Quiz Page with clear questions and structured recommendations.
    """
    st.title("Eco-Friendly & Organic Lifestyle Quiz")
    
    # Step 1: User Input
    user_focus = st.text_area(
        "What do you want to improve about your lifestyle?",
        placeholder="E.g., I want to reduce plastic use, eat healthier, and switch to eco-friendly products."
    )

    if st.button("Generate Quiz"):
        if user_focus:
            # Step 2: Generate Quiz Questions Using LLM
            quiz_questions = generate_quiz_questions(user_focus)
            st.session_state["quiz_questions"] = quiz_questions
        else:
            st.warning("Please describe your lifestyle focus!")

    # Step 3: Display Quiz
    if "quiz_questions" in st.session_state:
        st.subheader("Your Personalized Quiz")
        answers = {}
        for idx, question in enumerate(st.session_state["quiz_questions"]):
            st.write(f"{question}")
            answers[f"q{idx}"] = st.radio(f"Answer for Q{idx+1}:", ["Never", "Rarely", "Sometimes", "Often", "Always"], key=f"q{idx}")

        # Step 4: Submit Answers and Generate Recommendations
        if st.button("Get Results"):
            results = interpret_answers(answers, user_focus)
            # st.subheader("Your Sustainability Score")
            # st.write(f"**Score:** {results['score']}/100")
            st.subheader("Personalized Tips")
            for tip in results["tips"]:
                st.write(tip)
