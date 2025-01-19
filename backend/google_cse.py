import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(dotenv_path)

# Retrieve API Key and Search Engine ID from environment variables
API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

if not API_KEY or not SEARCH_ENGINE_ID:
    raise ValueError("GOOGLE_API_KEY or SEARCH_ENGINE_ID is not set. Please check your .env file.")

# Function to fetch product alternatives using Google CSE API
def search_products(query):
    """
    Fetches products using Google Custom Search API.
    """
    # Initialize the Google Custom Search API service
    service = build("customsearch", "v1", developerKey=API_KEY)

    try:
        # Debugging: Show the query being sent to the API
        print(f"Query Sent to API: {query}")
        result = service.cse().list(q=query, cx=SEARCH_ENGINE_ID).execute()

        # Debugging: Print raw API response for inspection
        print("Raw API Response:", result)

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
        print(f"Error occurred while fetching search results: {e}")
        return []
