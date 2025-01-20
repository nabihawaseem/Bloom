import os
from googleapiclient.discovery import build
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env for local development
dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Retrieve API Key and Search Engine ID
API_KEY = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = st.secrets.get("SEARCH_ENGINE_ID") or os.getenv("SEARCH_ENGINE_ID")

# Raise an error if either API_KEY or SEARCH_ENGINE_ID is not set
if not API_KEY or not SEARCH_ENGINE_ID:
    raise ValueError("GOOGLE_API_KEY or SEARCH_ENGINE_ID is not set. Please check your configuration.")

# Function to fetch product alternatives using Google CSE API
def search_products(query):
    """
    Fetches products using Google Custom Search API.
    """
    # Initialize the Google Custom Search API service
    service = build("customsearch", "v1", developerKey=API_KEY)

    try:
        # Debugging: Show the query being sent to the API
        st.write(f"Query Sent to API: {query}")
        result = service.cse().list(q=query, cx=SEARCH_ENGINE_ID).execute()

        # Parse the results into a list of products
        products = [
            {
                "product_name": item.get("title", "No Title"),
                "image_url": item.get("pagemap", {}).get("cse_image", [{}])[0].get("src", ""),
                "link": item.get("link", "#"),
            }
            for item in result.get("items", [])
        ]

        return products
    except Exception as e:
        st.error(f"Error occurred while fetching search results: {e}")
        return []
