# Bloom
Bloom is a productivity tool for fresh starts and sustainable living. It offers eco-friendly product suggestions, rescues surplus food to reduce waste, and provides personalized quizzes to inspire mindful habits. With Bloom, small steps lead to meaningful transformations for individuals and the planet. 🌱

## Features
1. **Eco Alternatives Finder**
   - Generate search queries for eco-friendly product alternatives.
   - Fetch alternatives using Google Custom Search API.

2. **Surplus Food Rescue**
   - View and add surplus food offers on an interactive map.

3. **Eco-Friendly Lifestyle Quiz**
   - Take a quiz and get personalized recommendations for sustainable living.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/nabihawaseem/Bloom.git
   cd Bloom

2. Set up a virtual environment:
   ```bash
   python -m venv virtual

4. Install dependencies:
   ```bash
   pip install -r requirements.txt

6. Create a .env file in the root directory with the following:
   ```bash
   GROQ_API_KEY="your_groq_api_key"
   GOOGLE_API_KEY="your_google_api_key"
   SEARCH_ENGINE_ID="your_search_engine_id"

8. Run the application:
   
   ```bash
   streamlit run app.py

## Project Structure
```bash
Bloom/
│
├── app.py                   # Main Streamlit app
├── quiz_page.py             # Handles the Eco-Friendly Lifestyle Quiz page
├── backend/                 # Backend logic
│   ├── google_cse.py        # Google Custom Search API
│   ├── llm_helper.py        # LLM-based question/answer generation
│   └── query_generator.py   # Generates search queries
├── food_waste/              # Surplus food rescue functionality
│   └── food.py              # Surplus food rescue logic
├── requirements.txt         # Project dependencies
└── .env                     # Environment variables (not tracked)

   
