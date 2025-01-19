import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables explicitly
dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(dotenv_path)

# Initialize Groq client
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY is not set. Please check your .env file.")
client = Groq(api_key=api_key)

def generate_query(product_name):
    """
    Generates a concise and tailored search query using Groke API's LLaMA 3.3 model.
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
        print(f"Generated Query: {concise_query}")  # Debugging output
        return concise_query.strip('"')  # Remove any surrounding quotes
    except Exception as e:
        print(f"Error generating query: {e}")
        return f"eco-friendly {product_name} alternatives"
