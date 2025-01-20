import os
from groq import Groq
import streamlit as st
from dotenv import load_dotenv

# Load environment variables for local development
dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Retrieve the GROQ_API_KEY securely
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY is not set. Please check your configuration (Streamlit Secrets or .env).")

# Initialize Groq client
client = Groq(api_key=api_key)

def generate_query(product_name):
    """
    Generates a concise and tailored search query using Groq API's LLaMA 3.3 model.
    """
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates concise and valid search queries."},
                {"role": "user", "content": f"Generate a short and precise search query for eco-friendly {product_name} alternatives. Only include one concise query."}
            ],
            model="llama-3.3-70b-versatile",
        )
        # Extract only the first suggestion (before any "or" or additional suggestions)
        full_response = chat_completion.choices[0].message.content.strip()
        concise_query = full_response.split(" or ")[0]  # Take only the first part
        st.write(f"Generated Query: {concise_query}")  # Debugging output in Streamlit
        return concise_query.strip('"')  # Remove any surrounding quotes
    except Exception as e:
        st.error(f"Error generating query: {e}")
        return f"eco-friendly {product_name} alternatives"
